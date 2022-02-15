from ast import arguments
import os, sys, time, signal, multiprocessing


sys.stdin = open("help.txt", "r")

fromFile = input()

print(fromFile)

sys.stdin.close()