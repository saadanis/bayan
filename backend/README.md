# Installation/Deployment Guide

## Installation and Deployment

The installion and deployment simply requires running the `./startup.sh` script file (or `./startup.ps1` on Windows).

***NOTE: Make sure that python and pip are installed before running the script.***

The script will install `virtualenv` and create an environment in the `backend` directory. The environment will then be activated and all requirements will be installed. Once that is complete, the Flask server will run on `http://127.0.0.1:8000`.

## Usage

To test the server, simply navigate to `http://127.0.0.1:8000`. The website should be loaded.