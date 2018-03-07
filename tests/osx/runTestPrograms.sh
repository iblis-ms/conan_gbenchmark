#!/bin/bash

set -e

echo "------------------ program tests ------------------"

callDir=`pwd`


./run.sh clang libc++


cd "$callDir"
