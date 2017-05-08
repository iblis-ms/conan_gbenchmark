#!/bin/bash

set -e

echo "------------------ program tests ------------------"

currentScriptPath=$(readlink -f "$0")
currentDir=$(dirname "$currentScriptPath")

if [ -d ~/.conan_server/data/GBenchmark ]
then
  rm -rf ~/.conan_server/data/GBenchmark
fi

if [ -d ~/.conan/data/GBenchmark ]
then
  rm -rf ~/.conan/data/GBenchmark
fi

./startConanServer.sh

for compiler in $clangName gcc
do
  for stdlib in libc++ libstdc++ libstdc++11
  do
    if [ "$compiler" != "gcc" ] || [ "$stdlib" != "libc++" ]
    then
      ./run.sh $compiler $stdlib
    fi
  done
done

./stopConanServer.sh

cd "$currentDir"
