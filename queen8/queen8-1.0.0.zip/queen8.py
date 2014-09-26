"""
one solution of Queen-8 question was saved in a list
list[0] save column index of line 0
list[1] save column index of line 1
...
list[n] save column index of line n
"""
def printSolution(souList):
    soulen = len(souList)
    ostlst = ['O']*soulen
    for idx in range(soulen):
        line = ostlst[:]
        line[ souList[idx] ] = 'X'
        linestr = '| ' + ' | '.join(line) + ' |'
        print('-'*len(linestr))
        print(linestr)
        if( idx+1 == soulen ):
            print('-'*len(linestr))

"""
Line 0~i have been placed queens
now check that if line i conflict with line 0~(i-1)
"""
def checkLine(souList,i):
    for lineIdx in range(i):
        if( souList[lineIdx]==souList[i] or abs(souList[lineIdx]-souList[i])==(i-lineIdx) ):
            return False
    return True

"""
one solution of Queen question was saved in a list
souList[0] save column index of line 0
souList[1] save column index of line 1
...
souList[n] save column index of line n

dim: dimension of square
i  : to place q queen of line i
"""
def placeQueen(solutions,souList,dim,i):
    if( i == dim ):
        solutions.append(souList[:])
        return
    for tmpIdx in range(dim):
        souList[i] = tmpIdx
        if( checkLine(souList,i) ):
            placeQueen(solutions,souList,dim,i+1)
"""
Give out all solutions of Queen X Problem(x is dimension such as 8,10)
Solutions will be saved in a list, every item is a seperate solution which
is also a list, just like this.
[ [3, 0, 4, 7, 1, 6, 2, 5],[4, 0, 7, 5, 2, 6, 1, 3],...]
"""
def getAllSolutions(dim):
    tmpsolution = [0]*dim
    solutions = []
    placeQueen(solutions,tmpsolution,dim,0)
    return solutions
    
if __name__ == '__main__':
    dim = 8
    solutions = getAllSolutions(dim)
        
    for x in range(len(solutions)):
        print('--solution %d--'%(x+1))
        printSolution( solutions[x] )

    print('There are %d solutions for queen-%d problem.'%(len(solutions),dim))
    
        
