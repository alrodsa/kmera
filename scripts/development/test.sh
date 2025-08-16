#!/bin/bash

export ENV=test

python3 -m pytest --cov=src tests/ -W ignore::DeprecationWarning --cov-report term-missing
