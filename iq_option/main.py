from logger_config import configure_logs
from iq_option import login, change_balance
from datetime import datetime
from utils import get_schedule_time
from mongo import get_signals, check_stop, cancel_signals
import sys
import time
import schedule
import threading

log = configure_logs(__file__)

log.info("Starting robot")

login()
change_balance()
list_signals = get_signals()

def teste():
	log.info("TESTE")

def buy_new_thread(line):
	job_thread = threading.Thread(target=teste)
	job_thread.start()

log.info("List:")
for line in list_signals:
	line.pop("__v")
	log.info(f"{line}")
	schedule.every().day.at(get_schedule_time(line["_id"]["time"])).do(buy_new_thread, line)

log.info(f"Waiting entries time - {sys.argv[6]}")

while True:
	
	if check_stop():
		log.info("Stoping robot")
		cancel_signals()
		break
	
	log.info("NOT Stoping robot")
	schedule.run_pending()
	time.sleep(1)

sys.exit