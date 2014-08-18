# -*- coding: utf-8 -*-
# pysteim.py - pure Python library for implement Steim compression method.
# Support reading Steim-1 and Steim-2, and recording Steim-2
#
#
#
__version__='0.2.1'

import struct, datetime, math

def mbin(value, bits=32):
    """ Support function. Print binary view of value of 'bits' bit"""
    sign='-' if '-' in bin(value) else ''
    s=bin(value)
    tmp=s[3:] if sign else s[2:]
    return tmp.rjust(bits, '0')+sign

class _Steim(object):
    """ Base class for Steim algorithms """
    
    def __init__(self, byte_order='>', block_size=512, warnings=True):
        self.byte_order=byte_order
        self.block_size=block_size
        self.warnings=warnings
        
        # offset level to convert unsigned value to signed in according of a bit depth
        # For example unsigned byte 128 to signed byte -1
        self.offset_level={}
        for i in (4,5,6,8,10,15,16,30,32):
            self.offset_level[i]=2**(i-1)-1
    
    def get_values_from_int(self, value, bits):
        """ Unpack a number of values of 'bits' bits from integer 'value'
        value - integer (32bit) value 
        bits - a number of bits which represent each value"""
        
        result=[]
        start_bits=32 if bits in (8,16,32) else 30
        
        corner=start_bits/bits
        for i in xrange(corner):
            # get some bits from value
            tmp=(value>>(bits*(corner-i-1)))&(2**bits-1)
            
            # convert from unsigned to signed value
            if tmp>self.offset_level[bits]:
                tmp=tmp-2**bits
            result.append(tmp)
        return result 
    
    def extract_block_header(self, binary_string):
        """ Extract from string header of block.
        binary_string must be raw string, first 48 chars must consist fixed section of data header """
        
        if not binary_string:
            return None
        
        #===================================================================
        # reading ASCII part of header
        #===================================================================
        header=dict(zip(('sequence_number',
                         'data_header_indicator',
                         'reserved_byte',
                         'station',
                         'location',
                         'channel',
                         'network'),
                        struct.unpack(self.byte_order+'6s2c5s2s3s2s', binary_string[:20])))
        
        #===================================================================
        # reading binary part of header
        #===================================================================
        d=struct.unpack(self.byte_order+'2h4bh', binary_string[20:30])
        header['record_start_time']=datetime.datetime(year=d[0], month=1, day=1, hour=d[2], minute=d[3], second=d[4], microsecond=d[6]*100)+datetime.timedelta(days=d[1]-1)
        
        header.update(dict(zip(('number_of_samples',
                               'sample_rate_factor',
                               'sample_rate_multiplier',
                               'activity_flags',
                               'io_and_clock_flags',
                               'data_quality_flags',
                               'number_of_blockettes_that_follow',
                               'time_correction',
                               'beginning_of_data',
                               'first_blockette'),
                           struct.unpack(self.byte_order+'3h4bi2h', binary_string[30:48]))))
        header.update(dict(zip(('blockette_type',
                                'next_blockettes_byte_number',
                                'encoding_format',
                                'word_order',
                                'data_record_length',
                                'reserved'
                                ),
                               struct.unpack(self.byte_order+'2h4b', binary_string[48:56]))))
        return header

    def read_block_header(self, binary_string):
        """ Read header of block to verbose mode """
        
        tmp=self.extract_block_header(binary_string)
        if not tmp:
            return None
        tmp['sequence_number']=int(tmp['sequence_number'])
        
        tmp['block_size']=2**tmp['data_record_length']
        
        # calcuate frequency sampling
        if tmp['sample_rate_multiplier']>0:
            value=1.0*tmp['sample_rate_factor']*tmp['sample_rate_multiplier']
        else:
            value=1.0*tmp['sample_rate_factor']/tmp['sample_rate_multiplier']
        
        if tmp['sample_rate_factor']<=0:
            value=1/value
        tmp['frequency_sampling']=abs(value)
        
        # extract bits
        for i in xrange(7):
            tmp['activity_flags_bit{}'.format(i)]=bool(tmp['activity_flags']>>i&0x1)
        for i in xrange(6):
            tmp['io_and_clock_flags_bit{}'.format(i)]=bool(tmp['io_and_clock_flags']>>i&0x1)
        for i in xrange(8):
            tmp['data_quality_flags_bit{}'.format(i)]=bool(tmp['data_quality_flags']>>i&0x1)
        return tmp
    
class Steim1_Reader(_Steim):
    """ Class implement Steim-1 compression algorithm """
    
    def __init__(self, *args, **kargs):
        super(Steim1_Reader, self).__init__(*args, **kargs)
      
    def read_block_data(self, binary_string):
        """ Reading record block with only data
        binary_string - binary string with data frames """
        
        start_value=None
        last_value=0
        result=[]
        
        
        for frame_index in xrange(len(binary_string)/64):
            diffs_values=[]
            
            frame_string=binary_string[frame_index*64 : (frame_index+1)*64]
            
            tmp='I2i13I' if not frame_index else '16I' 
            frame_values=struct.unpack(self.byte_order+tmp, frame_string)
            
            # reading data
            nibbles=frame_values[0]
            if frame_index==0:
                start_value=frame_values[1]
                end_value=frame_values[2]
                differences=frame_values[3:]
            else:
                differences=frame_values[1:]
            
            for i,diff in enumerate(differences):
                nibble=(nibbles>>((len(differences)-i-1)*2))&0b11
                
                if nibble==0b01:
                    diffs_values.extend(self.get_values_from_int(diff, 8))
                elif nibble==0b10:
                    diffs_values.extend(self.get_values_from_int(diff, 16))
                elif nibble==0b11:
                    diffs_values.extend(self.get_values_from_int(diff, 32))
                elif nibble==0b00 and self.warnings:
                    print 'Warning! Finded 0b00 bits in nibbles, perhaps data is wrong'
                 
            if frame_index==0:
                last_value=start_value
                result.append(last_value)
            
            for i,diff in enumerate(diffs_values):
                if frame_index==0 and i==0:
                    continue 
                last_value+=diff
                result.append(last_value)
        
        if end_value!=result[-1] and self.warnings:
            print 'ERROR - end value of block wrong!'
            
        return result
        

class Steim2_Reader(_Steim):
    """ Steim-2 it's advanced version of algorithm Steim """
    
    def __init__(self, *args, **kargs):
        super(Steim2_Reader, self).__init__(*args, **kargs)

    def read_block_data(self, binary_string):
        """ Reading data values inside block 
        
        binary_string - sting of bytes """
         
        start_value=None
        last_value=0
        result=[]
        
        for frame_index in xrange(len(binary_string)/64):
            diffs_values=[]
            
            frame_string=binary_string[frame_index*64 : (frame_index+1)*64]
            
            # First frame of block always have start and end values, other frames no.
            # Depending of frame number will be different template for parse binary string.
            tmp='I2i13I' if not frame_index else '16I' 
            frame_values=struct.unpack(self.byte_order+tmp, frame_string)

            # reading data
            nibbles=frame_values[0]
            if frame_index==0:
                start_value=frame_values[1]
                end_value=frame_values[2]
                differences=frame_values[3:]
            else:
                differences=frame_values[1:]
            
            # get differences values
            for i,diff in enumerate(differences):
                nibble=(nibbles>>((len(differences)-i-1)*2))&0b11
                
                dnib=diff>>30&0x3
                
                if nibble==0b01:
                    diffs_values.extend(self.get_values_from_int(diff, 8))
                
                elif nibble==0b10:
                    
                    if dnib==0b01:
                        diffs_values.extend(self.get_values_from_int(diff, 30))
                    elif dnib==0b10:
                        diffs_values.extend(self.get_values_from_int(diff, 15))
                    elif dnib==0b11:
                        diffs_values.extend(self.get_values_from_int(diff, 10))
                    elif self.warnings:
                        print 'Warning, founded dnib with bits 0b00 while c=0b10'
                
                elif nibble==0b11:
                    if dnib==0b00:
                        diffs_values.extend(self.get_values_from_int(diff, 6))
                    if dnib==0b01:
                        diffs_values.extend(self.get_values_from_int(diff, 5))
                    if dnib==0b10:
                        diffs_values.extend(self.get_values_from_int(diff, 4))
                    if dnib==0b11 and self.warnings:
                        print 'Warning, founded dnib with bits 0b11 while c=0b11'
                
                elif self.warnings:
                    print 'Warning, founded c=0b00,  data missing or incorrect'

            # getting results values
            if frame_index==0:
                last_value=start_value
                result.append(last_value)
            
            for i,diff in enumerate(diffs_values):
                if frame_index==0 and i==0:
                    continue
                last_value+=diff
                result.append(last_value)
        
        if end_value!=result[-1] and self.warnings:
            print 'ERROR - end value of block wrong!'
        
        return result 
    
class Steim2_Writer(object):
    """ Class implement pack values to miniSEED block with Steim-2 compression """
    
    # Block index counter
    block_index=0
    
    def __init__(self, block_size=4096, byte_order='>'):
        self.byte_order=byte_order
        self.block_size=block_size
        
        # Number frames in each block
        self._frame_number_in_block=(self.block_size-64)/64
        
        self.first_value_in_block=None
        
        # Frame index counter
        self.frame_index=0
        
        # Frame content
        self.frames_str=''
        
        self.last_value=None
        # buffer for diffs
        self.buffer=[]
        # buffer for values
        self.values=[]
        # buffer for datetimes of values
        self.buffer_datetimes=[]
        # buffer for unsigned integers
        self.tmp_integers=[]
        self.result_value=None
        
        # Number of values in block. This counter recorded in header of block
        self.number_of_values_in_block_counter=0
        
        # Header info
        self.header={}
        
        self.nibbs=[]
        
        # Flag of first value of block
        self._first_value_flag=True
        
        # STRONGLY for debug and unittest
        # if recording was cold start the very first diffs is 0, but
        # if needed to emulate situation that was previous blocks and was no cold start
        # use this parameter to emulate first diff of last value
        self.__cold_start_last_value=0
        
        # need for close block
        self.__need_close=False
    
    def _pack_header(self, dictionary=None):
        """ Pack header string from dictionary if exists or from header attribute """
        
        template=(self.byte_order+'6s1s1s5s2s3s2s'+\
             '2h4bh'+\
             '3h4bi2h'+\
             '2h3b9c')
        if dictionary:
            tmp=[]
            for item in ('sequence_number',
                         'data_header_indicator',
                         'reserved_byte',
                         'station',
                         'location',
                         'channel',
                         'network',
                         'record_start_time',
                         'number_of_samples',
                         'sample_rate_factor',
                         'sample_rate_multiplier',
                         'activity_flags',
                         'io_and_clock_flags',
                         'data_quality_flags',
                         'number_of_blockettes_that_follow',
                         'time_correction',
                         'beginning_of_data',
                         'first_blockette'):
                tmp.append(dictionary[item])

        else:
            tmp=[Steim2_Writer.block_index,
                 self.header.get('data_header_indicator','D'),
                 '\x00',
                 self.header.get('station').ljust(5, ' '),
                 self.header.get('location').ljust(2, ' '),
                 self.header.get('channel').ljust(3, ' '),
                 self.header.get('network').ljust(2, ' ')]+\
                 [getattr(self.first_datetime, x) for x in ('year','month','hour','minute','second','microsecond')]+\
                 [self.number_of_values_in_block_counter,
                 self.header.get('sample_rate_factor'),
                 self.header.get('sample_rate_multiplier'),
                 self.header.get('activity_flags', 0),
                 self.header.get('io_and_clock_flags', 0),
                 self.header.get('data_quality_flags', 0),
                 self.header.get('number_of_blockettes_that_follow', 0),
                 self.header.get('time_correction', 0),
                 self.header.get('beginning_of_data', 64),
                 self.header.get('first_blockette', 48)]
                 
        # 1000 blockette support 
        tmp.extend([1000, #blockette id
                    0, #there is no any next blockettes
                    11, # STEIM2 compression
                    1 if self.byte_order=='>' else 0, #encoding format
                    math.log(self.block_size, 2), # data record length
                    '\x00']+['\x00']*8) # reserved byte and just nulls
        
        #some postfixes
        tmp[0]='{:0>6}'.format(tmp[0])[-6:]
        tmp[8]=self.first_datetime.timetuple().tm_yday
        tmp.insert(12, 0)
        tmp[13]/=100
        
        return struct.pack(template, *tmp) 
            
            
    
    def _pack_values(self, values, bits):
        """ Pack values of bits into one integer value """
        
        target=0
        for index,value in enumerate(values):
            if value<0:
                if bits==30:
                    value+=2**31
                else:
                    value+=2**bits
            # if value overhead integer value then truncate it 
            if value>(2**31-1):
                value=2**31-1
            target=target|(value<<((len(values)-index-1))*bits)
        
        if bits in (5, 30):
            nibbs=1
        elif bits in (4, 15):
            nibbs=2
        elif bits==10:
            nibbs=3
        else:
            nibbs=0
        target=target|(nibbs<<30)
        return target
            
            
        
    def pack(self, value, datetime_value=None):
        """ Pack value into buffers """
        
        self.values.append(value)
        self.buffer_datetimes.append(datetime_value)
        
        if self.first_value_in_block==None:
            self.first_value_in_block=self.values[0]
            self.last_value=self.first_value_in_block
             
            for index in xrange(len(self.buffer)):
                self.buffer[index]=self.values[index]-self.last_value
                self.last_value=self.values[index]
            
            self.first_datetime=self.buffer_datetimes[0]

        
        if self._first_value_flag: # it may be looks ugly, but it just will be alive
            self._first_value_flag=False
            self.buffer.append(value-self.last_value)
            return (False, None)
        
        self.buffer.append(value-self.last_value)
        
        
        self.last_value=value
        
        # Если буфер не заполнен 7 значениями (для упаковки 7 самых маленьких разниц значений)
        # то сразу сообщаем о незавершенном блоке в ожидании наполнения буфера
        if not self.__need_close and len(self.buffer)<7:
            return (False,None)
        
        # Проверяем как много разниц можно упаковать в 1 число
        code_string,bits=self._process_diffs(self.buffer[:7])
        
        # упаковываем 
        self.tmp_integers.append(self._pack_values(self.buffer[:len(code_string)], bits))
        
        # увеличиваем счетчик количества упакованных значений
        self.number_of_values_in_block_counter+=len(code_string)
        
        # ck
        if bits==8:
            self.nibbs.append(1)
        elif bits in (10,15,30):
            self.nibbs.append(2)
        elif bits in (4,5,6):
            self.nibbs.append(3)
        else:
            raise Warning('Ck=00, frame_index={}, block_index={}, code_string={}, bits={}'.format(self.frame_index, Steim2_Writer.block_index, code_string, bits))
        
        self.last_value_in_block=self.values[len(code_string)-1]
        # delete needless values 
        del self.buffer[:len(code_string)]
        del self.values[:len(code_string)]
        del self.buffer_datetimes[:len(code_string)]
        
        if (self.frame_index==0 and len(self.tmp_integers)==13) or len(self.tmp_integers)==15:
            self._pack_frame()
        if self.frame_index==self._frame_number_in_block:
            return True, self._pack_header()+self._pack_block()
            
        return False,False

    def close_block(self): #FIXME: what happen if it not be the last frame of block???
        """ Flush buffer and fill zeroes free space of block """ 
        
        while True:
            if not self.buffer:
                break
            
            # Проверяем как много разниц можно упаковать в 1 число
            code_string,bits=self._process_diffs(self.buffer[:7])
            
            # упаковываем 
            self.tmp_integers.append(self._pack_values(self.buffer[:len(code_string)], bits))
            
            # увеличиваем счетчик количества упакованных значений
            self.number_of_values_in_block_counter+=len(code_string)
            
            # ck
            if bits==8:
                self.nibbs.append(1)
            elif bits in (10,15,30):
                self.nibbs.append(2)
            elif bits in (4,5,6):
                self.nibbs.append(3)
            else:
                raise Warning('Ck=00, frame_index={}, block_index={}, code_string={}, bits={}'.format(self.frame_index, Steim2_Writer.block_index, code_string, bits))
            
            self.last_value_in_block=self.values[len(code_string)-1]
            # delete needless values 
            del self.buffer[:len(code_string)]
            del self.values[:len(code_string)]
            del self.buffer_datetimes[:len(code_string)]
            
            if (self.frame_index==0 and len(self.tmp_integers)==13) or len(self.tmp_integers)==15:
                self._pack_frame()
            if self.frame_index==self._frame_number_in_block:
                return True, self._pack_header()+self._pack_block()
        
        self.tmp_integers.extend([0]*(15-len(self.tmp_integers)))
        self.nibbs.extend([0]*(15-len(self.nibbs)))
        
        return True, self._pack_header()+self._pack_block()
        
     
    def _pack_frame(self):
        """ Update string of frames for block content; clean attrs """
        
        if self.frame_index==0:
            self.frames_str+=struct.pack(self.byte_order+'I2i13I',
                                         self._pack_nibbs(),
                                         self.first_value_in_block,
                                         self.last_value,
                                         *self.tmp_integers)
        else:
            self.frames_str+=struct.pack(self.byte_order+'16I',
                                         self._pack_nibbs(),
                                         *self.tmp_integers)
        
        # Подготавливаем аттрибуты для новый итерации фреймов
        self.frame_index+=1
        self.nibbs=[]
        self.tmp_integers=[]
        
    def _pack_block(self):
        """ Return string with a complete block content; cleaning attrs """
              
        Steim2_Writer.block_index+=1
        self.frame_index=0
        self._tmp_number_of_values_in_block_counter=self.number_of_values_in_block_counter
        self.number_of_values_in_block_counter=0
        self.first_value_in_block=None
        result=self.frames_str[:8]+struct.pack(self.byte_order+'i', self.last_value_in_block)+self.frames_str[12:]
        self.frames_str=''
        
        return result
        
    def _pack_nibbs(self):
        """ Packing nibbs of frame into unsigned integer """
        
        result=0
        for index,value in enumerate(self.nibbs):
            result=result|(value<<((len(self.nibbs)-index-1))*2)
        return result
    
    def _process_diffs(self, data):
        """ Explore values in 'data' and return result string with the chars code of diffs and number of bits """
        
        tmp=self._explore_diffs(data)
        
        #------------------------------------------------------------------------------ 
        bits=0
        if tmp[:7]=='aaaaaaa':
            bits=4
            s='aaaaaaa'
        elif tmp[:6]=='bbbbbb':
            bits=5
            s='bbbbbb'
        elif tmp[:5]=='ccccc':
            bits=6
            s='ccccc'
        elif tmp[:4]=='dddd':
            bits=8
            s='dddd'
        elif tmp[:3]=='eee':
            bits=10
            s='eee'
        elif tmp[:2]=='ff':
            bits=15
            s='ff'
        elif tmp[0]=='g':
            bits=30
            s='g'
        if bits:
            return s,bits
        
        #------------------------------------------------------------------------------ 
        vn={'a':7,'b':6,'c':5,'d':4,'e':3,'f':2,'g':1}
        nv={7:'a',6:'b',5:'c',4:'d',3:'e',2:'f',1:'g'}
        vb={'a':4,'b':5,'c':6,'d':8,'e':10,'f':15,'g':30}
        
        
        value=max(tmp)
        
        for i in xrange(6,0,-1):
            value=max(tmp[:i])
            if vn[value]>=i:
                new_value=nv[i]
                return new_value*i, vb[new_value]    
        
    def _explore_diffs(self, data):
        """ Explore values in 'data' and return they chars code of bits"""
        
        result=[]
        for value in data:
            if -8<=value<=7:
                result.append('a')
            elif (-16<=value<-8) or (7<value<=15):
                result.append('b')
            elif (-32<=value<-16) or (15<value<=31):
                result.append('c')
            elif (-128<=value<-32) or (31<value<=127):
                result.append('d')
            elif (-512<=value<-128) or (127<value<=511):
                result.append('e')
            elif (-16384<=value<-512) or (511<value<=16383):
                result.append('f')
            else:
                result.append('g')
        return ''.join(result)
            

class miniSEED(object):
    ''' Simple high-level class for reading miniSEED files '''
    
    def __init__(self, filename):
        self.filename=filename
        self.miniSEED_file=open(filename, 'rb')
        
        self.compressors={}
        
    def read_block(self):
        """ Read miniSEED block and return tuple with header dictionary and data """
        
        # get header dictionary
        header=_Steim().read_block_header(self.miniSEED_file.read(64))
        
        # if header is None it mean that end of miniSEED file
        if not header:
            return None,None 
        
        tag='{encoding_format}_{word_order}_{block_size}'.format(**header)
        
        if tag not in self.compressors:
            byte_order='>' if header['word_order'] else '<'
            
            if header['encoding_format']==10:
                self.compressors[tag]=Steim1_Reader(block_size=header['block_size'], byte_order=byte_order)
            elif header['encoding_format']==11:
                self.compressors[tag]=Steim2_Reader(block_size=header['block_size'], byte_order=byte_order)
            else:
                exit('Unknown type of compression with code "{encoding_format}"'.format(**header))
        
        # getting data
        data=self.compressors[tag].read_block_data(self.miniSEED_file.read(self.compressors[tag].block_size-64))
        
        return header, data
        
    
if __name__=='__main__':
    pass
                