from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import subprocess


class Command(BaseCommand):
	help = "Grunt: The JavaScript Task Runner"

	def handle(self, *args, **options):
		
		#run npm install
		subprocess.call(['grunt'] + list(args))
	


		
	   
