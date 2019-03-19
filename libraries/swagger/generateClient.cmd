@echo off

rd /s /q generated
echo [91mWARNING:[0m There is manual code for lines 127-130 in attachments_operations_async.py and lines 12-26 in the connector_client.py.
echo [91mCalling this command script has removed those sections of code.[0m

@echo on
call npx autorest README.md --python --use=".\node_modules\@microsoft.azure\autorest.python"


pushd generated
call npx replace "FROM_PROPERTY" "FROM" . --recursive --include="*.py"
call npx replace "from_property" "from" . --recursive --include="*.py"
popd
@echo off

rd /s /q ..\botbuilder-schema\botbuilder\schema
rd /s /q ..\botframework-connector\botframework\connector\operations
del ..\botframework-connector\botframework\connector\connector_client.py

move generated\botframework\connector\models ..\botbuilder-schema\botbuilder\schema
move generated\botframework\connector\operations ..\botframework-connector\botframework\connector\operations
move generated\botframework\connector\connector_client.py ..\botframework-connector\botframework\connector\connector_client.py

@echo on
call npx autorest tokenAPI.md --python --use=".\node_modules\@microsoft.azure\autorest.python"
@echo off

echo [92mMove tokenAPI to botframework-connector[0m
rd /s /q ..\botframework-connector\botframework\connector\token_api
move tokenApi\botframework\tokenApi ..\botframework-connector\botframework\connector\token_api

echo [92mRemoving generated folders ("generated/", "tokenApi/")[0m
rd /s /q generated
rd /s /q tokenApi