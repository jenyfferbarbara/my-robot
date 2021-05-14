from logger_config import configure_logs
from iq_option import login, change_balance, buy_new_thread
from datetime import datetime
from utils import get_schedule_time
from mongo import get_signals, check_stop, cancel_signals
import sys
import time
import schedule
import threading

log = configure_logs(__file__)

exit = False

log.info("Starting robot")

login()
change_balance()
list_signals = get_signals()

def teste():
	log.info('teste: ', datetime.now)

log.info("List:")
for line in list_signals:
	line.pop("__v")
	log.info(f"{line}")
	log.info("schedule:", get_schedule_time(line["_id"]["time"]))
	schedule.every(1).day.at(get_schedule_time(line["_id"]["time"])).do(buy_new_thread, line)
	schedule.every(1).minute.do(teste)

log.info(f"Waiting entries time - {sys.argv[6]}")

while not exit:
	
	if check_stop():
		log.info("Stoping robot")
		cancel_signals()
		exit = True
		break
	else:
		schedule.run_pending()
		time.sleep(1)

sys.exit()