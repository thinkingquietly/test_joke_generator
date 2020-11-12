import pdb
import logging
import pytest
import subprocess
from random import randint
import TestApi
import TestData as d


testLogger = logging.getLogger(__name__)


@pytest.fixture(scope='function')
def joke_generator(request):
	
	testLogger.info("Running test {}".format(request.node.name))

	# Start the process and return the popen object
	p = subprocess.Popen(['dotnet run --project ../'],
		shell=True, 
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE,
		stderr=subprocess.PIPE,
		bufsize=1,
		universal_newlines=True)

	if p.poll() == None:
		testLogger.info("Succesfully started the JokeGenerator program!")
		yield p
	else:
		testLogger.error(
			"Program failed to start. Popen object returncode {}"\
			.format(p.poll()))
		raise Exception("Program failed to start")
	
	# Close the process if not already exited/terminated
	if p.poll() == None:
		testLogger.info('Closing the JokeGenerator program...')

		p.stdin.close()
		p.stdout.close()
		p.terminate()

		testLogger.debug('Object popen returncode is {}'.format(p.wait(3)))


@pytest.mark.positive
def test_GreetUser(joke_generator):
	'''Test the user greeting text and the main menu display.'''
	p = joke_generator

	assert TestApi.checkConsoleOutput(p, 
		d.GREET_USER_EXPECTED_OUTPUT)


@pytest.mark.positive
def test_SeeInstructions(joke_generator):
	'''Test the get instruction option.'''
	p = joke_generator

	assert TestApi.checkConsoleOutput(p, 
		d.GREET_USER_EXPECTED_OUTPUT)

	TestApi.input(p, d.SEE_INSTRUCTIONS)

	assert TestApi.checkConsoleOutput(p,
		d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT)


@pytest.mark.positive
def test_ExitFromMainMenu(joke_generator):
	'''Test exiting from the main menu.'''
	p = joke_generator

	assert TestApi.checkConsoleOutput(p, 
		d.GREET_USER_EXPECTED_OUTPUT)

	assert TestApi.checkExit(p)


@pytest.mark.positive
def test_SeeCategories(joke_generator):
	'''Test the see available joke categories option.'''
	p = joke_generator	

	assert TestApi.checkConsoleOutput(p, d.GREET_USER_EXPECTED_OUTPUT)
	
	TestApi.input(p, d.SEE_INSTRUCTIONS)

	assert TestApi.checkConsoleOutput(p, d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT)

	TestApi.input(p, d.VIEW_CATEGORIES)

	categories = TestApi.getCategories()
	testLogger.info(
		"Retrieve categories from external URL\n:{}\n".format(categories))

	assert TestApi.checkCategories(p, categories)

	# Check the menu is printed out after the categories
	assert TestApi.checkConsoleOutput(p, d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT)	


@pytest.mark.positive
def test_ViewJokesWithDefaultName(joke_generator):
	'''
	Test the view random jokes option when the default name is used.
	
	Check the following operation:
	Get Instruction -> View Jokes -> 
	Use Default Name -> Use Default Category Generation 
	-> Choose Number of Jokes -> Jokes Display 
	'''
	p = joke_generator

	# Check Greeting menu
	assert TestApi.checkConsoleOutput(p, d.GREET_USER_EXPECTED_OUTPUT)

	# Check Instruction menu
	TestApi.input(p, d.SEE_INSTRUCTIONS)

	assert TestApi.checkConsoleOutput(p, d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT)

	# Check Random Joke menu
	TestApi.input(p, d.GET_RANDOM_JOKES)

	# Check Random Name option
	assert TestApi.checkConsoleOutput(p, d.CHOOSE_RANDOM_NAME_EXPECTED_OUTPUT)

	TestApi.input(p, d.NO)
	
	# Check Choose Joke Category option
	assert TestApi.checkConsoleOutput(p, d.CHOOSE_JOKE_CATEGORY_EXPECTED_OUTPUT)

	TestApi.input(p, d.NO)

	# Check Choose Number of Joke option
	assert TestApi.checkConsoleOutput(p, d.CHOOSE_NUMBER_JOKES_EXPECTED_OUTPUT)

	numJokes = randint(1,9)
	TestApi.input(p, str(numJokes))

	# Check jokes
	assert TestApi.checkJokes(p, numJokes)


@pytest.mark.positive
def test_ViewJokesWithRandomName(joke_generator):
	'''
	Test the view random jokes option when a random name is used.

	Check the following operation:
	Get Instruction -> View Jokes -> Use Random Name ->
	Choose Category -> Choose Number of Jokes -> Joke Display
	'''
	p = joke_generator

	# Check Greeting menu
	assert TestApi.checkConsoleOutput(p, d.GREET_USER_EXPECTED_OUTPUT)

	# Check Instruction menu
	TestApi.input(p, d.SEE_INSTRUCTIONS)

	assert TestApi.checkConsoleOutput(p, d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT)

	# Check Random Joke menu
	TestApi.input(p, d.GET_RANDOM_JOKES)

	# Check Random Name option
	assert TestApi.checkConsoleOutput(p, d.CHOOSE_RANDOM_NAME_EXPECTED_OUTPUT)

	TestApi.input(p, d.YES)

	name = TestApi.getRandomName(p)
	testLogger.info("Using random name:{}\n".format(name))

	assert TestApi.checkRandomName(name)
	
	# Check Choose Joke Category option
	assert TestApi.checkConsoleOutput(p, d.CHOOSE_JOKE_CATEGORY_EXPECTED_OUTPUT)

	TestApi.input(p, d.YES)

	categories = TestApi.getCategories()
	testLogger.info(
		"Retrieve categories from external URL\n:{}\n".format(categories))

	assert TestApi.checkCategories(p, categories)
	assert TestApi.checkConsoleOutput(p, d.ENTER_CATEGORY_NUNBER_EXPECTED_OUTPUT)

	categoryNum = randint(1,len(categories))
	testLogger.info(
		"Using category: {num}.{category}\n".format(
			num=categoryNum,
			category=categories[categoryNum-1]))

	TestApi.input(p, categoryNum)
	assert TestApi.checkChosenCategory(p, categories[categoryNum-1])

	# Check Choose Number of Joke option
	assert TestApi.checkConsoleOutput(p, d.CHOOSE_NUMBER_JOKES_EXPECTED_OUTPUT)

	numJokes = randint(1,9)
	TestApi.input(p, numJokes)

	testLogger.info(
		"Choosing number of jokes: {num}\n".format(
			num=numJokes))

	# Check jokes
	assert TestApi.checkJokes(p, numJokes, name=name)


@pytest.mark.positive
def test_ExitFromInstructionMenu(joke_generator):
	'''Test exiting from the instruction menu.'''
	p = joke_generator
	
	TestApi.input(p, d.SEE_INSTRUCTIONS)

	assert TestApi.checkConsoleOutput(p, 
		d.GREET_USER_EXPECTED_OUTPUT + \
		d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT)

	assert TestApi.checkExit(p)


# Negative tests
@pytest.mark.negative
def test_CheckInvalidInputGreetingMenu(joke_generator):
	'''Test invalid inputs for the main greeting menu.'''
	p = joke_generator

	assert TestApi.checkConsoleOutput(p, d.GREET_USER_EXPECTED_OUTPUT)

	for x in ['0','h','1','!']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, 
			d.INVALID_VALUE_EXPECTED_OUTPUT + d.START_MENU_EXPECTED_OUTPUT)
	
	for x in ['exit','1000','help']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, 
			d.INVALID_LETTER_EXPECTED_OUTPUT)
	

@pytest.mark.negative
def test_CheckInvalidInputInstructionMenu(joke_generator):
	'''Test invalid inputs for the instruction menu.'''
	p = joke_generator

	TestApi.input(p, d.SEE_INSTRUCTIONS)

	assert TestApi.checkConsoleOutput(p, 
		d.GREET_USER_EXPECTED_OUTPUT + d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT)

	for x in ['0','?','1','.']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, 
			d.INVALID_VALUE_EXPECTED_OUTPUT + d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT)
	
	for x in ['exit','1000','help']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, 
			d.INVALID_LETTER_EXPECTED_OUTPUT)


@pytest.mark.negative
def test_CheckInvalidNumberOfJokes(joke_generator):
	'''Test invalid inputs for entering the number of jokes prompt.'''
	p = joke_generator

	TestApi.input(p, 
		[d.SEE_INSTRUCTIONS, d.GET_RANDOM_JOKES, d.NO, d.NO])

	assert TestApi.checkConsoleOutput(p, 
		d.GREET_USER_EXPECTED_OUTPUT + \
		d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT + \
		d.CHOOSE_RANDOM_NAME_EXPECTED_OUTPUT + \
		d.CHOOSE_JOKE_CATEGORY_EXPECTED_OUTPUT + \
		d.CHOOSE_NUMBER_JOKES_EXPECTED_OUTPUT)

	for x in ['0', '100', '10', '-1']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, 
			d.INVALID_VALUE_EXPECTED_OUTPUT + d.CHOOSE_NUMBER_JOKES_EXPECTED_OUTPUT)
	
	for x in ['none','one','x']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, 
		d.INVALID_NUMBER_EXPECTED_OUTPUT)


@pytest.mark.negative
def test_CheckInvalidCategory(joke_generator):
	'''Test invalid inputs for entering the category of jokes prompt.'''
	p = joke_generator

	TestApi.input(p, 
		[d.SEE_INSTRUCTIONS, d.GET_RANDOM_JOKES, d.NO, d.YES])

	assert TestApi.checkConsoleOutput(p, 
		d.GREET_USER_EXPECTED_OUTPUT + \
		d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT + \
		d.CHOOSE_RANDOM_NAME_EXPECTED_OUTPUT + \
		d.CHOOSE_JOKE_CATEGORY_EXPECTED_OUTPUT)

	categories = TestApi.getCategories()
	assert TestApi.checkCategories(p,categories)

	assert TestApi.checkConsoleOutput(p, 
		d.ENTER_CATEGORY_NUNBER_EXPECTED_OUTPUT)

	for x in ['0',str(len(categories)+1),'-1']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, 
			d.INVALID_VALUE_EXPECTED_OUTPUT + d.ENTER_CATEGORY_NUNBER_EXPECTED_OUTPUT)

	for x in ['none','all','x','?']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, d.INVALID_NUMBER_EXPECTED_OUTPUT)


@pytest.mark.negative
def test_CheckInvalidInputYesNoPrompt(joke_generator):
	'''Test invalid inputs for entering the category of jokes prompt.'''
	p = joke_generator

	TestApi.input(p, 
		[d.SEE_INSTRUCTIONS, d.GET_RANDOM_JOKES])

	assert TestApi.checkConsoleOutput(p, 
		d.GREET_USER_EXPECTED_OUTPUT + \
		d.SEE_INSTRUCTIONS_EXPECTED_OUTPUT + \
		d.CHOOSE_RANDOM_NAME_EXPECTED_OUTPUT)

	for x in ['0','1','x']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, 
			d.INVALID_VALUE_EXPECTED_OUTPUT + d.CHOOSE_RANDOM_NAME_EXPECTED_OUTPUT)

	for x in ['yes','no','exit','help']:
		testLogger.info("Testing with input {}\n".format(x))
		TestApi.input(p, x)
		assert TestApi.checkConsoleOutput(p, d.INVALID_LETTER_EXPECTED_OUTPUT)


if __name__ == "__main__":

	pytest.main()
