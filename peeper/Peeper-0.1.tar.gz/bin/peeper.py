import peeper
import argparse
parser = argparse.ArgumentParser(description='Peep inside a Python sdist tarball/zip and find its dirty requirements.')
parser.add_argument('file', help='File to peep into.')
parser.add_argument('-n', help='Optional name of package, peeper will guess if not supplied (needs to include version number if in tarball name.)')
args = parser.parse_args()
if not args.n:
	guessed = True
	if args.file.endswith('.zip'):
		args.n = args.file.replace('.zip', '')
	elif args.file.endswith('.tar'):
		args.n = args.file.replace('.tar', '')
	else:
		tarsearch = re.search('\.tar\.(.+)', args.file)
		if tarsearch:
			args.n = args.file.replace('.tar.'+tarsearch.group(1), '')
		else:
			# bad
			args.n = ''
	if re.search('/', args.n):
		args.n = args.n.split('/')[-1]
else:
	# bad 2: the baddening
	args.n = ''
print('['+args.n+' requires]')
for r in peeper.extract_requirements(args.file, args.n):
	print('\t'+r)
