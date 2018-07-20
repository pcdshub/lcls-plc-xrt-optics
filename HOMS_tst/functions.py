import datetime
import logging
import statistics
from timeout import timeout
import numpy as np

# create  logger
level = logging.INFO
log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers = [logging.FileHandler('HOMS_test.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = log_format, handlers = handlers)
logger = logging.getLogger(__name__)

def get_user_confirmation():
	# ask user for confirmation. case insensitive; returns true if positive confirmation.
	answer = ""
	while answer not in ["y", "n"]:
		answer = input("This script moves real hardware.\nMake sure limit switches are working.\nDo you want to continue(Y/N)?").lower()
	return answer == "y"

def verify_axes_coupled(object):
	logger.info("checking if %s axes are coupled" %object.name)
	if object.xgantry.decoupled.value == 1:
		logger.warning("xGantry status: decoupled")
	else:
		logger.info("xGantry status: coupled")

	if object.ygantry.decoupled.value == 1:
		logger.warning("ygantry status: decoupled")
	else:
		logger.info(" ygantry status: coupled")

def get_gantry_difference(object):
	logger.info("getting gantry differences for mirror %s" %object.name)
	logger.info("xgantry difference: %.4f" %object.xgantry.gantry_difference.value)
	logger.info("ygantry_difference: %.4f" %object.ygantry.gantry_difference.value)

def gantry_checks(object_method, how_much, original_position):
	logger.info("movement check....")
	initial_timestamp = object_method.readback.timestamp
	# request a move
	logger.info("moving by %f..." %how_much)
	try:
		object_method.umvr(how_much)
		# record final value
		logger.info("final gantry value for this axis: %.4f. Final gantry difference: %.4f. Time taken for move to complete: %.4f" %(object_method(), object_method.gantry_difference.value, object_method.readback.timestamp-initial_timestamp))
	except TimeoutError:
		logger.error("TimeoutError")
		object_method.stop()
	finally:
		# move in reverse direction
		logger.info("moving to original position...")
		object_method.move(original_position)
		logger.info("done")

def avg_noise_level(object_method):
	logger.info("recording 10 second average value ...")
	position_values = []
	while len(position_values) <= 9:
		position_values.append(object_method.position)
		import time; time.sleep(1)
	average_noise_level = statistics.stdev(position_values)
	logger.info("10 second noise level (standard deviation) is %f %s" %(average_noise_level, object_method.egu))    

def rec_time_for_a_move(object, how_much):
	logger.info("recording time for %f %s move ... " %(how_much, object.pitch.egu))
	initial_timestamp = object.pitch.readback.timestamp
	try:
		object.pitch.umvr(how_much)
		final_timestamp = object.pitch.readback.timestamp
		logger.info("it is: %f seconds" %(final_timestamp - initial_timestamp))
	except TimeoutError:
		logger.error("TimeoutError")
		object.pitch.stop()
	else:
		logger.info('done')

def move_to_limit(high_value, object_method):
	object_method.mv(high_value) # wait = False by default
	while 1:
		if object_method.low_limit_switch.value == False:
			object_method.stop()
			logger.warning("you hit low soft limit switch at %s" %object_method.position)
			limit = object_method.position
			break
	return limit

def low_high_limit(object_method):
	# object method corresponds to whichever axis you want to move eg: fee_m1.xgantry
	try:
		logger.info('going to low limit...')
		low_limit = move_to_limit(-1100, object_method)
	except TimeoutError:
		logger.info("TimeoutError while going to high limit")
		object_method.stop()
	finally:
		try:
			logger.info('going to high limit...')
			while 1:
				if object_method.done.value == 1:
					break
			high_limit = move_to_limit(1100, object_method)
		except TimeoutError:
			logger.info("TimeoutError while going to low limit")
			object_method.stop()
		finally:
			while 1:
				if object_method.done.value == 1:
					break
	return low_limit, high_limit


def request_changeRequest(object_method, initial_position, initial_move_to, move_here_after_change_request):
	try:
		logger.info("requesting a move")
		object_method.move(initial_move_to, wait = False)
		time.sleep(0.5)
		logger.info("issuing new move before previous move is complete")
		object_method.move(move_here_after_change_request, wait = True)

		logger.info("final position is %.4f" %object_method.position) 
		if np.isclose(object_method.position, move_here_after_change_request, atol = 0.1):
			logger.info("final position corresponds to changed target. success")
		else:
			logger.warning("final position doesnot match to changed target. failed: couldnot overwrite the command")
	except TimeoutError:
		logger.error("TimeoutError")