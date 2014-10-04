
""" this new module has like  a purpose deal with the list of clients that I will have in the prgram of the drone program """
' this new module has like  a purpose deal with the list of clients that I will have in the prgram of the drone program'
import os
Clients = []



class Client :
  def __init__(self, a_name  , a_dob = None  , a_adress = None) :
    self.name = a_name
    self.DOB = a_dob
    self.adress = a_adress
    
    
    
  @property
  def add_to_list(self):
     Clients.append(self.name)
  @property
  def put_in_list(self):
    general_list = [',',self.name,]
    with open('data/Clients.txt','a') as cl :
      cl.writelines(general_list)     
  
  def save_in_file(self ,filename):
    general_list = [self.name ,',', self.DOB ,',', self.adress]
    with open(filename , 'w') as f :
      f.writelines(general_list)
      
def get_from_file(filename):
  with open(filename ,'r') as f :
    data = f.readline()
    clena = data.strip().split(',')

  return(Client(clena.pop(0),clena.pop(0),clena.pop(0)))

def get_client_list(file):
   with open(file ,'r') as f :
    data = f.readline()
    clena = data.strip().split(',')
    return clena
""" this is the new method to edit my list ..... I hope it works !!!!"""



def eliminate_element(lis,cha) :
    lis.remove(cha)
    return lis

def create_client_list(lists):
  with open ('data/Clients.txt', 'w') as append:
    append.writelines(lists)

def replace(element):

    liss = get_client_list('data/Clients.txt')
    elemento = eliminate_element(liss,element)
    create_client_list(elemento)

""" ------------------------end---------------------------"""    

def empty(filename):  
  open(filename ,'w').close() 


def Remove(filename):
  os.remove(filename)
  

  
  

""" this function needs to be repared because whe you call it would return one (1)
number greater than the value """ """FIXED"""

def Get_lenght() :
  with open ('Clients.txt') as c :
    obj = c.readline()
    e = obj.strip().split(',')
  return len(e)


 
