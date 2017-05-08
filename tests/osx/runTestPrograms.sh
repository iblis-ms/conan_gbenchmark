#!/bin/bash

set -e

echo "------------------ program tests ------------------"

callDir=`pwd`

if [ -d ~/.conan_server/data/GBenchmark ]
then
  rm -rf ~/.conan_server/data/GBenchmark
fi

if [ -d ~/.conan/data/GBenchmark ]
then
  rm -rf ~/.conan/data/GBenchmark
fi

./startConanServer.sh

./run.sh clang libc++

./stopConanServer.sh

cd "$callDir"
