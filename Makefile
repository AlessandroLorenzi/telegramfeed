test:
	poetry run pytest --asyncio-mode=strict -v --cov=. --cov-report html

browse-htmlcov:
	firefox htmlcov/index.html
