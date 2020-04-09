#!/bin/python3.6
import os,sys,shutil
from lib.dump import *

if("-h" in sys.argv or "--help" in sys.argv):
    width=shutil.get_terminal_size()[0]
    print("#"*width)
    print("DumPy - A python based mysql dump tool\n")
    print(f"{sys.argv[0]} [DB-Name] --create           # Creates dump")
    print(f"{sys.argv[0]} [DB-Name] --apply (--force)  # Load dump into mySQL (Overwrite existent database)")
    print("#"*width)
    sys.exit(0)
if(len(sys.argv) >= 3):
    if(sys.argv[1][0] == "-"):
        print("Database can not start with a '-'")
        sys.exit(1)
    else:
        DB_NAME=sys.argv[1]


    if("--create" in sys.argv):
        createDump(db=DB_NAME)
    elif("--apply" in sys.argv):
        if("--force" in sys.argv):
            clearDB(db=DB_NAME)
        applyDump(db=DB_NAME)
else:
    print("Too few arguments!\nPlease try with -h or --help")
