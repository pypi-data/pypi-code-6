#!/usr/bin/python
# -*- coding: utf-8 -*-

################################################
#      ____            _       _               #
#     |  _ \ _   _    | | ___ | | _____        #
#     | |_) | | | |_  | |/ _ \| |/ / _ \       #
#     |  __/| |_| | |_| | (_) |   <  __/       #
#     |_|    \__, |\___/ \___/|_|\_\___|       #
#            |___/                             #
#                         version 2.0          #
################################################

from __future__ import division
#from __future__ import unicode_literals

#Sys, Os
import sys
import os

#Database, OrderedDict
from collections import OrderedDict

# PERSO
from KeywordsList import *
from Parameters import *

class PyJoke:
    # Init parameters
    params = Parameters()

    ###############################################
    ##    scoreJoke
    ##    Input:     A string (joke)
    ##               A list of Keywords
    ##    Output:    Score for joke
    ###############################################
    def scoreJoke(self,j,keyw):
        # Maximum keywords, will decrease
        n_keywords = len(keyw)
        # occurences of all keywords
        n_occurenc = 0
        weight=0 # postag or nothing much
        joke_len = len(j)

        ##    For each keyword...
        #################################
        for x in range(0,len(keyw)):
            keyword = keyw.getWord(x)                # Save keyword
            score = keyw.getScore(x)                 # And keyword score

            # find keyword in joke
            m = re.search(keyword,j.lower())
            f = re.findall(keyword, j.lower())

            n_occurenc += len(f)                     # add occurences of this keyw

            # keyword not found (-1)
            if(m is None):
                n_keywords-=1
            # keyword found, save its score
            else:
                weight = weight+score

        # % of keyword per sentence
        ratio = ((n_keywords*n_occurenc)/joke_len)*100

        if (self.params.debug):
            print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"+j+ \
            "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
            print "~ Keywords ("+str(len(keyw))+")"
            print "?"+str(x)
            print f
            print "> joke len: "+str(joke_len)
            print "> keywords:"+str(n_keywords*n_occurenc)
            print "> ratio:"+str(ratio)
            print "~ ~ ~ ~ "+str((n_keywords*100)+n_occurenc)

            print "#"+str((n_keywords*100)+n_occurenc+ratio*10)
            print "="+str(((n_keywords*100)+n_occurenc+ratio*10)*float(weight))

        # Return score for a joke
        return ((n_keywords*100)+n_occurenc+ratio*10)*float(weight)


    ###############################################
    ##    getJoke
    ##    Input:     A list of Keywords
    ##    Output:    2nd best joke
    ###############################################
    def getJoke(self,keyw):

        jokes = {}


        ##    QUERY
        #################################
        if self.params.database=="sqlite" and not self.params.nao:
            query = "SELECT text FROM "+self.params.table+" WHERE LENGTH(`text`)<"+str(self.params.jokelen)+" AND (`text` REGEXP  \'"+keyw.getWord(0)+"\'";
            for x in range(1,len(keyw)):
                query = query + " OR  `text` REGEXP  \'"+keyw.getWord(x)+"\'";
            query = query + ") ORDER BY score DESC "
        else:
            query = "SELECT text FROM "+self.params.table+" WHERE LENGTH(`text`)<"+str(self.params.jokelen)+" AND (`text` LIKE  \'%"+keyw.getWord(0)+"%\'";
            for x in range(1,len(keyw)):
                query = query + " OR  `text` LIKE  \'%"+keyw.getWord(x)+"%\'";
            query = query + ") ORDER BY score DESC "

        ##    Connection to Database
        #################################
        if self.params.database=="mysql":
            import MySQLdb
            conn = MySQLdb.connect(host=self.params.host, # your host, usually localhost
                             user=self.params.user, # your username
                              passwd=self.params.passwd, # your password
                              db=self.params.db) # name of the data base

        elif self.params.database=="sqlite":
            import sqlite3
            conn = sqlite3.connect(self.params.sqlite)
            if not self.params.nao:
                conn.enable_load_extension(True)
        else:
            print "[!] Error: Database should be sqlite or mysql"

        # Cursor
        c = conn.cursor()

        # Regexp for SQLite
        if self.params.database=="sqlite" and not self.params.nao:
            c.execute("SELECT load_extension('/usr/lib/sqlite3/pcre.so');")


        # Query
        c.execute(query)

        ##    For each joke...
        #################################
        for row in c.fetchall() :
            # For each keyword
            jokes.update({row[0]:self.scoreJoke(row[0],keyw)})

        conn.close()

        # Order by score
        jokes = OrderedDict(sorted(jokes.items(), key=lambda t: t[1]))

        # Debug
        #tmp = jokes.keys()
        #tmp.reverse()
        #print tmp[:2]

        try :
            ##    Return best joke
            #################################
            if self.params.conv!=0:
                # Second best joke (1st might be "the same in conversation")
                return jokes.keys()[-2]
            else:
                # First best joke
                return jokes.keys()[-1]

            #for k, v in jokes.items():
                #print "%s: %s" % (k, v)
        except IndexError:
            return "NO JOKE ERROR"


    ###############################################
    ##    init
    ##    Input:     String (argument)
    ##    Output:    best joke
    ###############################################
    def __init__(self,sentence):

        # Conversation
        if self.params.conv!=0:
            for i in range(self.params.conv):
                keyw = KeywordsList(sentence,self.params)
                print "[PyJoke - sentence {}] {}".format(i+1,sentence)
                answer = self.getJoke(keyw)
                print "[PyJoke - joke      ] "+answer+"\n"
                sentence = answer.encode('utf-8')
        # Single output
        else:
            keyw = KeywordsList(sentence,self.params)
            #print len(keyw)
            self.theJoke = self.getJoke(keyw).encode('utf-8')
            #print self.getJoke(keyw).encode('utf-8')

    def getTheJoke(self):
        return self.theJoke
