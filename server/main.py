#!/usr/bin/env python3

import dotenv
dotenv.load_dotenv()

from agenda import init_app


app = init_app()

if __name__ == "__main__":
    app.run()
