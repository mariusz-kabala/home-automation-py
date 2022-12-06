#!/bin/sh

cat pyproject.toml | grep -A2 '^\[tool\.poetry\]$'
