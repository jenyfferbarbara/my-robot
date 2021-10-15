from datetime import datetime, timedelta
from logger_config import configure_logs
from iq_option import login, change_balance, buy_new_thread, get_stop_win, get_stop_loss
from mongo import get_signal, get_signals, update_status, count_by_status, get_summaries, cancel_signals
import sys
import time

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

stop_win  = get_stop_win()
stop_loss = get_stop_loss()
stop = False

while len(keyMap) > 0 and stop == False:

	entry_time = datetime.now() + timedelta(seconds=30)
	date       = entry_time.strftime('%Y-%m-%d')
	entry_time = entry_time.strftime('%H:%M:%S')	
	
	summaries = get_summaries(date)
	profit    = sum(summary["profit"]  for summary in summaries)

	if profit >= stop_win or profit <= stop_loss:
		status = "WIN" if profit >= stop_win else "LOSS"
		log.info(f"STOP {status} - All Pending signals will be cancelled.")
		cancel_signals(list(keyMap.values()))
		stop = True
	else:
		if entry_time in keyMap:
			entry = keyMap[entry_time]
			log.info(entry)
			if count_by_status() > 0:
				update_status(entry, "Canceled")
				log.info("Canceled because there is already another transaction in progress")
			else:
				sig = get_signal(entry)
				if sig["signal"]["status"] == "Pending":
					buy_new_thread(entry)
				else:
					log.info("Buy not made because the signal does not have Pending status")	
			keyMap.pop(entry_time, None)

	time.sleep(1)

sys.exit