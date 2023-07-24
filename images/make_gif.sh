#!/bin/sh

# get a filename from the command line
filename=$1

# get temp filename $$
tmp_filename=xxx.mov

# get base name of the file
name=`basename -s .mov $filename`
gifname=$name.gif

ffmpeg -i $filename -vf setpts=PTS/3.0 -af atempo=3.0 $tmp_filename
ffmpeg  -i $tmp_filename -r 10  $gifname

# remove temp file
rm $tmp_filename

