#!/bin/bash

# to get source from 2.27.2 tag: ./source.sh 2.27.2

git clone https://github.com/grame-cncm/faust
cd faust
git checkout $1
git submodule init
git submodule update
find . -name .git -exec rm -rf {} \;
cd ..
tar cvfz faust.tar.gz faust/*
rm -rf faust
