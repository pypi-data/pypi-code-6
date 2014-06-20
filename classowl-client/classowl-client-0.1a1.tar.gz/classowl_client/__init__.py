from .client import create_client as create, get_token
from .shortcuts import LazyResource

username = None
password = None

users = LazyResource('users')
schools = LazyResource('schools')
courses = LazyResource('courses')
memberships = LazyResource('memberships')
assignments = LazyResource('assignments')
