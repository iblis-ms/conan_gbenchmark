#!/bin/bash

set -e

cd /test
conan_server&
conan export iblis_ms/stable
conan remote add local http://localhost:9300
conan user -p demo -r local  demo
conan upload GBenchmark/1.1.0@iblis_ms/stable --all -r=local
cd testPrograms
cd app
conan install --build
cd -
mkdir output
cd output
cmake ../app
make
cd bin
./GBenchmarkTestProgram_Linux_GNU
