import threading
import subprocess
from logging import debug

try:
    import pygments.lexers
    import pygments.token
    import pygments.util
except ImportError:
    pygments = None


class NoColor:
    def __init__(self):
        self.colors = [bytearray()]
        self.report = []

    def stop(self):
        pass

    def update(self, c1, r1, c2, r2, lines):
        pass

    def run(self):
        pass


class Color(NoColor):
    def __init__(self, doc):
        NoColor.__init__(self)
        self.doc = doc
        self.r = None
        self._stop = None
        self.thread = None
        self.athread = None
        if pygments:
            self.lexer = None
        else:
            self.lexer = False
        self.token2color = {}
        
    def stop(self):
        self._stop = True
        if self.thread:
            self.thread.join()
        if self.athread:
            self.athread.cancel()
            try:
                self.athread.join()
            except RuntimeError:
                pass

    def update(self, c1, r1, c2, r2, lines):
        if c1 != c2 or r1 != r2:
            start = self.colors[r1][:c1]
            end = self.colors[r2][c2:]
            if r1 == r2:
                self.colors[r1] = start + end
            else:
                self.colors[r1] = start
                del self.colors[r1 + 1:r2 + 1]
                self.colors[r1].extend(end)
        if lines != ['']:
            start = self.colors[r1][:c1]
            end = self.colors[r1][c1:]
            self.colors[r1] = start + bytearray(len(lines[0]))
            self.colors[r1 + 1:r1 + 1] = [bytearray(len(line))
                                          for line in lines[1:]]
            self.colors[r1 + len(lines) - 1].extend(end)

    def run(self, queue):
        if self.lexer is None:
            try:
                self.lexer = pygments.lexers.get_lexer_for_filename(
                    self.doc.name, stripnl=False)
            except pygments.util.ClassNotFound:
                self.lexer = False
            else:
                name = self.lexer.name
                self.doc.mode = name
                if name == 'reStructuredText':
                    self.tokens = [pygments.token.Operator,
                                   pygments.token.Generic,
                                   pygments.token.Name,
                                   pygments.token.Comment,
                                   pygments.token.Punctuation]
                else:
                    self.tokens = [pygments.token.Keyword,
                                   pygments.token.Number,
                                   pygments.token.String,
                                   pygments.token.Comment,
                                   pygments.token.Name.Builtin,
                                   pygments.token.Operator]

        self._stop = False
        if self.lexer:
            self.thread = threading.Thread(target=self.target, args=[queue])
            self.thread.start()

        self.athread = threading.Timer(2.0, self.analyse, [queue])
        self.athread.start()

    def target(self, queue):
        try:
            self.paint()
        except IndentationError:
            pass
        
        queue.put('draw colors')
        
    def analyse(self, queue):
        self.report = []
        self.pep8()
        self.pyflakes()
        queue.put('draw colors')
        
    def paint(self):
        text = '\n'.join(self.doc.lines)
        r = 0
        c = 0
        for token, s in pygments.lex(text, self.lexer):
            if self._stop:
                break
            color = self.token2color.get(token)
            if color is None:
                for color, t in enumerate(self.tokens):
                    if token in t:
                        color += 1
                        break
                else:
                    color = 0
                self.token2color[token] = color
                
            lines = s.split('\n')
            for i, line in enumerate(lines):
                n = len(line)
                for m in range(n):
                    self.colors[r][c + m] = color
                if i == len(lines) - 1:
                    break
                r += 1
                c = 0
            c += n

    def pep8(self):
        name = self.doc.filename
        if name is None or not name.endswith('.py'):
            return
            
        p = subprocess.Popen(['pep8', '--ignore=W293', '-'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
        for line in self.doc.lines:
            if self._stop:
                return
            print(line, file=p.stdin)
        output = p.communicate()[0]
        if p.returncode == 0:
            return
        
        for line in output.split('\n'):
            if self._stop:
                return
            try:
                pos, line = line.split(' ', 1)
                r, c = (int(n) - 1 for n in pos.split(':')[1:3])
                if (line.startswith('E226') and
                    self.doc.lines[r][c:c + 2] == '**'):
                    continue
                self.colors[r][c] = self.colors[r][c] % 7 + 7
            except (IndexError, ValueError):
                return
            self.report.append(((r, c), line))

    def pyflakes(self):
        name = self.doc.filename
        if name is None or not name.endswith('.py'):
            return

        p = subprocess.Popen(['pyflakes'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True)
        for line in self.doc.lines:
            if self._stop:
                return
            print(line, file=p.stdin)
        output = ''.join(o for o in p.communicate() if o is not None)
        if p.returncode == 0:
            return
        
        for line in output.split('\n'):
            if self._stop:
                return
            if line.startswith('<stdin>'):
                try:
                    pos, line = line.split(':', 2)[1:]
                    r = int(pos) - 1
                    self.colors[r][0] = self.colors[r][0] % 7 + 7
                except (IndexError, ValueError):
                    break
                self.report.append(((r, 0), line))
