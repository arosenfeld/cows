#!/bin/bash

pytest --cov=basco -s -v tests/ --tb=native

pycodestyle basco tests
pylint basco
