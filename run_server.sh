export DS_BROKER_TOKEN="test"
export DS_TESTING="True"
uvicorn --reload --reload-dir ./game/src --reload-dir ./game-server/src server.app:app