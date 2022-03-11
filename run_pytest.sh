cd "$(dirname "$0")"
export DS_TESTING="True"
export DS_MAX_WIDTH=400
export DS_MAX_HEIGHT=400
pytest --cov=minesweeper --cov=server --cov-report=term --cov-report=html --ignore=broker