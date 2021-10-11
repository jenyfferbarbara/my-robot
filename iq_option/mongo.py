from logger_config import configure_logs
from datetime import datetime
import pymongo
import json
import sys
import os

log = configure_logs(__file__)

with open(os.getcwd() + '/config.json') as config_file:
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

def update_results(doc, result, recovery_value, gale):	

	summary = get_summaries(doc)
	result  = round(result, 2)
	profit  = round(result + summary["profit"], 2)

	if result > 0:
		new_values_sig = { "$set": { "result.status": 'Win', 
									 "result.gain"  : result,
									 "signal.status": 'Done'} }

		new_values_sum = { "$set": { "profit": profit, 
									 "recovery": 0,
									 "win"   : summary["win"] + 1} }

		log.info(f"WIN: {result}")
	else:
		if gale:
			new_values_sig = { "$set": { "result.status": 'Loss', 
										 "result.gale"  : result,
										 "signal.status": 'Done'} }

			new_values_sum = { "$set": { "profit" : profit, 
									 	 "loss"   : summary["loss"] + 1,
									 	 "recovery": round(result - recovery_value + summary["recovery"], 2)} }

			log.info(f"LOSS: {result}")
		else:			
			new_values_sig = { "$set": { "result.status": 'Loss', 
										 "result.gain"  : result} }

			new_values_sum = { "$set": { "profit": profit } }

			log.info(f"GALE: {result}")
			
	update_signals(doc, new_values_sig)
	update_summaries(summary, new_values_sum)

def update_status(doc, new_status):

	new_values = { "$set": { "signal.status": new_status } }
	update_signals(doc, new_values)

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

def update_signals(doc, new_values):
	
	collection = database["signals"]
	result 	   = get_signal(doc)
	criteria   = {"_id": result["_id"]}	
	collection.update_one(criteria, new_values)

def get_summaries(doc):

	user   	   = sys.argv[1]
	collection = database["summaries"]

	query  = { "user"	 	    : user,
				"date"		    : doc["date"],
				"channel"	    : doc["channel"],
				"expiration"	: doc["expiration"]}
	result = collection.find(query)
	
	return result[0]

def update_summaries(doc, new_values):

	collection = database["summaries"]

	criteria   = {"_id": doc["_id"]}
	collection.update_one(criteria, new_values)

def count_by_status(status = "Processing"):

	user       = sys.argv[1]
	collection = database["signals"]
	criteria   = { "user"   	   : user, 
				   "signal.status" : status }

	return collection.count_documents(criteria)

def check_signals_by_status(status):
	
	retorno = False

	list_signals = get_signals(status)
	for line in list_signals:
		retorno = True
		break

	return retorno

def check_stop():

	if check_signals_by_status("Processing"):
		return False
	else:
		pending = check_signals_by_status("Pending")
		
		profit = 0
		list_signals = get_signals("TESTE")
		profit = sum(line["profit"] for line in list_signals)
		
		stop_win  = int(sys.argv[3])
		stop_loss = int(sys.argv[4])

		if profit >= stop_win or abs(profit) >= stop_loss or not pending:
			log.info(f"STOP - pending: {pending}, profit: {profit}, stop_win: {stop_win}, stop_loss: {stop_loss}")
			return True
		else:
			return False

def cancel_signals():

	list_signals = get_signals()
	for line in list_signals:
		update_status(line, "Canceled")