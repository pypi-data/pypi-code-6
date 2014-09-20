from distutils.core import setup

setup(name='PyWinMouse',
      version='1.0',
      description='Python Windows Mouse Utilities',
      author='Gaurav Ghosal',
      author_email='gauravrghosal@gmail.com',
      package_dirs={"":"C:/Users/Gaurav/Desktop/PyWinMouse"},
      py_modules =['PyWinMouse'],
      keywords = ["Windows", "Mouse", "User32"], 
      classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Desktop Environment",
        "Topic :: System",
        "Topic :: Utilities"
        ],
      long_description ="""
This is a simple module allowing python windows developers a simple interface to the User32 mouse control functions!This module exports a Mouse class which provides an object oriented way of controlling the Windows mouse.
Tutorial::

    >>>a=Mouse()#Creates a mouse object
    >>>a.left_click()#Left clicks
    >>>a.right_down()#Presses down the right mouse button
    >>>a.move_mouse(30, 22)#Moves mouse to (30, 22)
    >>>a.get_mouse_pos()
    (30, 22)#If the mouse has not been moved

It is very simple and easy to work with"""
      )
      
