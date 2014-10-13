import argparse
from . import config
from . import io
from . import utils
from . import stack

__version__ = "0.0.0-alpha.1.1"
__description__ = '''Get answers through your command line 
  from Stack...'''

def parse():
  '''Offers Options and Parses process arguments returning
  a dict of the  vars
  @return {dict}'''
  parser = argparse.ArgumentParser(
    description=__description__)
  parser.add_argument("question", metavar="QUESTION", nargs="*",
                      help="your question please")
  parser.add_argument("-s", "--save", metavar="FILE",
                      nargs=1, dest="save",
                      help="save answers to FILE")
  parser.add_argument("--api-key", metavar="ApiKey",
                      nargs=1, dest="apiKey",
                      help="add/change API Key")
  parser.add_argument("-nc", "--no-color", action="store_true",
                      help="disable colored input")
  parser.add_argument("-v", "--verbose", action="store_true",
                      help="log errors to screen")
  parser.add_argument("-V", "--version", action="version",
                      version="%(prog)s {0}".format(__version__))
  args = parser.parse_args()
  args = vars(args)
  return args


def run():
  'Main Program Entry Point'
  callbacks = []
  args = parse()
  # disabling colored output
  if args["no_color"]:
    io.disableColors()
  # being verbose
  if args["verbose"]:
    io.beVerbose()
  # saving to file
  if args["save"]:
    callbacks(utils.saveToFile(args["save"]))
  # changing api key
  if args["apiKey"]:
    return io.log("Not Implementated").error()
  # getting question
  if args["question"]:
    return stack.ask(" ".join(args["question"]), callbacks)
  # assuming user wants multiline input option
  print("Question please! Question mark (?) ends input")
  question  = io.multilineInput()
  return stack.ask(question, callbacks)


config = config.read()


if __name__ == "__main__":
  run()
