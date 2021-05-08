from iqoptionapi.stable_api import IQ_Option
from logger_config import configure_logs
import time

log = configure_logs(__file__)

def connect(API):

	log.info("Signing in IqOption")

	check, reason = API.connect()

	while True: 
		if API.check_connect() == False:
			log.info("Try reconnect")
			check,reason = API.connect()

			if check:
				log.info("Reconnect successfully")
			else:
				if "invalid_credentials" in reason:
					log.info("Wrong Password")
					break
				else:
					log.info("No Network")        
		else:    
			log.info("Connect successfully")
			break

		time.sleep(1)