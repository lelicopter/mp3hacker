#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True

from pyMP3hacker import MP3parser

if __name__ == '__main__':
    if len(sys.argv) == 1:
        src_filename = "test.mp3"
    else:
        src_filename = sys.argv[1]

    p = MP3parser(src_filename)
    frames = p.frames
    tags = p.tags

    print "frame;",
    print "hdr.raw;",
    print "ver;",
    print "layer;",
    print "has CRC;",
    print "bitrate(kps);",
    print "sample rate;",
    print "padding;",
    print "channel mode;",
    print "n channels;",
    print "mode extention;",
    print "copyrighted;",
    print "original copy;",
    print "emphasis;",
    print "crc.raw;",
    print "main_data_begin;",
    print "privatebits;",
    print "scale factor select info;",
    print "part 2_3 len;",
    print "big values;",
    print "global gain;",
    print "scalefac_compress;",
    print "win switch flag;",
    print "block type;",
    print "mixed block flag;",
    print "table select;",
    print "subblock gain;",
    print "region0_count;",
    print "region1_count;",
    print "preflag;",
    print "scalefac_scale;",
    print "count1table select;",
    print "side_info.raw;",
    print "scale_factors.raw;",
    print "main_data.raw;",
    print "ancillary_data.raw"
        
    for frame in frames:
        print frame.id,';',
        print "'"+frame.hdr.raw,';',
        print frame.hdr.mpeg_version,';',
        print frame.hdr.layer,';',
        print frame.hdr.has_CRC,';',
        print frame.hdr.bitrate,';',
        print frame.hdr.smpl_rate,';',
        print frame.hdr.padding,';',
        print frame.hdr.channel_mode,';',
        print frame.hdr.n_channels,';',
        print frame.hdr.mode_extention,';',
        print frame.hdr.copyrighted,';',
        print frame.hdr.original,';',
        print frame.hdr.emphasis,';',
        print "'"+frame.crc.raw,';',
        print frame.side_info.main_data_begin,';',
        print frame.side_info.private_bits,';',
        print frame.side_info.scfsi,';',
        print frame.side_info.part2_3_length,';',
        print frame.side_info.big_values,';',
        print frame.side_info.global_gain,';',
        print frame.side_info.scalefac_compress,';',
        print frame.side_info.window_switching_flag,';',
        print frame.side_info.block_type,';',
        print frame.side_info.mixed_block_flag,';',
        print frame.side_info.table_select,';',
        print frame.side_info.subblock_gain,';',
        print frame.side_info.region0_count,';',
        print frame.side_info.region1_count,';',
        print frame.side_info.preflag,';',
        print frame.side_info.scalefac_scale,';',
        print frame.side_info.count1table_select,';',
        print "'"+frame.side_info.raw,';',
        print "'"+frame.scale_factors.raw,';',
        print "'"+frame.main_data.raw,';',
        print "'"+frame.ancillary_data.raw
