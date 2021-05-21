from logger_config import configure_logs
from datetime import datetime
import pymongo
import sys

log = configure_logs(__file__)

client   = pymongo.MongoClient("mongodb://myRobot:6eJ%402chTyxn2%2as@vps31866.publiccloud.com.br:27017/")
database = client["my_robot"]

def get_auth():

	user       = sys.argv[1]
	collection = database["users"]
	criteria   = { "name" : user }
	docs       = collection.find(criteria)

	return docs[0]

def get_signals(status = "Pending"):

	date       = datetime.now().strftime('%Y-%m-%d')
	user       = sys.argv[1]
	expiration = sys.argv[5]
	channel    = sys.argv[6]

	collection = database[channel]
	criteria   = { "_id.user"   : user, 
				   "_id.date"   : date, 
				   "expiration" : int(expiration), 
				   "status"     : status }

	return collection.find(criteria)

def update_results(doc, result, gale):

	doc_updated = get_doc(doc)
	if doc_updated["profit"]:
		profit = round(result + doc_updated["profit"], 2)
	else:
		profit = result

	field = "entry_1" if not gale else "entry_2"

	if profit > 0:
		new_values = { "$set": { field: f"WIN: {result}", "profit": profit, "result": "WIN", "status": "Done" }}
	else:
		if gale:
			new_values = { "$set": { field: f"LOSS: {result}", "profit": profit, "result": "LOSS", "status": "Done" }}
		else:
			new_values = { "$set": { field: f"LOSS: {result}", "profit": profit }}
			
	update_doc(doc, new_values)

def update_status(doc, new_status):

	new_values = { "$set": { "status": new_status } }
	
	update_doc(doc, new_values)

def get_doc(doc):

	channel    = sys.argv[6]
	collection = database[channel]

	query = {"_id": doc["_id"]}
	result = collection.find(query)

	return result[0]

def update_doc(doc, new_values):

	channel    = sys.argv[6]
	collection = database[channel]

	query = {"_id": doc["_id"]}
	collection.update_one(query, new_values)

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
		list_signals = get_signals("Done")
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