[![Python Check](https://github.com/bmos/fg_forge_updater/actions/workflows/lint-python.yml/badge.svg)](https://github.com/bmos/fg_forge_updater/actions/workflows/lint-python.yml) [![CodeQL](https://github.com/bmos/fg_forge_updater/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/bmos/fg_forge_updater/actions/workflows/github-code-scanning/codeql)

# Forge Updater

Herein lies a Python module that will (someday) upload builds to the FantasyGrounds Forge automatically.

## Getting Started

To run this code, you'll need to have Python 3.9, 3.10, 3.11, or 3.12 installed on your machine. You'll also need to
install the required packages by running the following commands from inside the project folder:

```shell
python3 -m venv venv
```
```shell
source venv/bin/activate
```
```shell
python3 -m pip install .
```

## Usage

You will need to create a `.env` file in the project folder containing the following (but with your information):
```env
bb_userid=354681 # your user ID on the SmiteWorks forum
bb_password=0800fc577294c34e0b28ad2839435945 # md5 hash of your SmiteWorks account password
forge_item=33 # the item ID of the FantasyGrounds item you want to modify
php_session_id=mk7294c34e0b28ad2839435945 # the value of the PHPSESSID cookie (get this by monitoring the network tab of the web inspector for a POST request while setting an item to LIVE)
csrf_token=327t287tg237cn7aks87xg827282374618273462873x3nf823bf871287f1xm186f18 # the value of the X-CSRF-Token (get this from the "csrf-token" meta tag you can see here: view-source:https://forge.fantasygrounds.com/crafter/manage-craft).
upload_file=FG-PFRPG-Advanced-Effects.ext # the name of the ext file you want to upload
```


```shell
python3 src/app/py
```

## Features

TODO
