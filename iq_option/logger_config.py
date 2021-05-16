from datetime import datetime
import logging
import sys
import os

loggers = {}

def configure_logs(full_file_path, output_level=logging.INFO):

	global loggers
	
	file_name = os.path.basename(full_file_path)

	if loggers.get(file_name):
		return loggers.get(file_name)
	else:
		logger = logging.getLogger(file_name)
		logger.setLevel(output_level)
		logger.propagate = False

		formatter = logging.Formatter('%(asctime)s - %(message)s')

		ch = logging.StreamHandler()
		ch.setLevel(output_level)
		ch.setFormatter(formatter)

		date         = datetime.now().strftime('%Y-%m-%d')
		expiration   = sys.argv[5]
		channel      = sys.argv[6]
		file_name    = f"logs/{date}_{channel}_{expiration}.log"
		file_handler = logging.FileHandler(file_name)
		file_handler.setLevel(output_level)
		file_handler.setFormatter(formatter)

		if (logger.hasHandlers()):
			logger.handlers.clear()

		logger.addHandler(ch)
		logger.addHandler(file_handler)
		loggers[file_name] = logger

		return logger