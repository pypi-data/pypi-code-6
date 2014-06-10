from distutils.core import setup, Extension

# all - for configuration
# mathtexargs = [
# 	"-DLATEX=\"/usr/share/texmf/bin/latex\"", 	# path to LaTeX program
# 	"-DDVIPNG=\"/usr/share/texmf/bin/dvipng\"",	# dvipng(same as latex)
# 	"-DDVIPS=\"/usr/share/texmf/bin/dvips\"",  	# dvips (same as latex)
# 	"-DCONVERT=\"/usr/bin/convert\"", 			# path to convert executable
# 	"-DCACHE=\"mathtex/\"", 					# relative path to mathTeX\"s cache dir
# 	"-DGIF", 									# emit gif images
# 	"-DPNG", 									# emit png images
# 	"-DDISPLAYSTYLE", 							# \[ \displaystyle \]
# 	"-DTEXTSTYLE",								# $ \textstyle $
# 	"-DPARSTYLE",								# paragraph mode, supply your own $ $ or \[ \]
# 	"-DFONTSIZE=5",								# 1=\tiny,...,5=\normalsize,...,10=\Huge
# 	"-DUSEPACKAGE=\"filename\"", 				# file containing \usepackage\"s
# 	"-DNEWCOMMAND=\"filename\"", 				# file containing \newcommand\"s
# 	"-DDPI=\"120\"", 							# dvipng -D DPI  parameter (as \"string\")
# 	"-DTEXGAMMA=\"2.5\"",						# dvipng --gamma TEXGAMMA  param (as \"string\")
# 	"-DNOQUIET", 								# -halt-on-error (default reply q(uiet) to error)
# 	"-DTEXTAREANAME=\"formdata\"", 				# <textarea name=...> in a <form>
# 	"-DREFERER=\"\"", 							# comma-separated list of valid referers
# 	"-DMAXINVALID=0", 							# max length expression from invalid referer
# 	"-DADFREQUENCY=0", 							# one request out of n displayed along with ad
# 	"-DADVERTISEMENT=\"filename\"",				# file containing ad template
#   "-DTEMPDIRBASE=\"\\000\""					# where to work
#   "-DOUTFILEBASE=\"\\000\""					# if set to something other than \\000 it overvrites filename parameter in the mathtex procedure (allways!)
#   "-DDEBUG									# some messages and shell commands are outputed to stdout and tempdir is not removed
# ]

# ubuntu/debian ?
mathtexargs = [
	"-DLATEX=\"/usr/bin/latex\"", 		# path to LaTeX program
	"-DDVIPNG=\"/usr/bin/dvipng\"",		# dvipng(same as latex)
	"-DDVIPS=\"/usr/bin/dvips\"",  		# dvips (same as latex)
	"-DCONVERT=\"/usr/bin/convert\"", 	# path to convert executable
	"-DPNG", 							# emit png images
	"-DTEMPDIRBASE=\"/var/tmp\"",           # this makes /var/tmp/mathtex the temp dir for intermediate files
	"-DCACHE=\"\\000\"",			# this makes mathtex to output png file to /var/tmp
	#"-DDEBUG",				# this prints some messages and shell commands to stdout
]

pymathtex_module = Extension('pymathtex', 
                        define_macros = [('MAJOR_VERSION', '0'), ('MINOR_VERSION', '2')],
                        include_dirs = ['.'],
                        libraries = [],
                        library_dirs = ['.'],
                        sources = ['pymathtex.c'],
                        extra_compile_args = [] + mathtexargs)

setup (name = 'PyMathTex', version = '0.2', description = 'This is C-like binding package for MathTex', ext_modules = [pymathtex_module])
