# DS Minesweeper

---

### Distributed Systems Spring 2022 Project

#### Game

Found under [game](./game).

This contains the game logic for Minesweeper.

#### Game Server

Found under [game-server](./game-server).

Uses the following environment variables for setup:

```
DS_MAX_WIDTH
    Maximum width for the field, default: 256
    
DS_MAX_WIDTH
    Maximum width for the field, default: 256
    
DS_BROKER_TOKEN
    Auth token to match for requests, default: Throw
    
DS_TESTING
    This is used to enable docs, default: False
    Matches for case insensitive True.
```

Following convenience scripts are available:

```
run_server.sh
    This will run the Minesweeper game server locally.
    
    Environment:
    - DS_BROKER_TOKEN=test
    - DS_TESTING=True
   
run_pytest.sh
    Runs all the pytest tests found in the repo.
    The environment is used in one test that depends 
    on generation speed. Change these if needed.
    
    Environment:
    - DS_TESTING=True
    - DS_MAX_WIDTH=400
    - DS_MAX_HEIGHT=400
```