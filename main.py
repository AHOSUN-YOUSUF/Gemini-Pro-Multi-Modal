# Import necessary dependencies
from google.generativeai import (configure)
from dependencies import (GeminiCompletion, GenerativeModelConfig, ImageIO, BOT, MessageStuff)
from keep_alive import (keep_alive)
from discord import (Activity, ActivityType, Status, errors)
from os import (environ)


keep_alive()

# Event handler for when the bot is ready
@BOT.client.event
async def on_ready():
    # Notify when the bot is logged in
    print(f"Logged In as { BOT.client.user }")

    await BOT.client.user.edit(username = "Gemini Pro Multi-Modal")
    # Set bot username and presence
    await BOT.client.change_presence(activity = Activity(application_id = 1153053230377488456,
                                                         type = ActivityType.playing,
                                                         name =  f"In { BOT.in_guilds() } Servers",
                                                         state = "Looking for getting Mentioned!",
                                                         large_image = "gemini",
                                                         large_text = "Spinning around and helping people!"),
                                     status = Status.idle)

    # Output the number of servers the bot is connected to
    print(f"Connected to { BOT.in_guilds() } servers")
    print(f"In:\n{ BOT.client.guilds }\nServers...")

    # Configure Google Generative AI
    configure(api_key = "GEMINI_API_Key_PLAIN_VAL") # Replace with your actual Google Gemini API key

# Event handler for when a message is received
@BOT.client.event
async def on_message(message):
    # Do nothing if Author of the message is the BOT
    if message.author == BOT.client.user:
        return

    if message.content.startswith("<@1152586031149883423>") and message.attachments:
        command, user_message = message.content.split(" ", 1)
        image_data = await ImageIO.copy_image_data(message.attachments[0].url)
        mime_type = await ImageIO.get_image_type(image_data)
        bot_response = await GeminiCompletion(model_name = GenerativeModelConfig.TEXT_AND_IMAGE_TO_TEXT_MODEL_NAME,
                                              generation_config = GenerativeModelConfig.GENERATION_CONFIG,
                                              safety_settings = GenerativeModelConfig.SAFETY_SETTINGS).text_image_to_text(query = user_message, mime_type = mime_type, image_data = image_data)

        # Reply to the message with the bot's response
        await message.reply("The response to your message from <@1152586031149883423> was this:", mention_author = False)
        try: 
            for part in MessageStuff(text = bot_response).split_text(): await message.channel.send(part)
        except errors.HTTPException: pass

    elif message.content.startswith("<@1152586031149883423>"):
        command, user_message = message.content.split(" ", 1)
        bot_response = await GeminiCompletion(model_name = GenerativeModelConfig.TEXT_TO_TEXT_MODEL_NAME,
                                              generation_config = GenerativeModelConfig.GENERATION_CONFIG,
                                              safety_settings = GenerativeModelConfig.SAFETY_SETTINGS).text_to_text(query = user_message)

        # Reply to the message with the bot's response
        await message.reply("The response to your message from <@1152586031149883423> was this:", mention_author=False)
        try: 
            for part in MessageStuff(text = bot_response).split_text(): await message.channel.send(part)
        except errors.HTTPException: pass

# Run the bot
if __name__ == "__main__": BOT.client.run(token = environ.get("GEMINI_Multi_Modal_TOKEN")) # Replace with your actual bot token
