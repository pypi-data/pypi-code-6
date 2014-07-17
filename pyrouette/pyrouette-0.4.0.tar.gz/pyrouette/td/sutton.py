#! /usr/bin/env python
"""
Author: Jeremy M. Stober
Program: SUTTON.PY
Date: Wednesday, February 29 2012
Description: Sutton actor-critic method from 1983 paper.
"""

import random as pr
import numpy as np
import numpy.random as npr


class SuttonActorCritic(object):
    """
    Basically a copy of Suttons code from pole.c. Used for comparison.
    """
    def __init__(self):
        self.nboxes = 162
        self.w = np.zeros(self.nboxes)
        self.v = np.zeros(self.nboxes)
        self.xbar = np.zeros(self.nboxes)
        self.e = np.zeros(self.nboxes)
        self.lambdaw = 0.9
        self.lambdav = 0.8
        self.gamma = 0.95
        self.beta = 0.5
        self.alpha = 1000
        
    def policy(self, state):
        if pr.random() < 1.0 / (1.0 + np.exp(-np.max([-50.0,np.min([self.w[state],50.0])]))):
            return 1
        else:
            return 0

    def best(self, state):
        if self.w[state] > 0.5:
            return 1
        else:
            return 0

    def reset(self):
        self.e = np.zeros(self.nboxes)
        self.xbar = np.zeros(self.nboxes)

    def train(self, pstate, paction, reward, state, next_action):

        if reward == -1:
            s = 0
        else:
            s = self.v[state]

        self.e[pstate] += (1.0 - self.lambdaw) * (paction - 0.5)
        self.xbar[pstate] += (1.0 - self.lambdav)

        rhat = reward + self.gamma * s - self.v[pstate]

        self.w += self.alpha * rhat * self.e
        self.v += self.beta * rhat * self.xbar

        self.e *= self.lambdaw
        self.xbar *= self.lambdav
        
    def learn(self, nepisodes, env):
        """
        Right now this is specifically for learning the cartpole task.
        """

        # learn for niters episodes with resets
        count = 0
        for i in range(nepisodes):
            self.reset()
            env.reset()
            next_action = self.policy(env.state())
            print "Episode %d, Prev count %d" % (i, count)
            count = 0
            while True:
                pstate, paction, reward, state = env.move(next_action,boxed = True)
                next_action = self.policy(env.state())
                self.train(pstate, paction, reward, state, next_action)
                count += 1
                if count % 1000 == 0:
                    print "Count: %d" % count
                if count > 10000:
                    break
                if env.failure():
                    break

    def test(self, env):
        env.reset()
        count = 0
        while not env.failure():
            next_action = self.best(env.state())
            env.move(next_action)
            count += 1
            if count % 1000 == 0:
                print "Count: %d" % count
            if count > 10000:
                break
        print "Balanced for %d timesteps." % count

class SuttonActorCritic2(SuttonActorCritic):
    
    def __init__(self):
        SuttonActorCritic.__init__(self)
        self.w = np.zeros((2,self.nboxes))
        self.e = np.zeros((2,self.nboxes))

    def reset(self):
        self.e = np.zeros((2,self.nboxes))
        self.xbar = np.zeros(self.nboxes)

    def policy(self,state):
        vals = self.w[:,state]
        dist = softmax(vals)
        res = npr.multinomial(1,dist)
        return np.argmax(res)
            
    def train(self, pstate, paction, reward, state, next_action):
        if reward == -1:
            s = 0
        else:
            s = self.v[state]

        self.e[paction,pstate] += (1.0 - self.lambdaw) * 0.5
        self.xbar[pstate] += (1.0 - self.lambdav)

        rhat = reward + self.gamma * s - self.v[pstate]

        self.w += self.alpha * rhat * self.e
        self.v += self.beta * rhat * self.xbar

        self.e *= self.lambdaw
        self.xbar *= self.lambdav

class SuttonActorCritic3(SuttonActorCritic):

    def __init__(self):
        self.nboxes = 162
        self.w = np.zeros((2,self.nboxes))
        self.v = np.zeros((2,self.nboxes))
        self.xbar = np.zeros((2,self.nboxes))
        self.e = np.zeros((2,self.nboxes))
        self.lambdaw = 0.9
        self.lambdav = 0.8
        self.gamma = 0.95
        self.beta = 0.8
        self.alpha = 1000

    def reset(self):
        self.e = np.zeros((2,self.nboxes))
        self.xbar = np.zeros((2,self.nboxes))

    def policy(self,state):
        vals = self.w[:,state]
        dist = softmax(vals)
        res = npr.multinomial(1,dist)
        return np.argmax(res)

    def train(self, pstate, paction, reward, state, next_action):
        if reward == -1:
            s = 0
        else:
            s = self.v[next_action,state]

        self.e[paction,pstate] += (1.0 - self.lambdaw) * 0.5
        self.xbar[paction,pstate] += (1.0 - self.lambdav)

        rhat = reward + self.gamma * s - self.v[paction,pstate]

        self.w += self.alpha * rhat * self.e
        self.v += self.beta * rhat * self.xbar

        self.e *= self.lambdaw
        self.xbar *= self.lambdav



