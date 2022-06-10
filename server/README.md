# Agenda Tool

## Setup

### Get a copy of the source locally
`$ git clone git@github.com:apache/infrastructure-agenda.git`

### Install needed packages
1. `$ pip3 install virtualenv`
2. `$ cd infrastructure-agenda/server`
3. `$ python3 -m venv venv`
4. `$ source venv/bin/activate`
5. `$ pip install -r requirements.txt`

### Configure local application
Create a .env alongside main.py, which _minimally_ sets `FLASK_ENV` and possibly `DATA_DIR` (by default this uses sanitized test data, if the ENV variable is left unset), see below for example:
```bash
FLASK_ENV=development
DATA_DIR=/path/to/svn/files
```

The `DATA_DIR` path should be setup like the following:
```
data
└── repos
    ├── committers_board
    │   ├── calendar.txt
    │   └── committee-info.txt
    ├── foundation_board
    │   ├── board_agenda_2015_01_21.txt
    │   └── board_agenda_2015_02_18.txt
    └── minutes
        └── board_minutes_2015_01_21.txt
```

Each folder in repos contains a svn repository, and must be named as above.
