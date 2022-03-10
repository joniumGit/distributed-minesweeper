def s(o, **kwargs):
    return {'value': o, **kwargs}


def samples(o):
    return {
        'application/json': {
            'examples': o
        }
    }


def sample(o):
    return {
        'application/json': {
            'example': o
        }
    }


def location(o):
    from headers import LOCATION
    return {
        LOCATION: {
            'type': 'string',
            'description': o
        }
    }


FLOOD = {
    'items': [
        {
            'x': 0,
            'y': 0,
            'open': True,
            'value': 0
        },
        {
            'x': 1,
            'y': 2,
            'open': True,
            'value': 1
        },
        {
            'x': 0,
            'y': 2,
            'open': True,
            'value': 1
        },
    ]
}
NUMBER = {
    'items': [
        {
            'x': 2,
            'y': 2,
            'open': True,
            'value': 1
        }
    ]
}
MINE = {
    'status': 'lose',
    'items': [
        {
            'x': 3,
            'y': 2,
            'open': True,
            'mine': True
        },
        {
            'x': 0,
            'y': 2,
            'mine': True
        },
        {
            'x': 2,
            'y': 0,
            'mine': True
        }
    ]
}
WIN = {
    'status': 'win',
    'items': [
        {
            'x': 0,
            'y': 0,
            'open': True,
            'value': 0
        },
        {
            'x': 0,
            'y': 1,
            'open': True,
            'value': 0
        },
        {
            'x': 0,
            'y': 2,
            'open': True,
            'value': 0
        },
        {
            'x': 0,
            'y': 3,
            'open': True,
            'value': 0
        },
        {
            'x': 1,
            'y': 3,
            'open': True,
            'value': 0
        },
        {
            'x': 2,
            'y': 1,
            'open': True,
            'value': 1
        },
        {
            'x': 1,
            'y': 2,
            'open': True,
            'value': 0
        },
        {
            'x': 2,
            'y': 0,
            'open': True,
            'value': 1
        },
        {
            'x': 1,
            'y': 1,
            'open': True,
            'value': 0
        },
        {
            'x': 1,
            'y': 0,
            'open': True,
            'value': 0
        },
        {
            'x': 3,
            'y': 1,
            'open': True,
            'value': 1
        },
        {
            'x': 2,
            'y': 2,
            'open': True,
            'value': 0
        },
        {
            'x': 2,
            'y': 3,
            'open': True,
            'value': 0
        },
        {
            'x': 3,
            'y': 3,
            'open': True,
            'value': 0
        },
        {
            'x': 3,
            'y': 2,
            'open': True,
            'value': 0
        },
        {
            'x': 3,
            'y': 0,
            'mine': True
        }
    ]
}
RELOAD_ONGOING = {
    'items': [
        {
            'x': 0,
            'y': 0,
            'open': True,
            'value': 1
        },
        {
            'x': 0,
            'y': 2,
            'flag': True
        },
    ],
    'status': 'ongoing'
}
RELOAD_WIN = {
    'items': [
        {
            'x': 0,
            'y': 0,
            'open': True,
            'value': 1
        },
        {
            'x': 0,
            'y': 1,
            'open': True,
            'value': 1
        },
        {
            'x': 0,
            'y': 2,
            'open': True,
            'value': 0
        },
        {
            'x': 0,
            'y': 3,
            'open': True,
            'value': 0
        },
        {
            'x': 0,
            'y': 4,
            'open': True,
            'value': 0
        },
        {
            'x': 1,
            'y': 1,
            'open': True,
            'value': 1
        },
        {
            'x': 1,
            'y': 2,
            'open': True,
            'value': 0
        },
        {
            'x': 1,
            'y': 3,
            'open': True,
            'value': 0
        },
        {
            'x': 1,
            'y': 4,
            'open': True,
            'value': 0
        },
        {
            'x': 2,
            'y': 0,
            'open': True,
            'value': 1
        },
        {
            'x': 2,
            'y': 1,
            'open': True,
            'value': 1
        },
        {
            'x': 2,
            'y': 2,
            'open': True,
            'value': 0
        },
        {
            'x': 2,
            'y': 3,
            'open': True,
            'value': 0
        },
        {
            'x': 2,
            'y': 4,
            'open': True,
            'value': 0
        },
        {
            'x': 3,
            'y': 0,
            'open': True,
            'value': 0
        },
        {
            'x': 3,
            'y': 1,
            'open': True,
            'value': 0
        },
        {
            'x': 3,
            'y': 2,
            'open': True,
            'value': 0
        },
        {
            'x': 3,
            'y': 3,
            'open': True,
            'value': 0
        },
        {
            'x': 3,
            'y': 4,
            'open': True,
            'value': 0
        },
        {
            'x': 4,
            'y': 0,
            'open': True,
            'value': 0
        },
        {
            'x': 4,
            'y': 1,
            'open': True,
            'value': 0
        },
        {
            'x': 4,
            'y': 2,
            'open': True,
            'value': 0
        },
        {
            'x': 4,
            'y': 3,
            'open': True,
            'value': 0
        },
        {
            'x': 4,
            'y': 4,
            'open': True,
            'value': 0
        },
        {
            'x': 1,
            'y': 0,
            'mine': True
        }
    ],
    'status': 'win'
}
RELOAD_LOSE = {
    'items': [
        {
            'x': 0,
            'y': 0,
            'open': True,
            'mine': True
        },
        {
            'x': 2,
            'y': 2,
            'mine': True
        }
    ],
    'status': 'lose'
}

START_SAMPLES = {
    'easy': s({
        'width': 8,
        'height': 8,
        'mines': 10,
    }),
    'medium': s({
        'width': 16,
        'height': 16,
        'mines': 40,
    }),
    'hard': s({
        'width': 24,
        'height': 24,
        'mines': 90,
    })
}

GENERIC_UNPROCESSABLE = sample({
    'detail': [
        {
            'loc': [
                'x'
            ],
            'msg': 'ensure this value is less than 100',
            'type': 'value_error.number.not_lt',
            'ctx': {
                'limit_value': 100
            }
        },
        {
            'loc': [
                'y'
            ],
            'msg': 'ensure this value is less than 100',
            'type': 'value_error.number.not_lt',
            'ctx': {
                'limit_value': 100
            }
        }
    ]
})

TOO_BIG_FIELD = {
    'detail': [
        {
            'loc': [
                'query',
                'width'
            ],
            'msg': 'ensure this value is less than 256',
            'type': 'value_error.number.not_lt',
            'ctx': {
                'limit_value': 256
            }
        },
        {
            'loc': [
                'query',
                'height'
            ],
            'msg': 'ensure this value is less than 256',
            'type': 'value_error.number.not_lt',
            'ctx': {
                'limit_value': 256
            }
        }
    ]
}

TOO_MANY_MINES = {
    'detail': [
        {
            'loc': [
                '__root__'
            ],
            'msg': 'Too many mines, max: 81 got: 100',
            'type': 'value_error'
        }
    ]
}

SIMPLE_DETAIL = sample({
    'detail': 'Error Message'
})

S403 = {
    'description': 'The request is missing an auth token or the token is invalid',
    'content': SIMPLE_DETAIL
}
S410 = {
    'description': 'The game has ended and this resource is no longer available',
    'content': SIMPLE_DETAIL
}
S404 = {
    'description': 'The game has not yet started.',
    'content': SIMPLE_DETAIL
}

S422 = {
    'description': 'Invalid model',
    'content': GENERIC_UNPROCESSABLE
}

S202 = {
    'description': 'Game server is performing initial setup and is ready later',
    'content': SIMPLE_DETAIL
}

ENTRY = {
    200: {
        'description': 'Game has successfully been initialized'
    },
    202: S202,
    403: S403,
    404: S404,
    410: S410,
}

START = {
    201: {
        'description': 'The request was processed successfully and game creation queued',
        'headers': location('An url for querying game initialization status e.g. `https://example.com/`')
    },
    403: S403,
    410: {
        'description': 'The game has already been started and this endpoint is gone',
        'content': SIMPLE_DETAIL
    },
    422: {
        'description': 'Some of the field parameters were invalid',
        'content': samples({
            'Too Many Mines': s(TOO_MANY_MINES, description='Dynamic calculation `(width - 1)(height - 1)`'),
            'Too Huge Field': s(TOO_BIG_FIELD, description='The maximum dimensions can change from game to game'),
        })
    },
}

RELOAD = {
    200: {
        'description': 'Fetches the whole set of open squares on the field plus flags',
        'content': samples({
            'lose': s(RELOAD_LOSE, description='This will contain hidden mines for display'),
            'win': s(RELOAD_WIN, description='This will contain hidden mines for display'),
            'ongoing': s(RELOAD_ONGOING, description='This will only contain opened squares')
        })
    },
    202: S202,
    403: S403,
    404: S404,
}

CHECK = {
    200: {
        'description': 'Successfully checked square. This will never return unopened squares.',
        'content': samples({
            'none': s({
                'x': 0,
                'y': 0
            }),
            'number': s({
                'x': 0,
                'y': 0,
                'value': 8,
                'open': True
            }),
            'flag': s({
                'x': 1,
                'y': 1,
                'flag': True
            }),
            'mine': s({
                'x': 0,
                'y': 0,
                'mine': True,
                'open': True
            }),
        })
    },
    202: S202,
    403: S403,
    404: S404,
    422: S422,
}

FLAG_ADD = {
    201: {
        'description': 'Flag was created',
        'headers': location('Check url for the newly created flag `https://example.com/check?x=0&y=0`')
    },
    202: S202,
    304: {
        'description': 'No change',
        'headers': location('Check url for the square `https://example.com/check?x=0&y=0`')
    },
    403: S403,
    404: S404,
    410: S410,
    422: S422,
}

FLAG_DELETE = {
    204: {
        'description': 'Flag was deleted',
        'headers': location('Check url for the affected square `https://example.com/check?x=0&y=0`')
    },
    202: S202,
    304: {
        'description': 'No change',
        'headers': location('Check url for the square `https://example.com/check?x=0&y=0`')
    },
    403: S403,
    404: S404,
    410: S410,
    422: S422,
}

OPEN = {
    200: {
        'description': 'The square was successfully opened',
        'content': samples({
            'flood': s(FLOOD),
            'number': s(NUMBER),
            'win': s(WIN, description='Status marking game ended in a win. Also contains all mines.'),
            'mine': s(MINE, description='Status marking game ending in a lose. Also contains all other mines.')
        })
    },
    304: {
        'description': 'The square was already open',
        'headers': location('Check url for the square `https://example.com/check?x=0&y=0`')
    },
    403: S403,
    404: S404,
    410: S410,
    422: S422,
}
