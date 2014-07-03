import operator
import itertools
from SelectScript import SelectScript 

class SelectScript_Interpreter():
    
    def __init__(self):
        self = self
        self.fct_list = {}
        self.var_list = {}
        self.var_ages = {}
        
        self.fct_desc = {}
        
        self.addFunction('assign', self.addVariable, "", True)
        
        self.addFunction('and', operator.and_, "", True)
        self.addFunction('not', operator.not_, "", True)
        self.addFunction('xor', operator.xor , "", True)
        self.addFunction('or',  operator.or_ , "", True)
        
        self.addFunction('in',  self._in, "", True)
        
        self.addFunction('lt', operator.lt , "", True)
        self.addFunction('le', operator.le , "", True)
        self.addFunction('eq', operator.eq , "", True)
        self.addFunction('ne', operator.ne , "", True)
        self.addFunction('ge', operator.ge , "", True)
        self.addFunction('gt', operator.gt , "", True)
        
        self.addFunction('add', operator.add , "", True)
        self.addFunction('sub', operator.sub , "", True)
        self.addFunction('mul', operator.mul , "", True)
        self.addFunction('div', operator.div , "", True)
        self.addFunction('mod', operator.mod , "", True)
        self.addFunction('neg', operator.neg , "", True)
        self.addFunction('pos', operator.pos , "", True)
        self.addFunction('pow', operator.pow , "", True)
        
        self.addFunction('to', self._to, "Translates the function-name of an SELECT-clause.\nUsage: to(fct(...), 'new_name')")
        
        self.addFunction('clear',  self.clearMemory, "Delete all defined variables.\nUsage: clear()")
        
        self.addFunction('var', self.debugVariable )
        
        self.addFunction('help', self.help , "Lists all callable functions: help()\nGet help for a specific function: help('function_name')")
        
        #self.addFunction('getTime', self.getTime )
        
    def _in(self, v, l):
        return v in l
    
    def _to(self, value, name):
        return (value, name)
    
    def help(self, function=None):
        if function == None:
            fct_list = []
            for fct in self.fct_desc.keys():
                fct_list.append(fct)
            return fct_list
        if self.fct_desc.has_key(function):
            return function + "\n" + self.fct_desc[function]
        
        return function + " not found"        
    
    def addVariable(self, name, value, age=0):
        
        # first instantiation
        if not self.var_ages.has_key(name):
            self.var_ages[name] = age
            self.var_list[name] = {}
        
        if self.var_ages[name] == 0:
            self.var_list[name] = value

        else:
            self.var_list[name][self.getTime()] = value
            # remove the oldest ones ...
            if self.var_ages[name] > 0:
                timestamps = self.var_list[name].keys()
                timestamps.sort()
                max_age = self.getTime() - self.var_ages[name]
                for t in timestamps:
                    if t < max_age:
                        self.var_list[name].pop(t)
                    else:
                        break
        
        return value
    
    
    
    # a{9999.9}=12; a=122; a=44; a=122;
    def callVariable(self, name, age=0):
        if self.var_ages[name] == 0:
            return self.var_list[name]
        elif age > 0:
            ## XXXXXXXXXXXXXXXX naechste distanz ....
            return self.var_list[name][age]
        elif age < 0:
            t_min = self.getTime()+age
            
            values = []
            for timestamp in self.var_list[name].keys():
                if timestamp >= t_min:
                    values.append(self.var_list[name][timestamp])
            return values
        elif age == None:
            return self.var_list[name]
        
        else :
            timestamp = max(self.var_list[name].keys())
            return self.var_list[name][timestamp]
        
    def debugVariable(self, name):
        print "age: ", self.var_ages[name]
        print "val: ", self.var_list[name]

    def addFunction(self, name, ptr, description="", internal=False):
        self.fct_list[name] = ptr
        
        if not internal:
            self.fct_desc[name] = description
        
    def callFunction(self, name, params):
        return self.fct_list[name](*params)
    def clearMemory(self):
        self.var_list = {}
    
    def getTime(self):
        return 0
    
    def eval(self, prog, this=None, ids=None):
        
        #print prog
        if isinstance(prog[0], list):
            fin = []
            for stmt in prog:
                fin = self.eval(stmt, this, ids)
            return fin
                
        elif prog[0] == SelectScript.types['fct']:
            return self.evalFct(prog[1:], this, ids)
        
        elif prog[0] == SelectScript.types['val']:
            return prog[1]
            
        elif prog[0] == SelectScript.types['var']:
            return self.callVariable(prog[1], self.eval(prog[2], this, ids))
            
        elif prog[0] == SelectScript.types['this']:
            if prog[1] == '':
                return this[0]
            else :
                return this[ids[prog[1]]]
        
        elif prog[0] == SelectScript.types['list']:
            list_ = []
            for e in prog[1]:
                list_.append(self.eval(e, this, ids))
            return list_
        
        elif prog[0] == SelectScript.types['sel']:
            return self.evalSelect(prog[1:], this, ids)
            
        else:
            return prog
        
    def evalFct(self, prog, this=None, ids=None):
        params = []
        for elem in prog[1]:
            params.append(self.eval( elem, this, ids))
        
        # XXX{9999}= -1111111;
        #if prog[0] == 'assign':
        #    if params[0]=="XXX":
        #        print prog[0], params, self.current_time
        return self.callFunction( prog[0], params )
        
    def evalSelect(self, prog, this=None, ids=None):
        SELECT  = prog[0]
        if SELECT == []:
            SELECT = self.sel_list
        
        FROM = []
        FROM_n = {}
        
        for n, p in enumerate(prog[1]):
            r = self.eval( p, this, ids )

            FROM.append( self.getListFrom(r) )
            
            # Variable
            if p[0] == SelectScript.types['var']:
                FROM_n[p[1]] = n
            # Assignement
            elif p[0] == SelectScript.types['fct']:
                FROM_n[self.eval(p[2][0])] = n
            else:
                FROM_n[''] = n
        
        FROM = self.permutate(FROM)
        
        WHERE   = prog[2]
        AS      = self.eval(prog[3])
        results = []
        
        return self.evalAs(AS, SELECT, FROM, FROM_n, WHERE)
        
#        mark = True 
#        for elem in FROM:
#            if WHERE != []:
#                mark = self.eval(WHERE, elem, FROM_n)
#            
#            if mark:
#                
#                if AS == SelectScript.asTypes['dict']: 
#                    result = {}              
#                    for f in SELECT:
#                        if f[1] == 'to':
#                            f_val, f_name = self.eval(f, elem, FROM_n)
#                            result[f_name] = f_val
#                        else:
#                            result[f[1]] = self.eval(f, elem, FROM_n)
#                    results.append(result)
#                elif AS == SelectScript.asTypes['list']:    
#                    for f in SELECT:
#                        results.append( self.eval(f, elem, FROM_n))
#                        
#                elif AS == SelectScript.asTypes['value']:
#                    results = self.eval( SELECT[0] , elem, FROM_n )
#                    break
#                
#                elif AS == SelectScript.asTypes['scene']:
#                    pass
                
        return results
    
    def evalAs(self, AS, SELECT, FROM, FROM_n, WHERE):
        if AS == SelectScript.asTypes['list']:
            return self.evalAS_list(SELECT, FROM, FROM_n, WHERE)
        elif AS == SelectScript.asTypes['dict']:
            return self.evalAS_dict(SELECT, FROM, FROM_n, WHERE)
        elif AS == SelectScript.asTypes['value']:
            return self.evalAS_value(SELECT, FROM, FROM_n, WHERE)
        return None
    
    def evalAS_value(self, SELECT, FROM, FROM_n, WHERE):
        results = []
        mark = True 
        for elem in FROM:
            if WHERE != []:
                mark = self.eval(WHERE, elem, FROM_n)
            
            if mark:
                results = self.eval( SELECT[0] , elem, FROM_n )
                break              
                
        return results
    
    def evalAS_list(self, SELECT, FROM, FROM_n, WHERE):
        results = []
        mark = True 
        for elem in FROM:
            if WHERE != []:
                mark = self.eval(WHERE, elem, FROM_n)
            
            if mark:
                for f in SELECT:
                    results.append( self.eval(f, elem, FROM_n))                
                
        return results
    
    def evalAS_dict(self, SELECT, FROM, FROM_n, WHERE):
        results = []
        mark = True 
        for elem in FROM:
            if WHERE != []:
                mark = self.eval(WHERE, elem, FROM_n)
            
            if mark:
                result = {} 
                for f in SELECT:
                    if f[1] == 'to':
                        f_val, f_name = self.eval(f, elem, FROM_n)
                        result[f_name] = f_val
                    else:
                        result[f[1]] = self.eval(f, elem, FROM_n)
                results.append(result)
                
        return results
    
    def getListFrom(self, obj):
        if isinstance(obj, list):
            return obj
        else:
            return [obj]
    
    def permutate(self, values):
        return itertools.product(*values)

        