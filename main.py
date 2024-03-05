# Import necessary dependencies
from dependencies import (GeminiCompletion, GenerativeModelConfig, ImageIO, BOT, MessageStuff)
from keep_alive import (keep_alive)
from aiohttp import (client_exceptions)
from discord import (Activity, ActivityType, Status, errors)
from time import (time)
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
    GeminiCompletion.gemini_auth(auth_key = environ.get("GEMINI_API_Key_PLAIN_VAL")) # Replace with your actual Google Gemini API key

# Event handler for when a message is received
@BOT.client.event
async def on_message(message):
    # Do nothing if Author of the message is the BOT
    if message.author == BOT.client.user:
        return

    elif message.content.startswith("<@1152586031149883423>") and message.attachments:
        await message.add_reaction("<:Gemini:1209104350832762922>")
        start_time = time()
        command, user_message = message.content.split(" ", 1)
        image_data = await ImageIO.copy_image_data(message.attachments[0].url)
        mime_type = await ImageIO.get_image_type(image_data)
        bot_response = await GeminiCompletion(model_name = GenerativeModelConfig.TEXT_AND_IMAGE_TO_TEXT_MODEL_NAME,
                                              generation_config = GenerativeModelConfig.GENERATION_CONFIG,
                                              safety_settings = GenerativeModelConfig.SAFETY_SETTINGS).text_image_to_text(query = user_message, mime_type = mime_type, image_data = image_data)
        await message.add_reaction("<a:complition_done:1214170055210967090>")
        end_time = time()
        # Reply to the message with the bot's response
        async with message.channel.typing(): await message.reply(f"The response to your message from <@1152586031149883423> was this [Which was Generated in: {end_time - start_time} seconds]:", mention_author = False)
        try: 
            async with message.channel.typing(): 
                for part in MessageStuff(text = bot_response).split_text(): await message.channel.send(part)
        except errors.HTTPException: pass
        finally:
            server = BOT.client.get_guild(int(environ.get("MESSGAE_LOGGER_SERVER_ID")))
            channel = server.get_channel(int(environ.get("MESSGAE_LOGGER_CHANNEL_ID")))
            await channel.send(f"User: <@{message.author.id}>")
            await channel.send(f"User Message: {user_message}")
            await channel.send(f"User Image: [User Image link.]( {message.attachments[0].url} )")
            await channel.send(f"<@1152586031149883423> Responce to the Message:")
            async with message.channel.typing(): 
                for part in MessageStuff(text = bot_response).split_text(): await channel.send(part)

    elif message.content.startswith("<@1152586031149883423>"):
        await message.add_reaction("<:Gemini:1209104350832762922>")
        start_time = time()
        command, user_message = message.content.split(" ", 1)
        bot_response = await GeminiCompletion(model_name = GenerativeModelConfig.TEXT_TO_TEXT_MODEL_NAME,
                                              generation_config = GenerativeModelConfig.GENERATION_CONFIG,
                                              safety_settings = GenerativeModelConfig.SAFETY_SETTINGS).text_to_text(query = user_message)
        await message.add_reaction("<a:complition_done:1214170055210967090>")
        end_time = time()
        # Reply to the message with the bot's response
        async with message.channel.typing(): await message.reply(f"The response to your message from <@1152586031149883423> was this [Which was Generated in: {end_time - start_time} seconds]:", mention_author = False)
        try: 
            async with message.channel.typing(): 
                for part in MessageStuff(text = bot_response).split_text(): await message.channel.send(part)
        except errors.HTTPException: pass
        finally:
            server = BOT.client.get_guild(int(environ.get("MESSGAE_LOGGER_SERVER_ID")))
            channel = server.get_channel(int(environ.get("MESSGAE_LOGGER_CHANNEL_ID")))
            await channel.send(f"User: <@{message.author.id}>")
            await channel.send(f"User Message: {user_message}")
            await channel.send(f"User Image: [User Image link.]( {message.attachments[0].url} )")
            await channel.send(f"<@1152586031149883423> Responce to the Message:")
            async with message.channel.typing(): 
                for part in MessageStuff(text = bot_response).split_text(): await channel.send(part)

# Run the bot
try: 
    if __name__ == "__main__": BOT.client.run(token = environ.get("GEMINI_Multi_Modal_TOKEN")) # Replace with your actual bot token

except errors.LoginFailure: print("Improper token for the BOT, `@Gemini Pro Multi-Modal#0747`.\n",
                                  "• Check the BOT token of `@Gemini Pro Multi-Modal#0747` at:\n",
                                  "• https://discord.com/developers/applications/1153053230377488456/bot")

except client_exceptions.ClientConnectionError: print("Can't connect your client to `discord.com`.\n",
                                                      "Maybe problem came for not Stable Net Connection.\n",
                                                      "Connect to a Stable Net Connection and try again later.")
