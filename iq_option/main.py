from datetime import datetime, timedelta
from logger_config import configure_logs
from iq_option import login, change_balance, buy_new_thread
from utils import get_schedule_time
from mongo import get_signals, check_stop, cancel_signals, update_status, count_by_status
import sys
import time
import schedule

log = configure_logs(__file__)

log.info("Starting robot")

login()
change_balance()
list_signals = get_signals()

keyMap = dict()
for line in list_signals:

	sig = dict()
	sig["channel"]    = line["channel"]
	sig["par"]        = line["signal"]["par"]
	sig["date"]       = line["date"]
	sig["time"]       = line["signal"]["time"]
	sig["action"]     = line["signal"]["action"]
	sig["expiration"] = line["expiration"]
	
	key = line["signal"]["time"] + ':00'
	keyMap[key] = sig

log.info(f"Waiting entries time")

while len(keyMap) > 0:

	entry_time = datetime.now() + timedelta(seconds=15)
	entry_time = entry_time.strftime('%H:%M:%S')
	
	if entry_time in keyMap:
		entry = keyMap[entry_time]
		log.info(entry)
		if count_by_status() > 0:
			update_status(entry, "Canceled")
			log.info("Canceled because there is already another transaction in progress")
		else:
			buy_new_thread(entry)
		keyMap.pop(entry_time, None)

	time.sleep(1)

sys.exit