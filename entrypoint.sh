#!/bin/bash
flask --app app.app init-db
flask --app app.app run -h 0.0.0.0
