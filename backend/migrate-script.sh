#!/usr/bin/bash
flask db init
flask db migrate -m "initialize migration"
flask db upgrade
