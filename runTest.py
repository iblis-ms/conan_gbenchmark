#!/usr/bin/python

import os, sys
import platform


def runCommand(command):
  retcode = os.system(command)
  if retcode != 0:
    raise Exception("Error while executing:\n\t %s" % command)

def runTest(command, prefixCommands = []):
  commands = []
  for prefixCommand in prefixCommands:
    commands.append(prefixCommand)
  commands.append(command)
  print("-----------------------------------------------")
  print(command)
  print("-----------------------------------------------")
  if platform.system() == "Windows":
    fullCommand = " & ".join(commands)
  else:
    fullCommand = ";".join(commands)
  runCommand(fullCommand)

class TestData(object):

  def __init__(self, compilerConan, compilerVersionConan):
    self.compilerConan = compilerConan
    self.compilerVersionConan = compilerVersionConan


class GccClangTestData(TestData):

  def __init__(self, compilerCC, compilerCXX, compilerVersion, compilerConan, compilerVersionConan, libcpp):
    super(GccClangTestData, self).__init__(compilerConan, compilerVersionConan)
    self.compilerCC = compilerCC
    self.compilerCXX = compilerCXX
    self.compilerVersion = compilerVersion
    self.libcpp = libcpp

  def run(self):
    prefixCommands = []
    if platform.system() == "Windows":
      command1 = "SET CC=C:\\Program Files\\mingw-w64\\%s\\mingw64\\bin\\%s.exe" % (self.compilerVersion, self.compilerCC)
      command2 = "SET CXX=C:\\Program Files\\mingw-w64\\%s\\mingw64\\bin\\%s.exe" % (self.compilerVersion, self.compilerCXX)
      prefixCommands = [command1, command2]
    else:
      pathPrefix = "/usr/bin/"
      command1 = "export CC=%s%s-%s" % (pathPrefix, self.compilerCC, self.compilerVersion)
      command2 = "export CXX=%s%s-%s" % (pathPrefix, self.compilerCXX, self.compilerVersion)
      prefixCommands = [command1, command2]
      
    for lib in self.libcpp:
      command = "conan test_package -s compiler=%s -s compiler.version=%s -s compiler.libcxx=%s" % (self.compilerConan, self.compilerVersionConan, lib)
      runTest(command, prefixCommands)

  @staticmethod
  def createClangData(version):
    return GccClangTestData("clang", "clang++", version, "clang", version, ["libc++", "libstdc++11", "libstdc++"])

  @staticmethod
  def createGccData(fileSuffixVersion, conanVersion):
    return GccClangTestData("gcc", "g++", fileSuffixVersion, "gcc", conanVersion, ["libstdc++11", "libstdc++"])


class VisualStudioTestData(TestData):

  def __init__(self, compilerConan, compilerVersion):
    super(VisualStudioTestData, self).__init__(compilerConan, compilerVersion)

  def run(self):
    command = "conan test_package -s compiler=%s -s compiler.version=%s -s compiler.runtime=MD" % (self.compilerConan, self.compilerVersionConan)
    runTest(command)

  @staticmethod
  def createClangData(version):
    return VisualStudioTestData("\"Visual Studio\"", version)

if __name__ == "__main__":

  print("-----------------------------------------------")
  runCommand("conan --version")
  runCommand("cmake --version")
  print("-----------------------------------------------")

  if platform.system() == "Windows":
    testData = [VisualStudioTestData.createClangData("15"),
                GccClangTestData.createGccData("x86_64-6.3.0-posix-seh-rt_v5-rev2", "6.3"),
                GccClangTestData.createGccData("x86_64-5.4.0-posix-seh-rt_v5-rev0", "5.4")]
  else:
    testData = [GccClangTestData.createClangData("4.0"),
                GccClangTestData.createClangData("3.9"),
                GccClangTestData.createClangData("3.8"),
                GccClangTestData.createGccData("6", "6.2"),
                GccClangTestData.createGccData("5", "5.4"),
                GccClangTestData.createGccData("4.8", "4.8")]

  for data in testData:
    data.run()
