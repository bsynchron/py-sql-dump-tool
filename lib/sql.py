#!/bin/python3.6
import mysql.connector, shutil
import os, json, sys


DB_HOST="localhost"
DB_USER="root"
DB_USER_PASS=""

DB_NAME="to_backup"

BACKUP_PATH="/tmp/backup"



def createDump(db=DB_NAME):
    DB = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    passwd=DB_USER_PASS,
    database=db
    )

    cursor = DB.cursor()
    #create dump
    cursor.execute("SHOW TABLES;") #read all availiable table names from database
    result = cursor.fetchall()
    print(f"\nDatabase: {db}")
    for table in result:    #loop over tables
        os.makedirs(f"{BACKUP_PATH}/d_{db}",exist_ok=True)
        f = open(f"{BACKUP_PATH}/d_{db}/t_{table[0]}.json","wt")
        print(f"\nSaving to: {BACKUP_PATH}/d_{db}/t_{table[0]}.json")
        cursor.execute(f"SELECT * FROM {table[0]};")    #select all data from table
        result = cursor.fetchall()
        cursor.execute(f"SHOW COLUMNS FROM {table[0]};")    #select the column names
        COLS = cursor.fetchall()
        DUMP = [COLS] + [result]    #build representative array
        print(json.dumps(DUMP))
        f.write(json.dumps(DUMP))   #dump json array to file
        f.close()
    #tar dump
    shutil.make_archive(f"{BACKUP_PATH}/d_{db}_dump", "tar", f"{BACKUP_PATH}/d_{db}")
    shutil.rmtree(f"{BACKUP_PATH}/d_{db}/")


def applyDump(db=DB_NAME):
    DB = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    passwd=DB_USER_PASS,
    database=db
    )

    cursor = DB.cursor()

    DUMP_DIR="/tmp/backup/"
    try:
        _FILES=os.listdir(DUMP_DIR)
        if(f"d_{db}_dump.tar" not in _FILES):
            print(f"Dump not in Dump-Dir ({_FILES})")
            sys.exit(1)
        else:
            print("Found Dump!")
    except FileNotFoundError:
        print(f"Dump-Dir not found ({DUMP_DIR})")
        sys.exit(1)
    shutil.unpack_archive(f"{DUMP_DIR}/d_{db}_dump.tar",f"{DUMP_DIR}/d_{db}")
    _FILES=os.listdir(f"{DUMP_DIR}/d_{db}")
    print(_FILES)
    for i in _FILES:
        TABLENAME = i[2:-5]
        if(i[-5:] == ".json" and i[0:2] == "t_"):
            TABLENAME = i[2:-5]
            print(f"Found json: '{i}' / Containing Table: '{TABLENAME}'")
            f = open(f"{DUMP_DIR}/d_{db}/{i}","rt")
            TABLE=json.loads(f.read())
            f.close()
            SQL_QUERY = f"CREATE TABLE {TABLENAME} ("
            for j in TABLE[0]:
                if(j == TABLE[0][-1]):
                    SQL_QUERY+=f"{j[0]} {j[1]}"
                else:
                    SQL_QUERY+=f"{j[0]} {j[1]},"
            SQL_QUERY+=");"
            try:
                EXISTS=False
                cursor.execute(SQL_QUERY)
            except Exception as e:
                EXISTS=True
                print("Could not recreate SQL table! -> ",e)
            for k in TABLE[1]:
                #fill table
        else:
            pass
    shutil.rmtree(f"{BACKUP_PATH}/d_{db}/")

if("--create" in sys.argv):
    createDump("to_backup")
elif("--apply" in sys.argv):
    applyDump()
else:
    print("Please append --create or --apply to the command!")
