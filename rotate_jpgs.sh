#!/bin/bash
# rotates every other jpg image in a directory
# by default, rotates odd-numbered images by 180 degrees
# add "even" or "all" as an argument to rotate even-numbered or all images
# add a number from 0-360 as an argument to rotate (clockwise) by that many degrees
# https://github.com/montinevra/ebook_tools

rotation=180

re='^[0-9]+$'
if [[ $1 =~ $re && $1 -ge 0 && $1 -le 360 ]]
then
	rotation=$1
fi

if [[ $2 =~ $re && $2 -ge 0 && $2 -le 360 ]]
then
	rotation=$2
fi

if [[ $1 == "even" || $2 == "even" ]]
then
	sips -r $rotation *[02468].jpg
elif [[ $1 == "all" || $2 == "all" ]]
then
	sips -r $rotation *.jpg
else # [[ $1 == "odd" || $2 == "odd" ]]
	sips -r $rotation *[13579].jpg
fi