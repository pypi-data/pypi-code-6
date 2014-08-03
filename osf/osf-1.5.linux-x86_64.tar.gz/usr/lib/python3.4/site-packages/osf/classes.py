from .timeutils import milliseconds_to_hhmmss


class Header:
    def __init__(self):
        self.kv = {}
        self.v = []


class OSFLine():
    def __init__(self):
        self.time = None
        self.text = ""
        self.link = None
        self.tags = []
        self.indentation = 0

    def __str__(self):
        parts = []
        if self.indentation:
            parts.append('-' * self.indentation)
        if self.time is not None:
            parts.append(milliseconds_to_hhmmss(self.time))
        parts.append(self.text)
        if self.link:
            parts.append("<" + self.link + ">")
        parts.extend(["#" + tag for tag in self.tags])
        return " ".join(parts)
