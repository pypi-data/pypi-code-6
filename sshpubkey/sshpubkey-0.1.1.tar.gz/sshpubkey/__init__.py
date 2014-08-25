import shlex
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile

from . import exc

TEMP_SUFFIX = ".pub"
TEMP_PREFIX = "ssh-temp-key-"

KEY_TYPE_BLACKLIST = set([
    "RSA1",
])


def quoted_split(string, delim=None):
    if delim is None:
        delim = set([" ", "\t", "\n"])

    if isinstance(delim, basestring):
        delim = set([delim])

    pos = 0
    elems = []
    quoted = False

    for idx, char in enumerate(string):
        if char == "\"":
            quoted = not quoted
        if not quoted and char in delim:
            elems.append(string[pos:idx])
            pos = idx + 1

    if pos < len(string):
        elems.append(string[pos:])

    return elems


class PublicKey(object):
    def __init__(self, key_type, shortname, key_size, key, fingerprint,
                 random_art, bubblebabble="", comment="", options=None):
        self.key_type = key_type
        self.shortname = shortname
        self.key_size = key_size
        self.key = key
        self.fingerprint = fingerprint
        self.random_art = random_art
        self.bubblebabble = bubblebabble
        self.comment = comment
        self.options = options or {}

    def ra_no_border(self):
        ra = self.random_art.strip().splitlines()
        return "\n".join(line[1:-1] for line in ra[1:-1])

    @classmethod
    def from_str(cls, key_str):
        if not key_str.endswith("\n"):
            key_str += "\n"

        with NamedTemporaryFile(suffix=TEMP_SUFFIX, prefix=TEMP_PREFIX) as temp:
            temp.write(key_str)
            temp.flush()

            details = cls.get_key_details(key_str, temp.name)
            return cls(**details)

    @classmethod
    def from_file(cls, key_filename):
        with open(key_filename) as key_file:
            key_str = key_file.readline()

        if not key_str.endswith("\n"):
            key_str += "\n"

        details = cls.get_key_details(key_str, key_filename)
        return cls(**details)

    @staticmethod
    def get_key_details(key_str, key_filename, bubblebabble=True):

        details = PublicKey.get_fingerprint_details(key_filename)

        if details["shortname"] in KEY_TYPE_BLACKLIST:
            raise exc.PublicKeyInvalid("%s type keys not allowed." % details["shortname"])

        if bubblebabble:
            details["bubblebabble"] = PublicKey.get_bubblebabble(key_filename)

        details.update(PublicKey.parse_key_str(key_str))

        return details

    @staticmethod
    def parse_key_str(key_str):
        options = {}
        key_type = None
        key = None

        parts = quoted_split(key_str)

        if len(parts) == 2:
            key_type, key = parts[0:2]
        elif parts[0].startswith(("ssh-", "ecdsa-")):
            key_type, key = parts[0], parts[1]
        else:
            key_type, key = parts[1], parts[2]
            _options = quoted_split(parts[0], ",")
            for option in _options:
                key, value = option.split("=", 1)
                options[key] = value

        return {
            "options": options,
            "key_type": key_type,
            "key": key,
        }

    @staticmethod
    def parse_fp_line(line):
        parts = line.split()
        return {
            "key_size": parts[0],
            "fingerprint": parts[1],
            "comment": " ".join(parts[2:-1]),
            "shortname": parts[-1][1:-1],  # Strip parens.
        }

    @staticmethod
    def get_fingerprint_details(key_filename):
        proc = Popen(
            ["/usr/bin/ssh-keygen", "-vlf", key_filename],
            stdout=PIPE, stderr=PIPE
        )

        stdout, stderr = proc.communicate()

        if proc.returncode:
            output = "Failed to parse Public Key:"
            if stdout:
                output += "\n" + stdout
            if stderr:
                output += "\n" + stderr
            raise exc.PublicKeyParseError(output)

        fp_line, random_art = stdout.split("\n", 1)
        details = PublicKey.parse_fp_line(fp_line)
        details["random_art"] = random_art
        return details

    @staticmethod
    def get_bubblebabble(key_filename):
        proc = Popen(
            ["/usr/bin/ssh-keygen", "-Bf", key_filename],
            stdout=PIPE, stderr=PIPE
        )

        stdout, stderr = proc.communicate()

        if proc.returncode:
            output = "Failed to parse Public Key:"
            if stdout:
                output += "\n" + stdout
            if stderr:
                output += "\n" + stderr
            raise exc.PublicKeyParseError(output)

        return PublicKey.parse_fp_line(stdout.strip())["fingerprint"]
