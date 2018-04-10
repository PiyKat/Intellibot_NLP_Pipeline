# Intellibot 1.0 

The project has been created with an intention of creating a service bot that accepts user input, prases it using traditional NLP techniques in order to classify the serviuce request into services and extract relevant entities, and then call the relevant service request.


# Prerequisites

The project only works on <b>Python2.7</b> as of now due to dependencies, but you can expect it to work with Python 3+ as the integration with official python packages provided by Google is under development. Kindly refer to the requirements.txt file for checking the rest of the dependencies.


# Installing

1. Clone the repository
	```
	git clone https://github.com/PiyKat/Intellibot_NLP_Pipeline
	```

2. Install the requirements via requirements.txt
	```
	pip install requirements.txt
	```
3. Run alpha_intellibot.py script
	```
	python2.7 alpha_intellibot.py
	```

### Project Description

1. The program expects input from the user via speech with the intention of calling a particular service. Currently the 	  program handles flight, meeting, definition, stock price and nutrition services.

2. The user request sentence is tokenized and lemmatized to clarify the intent of what the user is asking. We do a greedy search of the list of lemmatized words to determine the user service we need to call.

3. For the purpose of extracting relevant entities from the user sentence, we use <b>chunking grammar</b> provided by the NLTK module. Using the chunking process, we first create a parse tree via grammar rules prewritten for each service, and then we traverse this tree to extract relevent entities. 
