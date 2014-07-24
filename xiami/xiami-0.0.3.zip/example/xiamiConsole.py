# -*- coding: utf-8 -*-
__author__ = 'rsj217'


from xiami import XiaMi

app = XiaMi(__file__)

def main():
    print '---------- Welcome to use xiamiMusic Download Tool ----------'
    print
    input_url = app.get_input()
    print
    app.run(input_url)
    i = raw_input('Please Enter AnyKey To Exit ')

if __name__ == '__main__':
    main()