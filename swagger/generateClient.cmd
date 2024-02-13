@echo off

rd /s /q generated
echo [91mWARNING:[0m There is manual code for lines 127-130 in attachments_operations_async.py and lines 12-26 in the connector_client.py.
echo [91mCalling this command script has removed those sections of code.[0m

@echo on
call npx autorest README.md --python --use=".\node_modules\@microsoft.azure\autorest.python"
@echo off

pushd generated
call npx replace "query_parameters\['api-version'\][^\n]+\n" "" . --recursive --include="*.py"
popd

rd /s /q ..\botbuilder-schema\botbuilder\schema
rd /s /q ..\botframework-connector\botframework\connector\operations
rd /s /q ..\botframework-connector\botframework\connector\aio
del ..\botframework-connector\botframework\connector\connector_client.py

move generated\botframework\connector\models ..\botbuilder-schema\botbuilder\schema
move generated\botframework\connector\operations ..\botframework-connector\botframework\connector\operations
move generated\botframework\connector\aio ..\botframework-connector\botframework\connector\aio
move generated\botframework\connector\_connector_client.py ..\botframework-connector\botframework\connector\connector_client.py
move generated\botframework\connector\version.py ..\botframework-connector\botframework\connector\version.py
move generated\botframework\connector\_configuration.py ..\botframework-connector\botframework\connector\_configuration.py

@echo on
call npx autorest tokenAPI.md --python --use=".\node_modules\@microsoft.azure\autorest.python"
@echo off

echo [92mMove tokenAPI to botframework-connector[0m
rd /s /q ..\botframework-connector\botframework\connector\token_api
move tokenApi\botframework\tokenApi ..\botframework-connector\botframework\connector\token_api

echo [92mRemoving generated folders ("generated/", "tokenApi/")[0m

rd /s /q tokenApi