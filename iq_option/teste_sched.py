from logger_config import configure_logs
import schedule
import time

log = configure_logs(__file__)

def teste():
	log.info("TESTE")

schedule.every(10).seconds.do(teste)

while True:
	schedule.run_pending()
	time.sleep(1)