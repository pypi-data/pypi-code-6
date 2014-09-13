import traceback
import sys
import ast
def ankit(l):
    try:
        sum =0
        for i in l:
            sum = sum + i
        return sum
    except:
        return traceback.format_exc()

if __name__=='__main__':
    print ankit(ast.literal_eval(sys.argv[1]))
