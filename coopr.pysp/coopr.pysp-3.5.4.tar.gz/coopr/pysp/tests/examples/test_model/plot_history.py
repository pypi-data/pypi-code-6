import matplotlib.pylab as plt
import json
import shelve
import sys
import os

assert len(sys.argv) == 2
filename = sys.argv[1]
assert os.path.exists(filename)

history = None
try:
    with open(filename) as f:
        history = json.load(f)
except:
    history = None
    try:
        history = shelve.open(filename,
                              flag='r')
    except:
        history = None

if history is None:
    raise RuntimeError("Unable to open ph history file as JSON "
                           "or python Shelve DB format")

scenario_tree = history['scenario tree']

try:
    iter_keys = history['results keys']
except KeyError:
    # we are using json format (which loads the entire file anyway)
    iter_keys = list(history.keys())
    iter_keys.remove('scenario tree')
iterations = sorted(int(k) for k in iter_keys)
iterations = [str(k) for k in iterations]

for node_name, node in scenario_tree['nodes'].items():
    # it's not a leaf node
    if len(node['children']):
        node_vars = history['0']['node solutions'][node_name]['variables'].keys()
        node_scenarios = node['scenarios']
        
        for varname in node_vars:
            figure = plt.figure()
            ax = figure.add_subplot(111)
            for scenario_name in node_scenarios:
                ax.plot([history[i]['scenario solutions']\
                         [scenario_name]['variables'][varname]\
                         ['value'] for i in iterations],label=scenario_name)
            ax.plot([history[i]['node solutions']\
                     [node_name]['variables'][varname]\
                     ['solution'] for i in iterations],'k--',label='Node Average')
            ax.set_title(node_name+' - '+varname)
            ax.legend(loc=0)
plt.show()
