from logger_config import configure_logs
from utils import get_schedule_time
from mongo import get_signals
import threading
import schedule
import time

log = configure_logs(__file__)

def teste():
	log.info("TESTE")

def buy_new_thread():
	job_thread = threading.Thread(target=teste)
	job_thread.start()

schedule.every().day.at("00:46:15").do(buy_new_thread)
schedule.every().day.at("00:46:30").do(teste)
schedule.every().day.at("00:46:45").do(buy_new_thread)
schedule.every().day.at("00:46:59").do(teste)

while True:
	schedule.run_pending()
	time.sleep(1)