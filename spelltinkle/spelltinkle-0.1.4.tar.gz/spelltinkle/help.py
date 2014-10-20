from spelltinkle.keys import keynames, doubles
from spelltinkle.document import Document


x = """
Fast and simple editor based on Python and Pygments.

spelltinkle.org: put sphinx-autodoc on there

XKCD: automation 1319

   ------
  | SPEL |
  | LTIN |
  | KLE  |
   ------

    ##### ##### ##### #
    #     #   # #     #
    ##### ##### ####  #
        # #     #     #
    ##### #     ##### #####
    
    #     ##### ##### #   #
    #       #     #   ##  #
    #       #     #   # # #
    #       #     #   #  ##
    #####   #   ##### #   #
    
    #   # #     #####
    #  #  #     #
    ###   #     ####
    # #   #     #
    #  #  ##### #####

    
     ____________
    |            |
    |  Hello     |
    |            |
    |____________|
    /S/P/E/L/L/ /
   /T/I/N/K/L/E/
  /___________/  
  
        S
        P
        E
T I N K L E
        L
        
        
p3 setup.py sdist (register) upload --show-response
Spelltinkle: pip+spell-check

autosave to /tmp after some time

$spelltinkle dir/ -> open fileinput

pkgutil, sys.modules

open-current-session-in-new-window-and-stop-the-old-one()

irc+email+todo-list+calender

only one file-list at the time

replace+color
no indent after return
run tests
replace marked area by abc and add line before with abc = <marked-area>

go to point before jump
go to next problem marker

Put help for opening files on the filelist page

When selcting area with mouse use scrollbar to scroll up or down

session.py: result=actions.method(doc);isgenerator(result)?
(for questions and other input)

remove tabs when reading (or replace with 4 tabs that display as spaces?)
smooth scrolling when jumping?
b block: b:begin, r:rectangle, l:lines
f replace,x:regex
g goto 123,()[]{},x:inner
h help,x:search in help
i-(tab) x:insert file or !shell
j- x:join
k kill,x:backwards
l delete line
m- x:makro
n
o open file or !shell
q quit,x:ask
r reverse find,x:word under cursor
s find
t
y mark: wl()[]{},x:inner
z delete wl()[]{},x:inner

How about ^Z?

^#12 or ^1^2?

Jump to marked point? Put position on stack

format text

reST mode

crash: report to launchpad

close single doc
<c-1><c-2>: repeat 12 times
spell check: ispell -a
scroll:up, down,center,top, bottom
big movements
swap two chars
look at to vim plugins: svn,snippets,easymove
complete

scripting: abc<enter><up><end>


Use number columns to show stuff: last changed line(s)

check state of file every two seconds when active?

write docs on errors and write debug info

python3 -m spelltinkle

spt --beginner --verbose --read-only --black-and-white

"""


class HelpDocument(Document):
    def __init__(self, actions):
        Document.__init__(self, actions=actions)
        self.name = '[help]'
        lines = []
        for c in sorted(keynames):
            k = keynames[c]
            if not isinstance(k, str):
                k = '+'.join(k)
            lines.append('  {}: {}'.format(c, k))
        for c1 in doubles:
            for c2, k in doubles[c1].items():
                if not isinstance(k, str):
                    k = '+'.join(k)
                lines.append('{}{:2}: {}'.format(c1, c2, k))
        lines += x.split('\n')
        self.change(0, 0, 0, 0, lines)
        self.view.move(0, 0)
