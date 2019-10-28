# suggested actions

Bot Framework v4 using adaptive cards bot sample

This bot has been created using [Bot Framework](https://dev.botframework.com), it shows how to use suggested actions.  Suggested actions enable your bot to present buttons that the user can tap to provide input.

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
- Bring up a terminal, navigate to `botbuilder-python\samples\02.echo-bot` folder
- In the terminal, type `pip install -r requirements.txt`
- In the terminal, type `python app.py`

## Testing the bot using Bot Framework Emulator
[Microsoft Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework emulator from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to bot using Bot Framework Emulator
- Launch Bot Framework Emulator
- Paste this URL in the emulator window - http://localhost:3978/api/messages

Suggested actions enable your bot to present buttons that the user can tap to provide input. Suggested actions appear close to the composer and enhance user experience.
