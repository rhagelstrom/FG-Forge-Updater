[![Python Check](https://github.com/bmos/fg_forge_updater/actions/workflows/lint-python.yml/badge.svg)](https://github.com/bmos/fg_forge_updater/actions/workflows/lint-python.yml) [![CodeQL](https://github.com/bmos/fg_forge_updater/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/bmos/fg_forge_updater/actions/workflows/github-code-scanning/codeql)

# Forge Updater

Herein lies a Python module that will upload builds to the FantasyGrounds Forge automatically via automation of a Chrome
browser instance.

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

1. Create a `.env` file in the project folder containing the following (but with your information):

> [!NOTE]
> You can add these values directly to your environment variables.

```env
# your FG forum user ID (you can get this from the URL of your profile)
FG_USER_ID=354681
# your FG forum username
FG_USER_NAME=**********
# your FG forum password
FG_USER_PASS=**********
# the item ID of the FG Forge item you want to modify
FG_ITEM_ID=33
# the name of the ext file you want to upload
FG_UL_FILE=FG-PFRPG-Advanced-Effects.ext
```

2. Put an ext file to upload into the project folder.
3. Run the following command from inside the project folder:

```shell
python3 src/app.py
```

## Features

TODO
