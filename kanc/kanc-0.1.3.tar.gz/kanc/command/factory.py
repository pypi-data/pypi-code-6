from board import BoardCommand
from user import UserCommand
from project import ProjectCommand
from task import TaskCommand
import inspect
import sys

def create(name, client, rcfile):
    commands = [BoardCommand, UserCommand, ProjectCommand, TaskCommand]
    for c in commands:
        if c.name == name:
            return c(client, rcfile)
    return None

def create_all(client, rcfile):
    commands = [BoardCommand, UserCommand, ProjectCommand, TaskCommand]
    created = []
    for c in commands:
        created += [c(client, rcfile)]
    return created

