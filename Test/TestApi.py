# Methods for test_JokeGenerator
import logging
import requests
from re import compile

import TestData as d

testLogger = logging.getLogger(__name__)


def input(p, inputs):
	'''Method to enter input to the program.'''
	if isinstance(inputs, list): 
		for x in inputs:
			p.stdin.write('{}\n'.format(x))
	else:
		p.stdin.write('{}\n'.format(inputs))
	p.stdin.flush()


def checkConsoleOutput(p, expectedOut):
	'''Method to compare console input with expected output.'''
	match = True
	for x in expectedOut:
		#print("expectedOut {}".format(x))
		out = p.stdout.readline()
		#print("out {}".format(out))

		if out != x:
			testLogger.debug("Console output does not match expected ouput.\n\
				\t Expected output: {expected},\n\
				\t Actual output: {actual}".format(
					expected=x,
					actual=out))
			match = False

	return match


def checkExit(p):
	'''Method to check program exits with expected output.'''
	(out,err) = p.communicate(input='{}\n'.format(d.EXIT_PROGRAM))

	if out != ''.join(d.EXIT_PROGRAM_EXPECTED_OUTPUT):
		testLogger.debug(
			"Console output does not match expected ouput.\n\
			\t Expected output: {expected},\n\
			\t Actual output: {actual}".format(
				expected=x,
				actual=out))
		return False

	if err != '':
		testLogger.debug(
			"Error found when exiting.\n\
			Error: {err}".format(err=err))	
		return False

	# returncode values:
	# None if the pess is not closed yet
	# negative value -N if the pess was terminated by signal N
	returnCode = p.poll()
	if returnCode == None:
		testLogger.debug(
			"Program is not exited.\n\
			returncode: {returnCode}".format(returnCode=returnCode))	
		return False
	elif returnCode < 0:
		testLogger.debug(
			"Program is terminated unexpectedly.\n\
			returncode: {returnCode}".format(returnCode=returnCode))	
		return False
	else:
		return True


def getCategories():
	'''Method to retrieve joke category from the external URL.'''

	response = requests.get('{baseURL}/categories'.format(
		baseURL=d.JOKE_BASE_URL))

	import json

	categories = None
	if response.status_code == 200:
		categories = json.loads(response.text)
	else:
		testLogger.debug(
			"Request to {baseURL} is unsuccesful. \n\
			\tStatus Code: {status_code}\n\
			\tResponse Text: {text} ".format(
				baseURL=d.JOKE_BASE_URL,
				status_code=response.status_code,
				text=response.text))
		raise Exception('Request to joke server failed')

	return categories


def checkCategories(p, categories):
	'''
	Method to compare the displayed categories with 
	the ones retrieved from the external URL.
	'''
	if not checkConsoleOutput(p, d.VIEW_CATEGORIES_EXPECTED_OUTPUT):
	 	return False

	match = True
	for idx,c in enumerate(categories, 1):
		out = p.stdout.readline()
		if out != \
			"{idx}. {category}\n".format(idx=idx, category=c):
			testLogger.debug("Displayed categories do not match the external URL\n\
				Expected category: {category}, actual output: {out}"\
				.format(category=category))
			match = False
	return match


def checkChosenCategory(p, category):
	'''Method to check output is expected after a category is chosen.'''
	out = p.stdout.readline()
	if out == \
		"Category Chosen: {}\n".format(category):
		return True
	else:
		return False


def getRandomName(p):
	'''Method to check output is expected after a random name is selected.'''
	out = p.stdout.readline()
	
	pattern = compile("Name Chosen:\\s(.*)\\n")
	match = pattern.match(out)

	name = ''
	if match:
		name = match.group(1)
	else:
		testLogger.debug("Name not found. \n\
			Actual output {out}".format(out=out))
	return name


def checkRandomName(name):
	'''Method to check the random name is valid.'''
	return name != ''


def checkJoke(joke, idx, name):
	'''Check each joke is displayed as expected.'''
	
	# Not in use:
	# Pattern re1 doesn't work for all jokes 
	# since some jokes don't have a name in them
	# re1 = "{idx}.\\s.*{name}.*\\n".format(idx=idx, name=name)
	
	re2 = "{idx}.\\s.+\\n".format(idx=idx)
	pattern = compile(re2)

	if pattern.match(joke) == None:
		testLogger.debug(
			"Joke {idx} is not displayed as expected.\n\
			Expected a joke with index {idx} for name {name}.\n\
			Actual output: {joke}".format(
				idx=idx,
				name=name,
				joke=joke))
		return False
	else:
		return True


def checkJokes(p, num, name=""):
	''' Check expected number of jokes are displayed in correct format.'''

	if name == "":
		name = "Chuck Norris"

	if not checkConsoleOutput(p, ['\n']):
		return False

	title = p.stdout.readline()

	allJokesRetrived = True
	if title == "Jokes:\n":
		testLogger.info("{} jokes are retrived.".format(num))
	elif title == "Could get some of the jokes requested:\n":
		# When no enough jokes retrieved
		allJokesRetrived = False
		testLogger.info("Less than {} jokes are retrived.".format(num))
	else:
		testLogger.debug('Unexpected title of jokes: {}\n'.format(title))
		return False

	count = 0
	while True:
		out = p.stdout.readline()
		if out == '\n':
			break
		if not checkJoke(out, count+1, name):
			return False
		count += 1

	if allJokesRetrived and count != num:
		testLogger.debug(
			'Not enough jokes are displayed.\n\
			\tExpected {expected} jokes\n\
			\tActually displayed {acutal} jokes'.format(
				expected=num,
				actual=count))

		return False

	if not checkConsoleOutput(
		p, d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT[1:]):
		return False

	return True
