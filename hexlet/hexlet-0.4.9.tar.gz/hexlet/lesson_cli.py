from commands import lesson
from hexlet import utils

# @utils.UpdateBeforeCall("hexlet")
def main():
    lesson.cli(auto_envvar_prefix="HEXLET")
