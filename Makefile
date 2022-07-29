qa: black isort safety mypy test browse-htmlcov

run:
	poetry run python anyfeed.py

black:
	poetry run black .

isort: 
	poetry run isort .

safety:
	poetry run safety check

mypy:
	poetry run mypy --ignore-missing-imports .

test:
	poetry run pytest --asyncio-mode=strict -v --cov=. --cov-report html

browse-htmlcov:
	firefox htmlcov/index.html
