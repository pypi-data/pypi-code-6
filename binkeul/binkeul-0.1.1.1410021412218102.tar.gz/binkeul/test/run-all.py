#!/usr/bin/python3
'''
# python3 -m nose_check binkeul cmp

# nosetests --pdb
'''
import nose, os

os.system("python3 -m nose_check binkeul cmp" )

print( "="*77 )

#os.system("nosetests3 -v" )

# > nosetests3  -v
#nose.main(argv=["test*", '--with-doctest', '-vv'])
#nose.main(argv=["test*", '--with-doctest', '--pdb','-v'])

# '--with-doctest' 를 사용하면 nose_check 가 두 번 실행
nose.main(argv=["test*", '--pdb','-v'])
