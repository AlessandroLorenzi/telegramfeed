qa: black isort safety mypy test browse-htmlcov

black:
	poetry run black .

isort: 
	poetry run isort .

safety:
	poetry run safety check

mypy:
	poetry run mypy .

test:
	poetry run pytest --asyncio-mode=strict -v --cov=. --cov-report html

browse-htmlcov:
	firefox htmlcov/index.html
