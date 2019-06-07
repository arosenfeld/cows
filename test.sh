#!/bin/bash

pytest --cov=cows --cov-branch -s -v tests/ --tb=native
