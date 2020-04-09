#!/bin/python3.6
import time, schedule
import lib.dump as dump
#this code should run in the background and control time defined action (create a backup every 2h.... etc.)

var=True

def run():
    global var
    if(var==True):
        print("RUN A")
        var=False
    else:
        print("RUN B")
        var=True

def setup():
    print("SETUP")
    schedule.every().day.at("12:00").do(run)
    schedule.every().day.at("20:00").do(run)
    main()

def main():
    while True:
        schedule.run_pending()
        time.sleep(1)



setup()
