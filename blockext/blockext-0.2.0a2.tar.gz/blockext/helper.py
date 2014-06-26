"""Code to interface with Scratch/Snap! as a "helper app".

Uses blockext.server as an HTTP nanoframework.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from future.builtins import *

import itertools
import threading
import time

from .blocks import Block
from .server import Server, Response, NotFound, Download, Redirect, quote
from .generate import Program




class HelperApp(object):
    CHECK_INTERVAL = 0.5 # seconds

    def __init__(self, helper_cls, blocks_by_selector, descriptor, debug=False):
        self.blocks_by_selector = blocks_by_selector
        self.helper_cls = helper_cls

        self.debug = debug
        self.descriptor = descriptor

        self.requests = set()
        self.helper_cls = helper_cls
        self.helper = helper_cls()

        self.connection_lock = threading.Lock()
        self.last_checked = 0
        self._connected = False

    def get_response(self, selector=None, *args):
        if not selector:
            return self.index()

        func_name = "handle_" + selector.replace(".", "_dot_")
        func = getattr(self, func_name, None)
        if func:
            return func(*args)
        else:
            return self.handle(selector, *args)

    def is_connected(self):
        if hasattr(self.helper, "_is_connected"):
            if time.time() > self.last_checked + self.CHECK_INTERVAL:
                with self.connection_lock:
                    self._connected = self.helper._is_connected()
                self.last_checked = time.time()
            return self._connected
            return connected
        else:
            return True

    def handle(self, selector, *args):
        try:
            block = self.blocks_by_selector[selector]
        except KeyError:
            return NotFound()

        content = self.run_block(block, args)
        return Response(content.encode("utf-8"))

    def run_block(self, block, args, is_poll=False):
        func = getattr(self.helper, block.selector)
        if not is_poll and getattr(func, '_needs_connection', False):
            if not self.is_connected():
                return ''

        args = list(args)
        if block.is_blocking:
            request_id = args.pop(0)
            # Snap! doesn't use _busy, so we have it send "-" as the request_id
            if request_id != "-":
                self.requests.add(request_id)

        assert len(args) == len(block.inputs)

        args = [decode_arg(a, t) for (a, t)
                in zip(args, block.inputs)]

        result = func(*args)
        content = encode_result(result, block.shape)

        if block.is_blocking:
            if request_id in self.requests:
                self.requests.remove(request_id)

        return content

    def handle_poll(self):
        connected = self.is_connected()

        reporter_values = {}
        for selector, block in self.blocks_by_selector.items():
            if block.is_blocking:
                continue
            if block.shape not in ("reporter", "predicate"):
                continue
            func = getattr(self.helper, selector)
            if not connected and getattr(func, '_needs_connection', False):
                continue
            menu_names = [input_.menu for input_ in block.inputs]
            if all(menu_names): # they're all menu inputs
                insert_options = map(self.descriptor.menus.get, menu_names)
                for args in itertools.product(*insert_options):
                    path = "/".join([selector] + list(args))
                    reporter_values[path] = self.run_block(block, args, True)

        if self.requests:
            reporter_values["_busy"] = " ".join(map(str, self.requests))

        if hasattr(self.helper, "_problem"):
            problem = self.helper._problem()
            if problem:
                reporter_values["_problem"] = str(problem)

        lines = []
        for name, value in reporter_values.items():
            lines.append(quote(name) + " " + quote(value))

        content = "\n".join(lines).encode("utf-8")
        return Response(content)

    def handle_reset_all(self):
        self.is_connected() # Ping the extension
        if hasattr(self.helper, "_on_reset"):
            self.helper._on_reset()
            self.requests = set()
            # TODO clear self.requests, kill threads (?)
        return Response("")

        # TODO what if the helper isn't connected?
        #   -> I think pinging the extension is sufficient


    # For debugging extensions #

    def index(self):
        if not self.debug:
            return NotFound()

        return Response("""\
        <!doctype html>
        <p><a href="/_generate_blocks/scratch">Download Scratch 2 extension file</a>
        <p><a href="/_generate_blocks/snap">Download Snap! blocks</a>
        """, content_type="text/html")

    def handle__generate_blocks(self, program_name, language_code="en", filename=None):
        if not self.debug:
            return NotFound()

        program = Program.by_short_name[program_name]
        language = self.descriptor.translations[language_code]

        if not filename:
            filename = program.get_filename(self.descriptor, language_code)
            new_path = "/".join((
                "/_generate_blocks",
                quote(program_name),
                quote(language_code),
                quote(filename))
            )
            return Redirect(new_path)

        return Download(program.generate_file(self.descriptor, language),
                        program.content_type)

    def handle_crossdomain_dot_xml(self):
        return Response("""<?xml version="1.0"?>
        <cross-domain-policy>
            <allow-access-from domain="*" to-ports="*"/>
        </cross-domain-policy>
        """, content_type="application/xml")



#- Translate between block language strings and Pythonic values. -#

def decode_arg(arg, input_):
    if input_.shape == "number":
        try:
            return int(arg)
        except ValueError:
            try:
                return float(arg)
            except ValueError:
                return 0
    elif input_.shape == "boolean":
        if arg == "true":
            return True
        elif arg == "false":
            return False
        else:
            return
    else:
        return arg

def encode_result(result, shape="reporter"):
    if shape == "command":
        result = None
    if shape == "predicate":
        result = bool(result)

    if result is True:
        return "true"
    elif result is False:
        return "false"
    elif result is None:
        return ""
    return str(result)



class Extension(object):
    def __init__(self, helper_cls, descriptor, deprecated_blocks=None):
        self.helper_cls = helper_cls
        """The class implementing the block methods.

        Block selectors must correspond to method names on this class.

        """

        self.descriptor = descriptor
        """Information about the extension."""

        deprecated_blocks = deprecated_blocks or []
        self._blocks_by_selector = {}
        for block in descriptor.blocks + deprecated_blocks:
            if not isinstance(block, Block):
                raise ValueError("not a block: " + repr(block))
            if block.selector in self._blocks_by_selector:
                raise ValueError("block selectors must be unique")
            if not hasattr(helper_cls, block.selector):
                raise ValueError(
                    "helper class needs method for block: " + repr(block.selector)
                )
            self._blocks_by_selector[block.selector] = block

    def run_forever(self, debug=False):
        host = "localhost"
        app = HelperApp(self.helper_cls, self._blocks_by_selector,
                        self.descriptor, debug)
        server = Server(app, host, self.descriptor.port)
        print("Listening on {host}:{self.descriptor.port}".format(**vars()))
        server.serve_forever()

