#!/bin/bash
pip install -r requirements.txt
#flask --app app.app init-db
flask --app app.app run -h 0.0.0.0
