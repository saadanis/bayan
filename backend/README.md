# Installation/Deployment Guide

## Installation and Deployment

1. Navigate to the `hadith` directory and extract `data.rar`.
2. Make sure that `python` and `pip` are installed.
3. Run the `./startup.sh` script file (or `./startup.ps1` on Windows) from the current directory (`backend`).

The script will install `virtualenv` and create an environment in the `backend` directory. The environment will then be activated and all requirements will be installed. Once that is complete, the Flask server will run on `http://127.0.0.1:8000`.

## Usage

To test the server, simply navigate to `http://127.0.0.1:8000`. The website should be loaded.