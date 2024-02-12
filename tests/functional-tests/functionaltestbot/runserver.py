# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""
To run the Flask bot app, in a py virtual environment,
```bash
pip install -r requirements.txt
python runserver.py
```
"""

from flask_bot_app import APP


if __name__ == "__main__":
    APP.run(host="0.0.0.0")
