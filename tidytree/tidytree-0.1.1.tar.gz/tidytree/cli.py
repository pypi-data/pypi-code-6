#!/usr/bin/python

from __future__ import print_function
import sys, os

def warning(*objs):
    print("Warning: ", *objs, file=sys.stderr)

def getListofFiles(folder):
    l = []
    for filename in os.listdir(folder):
        l += [filename]
    return l

def getUniqueKey(dictio):
    if(len(dictio) != 1):
        return False
    for k in dictio:
        return k

class TidyTree:

    def __init__(self, letter=None, limit=0):
        self.limit = limit
        self.letters = {}
        if(isinstance(letter, list)):
            for i in letter:
                self.add(i)
            self.optimize()
        elif(letter != None and letter != ""):
            self.add(letter)

    def add(self, filename):
        key = filename[0]
        if not key in self.letters:
            self.letters[key] = TidyTree(filename[1:])
        else:
            self.letters[key].add(filename[1:])

    # ( len(letter) == 1 ) ? merge keys & repeat : repeat
    def optimize(self):
        new_letters = {}
        aux_key = ""
        l = self.letters

        for letter in l:
            ite = l[letter]
            aux_key = letter
            if(len(ite.letters) == 1):
                while(len(ite.letters) == 1 ):
                    k = getUniqueKey(ite.letters)
                    new_letters[aux_key + k] = ite.letters[k]
                    ite = ite.letters[k]
                    new_letters.pop(aux_key, None)
                    aux_key = aux_key + k
                ite.optimize()
            else:
                ite.optimize()
                new_letters[letter] = l[letter]
        self.letters = new_letters

    def size(self):
        if (self.letters == {}):
            return 1
        else:
            s = 0
            for l in self.letters:
                s = s + self.letters[l].size()
            return s

    def getFiles(self, letter=""):
        if(len(self.letters) == 0):
            return [letter]
        files = []
        for l in self.letters:
            file_name = self.letters[l].getFiles(letter + l)
            files += file_name
        return files

    def move_inDir(self, directory_name):
        if not os.path.exists("local_test/" + directory_name):
            os.makedirs("local_test/" + directory_name)
        files = self.letters[directory_name].getFiles(directory_name)
        directory_name = "local_test/" + directory_name
        for f in files:
            print("(",f,")")
            os.rename("local_test/" + f, directory_name + "/" + f)

    def jointure(self):
        for letter in self.letters:
            start_size = self.letters[letter].size();
            if(start_size >= self.limit):
                self.move_inDir(letter)

    def toString(self):
        ret_str = ""
        for l in self.letters:
            ret_str = ret_str + l + "(" + self.letters[l].toString() + ")"
        return (ret_str)

def main():
    if(len(sys.argv) != 3):
        warning("Need a folder name past and a limit as arguments")
        sys.exit(1);
    folder=sys.argv[1]
    if(not os.path.exists(folder)):
        warning("The folder '" + folder + "' doesn't exist")
        sys.exit(1);

    tidy = TidyTree(folder, int(sys.argv[2]))
    tidy.jointure()
