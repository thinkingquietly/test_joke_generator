# Test data for test_JokeGenerator

SEE_INSTRUCTIONS = '?';
VIEW_CATEGORIES = 'c';
GET_RANDOM_JOKES = 'r';
EXIT_PROGRAM = 'x';
YES = 'y';
NO = 'n';


JOKE_BASE_URL = "https://api.chucknorris.io/jokes/"


GREETING_EXPECTED_OUTPUT = [
	'\n',
	'Welcome to the Joke Generator\n'
]


START_MENU_EXPECTED_OUTPUT = [
	'\n',
	'Options:\n',
	'  - Press ? to get instructions\n',
	'  - Press x to exit program\n'
]


GREET_USER_EXPECTED_OUTPUT = GREETING_EXPECTED_OUTPUT + START_MENU_EXPECTED_OUTPUT


SEE_INSTRUCTIONS_EXPECTED_OUTPUT = [
	'\n', 
	'Options:\n', 
	'  - Press r to view some random jokes\n', 
	'  - Press c to see available joke categories\n',
	'  - Press x to exit program\n']


VIEW_CATEGORIES_EXPECTED_OUTPUT = [
	'\n', 
	'Available Categories:\n'
]


EXIT_PROGRAM_EXPECTED_OUTPUT = [
	'\n', 
	'Thank you for using the Joke Generator\n'
]


CHOOSE_RANDOM_NAME_EXPECTED_OUTPUT = [
	"\n",
	"Should a random name be used? (y/n)\n"
]


CHOOSE_JOKE_CATEGORY_EXPECTED_OUTPUT = [
	"\n",
	"Do you want to choose the joke category? (y/n)\n"
]


ENTER_CATEGORY_NUNBER_EXPECTED_OUTPUT = [
	"\n",
	"Enter the number for the category you want to select:\n"
]


CHOOSE_NUMBER_JOKES_EXPECTED_OUTPUT = [
	"\n",
	"How many jokes do you want? (1-9)\n"
]


INVALID_VALUE_EXPECTED_OUTPUT = [
	"\n",
	"Oops, that is not a valid value\n",
	"Please try again\n"
]


INVALID_NUMBER_EXPECTED_OUTPUT = [
	'\n',
	"Oops, looks like you didn't enter a valid number.\n",
	"Please enter a valid number.\n"
]


INVALID_LETTER_EXPECTED_OUTPUT = [
	"Oops, looks like you didn't enter a letter.\n",
	"Please enter a valid letter.\n"
]
