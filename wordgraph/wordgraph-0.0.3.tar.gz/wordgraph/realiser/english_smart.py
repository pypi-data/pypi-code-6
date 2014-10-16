'''
This module provides an advanced English-language grammar realiser (templating engine). It includes
in-build support for many English-language sentence construction rules and is easily extensible.

optionals:
  -- Use if defined / all contents valid
  -- Include external definition
  -- Mandatory with a default

Handle: space compression (support non-breaking space) and comma insertion.
Support: autocapitalise
'''

example_sentence = ''' 
This graph, "Height in Australia", shows the relationship between average height and age category. 
It contains 1 series. The series "Adults between 18 and 60" starts at 1.8m for ages 18-24 and ends at 
1.5m for ages 55-60.
'''

sample_grammar = '''
This graph [, $title ,] shows the relationship between <$x_label | 'an unlabeled variable'> 
and <$y_label | 'another unlabeled variable'>. [It contains $series_count series.] [:component:series:]
'''

series_grammar = '''
<The series $title | 'The first series'> starts at $x_start for $y_start and ends at $x_end for $y_end
'''

sample_values = {
    'values': {
        'title': 'Height in Australia',
        'x_label': 'Average height',
        'y_label': 'Age category',
        'series_count': 1,
        },

    'components': {
        'series': {
            'title': 'Adults between 18 and 60',
            'x_start': '1.8m',
            'y_start': 'ages 18-24',
            'x_end': '1.5m',
            'y_end': 'ages 55-60'
            }
        }

    }

variable_indicator = '%'
optional = '[]'
component = ':component:target:'
mandatory = '<|>'
escape = '^'
space = ' '

class GeneralRealiser():

    def __init__(self, grammar, component_grammars):

        self.grammar = grammar
        self.component_grammars = component_grammars

    def realise(self, variables):
        accepted = ''

        bufr = ''
        for char in self.grammar:



            bufr += char

        accepted += bufr

        return accepted

        

    def realise_optional(self, snippet, variables):
        pass

    def realise_mandatory(self, snippet, variables):
        pass

    def realise_component(self, snippet, variables):
        pass


def test_realiser():
    r = GeneralRealiser(sample_grammar, component_grammars = {'series': series_grammar})
    text = r.realise(sample_values)
    assert text == example_sentence