# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/rhagelstrom/FG-Forge-Updater/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                     |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| src/\_\_init\_\_.py      |        0 |        0 |        0 |        0 |    100% |           |
| src/build\_processing.py |       41 |        0 |       10 |        0 |    100% |           |
| src/dropzone.py          |       56 |        4 |        2 |        1 |     91% |41, 43, 51->exit, 55, 67 |
| src/forge\_api.py        |      148 |       70 |        6 |        0 |     52% |107-108, 114-120, 124-131, 135-140, 144-155, 159-168, 172-182, 186-189, 193-196, 200-214, 218-222 |
| src/main.py              |       43 |       13 |       10 |        1 |     62% | 48-60, 64 |
| src/users\_graph.py      |       27 |       15 |        0 |        0 |     44% |     19-40 |
|                **TOTAL** |  **315** |  **102** |   **28** |    **2** | **67%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/rhagelstrom/FG-Forge-Updater/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/rhagelstrom/FG-Forge-Updater/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/rhagelstrom/FG-Forge-Updater/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/rhagelstrom/FG-Forge-Updater/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Frhagelstrom%2FFG-Forge-Updater%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/rhagelstrom/FG-Forge-Updater/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.