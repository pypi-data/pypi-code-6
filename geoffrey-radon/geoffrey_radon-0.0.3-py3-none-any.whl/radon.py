import json
import logging
import asyncio

from geoffrey import plugin
from geoffrey.data import datakey
from geoffrey.utils import execute
from geoffrey.subscription import subscription


class Radon(plugin.GeoffreyPlugin):
    """
    radon plugin.

    """
    @subscription
    def modified_files(self, event):
        """
        Subscription criteria.

        Should be used as annotation of plugin.Tasks arguments.
        Can be used multiple times.

        """
        return (self.project.name == event.project and
                event.plugin == "filesystem" and
                event.key.endswith('.py'))

    @asyncio.coroutine
    def run_radon_mi(self, events:"modified_files") -> plugin.Task:
        """
        Maintainability index plugin task.

        Process `events` of the subscription `modified_files` and put
        states or events to the hub.

        """
        radon_path = self.config.get(self._section_name, "radon_path")
        while True:
            event = yield from events.get()

            filename = event.key
            task = 'mi'

            exitcode, stdout, stderr = yield from execute(radon_path, task,
                                                          '-s', filename)

            data = stdout.decode('utf-8').strip().split(' - ')
            rank, strscore = data[1].split()
            score = float(strscore[1:-1])
            state = self.new_state(key=filename, task=task, rank=rank,
                                   score=score)

            if state is not None:
                yield from self.hub.put(state)
            else:
                self.log.debug("No state generated")

    @asyncio.coroutine
    def run_radon_raw(self, events:"modified_files") -> plugin.Task:
        """
        Raw data plugin task.

        Process `events` of the subscription `modified_files` and put
        states or events to the hub.

        """
        radon_path = self.config.get(self._section_name, "radon_path")
        while True:
            event = yield from events.get()

            filename = event.key
            task = 'raw'

            state = yield from self.generate_state(radon_path, task, filename)

            if state is not None:
                yield from self.hub.put(state)
            else:
                self.log.debug("No state generated")

    @asyncio.coroutine
    def run_radon_cc(self, events:"modified_files") -> plugin.Task:
        """
        Ciclomatic Complexity plugin task.

        Process `events` of the subscription `modified_files` and put
        states or events to the hub.

        """

        from itertools import chain

        def extract_cc_data(data, base=None):
            name = data.get("name", "<noname>")
            classname = data.get("classname")

            components = []
            if base:
                components.append(base)
            if classname:
                components.append(classname)
            components.append(name)
            fqn = ".".join(components)

            clojures = data.pop('clojures', [])
            data.pop('methods', None)
            for d in clojures:
                yield from extract_cc_data(d, base=fqn)

            data['fqn'] = fqn
            yield data

        def generate_all_cc_data(datas):
            for d in datas:
                yield from extract_cc_data(d)

        radon_path = self.config.get(self._section_name, "radon_path")
        while True:
            event = yield from events.get()

            filename = event.key
            task = 'cc'

            state = yield from self.generate_state(radon_path, task, filename)

            if state is not None:
                newstate = self.new_state(
                    key=filename, task=task,
                    data=list(generate_all_cc_data(state.data)))
                yield from self.hub.put(newstate)
            else:
                self.log.debug("No state generated")

    @asyncio.coroutine
    def generate_state(self, radon_path, task, filename):
        """ Call radon and convert output to json """
        exitcode, stdout, stderr = yield from execute(radon_path, task, '-j',
                                                      filename)

        if stderr:
            self.log.warning('Radon found errors while reading {filename}:'
                             ' {errors}'.format(filename=filename,
                                                errors=stderr))
        if stdout:
            data = json.loads(stdout.decode('utf-8'))[filename]

            state = self.new_state(key=filename, task=task, data=data)
            return state

    @subscription
    def cc_states(self, event):
        """
        Ciclomatic complexity subscription.

        """
        return (self.project.name == event.project and
                event.plugin == "radon" and
                event.content_type == "data" and
                event.task == "cc")

    @subscription
    def mi_states(self, event):
        """
        Maintainability Index subscription.

        """
        return (self.project.name == event.project and
                event.plugin == "radon" and
                event.content_type == "data" and
                event.task == "mi")

    def cc_to_highlight(self, data):
        """Convert CC information to highlight protocol."""
        highlight = {}

        rank = data.get("rank")
        if rank in ("A", "B"):
            type_ = "info"
        elif rank == "C":
            type_ = "warning"
        elif rank in ("D", "E", "F"):
            type_ = "error"
        else:
            self.log.error("Unknown CC type %s", rank)

        highlight['type'] = type_
        highlight['start_line'] = highlight['end_line'] = data.get("lineno", 0)
        highlight['start_char'] = highlight['end_char'] = 0
        highlight['text'] = "CC[{rank}] - {type} '{name}': ".format(
            type=data.get('type', '').title(), name=data.get('name'),
            rank=rank)

        return highlight

    @asyncio.coroutine
    def cc_highlights(self, events:"cc_states") -> plugin.Task:
        """
        Generate highlights with the ciclomatic complexity information.

        """
        while True:
            event = yield from events.get()

            data = event.data
            if not data:
                state = self.new_state(key=event.key, task="cc_highlights",
                                       content_type="highlight")
            else:
                highlights = []

                def mark2highlight(mark):
                    highlights.append(self.cc_to_highlight(mark))
                    if 'clojures' in mark:
                        for clojure in mark['clojures']:
                            mark2highlight(clojure)

                for mark in data:
                    mark2highlight(mark)

                state = self.new_state(key=event.key, task="cc_highlights",
                                       content_type="highlight",
                                       highlights=highlights)

            yield from self.hub.put(state)

    @asyncio.coroutine
    def cc_histogram(self, events: "cc_states") -> plugin.Task:
        """Updates the Ciclomatic Complexity histogram."""
        from copy import copy
        while True:
            event = yield from events.get()
            filename = event.key
            data = event.data or []

            last_state = self.hub.get_one_state(datakey(
                key=event.key,
                content_type="data",
                project=self.project.name,
                plugin="radon",
                task="cc_histogram"))

            last_histograms = {}
            if last_state:
                for symbol in last_state.data:
                    if 'fqn' in symbol:
                        current_histograms = {
                            'complexities': symbol.get('complexities', []),
                            'ranks': symbol.get('ranks', [])}
                        last_histograms[symbol['fqn']] = current_histograms

            new_symbols = []
            for symbol in data:
                fqn = symbol.get('fqn')
                if fqn is None:
                    continue
                current_symbol = copy(symbol)

                new_complexity = current_symbol.pop('complexity', None)
                new_rank = current_symbol.pop('rank', None)
                histograms = last_histograms.get(fqn, {})

                current_symbol.update({
                    'ranks': histograms.get('ranks', [])[-50:] + [new_rank],
                    'complexities': histograms.get('complexities', [])[-50:] + [new_complexity]})

                new_symbols.append(current_symbol)

            if new_symbols:
                state = self.new_state(key=event.key, task="cc_histogram",
                                       data=new_symbols)
            else:
                state = self.new_state(key=event.key, task="cc_histogram")

            yield from self.hub.put(state, force_change=True)

    @asyncio.coroutine
    def mi_histogram(self, events:"mi_states") -> plugin.Task:
        """
        Updates the Maintainability Index histogram.

        """
        while True:
            event = yield from events.get()

            new_score = event.score
            new_rank = event.rank

            if new_score is None or new_rank is None:  # Not removing history
                continue

            last_state = self.hub.get_one_state(datakey(
                key=event.key,
                content_type="data",
                project=self.project.name,
                plugin="radon",
                task="mi_histogram"))

            if last_state is not None:
                scores = (last_state.scores or [])[-50:]
                ranks = (last_state.ranks or [])[-50:]
            else:
                scores = []
                ranks = []

            scores.append(new_score)
            ranks.append(new_rank)

            state = self.new_state(
                key=event.key,
                task="mi_histogram",
                scores=scores,
                ranks=ranks)

            yield from self.hub.put(state, force_change=True)
