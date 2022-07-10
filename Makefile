test:
	poetry run pytest --asyncio-mode=strict -v --cov=. --cov-report html

htmlcov:
	firefox htmlcov/index.html
