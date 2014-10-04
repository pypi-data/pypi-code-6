from .play import play
from .parse_mplayer import parse_mplayer

def knurko(filename):
    final_line = play(filename)
    frame_number = parse_mplayer(final_line)
    if frame_number == None:
        msg = "There weren't enough lines in mplayer's output."
        raise ValueError(msg)
    else:
        return frame_number
