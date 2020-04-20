.PHONY: clean train-nlu train-core cmdline server

TEST_PATH=./

help:
	@echo "    clean"
	@echo "        Remove python artifacts and build artifacts."
	@echo "    train-nlu"
	@echo "        Trains a new nlu model using the projects Rasa NLU config"
	@echo "    train-core"
	@echo "        Trains a new dialogue model using the story training data"
	@echo "    action-server"
	@echo "        Starts the server for custom action."
	@echo "    cmdline"
	@echo "       This will load the assistant in your terminal for you to chat."


clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf docs/_build

train-nlu:
	python -m rasa_nlu.train -c Config/config.yml --data Data/nlu.json -o models --fixed_model_name nlu --project current --verbose

train-core:
	python -m rasa_core.train -d Config/domain.yml -s Data/stories.md -o models/dialogue -c Config/policies.yml

cmdline:
	python -m rasa_core.run -d models/dialogue -u models/current/nlu --endpoints endpoints.yml
	
action-server:
	python -m rasa_core_sdk.endpoint --actions actions
