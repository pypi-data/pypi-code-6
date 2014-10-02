#!/usr/bin/python3

from binkeul import *
import os

# 글이미지를 만들기 위해 BtKeul 을 생성 
kl01 = BtKeul( [ 
       LKode(1141119), 
       LKode(1933311), 
       LKode(6066683), 
       LKode(33626735), 
       LKode(324602), 
       LKode(1192831), 
       LKode(437532127), 
       LKode(84021119),
      ] ,
    # 획 폭이 6 픽셀, 획 폭은 반드시 짝수값이여야 함
    btconf=BtConf( 6 ) 
)

kio01 = kl01.toKioBytes()
kio01.seek(0)

# Keul 를 바이너리로
assert kio01.read() == b"\xfbK\x8b\x00\xfb\xff\xeb\x00\xdb\x8f\xe4\x02{\xd3\x08\x10\xd3\x9f'\x00\xfb\x9b\x91\x00\xfb\xae\xa1\xd0\xfb{\x10("

kio02 = kl01.toKioZ3a2s()
kio02.seek(0)

# Keul 를 Z3A2로 
assert  kio02.read() == 'RytGfzzxhfujxOaYxUvoHQVXnedVnpGiWidxNutNbpOY'

im01 = kl01.getImage()
im01.save( os.path.join( '_img' , 'a002-01.png' ) )

# 세로쓰기를 위해서 BtConf 를 설정한다.
btconf01 = BtConf( 4 , coldir= Dir.하 )
kl01.setBtConf( btconf01 )

im02 = kl01.getImage()
im02.save( os.path.join( '_img' , 'a002-02.png' ) )
