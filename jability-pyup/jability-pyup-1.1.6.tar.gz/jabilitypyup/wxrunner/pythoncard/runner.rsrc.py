{'application':{'type':'Application',
          'name':'Template',
    'backgrounds': [
    {'type':'Background',
          'name':'bgTemplate',
          'title':'ijgHL7ADT GUI Console',
          'size':(400, 00),
          'style':['resizeable'],

        'menubar': {'type':'MenuBar',
         'menus': [
             {'type':'Menu',
             'name':'menuFile',
             'label':'&File',
             'items': [
                  {'type':'MenuItem',
                   'name':'menuFileExit',
                   'label':'E&xit',
                   'command':'exit',
                  },
              ]
             },
         ]
     },
         'components': [

{'type':'CheckBox',
    'name':'cbDebug',
    'position':(100, 16),
    'backgroundColor':(228, 220, 208, 255),
    'label':'Debug',
    },

{'type':'ToggleButton',
    'name':'ToggleButton',
    'position':(10, 10),
    'label':'Go/Stop',
    },

{'type':'TextArea',
    'name':'textConsole',
    'position':(5, 45),
    'size':(-1, 34),
    'backgroundColor':(0, 0, 0, 255),
    'editable':True,
    'font':{'faceName': u'Sans', 'family': 'sansSerif', 'size': 10},
    'foregroundColor':(255, 255, 255, 255),
    },

] # end components
} # end background
] # end backgrounds
} }
