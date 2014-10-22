#!/usr/bin/python

import sys  

def print_comment(message, width, java=False, xml=False):
    '''Prints the commentmessage.'''
    ############################# Exit on width error ##############################
    if len(message)>width:
    	sys.stderr.write('Warning: "%s": length is %d, wider than %d\n' % (message, 
                         len(message), width))

    ############################## Calculate # width ###############################
    filler_width = (width-len(message)-2)/2

    if java:
    	filler       = "*"*(filler_width-1)
    	filler_start = '/'+filler
    	filler_end   = filler+'/'

    elif xml:
    	filler       = " "*(filler_width-3)
    	filler_start = "<!--"+filler[:-1]
    	filler_end   = filler+"-->"

    else:
    	filler_start=filler_end= "#"*max(1, filler_width)

    if len(message)%2==1:
    	filler_end = filler_end[0]+filler_end

    ################################# Print result #################################
    print filler_start+" %s " % message+filler_end

