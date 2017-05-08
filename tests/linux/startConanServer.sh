#!/bin/bash

echo "------------------ start server conan ------------------"

callDir=`pwd`

conan remove -f GBenchmark*

conan_server&
echo "Conan server 1st run: $?"
./stopConanServer.sh
echo "Conan server 1st run was stopped: $?"
cp ../server.conf $HOME/.conan_server/

conan_server&
echo "Conan server 2nd run: $?"

cd $repoBaseDir

conan export iblis_ms/stable

remote=`conan remote list | grep "http://localhost:9300"`
if [ -z "$remote" ]; then
  conan remote add local http://localhost:9300
fi

conan user -p demo -r local  demo
≈
conan upload GBenchmark/1.1.0@iblis_ms/stable --all -r=local --force

echo "GBenchmark was uploaded: $?"

cd "$callDir"
