#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True

from pyMP3hacker import MP3parser

_not = lambda(x): x[0] in x[1]
_equ = lambda(x): x[0] not in x[1]

def remake_mp3(mp3file_in, mp3file_out, func_check, filterlist):
    if type(mp3file_in) == type('string'):
        p = MP3parser(mp3file_in)
    else:
        p = mp3file_in

    with open(mp3file_out, 'wb') as mp3out:
        mp3out.write(p.tags)
        for frame in p.frames:
            if func_check([frame.id, filterlist]):
                continue
            mp3out.write(frame.rawstr)
    return p

if __name__ == '__main__':
    p = remake_mp3("test.mp3", "frame_15.mp3", _equ, [15])
    remake_mp3(p, "frame_4.mp3", _equ, [4])
    remake_mp3(p, "frame_131.mp3", _equ, [131])
    remake_mp3(p, "frame_not_4_15_131.mp3", _not, [4,15,131])
    remake_mp3(p, "frame_equ_4_15_131.mp3", _equ, [4,15,131])
