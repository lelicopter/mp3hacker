#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True

dbg_output = True
dbg_output = False

#MP3 HEADER DECODING TABLES
mp3_hdr_ver_tbl = {
    0b00:'MPEG Version 2.5 (later extension of MPEG 2)',
    0b01:'reserved',
    0b10:'MPEG Version 2 (ISO/IEC 13818-3)',
    0b11:'MPEG Version 1 (ISO/IEC 11172-3)',
    }

mp3_hdr_layer_tbl = {
    0b00:  'reserved',
    0b01:  'Layer III',
    0b10:  'Layer II',
    0b11:  'Layer I',
    }

mp3_hdr_bitrate_tbl = {
    '00001111':0,
    '00011111':32,
    '00101111':64,
    '00111111':96,
    '01001111':128,
    '01011111':160,
    '01101111':192,
    '01111111':224,
    '10001111':256,
    '10011111':288,
    '10101111':320,
    '10111111':352,
    '11001111':384,
    '11011111':416,
    '11101111':448,
    '11111111':-1,
    
    '00001110':0,
    '00011110':32,
    '00101110':48,
    '00111110':56,
    '01001110':64,
    '01011110':80,
    '01101110':96,
    '01111110':112,
    '10001110':128,
    '10011110':160,
    '10101110':192,
    '10111110':224,
    '11001110':256,
    '11011110':320,
    '11101110':384,
    '11111110':-1,
    
    '00001101':0,
    '00011101':32,
    '00101101':40,
    '00111101':48,
    '01001101':56,
    '01011101':64,
    '01101101':80,
    '01111101':96,
    '10001101':112,
    '10011101':128,
    '10101101':160,
    '10111101':192,
    '11001101':224,
    '11011101':256,
    '11101101':320,
    '11111101':-1,
    
    '00001011':0,
    '00011011':32,
    '00101011':48,
    '00111011':56,
    '01001011':64,
    '01011011':80,
    '01101011':96,
    '01111011':112,
    '10001011':128,
    '10011011':144,
    '10101011':160,
    '10111011':176,
    '11001011':192,
    '11011011':224,
    '11101011':256,
    '11111011':-1,
    
    '00001010':0,
    '00011010':8,
    '00101010':16,
    '00111010':24,
    '01001010':32,
    '01011010':40,
    '01101010':48,
    '01111010':56,
    '10001010':64,
    '10011010':80,
    '10101010':96,
    '10111010':112,
    '11001010':128,
    '11011010':144,
    '11101010':160,
    '11111010':-1,
    
    '00001001':0,
    '00011001':8,
    '00101001':16,
    '00111001':24,
    '01001001':32,
    '01011001':40,
    '01101001':48,
    '01111001':56,
    '10001001':64,
    '10011001':80,
    '10101001':96,
    '10111001':112,
    '11001001':128,
    '11011001':144,
    '11101001':160,
    '11111001':-1,

    '00000011':0,
    '00010011':32,
    '00100011':48,
    '00110011':56,
    '01000011':64,
    '01010011':80,
    '01100011':96,
    '01110011':112,
    '10000011':128,
    '10010011':144,
    '10100011':160,
    '10110011':176,
    '11000011':192,
    '11010011':224,
    '11100011':256,
    '11110011':-1,
    
    '00000010':0,
    '00010010':8,
    '00100010':16,
    '00110010':24,
    '01000010':32,
    '01010010':40,
    '01100010':48,
    '01110010':56,
    '10000010':64,
    '10010010':80,
    '10100010':96,
    '10110010':112,
    '11000010':128,
    '11010010':144,
    '11100010':160,
    '11110010':-1,
    
    '00000001':0,
    '00010001':8,
    '00100001':16,
    '00110001':24,
    '01000001':32,
    '01010001':40,
    '01100001':48,
    '01110001':56,
    '10000001':64,
    '10010001':80,
    '10100001':96,
    '10110001':112,
    '11000001':128,
    '11010001':144,
    '11100001':160,
    '11110001':-1,
    }

mp3_hdr_smpl_rate_tbl = {
    '0011':44100,
    '0111':48000,
    '1011':32000,
    '1111':0,
      
    '0010':22050,
    '0110':24000,
    '1010':16000,
    '1110':0,
      
    '0000':11025,
    '0100':12000,
    '1000':8000,
    '1100':0,
    }

mp3_hdr_channel_mode_tbl = {
    0b00:'Stereo',
    0b01:'Joint stereo (Stereo)',
    0b10:'Dual channel (2 mono channels)',
    0b11:'Single channel (Mono)',
    }

mp3_hdr_mode_extension_tbl = {
    '0011':'bands 4 to 31',
    '0111':'bands 8 to 31',
    '1011':'bands 12 to 31',
    '1111':'bands 16 to 31',
    
    '0010':'bands 4 to 31',
    '0110':'bands 8 to 31',
    '1010':'bands 12 to 31',
    '1110':'bands 16 to 31',
    
    '0001':'Intensity stereo:off, MS stereo:off',
    '0101':'Intensity stereo:on, MS stereo:off',
    '1001':'Intensity stereo:off, MS stereo:on',
    '1101':'Intensity stereo:on, MS stereo:on',
    }

mp3_hdr_emphasis_tbl = {
    0b00: 'none',
    0b01: '50/15ms',
    0b10: 'reserved',
    0b11: 'CCIT J.17',
    }

sfbtable_l = [0,6,11,16,21]
sfbtable_s = [0,6,12]

slen = [[0, 0, 0, 0, 3, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4],
        [0, 1, 2, 3, 0, 1, 2, 3, 1, 2, 3, 1, 2, 3, 2, 3]]

class BitBfr:
    def __init__(self, s = []):
        self.s=[ord(x) for x in s]
        self.pos = 0
        self.bit_len = len(s)*8

    def seek_abs(self, pos):
        self.pos = pos

    def seek_rel(self, ofst):
        self.pos += ofst

    def read_bits(self, n_bits):
        val = 0
        bits_read = 0
        
        while(bits_read < n_bits):
            val = val << 1
            src_byte = self.s[self.pos//8]
            src_bit = src_byte & (0x80>>(self.pos%8))
            if src_bit != 0:
                val |= 1
            self.pos += 1
            bits_read += 1
        return val      
    
    def bits_left(self):
        if(self.bit_len <= self.pos):
            return 0
        else:
            return (self.bit_len - self.pos)

    def get_pos(self):
        return self.pos

def bf(bv, bl):
    return bin(bv)[2:].zfill(bl)

def decode_binary_string(s):
    return ''.join(chr(int(s[i*8:i*8+8],2)) for i in range(len(s)//8))

class mp3_frame_hdr(object):
    def __init__(self, bitbfr):
        self.mpeg_version = "unknown"
        self.layer = "unknown"
        self.has_CRC = False
        self.bitrate = 0
        self.smpl_rate = 0
        self.padding = False
        self.private = False
        self.channel_mode = "unknown"
        self.mode_extention = "unknown"
        self.copyrighted = False
        self.original = False
        self.emphasis = "unknown"
        self.n_channels = 0
        self.data = 0
        self.size = 32
        self._decode(bitbfr)

    def _decode(self, bitbfr):
        mpeg_version = bitbfr.read_bits(2)
        layer = bitbfr.read_bits(2)

        self.mpeg_version   = mp3_hdr_ver_tbl[mpeg_version]
        self.layer          = mp3_hdr_layer_tbl[layer]
        self.has_CRC        = not bitbfr.read_bits(1)

        bitrate = bf(bitbfr.read_bits(4),4) + bf(mpeg_version,2) + bf(layer,2)
        self.bitrate = mp3_hdr_bitrate_tbl[bitrate]

        smpl_rate = bf(bitbfr.read_bits(2),2)+bf(mpeg_version,2)
        self.smpl_rate = mp3_hdr_smpl_rate_tbl[smpl_rate]

        self.padding        = bitbfr.read_bits(1)
        self.private        = bitbfr.read_bits(1)
        self.channel_mode   = mp3_hdr_channel_mode_tbl[bitbfr.read_bits(2)]

        mode_extention = bf(bitbfr.read_bits(2),2) + bf(layer,2)
        self.mode_extention = mp3_hdr_mode_extension_tbl[mode_extention]

        self.copyrighted    = bitbfr.read_bits(1)
        self.original       = bitbfr.read_bits(1)  
        self.emphasis       = mp3_hdr_emphasis_tbl[bitbfr.read_bits(2)]  
        if(self.channel_mode == "mono"):         
            self.n_channels = 1
        else:
            self.n_channels = 2
        bitbfr.seek_rel(-self.size)
        self.data = bitbfr.read_bits(self.size)

    @property
    def raw(self):
        return bin(self.data)[2:].zfill(self.size) if self.size > 0 else ''

    @property
    def rawstr(self):
        return decode_binary_string(self.raw) if self.size > 0 else ''




class mp3_frame_side_info(object):
    def __init__(self, bitbfr, hdr):
        self.main_data_begin        = 0
        self.private_bits           = 0
        self.scfsi                  = [[0,0,0,0],[0,0,0,0]]
        self.part2_3_length         = [[0,0],[0,0]]
        self.big_values             = [[0,0],[0,0]]
        self.global_gain            = [[0,0],[0,0]]
        self.scalefac_compress      = [[0,0],[0,0]]
        self.window_switching_flag  = [[0,0],[0,0]]
        self.block_type             = [[0,0],[0,0]]
        self.mixed_block_flag       = [[0,0],[0,0]]
        self.table_select           = [[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]]
        self.subblock_gain          = [[[0,0,0],[0,0,0]],[[0,0,0],[0,0,0]]]
        self.region0_count          = [[0,0],[0,0]]
        self.region1_count          = [[0,0],[0,0]]
        self.preflag                = [[0,0],[0,0]]
        self.scalefac_scale         = [[0,0],[0,0]]
        self.count1table_select     = [[0,0],[0,0]]
        self.data = 0
        self.size = 0
        self._decode(bitbfr, hdr)

    def _decode(self, bitbfr, hdr):
        startpos = bitbfr.get_pos()
        self.main_data_begin = bitbfr.read_bits(9)

        if(self.main_data_begin != 0):
            print "Error - dont support bitreservoir yet", self.main_data_begin

        if(hdr.n_channels==1):
            self.private_bits = bitbfr.read_bits(5)
        else:
            self.private_bits = bitbfr.read_bits(3)

        for ch in xrange(hdr.n_channels):
            for i in xrange(4):
                self.scfsi[ch][i] = bitbfr.read_bits(1)

        for gr in xrange(2):
             for ch in xrange(hdr.n_channels):
                  self.part2_3_length[ch][gr] = bitbfr.read_bits(12)
                  self.big_values[ch][gr] = bitbfr.read_bits(9)
                  self.global_gain[ch][gr] = bitbfr.read_bits(8)
                  self.scalefac_compress[ch][gr] = bitbfr.read_bits(4)
                  self.window_switching_flag[ch][gr] = bitbfr.read_bits(1)
                  if(self.window_switching_flag[ch][gr]):
                      self.block_type[ch][gr] = bitbfr.read_bits(2)
                      self.mixed_block_flag[ch][gr] = bitbfr.read_bits(1)
                      for i in xrange(2):
                           self.table_select[ch][gr][i] = bitbfr.read_bits(5)
                      for i in xrange(3):
                           self.subblock_gain[ch][gr][i] = bitbfr.read_bits(3)
                      if(self.block_type[ch][gr] == 2 and self.mixed_block_flag[ch][gr] == 0):
                          self.region0_count[ch][gr] = 8
                      else:
                          self.region0_count[ch][gr] = 7
                      self.region1_count[ch][gr] = 20 - self.region0_count[ch][gr]
                  else:
                       for i in xrange(3):
                           self.table_select[ch][gr][i] = bitbfr.read_bits(5)
                       self.region0_count[ch][gr] = bitbfr.read_bits(4)
                       self.region1_count[ch][gr] = bitbfr.read_bits(3)
                       self.block_type[ch][gr] = 0
                  self.preflag[ch][gr] = bitbfr.read_bits(1)
                  self.scalefac_scale[ch][gr] = bitbfr.read_bits(1)
                  self.count1table_select[ch][gr] = bitbfr.read_bits(1)

        endpos = bitbfr.get_pos()
        self.size = endpos - startpos
        bitbfr.seek_rel(-self.size)
        self.data = bitbfr.read_bits(self.size)

    @property
    def raw(self):
        return bin(self.data)[2:].zfill(self.size) if self.size > 0 else ''

    @property
    def rawstr(self):
        return decode_binary_string(self.raw) if self.size > 0 else ''




class mp3_frame_scale_factors(object):
    def __init__(self, bitbfr, hdr, side_info):
        self.data = 0
        self.size = 0
        self._decode(bitbfr, hdr, side_info)

    def _decode(self, bitbfr, hdr, side_info):
        totalbits = 0
        for gr in xrange(2):
            for ch in xrange(hdr.n_channels):
                #Get scale factors        
                part2_start = bitbfr.get_pos()
                if side_info.window_switching_flag[ch][gr] == 1 and side_info.block_type[ch][gr] == 2:
                    if side_info.mixed_block_flag[ch][gr]:
                        print "mixed scale blocks not supported yet"
                    else:
                        #short blocks
                        for i in xrange(2):
                            for sfb in xrange(sfbtable_s[i], sfbtable_s[i+1]):
                                for window in xrange(3):
                                    totalbits += slen[i][side_info.scalefac_compress[ch][gr]]
                else:
                    #long blocks                   
                    for i in xrange(4):
                        if side_info.scfsi[ch][i] == 0 or gr == 0:
                            for sfb in xrange(sfbtable_l[i], sfbtable_l[i+1]):
                                k = 0 if i < 2 else 1
                                totalbits += slen[k][side_info.scalefac_compress[ch][gr]]
        self.size = totalbits
        self.data = bitbfr.read_bits(self.size)

    @property
    def raw(self):
        return bin(self.data)[2:].zfill(self.size) if self.size > 0 else ''

    @property
    def rawstr(self):
        return decode_binary_string(self.raw) if self.size > 0 else ''




class mp3_frame_crc(object):
    def __init__(self, bitbfr, hdr):
        self.data = 0
        self.size = 0
        self._decode(bitbfr, hdr)

    def _decode(self, bitbfr, hdr):
         if hdr.has_CRC:
            self.size = 16
            self.data = bitbfr.read_bits(self.size)

    @property
    def raw(self):
        return bin(self.data)[2:].zfill(self.size) if self.size > 0 else ''

    @property
    def rawstr(self):
        return decode_binary_string(self.raw) if self.size > 0 else ''




class mp3_frame_main_data(object):
    def __init__(self, bitbfr, side_info):
        self.data = 0
        self.size = 0
        self._decode(bitbfr, side_info)

    def _decode(self, bitbfr, side_info):
        self.size = sum(sum(side_info.part2_3_length,[]))
        self.data = bitbfr.read_bits(self.size)

    @property
    def raw(self):
        return bin(self.data)[2:].zfill(self.size) if self.size > 0 else ''

    @property
    def rawstr(self):
        return decode_binary_string(self.raw) if self.size > 0 else ''




class mp3_frame_ancillary_data(object):
    def __init__(self, bitbfr, frame_size, hdr, crc, side_info, scale_factors, main_data):
        self.data = 0
        self.size = 0
        self._decode(bitbfr,
            frame_size,
            hdr.size,
            crc.size,
            side_info.size,
            scale_factors.size,
            main_data.size)

    def _decode(self, bitbfr,
            frame_size,
            hdr_size,
            crc_size,
            side_info_size,
            scale_factors_size,
            main_data_size):
        self.size = (frame_size*8)-hdr_size-crc_size-side_info_size-scale_factors_size-main_data_size
        self.data = bitbfr.read_bits(self.size)

    @property
    def raw(self):
        return bin(self.data)[2:].zfill(self.size) if self.size > 0 else ''

    @property
    def rawstr(self):
        return decode_binary_string(self.raw) if self.size > 0 else ''




class mp3_frame:
    def __init__(self, bitbfr, framenum):
        self.id       = framenum
        self.hdr            = mp3_frame_hdr(bitbfr)
        self.crc            = mp3_frame_crc(bitbfr, self.hdr)
        self.side_info      = mp3_frame_side_info(bitbfr, self.hdr)
        self.scale_factors  = mp3_frame_scale_factors(bitbfr, self.hdr, self.side_info)
        self.main_data      = mp3_frame_main_data(bitbfr, self.side_info)
        self.ancillary_data = mp3_frame_ancillary_data(bitbfr, self.size, self.hdr, self.crc, self.side_info, self.scale_factors, self.main_data)

    @property
    def size(self):
        return 144 * self.hdr.bitrate * 1000 / self.hdr.smpl_rate + (1 if self.hdr.padding else 0)

    @property
    def raw(self):
        res = ''.join([self.hdr.raw,
            self.crc.raw,
            self.side_info.raw,
            self.scale_factors.raw,
            self.main_data.raw,
            self.ancillary_data.raw])
        return res

    @property
    def rawstr(self):
        return decode_binary_string(self.raw)




class MP3parser:
    def __init__(self, filename):
        file_data = open(filename, "rb").read()
        self.bitbfr = BitBfr(file_data)
        self.frames = []
        self.tags = ''
        self.decode()

    def decode(self):
        #get tags
        self.find_next_syncword()
        tagslen = self.bitbfr.get_pos()-11
        self.bitbfr.seek_abs(0)
        self.tags = decode_binary_string(bf(self.bitbfr.read_bits(tagslen), tagslen))

        #get frames
        self.bitbfr.seek_rel(-1)
        self.framecount = 0
        while self.find_next_syncword():
            self.framecount += 1
            frame = mp3_frame(self.bitbfr, self.framecount)
            self.frames.append(frame)

    def find_next_syncword(self):
        if dbg_output:        
            print "start search sync from %d" % (self.bitbfr.get_pos())
        align = self.bitbfr.get_pos()%8
        if align != 0:        
            if dbg_output:        
                print "align to %d" % (8-align)
            self.bitbfr.read_bits(8-align)
    
        cnt = 0        
        while self.bitbfr.bits_left() > 0:
            b = self.bitbfr.read_bits(1)
            if b == 1:
                cnt += 1
                if cnt == 11:
                    if dbg_output:
                        print "sync found at %d" % (self.bitbfr.get_pos())
                    return True
            else:                
                cnt = 0
        if dbg_output:
            print "sync not found"
        return False
