from iqoptionapi.stable_api import IQ_Option
from logger_config import configure_logs
from datetime import datetime
from mongo import get_auth, update_status, update_results
from login import connect
from utils import check_entry_time, get_entry_value, wait_entry, get_check_time
import threading
import time
import sys

log = configure_logs(__file__)

auth       = get_auth()
email      = auth["email"]
password   = auth["password"]
lost_value = 0

API = IQ_Option(email, password)

def login():
	
	connect(API)

def change_balance(): 

	wallet = sys.argv[2]
	API.change_balance(wallet) 
	log.info(f"Wallet: {wallet}")

def get_binaria_payout(par, timeframe):

	log.info(f"get_binaria_payout")

	open_candles = API.get_binary_option_detail()
	binaria_payout = API.get_all_profit()	

	if timeframe <= 5:
		turbo_details = open_candles[par]["turbo"]
		open = turbo_details["enabled"] if turbo_details else False
		return int(100 * binaria_payout[par]["turbo"]) if open else 0
	else:
		binary_details = open_candles[par]["binary"]
		open = binary_details["enabled"] if binary_details else False

		log.info(f"binary_details: {binary_details}")
		log.info(f"open: {open}")

		return int(100 * binaria_payout[par]["binary"]) if open else 0

def get_digital_payout(par):

	log.info(f"get_digital_payout")

	digital_details = API.get_digital_underlying_list_data()["underlying"] # pylint: disable=E1136
	par_details = next((x for x in digital_details if x["underlying"] == par), None)

	log.info(f"digital_details: {digital_details}")
	log.info(f"par_details: {par_details}")

	if(par_details):
		open = next((True for x in par_details["schedule"] if x["open"] < time.time() < x["close"]), False)
		log.info(f"open: {open}")
		return API.get_digital_payout(par) if open else 0
	else:
		return 0

def best_payout(par, timeframe):

	log.info(f"best_payout")

	binaria_payout = get_binaria_payout(par, timeframe)
	digital_payout = get_digital_payout(par)

	if binaria_payout > digital_payout:
		return "BINARIA", binaria_payout  
	else: 
		return "DIGITAL", digital_payout

def buy_new_thread(line):

	log.info(f"buy_new_thread")

	job_thread = threading.Thread(target=buy, args=[line])
	job_thread.start()

def buy(line):

	log.info(f"buy")

	time = line["_id"]["time"]
	par  = line["_id"]["par"]

	if check_entry_time(time):

		option, payout = best_payout(par, 1)
		
		log.info(f"option: {option} - payout: {payout}")

		if payout > 0:
			update_status(line, "Processing")

			if option == "BINARIA":
				buy_binaria(line, payout)
			else:
				buy_digital(line, payout)
		else:
			update_status(line, "Closed")

def buy_digital(line, payout, recovery_value = None, gale = False):

	global lost_value
	entry_time = line["_id"]["time"]
	par        = line["_id"]["par"]
	action     = line["action"]
	timeframe  = int(line["expiration"])

	if recovery_value == None:
		recovery_value = abs(lost_value)
		
	entry_value = get_entry_value(recovery_value, payout)
	
	wait_entry(entry_time)

	buys_status, id = API.buy_digital_spot_v2(par, entry_value, action, timeframe)
		
	if(buys_status):
		
		buy_gale(line, payout, entry_value, id, buy_digital, gale)

		while True:
			status,result = API.check_win_digital_v2(id)
			
			if status:
				calculate_result(line, result, gale, entry_value, recovery_value)
				break
	else :
		update_status(line, "Fail Dig")
		buy_binaria(line, payout)

def buy_binaria(line, payout, recovery_value = None, gale = False):

	global lost_value
	entry_time = line["_id"]["time"]
	par        = line["_id"]["par"]
	action     = line["action"]
	timeframe  = int(line["expiration"])

	if recovery_value == None :
		recovery_value = abs(lost_value)
		
	entry_value = get_entry_value(recovery_value, payout)

	wait_entry(entry_time)

	status,id = API.buy(entry_value, par, action, timeframe)
	
	if(status):
		
		buy_gale(line, payout, entry_value, id, buy_binaria, gale)
		
		result = API.check_win_v3(id)
		calculate_result(line, result, gale, entry_value, recovery_value)
	else:
		update_status(line, "Fail Bin")
		buy_digital(line, payout)

def buy_gale(line, payout, entry_value, id, option, gale):

	par       = line["_id"]["par"]
	action    = line["action"]
	timeframe = int(line["expiration"])

	if not gale and check_gale(id, par, timeframe, action):
		job_thread = threading.Thread(target=option, args=[line, payout, entry_value, True])
		job_thread.start()

def check_gale(id, par, timeframe, action):

	check_time = get_check_time(timeframe)

	while True:
		now = datetime.now().strftime('%H:%M:%S')
		if(now == check_time):
			result = check_win_current(id, par, timeframe, action)
			return True if result == "LOSS" else False
		time.sleep(1)	

def check_win_current(id, par, timeframe, action):

	vela = API.get_candles(par, 60*timeframe, 1, time.time())[0] # pylint: disable=E1136
	
	open = vela["open"]
	close = vela["close"]
	result = "LOSS"

	if (action == "CALL" and open < close) or (action == "PUT" and open > close):
		result = "WIN"

	return result

def calculate_result(line, result, gale, entry_value, recovery_value):

	global lost_value

	result     = round(result, 2)
	time       = line["_id"]["time"]
	par        = line["_id"]["par"]
	action     = line["action"]
	timeframe  = int(line["expiration"])

	if result > 0:
		log.info(f"{time} - {par} - {action} - {timeframe} - WIN: {result}")
		if recovery_value > 0 and (not gale and abs(lost_value) >= recovery_value):
			lost_value = lost_value + recovery_value
	else:
		if gale:
			log.info(f"{time} - {par} - {action} - {timeframe} - LOSS: {result - recovery_value}")
			lost_value = round(lost_value - entry_value - recovery_value, 2)

	update_results(line, result, gale)
	