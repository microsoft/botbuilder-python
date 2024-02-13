# BotFramework Token

> see https://aka.ms/autorest

Configuration for generating BotFramework Token SDK.

``` yaml
add-credentials: true
openapi-type: data-plane
```
The current release for the BotFramework Token is v3.0.

# Releases

## Token API 3.0

``` yaml
input-file: TokenAPI.json
```

### Token API 3.0 - Python Settings

These settings apply only when `--python` is specified on the command line.
DO NOT use `--basic-setup-py` as this will overwrite the existing setup.py files.
If you upgrade autorest from npm you may need to run `autorest ---reset` before continuing.

``` yaml $(python)
python:
  license-header: MICROSOFT_MIT_NO_VERSION
  add-credentials: true
  payload-flattening-threshold: 2
  namespace: botframework.tokenApi
  package-name: botframework-Token
  override-client-name: TokenApiClient
  clear-output-folder: true
  output-folder: ./tokenApi
```