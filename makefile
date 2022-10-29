default: install

define preconditions
	@python scripts/assert_python.py
    @python scripts/assert_venv.py
endef

install: # install dependencies and setup
	$(call preconditions)
	@python -m pip install --upgrade pip
	@pip install -r requirements.txt

lock: ## install only minial dependencies and freeze
	$(call preconditions)
	@python -m pip install --upgrade pip
	@pip install -r requirements.min.txt
	@pip freeze > requirements.txt

clean: ## clean project from dependencies and configurations
	$(call preconditions)
	@pip uninstall -r requirements.txt -y


start: ## start default entry program
	$(call preconditions)
	@python -m src


lint: ## check for linting issues in the codebase
	$(call preconditions)
	@python -m pycodestyle --exclude='.venv,.git,.env'  --ignore=E501,E741,W504,W503,E731,E704 .
	@python -m isort --ca --line-length=140 --check-only .


format: ## auto fix most linting issues in the codebase
	$(call preconditions)
	@python -m autopep8 --in-place --recursive -a -a --exclude=.env --ignore=E501,E741,W504,W503,E731,E704 --max-line-length=140 --experimental . 
	@python -m isort --ca --line-length=140 .


test: ## run unit tests
	$(call preconditions)
	@python -m pytest src


typecheck: ## runs static type checker analysis
	$(call preconditions)
	@python -m pyright src
