#!/usr/bin/env python3

import os

import dotenv
dotenv.load_dotenv()

from agenda import init_app

APP_DIR = os.path.abspath(os.path.dirname(__file__))

app = init_app(APP_DIR)

if __name__ == "__main__":
    # TODO: create list of all template files to feed below
    app.run(port=app.config['SERVER_PORT'], extra_files=['./agenda/templates/agenda.html.ezt',])
