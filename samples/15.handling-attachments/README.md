# Handling Attachments

Bot Framework v4 handling attachments bot sample

This bot has been created using [Bot Framework](https://dev.botframework.com), it shows how to send outgoing attachments and how to save attachments to disk.

## Running the sample
- Clone the repository
```bash
git clone https://github.com/Microsoft/botbuilder-python.git
```
- Activate your desired virtual environment
- Bring up a terminal, navigate to `botbuilder-python\samples\15.handling-attachments` folder
- In the terminal, type `pip install -r requirements.txt`
- In the terminal, type `python app.py`

## Testing the bot using Bot Framework Emulator
[Microsoft Bot Framework Emulator](https://github.com/microsoft/botframework-emulator) is a desktop application that allows bot developers to test and debug their bots on localhost or running remotely through a tunnel.

- Install the Bot Framework emulator from [here](https://github.com/Microsoft/BotFramework-Emulator/releases)

### Connect to bot using Bot Framework Emulator
- Launch Bot Framework Emulator
- File -> Open Bot
- Paste this URL in the emulator window - http://localhost:3978/api/messages

## Attachments

A message exchange between user and bot may contain cards and media attachments, such as images, video, audio, and files.
The types of attachments that may be sent and received varies by channel. Additionally, a bot may also receive file attachments.

## Further reading

- [Bot Framework Documentation](https://docs.botframework.com)
- [Bot Basics](https://docs.microsoft.com/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0)
- [Activity processing](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-activity-processing?view=azure-bot-service-4.0)
- [Attachments](https://docs.microsoft.com/en-us/azure/bot-service/nodejs/bot-builder-nodejs-send-receive-attachments?view=azure-bot-service-4.0)
- [Channels and Bot Connector Service](https://docs.microsoft.com/en-us/azure/bot-service/bot-concepts?view=azure-bot-service-4.0)
