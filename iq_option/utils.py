from datetime import datetime, timedelta
from dateutil import tz
import time

def get_schedule_time(entry_time):

	return calculate_time(entry_time, 10)

def get_entry_time(entry_time):
	
	return calculate_time(entry_time, 3)

def check_entry_time(entry_time):
	
	now = datetime.now().strftime('%H:%M:%S')
	return now <= entry_time

def wait_entry(entry_time):

	if(entry_time):
		wait_time = get_entry_time(entry_time)

		while True:
			now = datetime.now().strftime('%H:%M:%S')
			if(now >= wait_time):
				break
			time.sleep(1)

def calculate_time(entry, sec):

	time = entry.split(":")
	date = datetime(2021, 1, 1, int(time[0]), int(time[1])) - timedelta (seconds=sec)

	return date.strftime('%H:%M:%S')

def get_check_time(timeframe):

	time = get_time_close(timeframe).split(":")
	date = datetime(2021, 1, 1, int(time[0]), int(time[1]))
	date = date - timedelta (seconds=3)

	return date.strftime('%H:%M:%S')

def get_time_close(timeframe):

	now = datetime.now()
	now_date = now + timedelta(seconds=30)
	if (timeframe > 1):
		now_date = now_date + timedelta(minutes=1)

	while True:
		if now_date.minute % timeframe == 0 and time.mktime(now_date.timetuple()) - now.timestamp() > 30:
			break
		now_date = now_date + timedelta(minutes=1)
	exp = time.mktime(now_date.timetuple())

	return datetime.fromtimestamp(exp).strftime("%H:%M")
	
def get_entry_value(lost_value, payout):

	if(lost_value > 0):
		return get_gale_value(lost_value, payout)
	else:
		return 2

def get_gale_value(entry_value, payout):

	payout = payout/100	
	profit = round(2 * payout, 2)
	loss = float(entry_value)

	while True:
		if round(entry_value * payout, 2) >= round(abs(loss) + profit, 2):
			break
		entry_value += 0.01

	return round(entry_value, 2)