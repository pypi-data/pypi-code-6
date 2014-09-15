from helga.plugins import command
import textwrap
import time

FLOOD_RATE = 30

LAST_USED = {}


@command('cowsay', aliases=['cow'])
def cowsay(client, channel, nick, message, cmd, args):
    """
    cowsay:
     ____________
    < I Love nix >
     ------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """
    global FLOOD_RATE, LAST_USED
    now = time.time()

    if channel in LAST_USED and (now - LAST_USED[channel]) < FLOOD_RATE:
        return
    LAST_USED[channel] = now

    text = ' '.join(args)
    return build_bubble(text) + build_cow()


def build_cow():
    return u"""
         \   ^__^
          \  (oo)\_______
             (__)\       )\/\\
                 ||----w |
                 ||     ||
    """


def build_bubble(str, length=40):
    bubble = []
    lines = normalize_text(str, length)
    bordersize = len(lines[0])
    bubble.append("  " + "_" * bordersize)
    for index, line in enumerate(lines):
        border = get_border(lines, index)
        bubble.append("%s %s %s" % (border[0], line, border[1]))
    bubble.append("  " + "-" * bordersize)

    return "\n".join(bubble)


def normalize_text(str, length):
    lines = textwrap.wrap(str, length)
    maxlen = len(max(lines, key=len))
    return [line.ljust(maxlen) for line in lines]


def get_border(lines, index):
    if len(lines) < 2:
        return ["<", ">"]
    elif index == 0:
        return ["/", "\\"]
    elif index == len(lines) - 1:
        return ["\\", "/"]
    else:
        return ["|", "|"]
