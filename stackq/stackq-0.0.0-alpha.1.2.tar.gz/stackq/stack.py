import html2text
import readline
import stackexchange
from . import io
from . import utils


readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set editing-mode vi")
SITE = stackexchange.Site(stackexchange.StackOverflow)


def ask(question, callbacks=[]):
  '''Asking a Question. Checks network connectivity before
  asking.
  @param {str} question
  @param {def} callbacks called after getting answer back'''
  pingRes = utils.ping()
  if pingRes is not True:
    return pingRes
  question =  searchQuestion(question)
  if not question:
    return None
  answer = getAnswer(question)
  answer = processAnswer(answer)
  displayAnswer(answer)
  for callback in callbacks:
    callback(answer)


# TODO: better algorithm for choosing question
def searchQuestion(question):
  '''Searches SITE for a suitable question
  @param {str} question'''
  searchProgress = io.log("Searching for such a Question")
  try:
    question = question.replace("?", "")
    qs = SITE.search(intitle=question)
    if len(qs)  is 0:
      return searchProgress.error("none found")
    searchProgress.ok()
    questionId = displayQuestions(qs)
    return questionId
  except EOFError as e:
    searchProgress.error("cancelling query")
  return None
    

def displayQuestions(questions):
  '''Displays fetched questions from SITE
  @param {list} questions'''
  io.println("")
  io.println("%-15s %s" % ("#ID", "Question Title"))
  io.println("")
  ids = []
  for q in questions:
    # calling str here to avoid re-looping ahead
    ids.append(str(q.id))
    io.println("%-15s" % (q.id), status="priority", append="")
    io.println(q.title)
  io.println("")
  return chooseQuestion(ids)


def completerInit(ids):
  '''Decorates the readline completer
  @param {dict} ids - string ids of target questions
  @return {def} readline completer function'''
  def completer(text, state):
    matches = [_id for _id in ids if _id and _id.startswith(text)]
    try:
      return matches[state]
    except:
      return None
  return completer


def chooseQuestion(ids):
  '''Allows user to enter a id for question whose
  answers will be fetched. Incorrect user entries
  prompts user to key in again
  @param {dict} ids - string ids of target quesions'''
  readline.set_completer(completerInit(ids))
  questionId = io.getInput("Choose a Question")
  if questionId in ids:
    try:
      return questionId
    except KeyboardInterrupt:
      io.log("Choosing question").error("cancelled")
      return None
  else:
    io.log("Choosing question").error("none with that id")
    return chooseQuestion(ids)


def getAnswer(id):
  '''Refactor :: Useless round trip'''
  getProgress = io.log("Getting answers")
  SITE.be_inclusive()
  answer = SITE.question(int(id))
  getProgress.ok()
  return answer


# TODO: html2text conversion
def processAnswer(answer):
  '''Processes the answer for callbacks to be called
  and anwers displayed to user'''
  processProgress = io.log("Processing answers")
  answer.body = html2text.html2text(answer.body)
  answers = []
  for ans in answer.answers:
    ans = SITE.answer(ans.id)
    answers.append(html2text.html2text(ans.body))
  answer.answers = answers
  return answer


def highlight(text, langs):
  #nText = re.sub(r"(\s{4}\w\n)*", , text)
  return True

# TODO: syntax highlighting
def displayAnswer(answer):
  '''Displays the question & its answers to the user
  @param {str} answer'''
  io.log("displaying answer").error("Not Implemented")
  print("\n" + answer.title)
  print(answer.body)
  print(answer.answers[0])
  print(answer.tags)
  return answer
