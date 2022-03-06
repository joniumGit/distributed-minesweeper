def s(o):
    return {"value": o}


def samples(o):
    return {
        "application/json": {
            "examples": o
        }
    }


def location(o):
    from headers import LOCATION
    return {
        LOCATION: {
            "type": "string",
            "description": o
        }
    }


FLOOD = {
    "items": [
        {
            "x": 0,
            "y": 0,
            "open": True,
            "value": 0
        },
        {
            "x": 1,
            "y": 2,
            "open": True,
            "value": 1
        },
        {
            "x": 0,
            "y": 2,
            "open": True,
            "value": 1
        },
    ]
}
NUMBER = {
    "items": [
        {
            "x": 2,
            "y": 2,
            "open": True,
            "value": 1
        }
    ]
}
MINE = {
    "status": "lose",
    "items": [
        {
            "x": 5,
            "y": 5,
            "open": True,
            "mine": True
        }
    ]
}
WIN = {
    "status": "win",
    "items": [
        {
            "x": 5,
            "y": 5,
            "open": True
        }
    ]
}
RELOAD_ONGOING = {
    "items": [
        {
            "x": 0,
            "y": 0,
            "open": True,
            "value": 1
        },
        {
            "x": 0,
            "y": 2,
            "flag": True
        },
    ],
    "status": "RELOAD_ONGOING"
}
RELOAD_WIN = {
    "items": [
        {
            "x": 0,
            "y": 0,
            "open": True,
            "value": 1
        },
        {
            "x": 0,
            "y": 1,
            "open": True,
            "value": 1
        },
        {
            "x": 0,
            "y": 2,
            "open": True,
            "value": 0
        },
        {
            "x": 0,
            "y": 3,
            "open": True,
            "value": 0
        },
        {
            "x": 0,
            "y": 4,
            "open": True,
            "value": 0
        },
        {
            "x": 1,
            "y": 1,
            "open": True,
            "value": 1
        },
        {
            "x": 1,
            "y": 2,
            "open": True,
            "value": 0
        },
        {
            "x": 1,
            "y": 3,
            "open": True,
            "value": 0
        },
        {
            "x": 1,
            "y": 4,
            "open": True,
            "value": 0
        },
        {
            "x": 2,
            "y": 0,
            "open": True,
            "value": 1
        },
        {
            "x": 2,
            "y": 1,
            "open": True,
            "value": 1
        },
        {
            "x": 2,
            "y": 2,
            "open": True,
            "value": 0
        },
        {
            "x": 2,
            "y": 3,
            "open": True,
            "value": 0
        },
        {
            "x": 2,
            "y": 4,
            "open": True,
            "value": 0
        },
        {
            "x": 3,
            "y": 0,
            "open": True,
            "value": 0
        },
        {
            "x": 3,
            "y": 1,
            "open": True,
            "value": 0
        },
        {
            "x": 3,
            "y": 2,
            "open": True,
            "value": 0
        },
        {
            "x": 3,
            "y": 3,
            "open": True,
            "value": 0
        },
        {
            "x": 3,
            "y": 4,
            "open": True,
            "value": 0
        },
        {
            "x": 4,
            "y": 0,
            "open": True,
            "value": 0
        },
        {
            "x": 4,
            "y": 1,
            "open": True,
            "value": 0
        },
        {
            "x": 4,
            "y": 2,
            "open": True,
            "value": 0
        },
        {
            "x": 4,
            "y": 3,
            "open": True,
            "value": 0
        },
        {
            "x": 4,
            "y": 4,
            "open": True,
            "value": 0
        },
        {
            "x": 1,
            "y": 0,
            "mine": True
        }
    ],
    "status": "win"
}
RELOAD_LOSE = {
    "items": [
        {
            "x": 0,
            "y": 0,
            "open": True,
            "mine": True
        },
        {
            "x": 2,
            "y": 2,
            "mine": True
        }
    ],
    "status": "lose"
}

FLOOD = s(FLOOD)
NUMBER = s(NUMBER)
MINE = s(MINE)
WIN = s(WIN)
RELOAD_ONGOING = s(RELOAD_ONGOING)
RELOAD_WIN = s(RELOAD_WIN)
RELOAD_LOSE = s(RELOAD_LOSE)

OPEN_SAMPLES = samples({
    "flood": FLOOD,
    "number": NUMBER,
    "win": WIN,
    "mine": MINE
})

RELOAD_SAMPLES = samples({
    "lose": RELOAD_LOSE,
    "win": RELOAD_WIN,
    "ongoing": RELOAD_ONGOING
})

START_SAMPLES = {
    "easy": s({
        "width": 8,
        "height": 8,
        "mines": 10,
    }),
    "medium": s({
        "width": 16,
        "height": 16,
        "mines": 40,
    }),
    "hard": s({
        "width": 24,
        "height": 24,
        "mines": 90,
    })
}

CHECK_SAMPLES = samples({
    "none": s({
        "x": 0,
        "y": 0
    }),
    "number": s({
        "x": 0,
        "y": 0,
        "value": 8,
        "open": True
    }),
    "win": s({
        "x": 1,
        "y": 1,
        "flag": True
    }),
    "mine": s({
        "x": 0,
        "y": 0,
        "mine": True,
        "open": True
    })
})
