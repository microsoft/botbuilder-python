# multi-turn prompt

Bot Framework v4 welcome users bot sample

This bot has been created using [Bot Framework](https://dev.botframework.com), it shows how to use the prompts classes included in `botbuilder-dialogs`.  This bot will ask for the user's name and age, then store the responses. It demonstrates a multi-turn dialog flow using a text prompt, a number prompt, and state accessors to store and retrieve values.

## Running the sample
- Clone the repository
```bash
git clone https://github.com/Microsoft/botbuilder-python.git
```
- Run `pip install -r requirements.txt` to install all dependencies
- Run `python app.py`
- Alternatively to the last command, you can set the file in an environment variable with `set FLASK_APP=app.py` in windows (`export FLASK_APP=app.py` in mac/linux) and then run `flask run --host=127.0.0.1 --port=3978`


### Visual studio code
- Activate your desired virtual environment
- Open `botbuilder-python\samples\45.state-management` folder
- Bring up a terminal, navigate to `botbuilder-python\samples\05.multi-turn-prompt` folder
- In the terminal, type `pip install -r requirements.txt`
- In the terminal, type `python app.py`

## Testing the bot using Bot Framework Emulator
[Microsoft Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework emulator from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to bot using Bot Framework Emulator
- Launch Bot Framework Emulator
- Paste this URL in the emulator window - http://localhost:3978/api/messages


## Prompts

A conversation between a bot and a user often involves asking (prompting) the user for information, parsing the user's response,
and then acting on that information. This sample demonstrates how to prompt users for information using the different prompt types
included in the [botbuilder-dialogs](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-dialog?view=azure-bot-service-4.0) library
and supported by the SDK.

The `botbuilder-dialogs` library includes a variety of pre-built prompt classes, including text, number, and datetime types. This
sample demonstrates using a text prompt to collect the user's name, then using a number prompt to collect an age.

# Further reading

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Dialogs](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-dialog?view=azure-bot-service-4.0)
- [Gathering Input Using Prompts](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-prompts?view=azure-bot-service-4.0&tabs=csharp)
- [Activity processing](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-activity-processing?view=azure-bot-service-4.0)
