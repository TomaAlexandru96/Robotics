#!/bin/bash

scp pi@129.31.229.243:~/Robotics/logfile.txt . 
# python plot.py & 
python plot.py d=True m=True &

