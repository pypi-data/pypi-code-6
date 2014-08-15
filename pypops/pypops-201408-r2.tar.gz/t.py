import copy
import multiprocessing

mgr = multiprocessing.Manager()

mylist = mgr.list()
mylist.append({'name': 'bot'})
mylist.append({'name': 'bar'})
mylist.append({'name': 'foo', 'status': 123})
mylist.append({'name': '141241'})
mylist.append({'name': 'foo'})

new_list = mgr.list()
for item in mylist:
    item_copy = copy.deepcopy(item)
    if item['name'] == 'foo':
        item_copy['status'] = 456
    new_list.append(item_copy)

print mylist
print new_list
