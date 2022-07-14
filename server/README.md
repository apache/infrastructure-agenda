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
Copy `agenda.yaml.example` to `agenda.yaml` and edit to your needs. The contents of said file are show below for reference:
```yaml
SERVER_PORT: 5000

AGENDA_REPO: /path/to/repo/containing/agendas
COMMITTERS_REPO: /path/to/repo/containing/committer/info
MINUTES_REPO: /path/to/repo/containing/minutes
```

### Run the app
First, ensure you are in the `server/` directory and you have activated the virtual environment:

`$ infrastructure-agenda/server`

`$ source venv/bin/activate`

Run the application:

`$ python main.py`
