#!/usr/bin/python3

from binkeul import *
import os 

# 베틀문자를 위한 Kode 를 생성합니다.
kd01 = LKode( 17929083 )

# Kode 를 바이너리로 
assert kd01.toBytes() == b'\xdb\x9b\x8c\x08'

# Kode 를 Z3A2로 
assert kd01.toZ3a2s() == 'VNzOoU'

# 정체문자인가?
assert kd01.isJung() == True

# L3값을 구한다.
assert kd01.getL3() == 2645865497046673660219235840

# 획 두께가 20 픽셀인 베틀문자를 생성하는 BtGrid 를 생성 
BG30 = BtGrid( 20 )

# 문자이미지를 생성하기 위해서는 L3 값으로 입력해야 함 
im1 = BG30.getImage(2645865497046673660219235840)
im1.save( os.path.join( '_img' , 'a001-01.png' ) )


# 핵체코드
kd02 = LKode( 17929083 - 1 )

# 정체문자인가?
assert kd02.isJung() == False 

im2 = BG30.getImage(kd02.getL3())
im2.save( os.path.join( '_img' , 'a001-02.png' ) )




