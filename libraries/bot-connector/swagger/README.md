# BotFramework Connector

> see https://aka.ms/autorest

Configuration for generating BotFramework Connector SDK.

``` yaml
add-credentials: true
openapi-type: data-plane
```
The current release for the BotFramework Connector is v3.0.

# Releases

## Connector API 3.0

``` yaml
input-file: ConnectorAPI.json
```

### Connector API 3.0 - Python Settings

These settings apply only when `--python` is specified on the command line. Use `--python-mode=update` if you already have a setup.py and just want to update the code itself.

``` yaml $(python)
python-mode: create
python:
  license-header: MICROSOFT_MIT_NO_VERSION
  add-credentials: true
  payload-flattening-threshold: 2
  namespace: bot.connector
  package-name: bot-connector
  override-client-name: BotConnector
  clear-output-folder: true
```
``` yaml $(python) && $(python-mode) == 'update'
python:
  no-namespace-folders: true
  output-folder: ../microsoft
```
``` yaml $(python) && $(python-mode) == 'create'
python:
  basic-setup-py: true
  output-folder: ../microsoft
```