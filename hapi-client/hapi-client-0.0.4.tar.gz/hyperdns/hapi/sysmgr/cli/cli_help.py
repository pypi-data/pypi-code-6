import textwrap
from hyperdns.hapi.sysmgr.cli import SHAPICLI

def _raw_to_end(doc):
    s=doc.split("Example Invocations",2)
    if len(s)>1:
        return s[1]
    return ''
    
@SHAPICLI.command('Help')
def cmd_help(arguments,hapi):
    """
    Provide various help displays:
    
    Example Invocations
        help
            Print a general purpose usage summary
            
        help <command>
            Print complete command help
            
        help <command> --examples
            Print a summary of examples
            
    """
    cmd=arguments['<command>']
    bold='\033[1m' if not arguments['--nobold'] else ''
    unbold='\033[0m' if not arguments['--nobold'] else ''
    show_examples=arguments['--examples']
    newline="\n"
    result=""
    cmds=SHAPICLI.command.registry
    if cmd==None:
        result+=textwrap.dedent("""
        Try "shapi" to get the Usage summary from docopt
        Try "shapi help" to get this alternative usage summary
        Try "shapi help --examples" to get an expanded usage summary
        Try "shapi help <command>" to get command specific help
        Try "shapi help <command> --examples" to get detailed usage info
        Add --nobold if the bolding escape characters are in the way
        """)
        for command in sorted(cmds.keys()):
            func=cmds[command]
            oneline=func.oneline
            doc=func.__doc__
            usage=doc.split("\n",1)[0]
            result+= "%s%-10s %s%s\n" % (bold,command,oneline,unbold)
            result+= "%-10s %s\n" % ('',usage)
            if show_examples:
                raw_to_end=_raw_to_end(doc)
                for ex in textwrap.dedent(raw_to_end.lstrip("\n")).split("\n\n"):
                    parts=ex.split("\n",1)
                    usage=parts[0]
                    info="" if len(parts)<=1 else textwrap.dedent(parts[1])
                    oneline=info.split("\n",1)[0]
                    ##print "%10s '%s' : %s" % ("",usage,oneline)
                    result+= "%10s * %s\n" % ("",usage)
                    result+= "%10s   %s\n" % ("",oneline)
    else:
        if cmd in cmds.keys():
            doc=cmds[cmd].__doc__
            if show_examples:
                raw_to_end=_raw_to_end(doc)
                for ex in textwrap.dedent(raw_to_end.lstrip("\n")).split("\n\n"):
                    parts=ex.split("\n",1)
                    usage=parts[0]
                    info="" if len(parts)<=1 else textwrap.dedent(parts[1])
                    result += "%s%s%s\n" % (bold,usage,unbold)
                    for l in info.split("\n"):
                        if l=='.':
                            l=''
                        result += "   " + l + newline
            else:
                raw_to_end=_raw_to_end(doc)
                parts=raw_to_end.split("\n",1)
                usage=parts[0]
                info="" if len(parts)<=1 else textwrap.dedent(parts[1]).rstrip("\n    ")
                result += "%s%s%s\n" % (bold,usage,unbold)
                result += info + newline
                result += newline
                result += "'help %s --examples' will describe the following examples in detail\n" % cmd
                result += newline
                raw_to_end=doc.split("Example Invocations",2)[1]
                for ex in textwrap.dedent(raw_to_end.lstrip("\n")).split("\n\n"):
                    parts=ex.split("\n",1)
                    usage=parts[0]
                    info="" if len(parts)<=1 else textwrap.dedent(parts[1])
                    oneline=info.split("\n",1)[0]
                    result += "   %s%s%s\n" % (bold,usage,unbold)
                    result += "        " + oneline + newline
                
        else:
            result= "Command %s not found" % cmd
    print(result)


