#!/usr/bin/env python

import sched
import time
import logging
import sys
import os

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh = logging.FileHandler("sasayaki.log")
fh.setFormatter(formatter)

logger = logging.getLogger("Sasayaki")
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

def alerter(st, d):
    st = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st))
    m = "Check Milk-Pump Sterilizer (start at {} then reached {} minutes)".format(st, d)
    logger.info(m)
    send_mesg(m)

def send_mesg(mesg, subtitle='Please!'):
    context = [
        "-title Sasayaki Notification",
        "-subtitle {!r}".format(subtitle),
        "-message {!r}".format(mesg)
    ]
    os.system("terminal-notifier {}".format(' '.join(context)))


if __name__ == '__main__':
    time_schedule_min = int(sys.argv[1])
    time_schedule_sec = time_schedule_min * 60
    pre_alert_sec = time_schedule_sec - 30
    scheduler = sched.scheduler(time.time, time.sleep)

    start_time = time.time()
    scheduler.enter(
        delay=pre_alert_sec,
        priority=1,
        action=send_mesg,
        argument=("30 sec to complete {} minutes".format(time_schedule_min),)
    )
        
    scheduler.enter(
        delay=time_schedule_sec, 
        priority=1, 
        action=alerter,
        argument=(start_time, time_schedule_min,)
    )
    scheduler.run()