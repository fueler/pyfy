# pyfy
Python Finance

## Setup
Store `SPREADSHEET_ID` in `.env` file where `SPREADSHEET_ID` is the Google Sheets' document id. Run `poetry run pre-commit install` to install pre-commit's hooks.

## VSCode Setup with Poetry
Use `poetry env info --path` to get the path.
Make it usable, `poetry env info --path | pbcopy`.
Add it to VS Code as your interpreter
