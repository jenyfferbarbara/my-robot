import schedule
import time

def teste():
	print("TESTE")

schedule.every(10).seconds.do(teste)

while True:
	schedule.run_pending()
	time.sleep(1)