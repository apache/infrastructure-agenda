#!/usr/bin/env python3

import sys
import argparse

import dotenv
dotenv.load_dotenv()

from agenda import init_app
import config

argv = sys.argv[1:]
parser = argparse.ArgumentParser(description='ASF Agenda Tool launcher')
parser.add_argument('--production', action='store_true',
                    help='Run as the "production" server.')
args = parser.parse_args(argv)

if not args.production:
    app = init_app()
else:
    app = init_app(config.ProductionConfig)

if __name__ == "__main__":
    app.run()
