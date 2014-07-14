from doubly_linked_list import DoublyLinkedList

class LruCacher(object):
	def __init__(self, max_size, plan_b_func):
		"max_size: the largest number of items the cache can have."
		"plan_b_func: the function that will be called with the query as its"
		"             argument if a query isn't cached. The result will then"
		"             be associated with the query."
		
		if max_size < 0:
			raise ValueError("max_size must be positive.")
		if not callable(plan_b_func):
			raise TypeError("plan_b_func must be callable.")
			
		self.max_size = max_size
		self.ht = {}
		self.ll = DoublyLinkedList()
		self.plan_b_func = plan_b_func
		
	def lookup(self, query):
		"Perform a query on the cache. The elements of the cache are "
		"automatically adjusted. If the query is in the cache, move it to the "
		"front of the linked list then return it. If it's not in the cache, "
		"remove the last query in the linked list, queries the plan_b_func for"
		"the result, adds it to the cache, and returns it. This should be a "
		"decorator."
		
		"Cached items have their queries as keys in the hashtable, which point"
		"to elements in a doubly linked list. Linked lsit nodes have two "
		"attributesdata: data, which is the result of calling plan_b_func, and"
		"and query, which is the query itself."
		
		found_in_cache = None
		if query not in self.ht:
			found_in_cache = False
			result = self.plan_b_func(query)
			if len(self.ht) == self.max_size and self.max_size is not 0:
				if self.ll.tail is not None:
					del self.ht[self.ll.tail.query]
					self.ll.removeTail()
			if self.max_size != 0:
				self.ll.addToHead(result)
				self.ll.head.query = query
				self.ht[query] = self.ll.head
		else:
			#The query was in the cache. Move it to the front of 
			#the linked list.
			found_in_cache = True
			node = self.ht[query]
			result = node.data
		
		return result, found_in_cache
		
	def update(self, query, val):
		"Update the value stored in the cache pointed to by query. If query "
		"isn't cached, nothing happens."
		
		if query not in self.ht:
			return
		
		node = self.ht[query]
		node.data = val
		
	def size(self):
		return len(self.ht)
		
if __name__ == '__main__':
	test_cache()