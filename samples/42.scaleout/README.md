# Scale Out

Bot Framework v4 bot Scale Out sample

This bot has been created using [Bot Framework](https://dev.botframework.com), is shows how to use a custom storage solution that supports a deployment scaled out across multiple machines.

The custom storage solution is implemented against memory for testing purposes and against Azure Blob Storage.  The sample shows how storage solutions with different policies can be implemented and integrated with the framework.  The solution makes use of the standard HTTP ETag/If-Match mechanisms commonly found on cloud storage technologies.

## Running the sample
- Clone the repository
```bash
git clone https://github.com/Microsoft/botbuilder-python.git
```
- Activate your desired virtual environment
- Bring up a terminal, navigate to `botbuilder-python\samples\42.scaleout` folder
- In the terminal, type `pip install -r requirements.txt`
- In the terminal, type `python app.py`

## Testing the bot using Bot Framework Emulator
[Microsoft Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework emulator from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to bot using Bot Framework Emulator
- Launch Bot Framework Emulator
- File -> Open Bot
- Paste this URL in the emulator window - http://localhost:3978/api/messages

## Further reading

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Implementing custom storage for you bot](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-custom-storage?view=azure-bot-service-4.0)
- [Bot Storage](https://docs.microsoft.com/en-us/azure/bot-service/dotnet/bot-builder-dotnet-state?view=azure-bot-service-3.0&viewFallbackFrom=azure-bot-service-4.0)
- [HTTP ETag](https://en.wikipedia.org/wiki/HTTP_ETag)
- [Activity processing](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-activity-processing?view=azure-bot-service-4.0)
