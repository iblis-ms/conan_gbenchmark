#!/bin/bash

set -e

export repoBaseDir=`pwd`/../..

export clangVersionMajor=8
export clangVersionMinor=1

export clangVersion=$clangVersionMajor.$clangVersionMinor
export clangCppBin=/usr/bin/clang++
export clangCcBin=/usr/bin/clang
export clangName="apple-clang"

if [ -d ~/.conan_server/data/GBenchmark ]
then
  rm -rf ~/.conan_server/data/GBenchmark
fi

if [ -d ~/.conan/data/GBenchmark ]
then
  rm -rf ~/.conan/data/GBenchmark
fi

./startConanServer.sh

./runConanPackageTest.sh

./runTestPrograms.sh


./stopConanServer.sh