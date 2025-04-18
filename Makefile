HOST = 127.0.0.1
PORT = 8000

run:
	uvicorn main:app --host $(HOST) --port $(PORT) --reload --env-file $(ENV_FILE)

