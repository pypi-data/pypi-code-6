# -*- coding: utf-8 -*-
__author__ = 'rsj217'


from xiami import XiaMi

app = XiaMi(__file__)

def main():
    app.get_input()
    app.run()

if __name__ == '__main__':
    main()
