from logger_config import configure_logs
from datetime import datetime
import pymongo
import json
import sys
import os

log = configure_logs(__file__)

with open(os.getcwd() + "/config.json") as config_file:
	data = json.load(config_file)

client   = pymongo.MongoClient(f"mongodb://myRobot:6eJ%402chTyxn2%2as@{data['host']}:27017/")
database = client["my_robot"]

def get_auth():

	user       = sys.argv[1]
	collection = database["users"]
	criteria   = { "name" : user }
	docs       = collection.find(criteria)

	return docs[0]

def get_signals(status = "Pending"):

	user       = sys.argv[1]
	collection = database["signals"]
	criteria   = { "user"   	   : user, 
				   "signal.status" : status }

	return collection.find(criteria)

def get_signals_to_cancel(doc):

	user   	   = sys.argv[1]
	collection = database["signals"]		
	query	   = { 	"user"	 	    : user,
					"date"		    : doc["date"],
					"channel"	    : doc["channel"],
					"expiration"	: doc["expiration"],
					"signal.status" : "Pending" }

	list_signals = collection.find(query)

	signals = []
	for line in list_signals:
		sig = dict()
		sig["channel"]    = line["channel"]
		sig["par"]        = line["signal"]["par"]
		sig["date"]       = line["date"]
		sig["time"]       = line["signal"]["time"]
		sig["action"]     = line["signal"]["action"]
		sig["expiration"] = line["expiration"]
		signals.append(sig)

	return signals

def get_signal(doc):

	user   	   = sys.argv[1]
	collection = database["signals"]		
	query	   = { 	"user"	 	    : user,
					"date"		    : doc["date"],
					"channel"	    : doc["channel"],
					"expiration"	: doc["expiration"],
					"signal.par"    : doc["par"],
					"signal.time"   : doc["time"],
					"signal.action" : doc["action"]}

	result = collection.find(query)
	return result[0]

def update_results(doc, result, recovery_value, gale):	

	summary = get_summary(doc)
	result  = round(result, 2)
	profit  = round(result + summary["profit"], 2)
	channel = get_channel(doc["channel"])

	if result > 0:
		new_values_sig = { "$set": 
			build_new_values_sig(
				"Win", 
				"Done", 
				None if gale else result, 
				result if gale else None) }
		new_values_sum = { "$set": 
			build_new_values_sum(
				profit, 
				None if gale else 0, 
				summary["win"] + 1, 
				None) }
		log.info(f"WIN: {result}")
	else:
		new_values_sig = { "$set": 
			build_new_values_sig(
				"Loss", 
				"Done" if gale or channel["gale"] == False else None, 
				None if gale else result, 
				result if gale else None) }
		new_values_sum = { "$set": 
			build_new_values_sum(
				profit, 
				round(result - recovery_value + summary["recovery"], 2) if gale or channel["gale"] == False else None, 
				None, 
				summary["loss"] + 1 if gale or channel["gale"] == False else None) }
		log.info(f"LOSS: {result}")
			
	update_signals(doc, new_values_sig)
	update_summaries(summary, new_values_sum)
	check_stop(doc)
	sys.exit

def build_new_values_sig(res_status, sig_status, res_gain, res_gale):

	new_values_sig = {}
	new_values_sig["result.status"] = res_status

	if res_gain != None:
		new_values_sig["result.gain"] = res_gain
	else:
		new_values_sig["result.gale"] = res_gale

	if sig_status != None:
		new_values_sig["signal.status"] = sig_status
	
	return new_values_sig

def build_new_values_sum(profit, recovery, win, loss):

	new_values_sum = {}
	new_values_sum["profit"] = profit

	if recovery != None:
		new_values_sum["recovery"] = recovery
	
	if win != None:
		new_values_sum["win"] = win

	if loss != None:
		new_values_sum["loss"] = loss
	
	return new_values_sum

def update_status(doc, new_status):

	new_values = { "$set": { "signal.status": new_status } }
	update_signals(doc, new_values)

def update_signals(doc, new_values):
	
	collection = database["signals"]
	result 	   = get_signal(doc)
	criteria   = {"_id": result["_id"]}	
	collection.update_one(criteria, new_values)

def get_summary(doc):

	user   	   = sys.argv[1]
	collection = database["summaries"]

	query  = {  "user"	 	    : user,
				"date"		    : doc["date"],
				"channel"	    : doc["channel"],
				"expiration"	: doc["expiration"]}
	result = collection.find(query)
	
	return result[0]

def get_summaries(date):

	user   	   = sys.argv[1]
	collection = database["summaries"]

	query  = {  "user" : user,
				"date" : date }

	return collection.find(query)

def update_summaries(doc, new_values):

	collection = database["summaries"]

	criteria   = {"_id": doc["_id"]}
	collection.update_one(criteria, new_values)

def count_by_status(doc, status = "Processing"):

	user       = sys.argv[1]
	collection = database["signals"]
	criteria   = { "user"   	    : user,
					"date"		    : doc["date"],
					"channel"	    : doc["channel"],
					"expiration"    : doc["expiration"],
				    "signal.status" : status }

	return collection.count_documents(criteria)

def check_stop(doc):

	summary = get_summary(doc)
	profit = summary["profit"]
	stop_win = summary["stop_win"]
	stop_loss = summary["stop_loss"]

	if  profit >=  stop_win or profit <= stop_loss:
		status = "WIN" if profit >= stop_win else "LOSS"
		log.info(f"STOP {status} - Profit: {profit}, stop_win: {stop_win}, stop_loss: {stop_loss}")
		cancel_signals(get_signals_to_cancel(doc))

def cancel_signals(list_signals):

	for line in list_signals:
		update_status(line, "Canceled")

def get_channel(channel):

	collection = database["channels"]

	query  = { "name" : channel }
	result = collection.find(query)
	
	return result[0]