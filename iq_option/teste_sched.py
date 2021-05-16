from logger_config import configure_logs
import threading
import schedule
import time

log = configure_logs(__file__)

def teste():
	log.info("TESTE")

def buy_new_thread():
	job_thread = threading.Thread(target=teste)
	job_thread.start()

schedule.every(10).seconds.do(buy_new_thread)

while True:
	schedule.run_pending()
	time.sleep(1)