#!/usr/bin/env python3
# -*- coding: utf8 -*-
SRC_DIR='/media/olivier/USB/playlist voiture'
DST_DIR='/home/olivier/au/pv'
T_MIX=5000
import os
from pydub import AudioSegment
def save_song(song,i,output='mp3'):
    dst=os.path.join(
            DST_DIR,
            '{}.{}'.format(str(i).zfill(5),output),
        )
    print('[W] {} [{}s]'.format(dst,len(song)/1000))
    song.export(
            dst,
            format=output,
            bitrate='192k',
        )
def main():
    if not os.path.isdir(DST_DIR):
        os.makedirs(DST_DIR)
    last,last_method,i=None,None,0
    for root,dirs,files in os.walk(SRC_DIR):
        for f in sorted(files):
            fullname=os.path.join(
                    root,
                    f,
                )
            ext=f.split('.')[-1]
            if ext == 'ogg':
                method=AudioSegment.from_ogg
            elif ext == 'mp3':
                method=AudioSegment.from_mp3
            else:
                continue
            print('[R] {}'.format(fullname))
            song=method(fullname)
            if None is last:
                lhistoiresansfin=song[:-T_MIX]
                save_song(lhistoiresansfin,i)
                i=i+1
            else:
                lastsong=last_method(last)
                mix=lastsong[-T_MIX:].overlay(song[:T_MIX])
                save_song(mix,i)
                i=i+1
                bayrou=song[T_MIX:-T_MIX]
                save_song(bayrou,i)
                i=i+1
            last,last_method=fullname,method
    fin=song[-T_MIX:]
    save_song(fin,i)
if __name__ == '__main__':
    main()
