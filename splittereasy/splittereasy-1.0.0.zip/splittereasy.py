def sanitize(time_string):
    global separator
    if '-' in time_string:
        separator='-'
    elif ':' in time_string:
        separator=':'
    else:
        return (time_string)
        separator=''
    (mins,secs)=time_string.split(separator,1)
    return (mins+'.'+secs)
