#!/bin/bash


while read -r link name;
do
	wget $link -O $name.cbr
	
done

