'''
Created on 09.09.2011

@author: prefer
'''
import os
import sys

from django.core.management.base import BaseCommand

from ...prepare_env import start

class Command(BaseCommand):
    """
    """
    
    def handle(self, *args, **options):
        path_to_manage_py = os.path.abspath(sys.argv[0])        
        path_to_src = os.path.dirname( os.path.dirname( path_to_manage_py ) )             
        start(path_to_src)