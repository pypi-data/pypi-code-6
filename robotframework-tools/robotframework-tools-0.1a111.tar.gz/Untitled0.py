
# coding: utf-8

# In[1]:

get_ipython().magic(u'pdb')


# In[2]:

from robot.api import TestSuiteBuilder


# In[3]:

from robottools.modeled.testsuite import TestSuite


# In[4]:

from modeled.Qt import Qt


# In[5]:

mQt = Qt('PyQt4')


# In[6]:

Q = mQt.Q


# In[7]:

app = Q.Application([])


# In[8]:

mTestSuite = mQt[TestSuite]


# In[9]:

tsb = TestSuiteBuilder()


# In[10]:

suite = tsb.build('StefanSuite.txt')


# In[11]:

suite.name


# In[13]:

msuite = mTestSuite(testsuite=suite)


# In[16]:

msuite.nameWidget


# In[17]:

gui = Q.MainWindow(centralWidget=msuite.nameWidget)


# In[18]:

gui.show()


# In[ ]:



