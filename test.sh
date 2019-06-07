#!/bin/bash

pytest --cov=cows -s -v tests/ --tb=native

pycodestyle cows tests
pylint cows
