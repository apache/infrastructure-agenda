#!/usr/bin/env python3
import sys
import os

import coverage

import helpers


THIS_DIR = os.path.realpath(os.path.dirname(__file__))
PARENT_DIR = os.path.dirname(THIS_DIR)
sys.path.insert(0, PARENT_DIR)


def touch_every_line():
    from agenda import init_app

    app = init_app()
    app.run()


def main():
    helpers.setup_svn_repo()
    cov = coverage.Coverage(data_file=None, branch=True, config_file=False,
                            source_pkgs=['agenda'], messages=True,)

    cov.start()

    try:
        touch_every_line()
    finally:
        cov.stop()
        helpers.teardown_svn_repo()

    cov.report(file=sys.stdout)
    cov.html_report(directory='htmlcov')


if __name__ == '__main__':
    main()