'''
==================
테스트 명령
==================

pinus 라이부러리 폴더를 읽어서 파일목록을 구하여 test 파일명을 만든다.
::

   * binus/betl/chpixscan.py
   -->
   * test-betl-chpixscan.py

경로명의 분리자는 모두 "-" 로 치환된다.


디렉토리 내의 테스트 실행
===================================
직접명령 
::

    > nosetests -v test-*
    > nosetests -vv test-*
    
    # 오류 발생시 PDB 
    > nosetests -v --pdb test-*


``run-all-test.py`` 파일 
::

    #!/usr/bin/python3
    import nose

    #nose.main(argv=["test*", '--with-doctest', '-vv'])
    nose.main(argv=["test*", '--with-doctest', '-v'])

주요기능
===============
out.txt 파일에 비교결과 를 출력한다.

   ::


      > py3 __cmd@.py  cmp

      > py3 __cmd@.py  cmp -o



   ``out.txt``
   ::

      Namespace(command=['cmp'], o=True, out=None)
      -----------------------------------------------------------------------------
       테스트파일 목록에 없는 모듈파일
      {'test-betle-bcode.py',
       'test-betle-char.py',
       'test-betle-charset.py',
       'test-betle-choxscan.py',
       'test-betle-chpix.py',
       'test-betle-chscan.py',
       'test-betle-const.py',
       'test-betle-dicdb.py',
       'test-betle-initdb.py',
       'test-betle-scanimg.py',
       'test-betle-selchlist.py',
       'test-qb-bmchar.py',
       'test-qb-mainwin.py',
       'test-qb-oxpad.py',
       'test-qb-oxpsr.py',
       'test-utils-root_include.py'}
      -----------------------------------------------------------------------------
       모듈파일 목록에 없는 테스트파일, 또는 잘못된 파일명
      {'test-b_1.py'}
      -----------------------------------------------------------------------------
       모듈파일 목록에 있는 테스트파일
      {'test-betle-chpixscan.py'}



'''


import os ,  shutil, re , pprint, codecs, datetime , sys
import picxpot
import nose

class TestfileCheck :

    테스트파일_접두어 = "test-"

    def __init__( self , LibDir, UnittestDir ) :
        self.LibDir = LibDir
        self.UnittestDir = UnittestDir

    def run( self ):
        LibSet = self.파일목록구하기( self.LibDir , False )
        UnittestSet = self.파일목록구하기( self.UnittestDir , True )

        # 두폴더셋비교하기( LibSet , UnittestSet )
        print("-"*77,os.linesep, "테스트파일 목록에 없는 모듈파일")
        pprint.pprint( LibSet - UnittestSet )

        print("-"*77,os.linesep, "모듈파일 목록에 없는 테스트파일, 또는 잘못된 파일명")
        pprint.pprint( UnittestSet - LibSet )

        print("-"*77,os.linesep, "모듈파일 목록에 있는 테스트파일")
        pprint.pprint( UnittestSet & LibSet )

    def _Q제외root( self, rootname ) :
        # 제외할 폴더명의 중간이름 , [-+ #@] 기호 있으면 제외
        조건식  = lambda name : \
           re.match( r"_|-|dic|test|Locale", name , re.I ) or \
           not re.search( "^[A-Z]+$" , name , re.I )

        names = rootname.split(os.sep)[1:]
        return any( map( 조건식 , names ) )

    def _Q제외file( self, filename , 테스트파일 ) :

        fname, ext = os.path.splitext( filename )

        if ext != ".py" :
            return True

        if 테스트파일 :
            # if not re.search( r"^(?!\-)[A-Z-]+(?<!\-)$", fname , re.I ) :
            if not re.search( r"^{}[A-Z0-9-_]+$".format(self.테스트파일_접두어), fname , re.I ) :
                return True
        else :
            if not re.search( r"^(?=[A-Z])[A-Z0-9_]+$", fname , re.I ) :
                return True

        return False


    def 파일목록구하기( self, 시작경로 , 테스트파일=False ) :
        os.chdir(시작경로)

        접두어 = {
              True : '' ,
              False : self.테스트파일_접두어  ,
           }[ 테스트파일 ]

        get테스트파일이름 = lambda root, file : 접두어 + "-".join(os.path.join( root, file ).split( os.sep )[1:])

        파일목록SET = set()
        for root, dirs, files in os.walk("."):
            if self._Q제외root( root ) : continue
            # print( root )

            for f in files :
                if self._Q제외file( f , 테스트파일 ) : continue

                테스트파일이름 = get테스트파일이름(root,f)

                assert not 테스트파일이름 in 파일목록SET , "중복된 테스트파일이름이 있습니다. ({})".format(테스트파일이름)

                파일목록SET.add( 테스트파일이름 )

        return 파일목록SET



if __name__ == "__main__" :
    import argparse

    LIBDIR = picxpot.__path__[0]
    UNITTESTDIR = os.path.dirname(os.path.abspath(__file__))

    command = {
       "cmp" :
          TestfileCheck(
                LibDir =  LIBDIR ,
                UnittestDir = UNITTESTDIR
             ).run ,

       "test" : lambda : os.system( "nosetests -v" )
       }

    parser = argparse.ArgumentParser(description='picxpot unittest 실행')

    parser.add_argument(
       'command',
       nargs=1,
       type=str,
       action="store",
       help=" `cmp` , `test` 명령중 하나를 입력합니다."
       )

    parser.add_argument(
       '-o',
       action="store_true",
       help="기본 출력파일을 설정합니다."
       )

    parser.add_argument(
       '--out',
       type=str,
       action="store",
       help="출력파일을 설정합니다."
       )

    args = parser.parse_args()

    if args.out or args.o :
        if args.o : outfile = "__out.txt"
        if args.out : outfile = args.out
        f = codecs.open( os.path.join( UNITTESTDIR, outfile ) , 'w' , encoding='utf8' )
        sys.stdout = f

    print( args )

    command[args.command.pop()]()
