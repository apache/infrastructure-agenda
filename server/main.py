#!/usr/bin/env python3

import os

import dotenv
dotenv.load_dotenv()

from agenda import init_app
import config

if os.getenv('FLASK_ENV') == 'production':
    app = init_app(config.ProductionConfig)
else:
    app = init_app()

if __name__ == "__main__":
    app.run()
