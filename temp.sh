#!/bin/bash

# val = $(($1))

while true
do
	vcgencmd measure_temp
	# sleep $val
	sleep $1
done

