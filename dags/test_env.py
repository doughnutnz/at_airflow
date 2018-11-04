import sys
import os

print(sys.prefix, sys.base_prefix)
dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
cwd = os.getcwd()
print(cwd)
dirlst = os.listdir()
print(dirlst)
