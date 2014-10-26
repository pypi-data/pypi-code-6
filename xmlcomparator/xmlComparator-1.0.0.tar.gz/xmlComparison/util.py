class Stack(list):
  
  def push(self, item):
    self.append(item)
  
  def pop(self):
    try:
      return list.pop(self)
    except IndexError:
      return None

  def peek(self):
    try:
      return self[len(self) - 1]
    except IndexError:
      return None

