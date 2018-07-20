import datetime
import logging
import statistics
from timeout import timeout

# create  logger
level = logging.INFO
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers = [logging.FileHandler('HOMS_test.log'), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)
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

def gantry_checks(object_method, how_much, original_position, timeout_seconds):
	logger.info("movement check....")
	initial_timestamp = object_method.readback.timestamp
	# request a move
	logger.info("moving by %f..." %how_much)
	try:
		object_method.umvr(how_much, timeout = timeout_seconds)
		# record final value
		logger.info("final gantry value for this axis: %.4f. Final gantry difference: %.4f. Time taken for move to complete: %.4f" %(object_method(), object_method.gantry_difference.value, object_method.readback.timestamp-initial_timestamp))
	except TimeoutError:
		logger.error("TimeoutError")
		object_method.stop()
	finally:
		try:
			# move in reverse direction
			logger.info("moving to original position...")
			object_method.move(original_position, timeout = timeout_seconds)
			logger.info("done")
		except TimeoutError:
			logger.error('TimeoutError while moving to original position')


def avg_noise_level(object_method):
	logger.info("recording 10 second average value ...")
	position_values = []
	while len(position_values) <= 9:
		position_values.append(object_method.position)
		import time; time.sleep(1)
	average_noise_level = statistics.stdev(position_values)
	logger.info("10 second noise level (standard deviation) is %f %s" %(average_noise_level, object_method.egu))    

def rec_time_for_a_move(object, how_much, timeout_seconds):
	logger.info("recording time for %f %s move ... " %(how_much, object.pitch.egu))
	initial_timestamp = object.pitch.readback.timestamp
	try:
		object.pitch.umvr(how_much, timeout = timeout_seconds)
		final_timestamp = object.pitch.readback.timestamp
		logger.info("it is: %f seconds" %(final_timestamp - initial_timestamp))
	except TimeoutError:
		logger.error("TimeoutError")
		object.pitch.stop()
	else:
		logger.info('done')

def low_high_limit(object_method, timeout_seconds):
	# object method corresponds to whichever axis you want to move eg: fee_m1.xgantry
	try:
		logger.info('going to low limit...')
		object_method.mv(-1100, timeout = timeout_seconds) # wait = False by default
		while 1:
			if object_method.low_limit_switch.value == False:
				object_method.stop()
				logger.warning("you hit low soft limit switch at %s" %object_method.position)
				high_limit = object_method.position
				break
	except TimeoutError:
		logger.info("TimeoutError while going to high limit")
		object_method.stop()
	finally:
		try:
			logger.info('going to high limit...')
			while 1:
				if object_method.done.value == 1:
					break
			object_method.mv(1100, timeout = timeout_seconds) # wait = False by default
			while 1:
				if object_method.high_limit_switch.value == False:
					object_method.stop()
					logger.warning("you hit high soft limit switch at %s" %object_method.position)
					low_limit = object_method.position
					break
		except TimeoutError:
			logger.info("TimeoutError while going to low limit")
			object_method.stop()
		finally:
			while 1:
				if object_method.done.value == 1:
					break
	return low_limit, high_limit

def request_changeRequest(object_method, initial_position, initial_move_to, move_here_after_change_request, timeout_seconds):
	try:
		logger.info("requesting a move")
		object_method.mv(initial_move_to, timeout = timeout_seconds)
		while 1:
			# print("current position is %.9f" %object_method.position)
			if object_method.position > initial_move_to - 0.1 and object_method.position < initial_move_to + 0.1:
				logger.info("issuing new move...")
				object_method.mv(move_here_after_change_request, timeout = timeout_seconds, wait = True)
				break
		logger.info("final position is %.4f" %object_method.position) 
		if object_method() > move_here_after_change_request - 0.02 and object_method() < move_here_after_change_request + 0.02:
			logger.info("final position corresponds to changed target. success")
		else:
			logger.warning("final position doesnot match to changed target. failed: couldnot overwrite the command")
	except TimeoutError:
		logger.error("TimeoutError")