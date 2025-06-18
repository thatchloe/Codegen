#!/usr/bin/env bash

# Fail the build if any command fails
set -o errexit

# Upgrade pip and install wheels support
pip install --upgrade pip
pip install wheel setuptools

# Install Python dependencies
pip install -r requirements.txt
