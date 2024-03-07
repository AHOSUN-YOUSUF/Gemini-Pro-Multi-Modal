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

    elif message.content.startswith("<@1152586031149883423> Help") or message.content.startswith("<@1152586031149883423> help"):
        help_embed = Embed()
        help_embed.color = Colour.blurple()
        help_embed.title = "Someone needs help about @Gemini Pro Multi-Modal Beta, I see!"
        help_embed.url = "https://discord.gg/ukZUPTSQVV"
        help_embed.description = "Help menu for <@1152586031149883423>!"
        help_embed.add_field(name = "Help menu below:\n",
                             value = "How to Use BOT for Text-To-Text Completions | Sending Messages:\n• Mention the BOT using this format:\n <@1152586031149883423> `Your-Message-Goes-Here`.\n• It will then try to produce a AI Generated Text content, by using User Message.\n\nHow to Use BOT for Text-and-Image-To-Text Completions | Sending Messages:\n• Mention the BOT using this format:\n <@1152586031149883423> `Your-Message-Goes-Here`     and attach a Image after the message.\n• It will then try to produce a AI Generated Text content, by using User Message and the Image.\n")
        help_embed.set_image(url = choices(["https://thetechscenes.com/wp-content/uploads/2023/12/Google-Gemini.webp", 
                                            "https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Gemini_SS.width-1300.jpg",
                                            "https://s.yimg.com/ny/api/res/1.2/FWWVOW6s2MUFV_yLq9E36g--/YXBwaWQ9aGlnaGxhbmRlcjt3PTEyMDA7aD02NzU-/https://s.yimg.com/os/creatr-uploaded-images/2023-12/5f7be670-943f-11ee-af7f-41b7060d20ba",
                                            "https://deepmind.google/technologies/gemini/static/images/share.png",
                                            "https://lavocedinewyork.com/wp-content/uploads/2023/12/Gemini-era.jpg"])[0])
        await message.reply(embed = help_embed, mention_author = False)

    elif message.content.startswith("<@1152586031149883423>") and message.attachments:
        await message.add_reaction("<:Gemini:1209104350832762922>")
        # Reply to the message with the bot's response
        try:
            start_time = time()
            _, user_message = message.content.split(" ", 1)
            image_data = await ImageIO.copy_image_data(message.attachments[0].url)
            mime_type = await ImageIO.get_image_type(image_data)
            bot_response = await GeminiCompletion(model_name = GenerativeModelConfig.TEXT_AND_IMAGE_TO_TEXT_MODEL_NAME,
                                                  generation_config = GenerativeModelConfig.GENERATION_CONFIG,
                                                  safety_settings = GenerativeModelConfig.SAFETY_SETTINGS).text_image_to_text(query = f"<start_of_text>\n{user_message}\n<end_of_text>", mime_type = mime_type, image_data = image_data)
            end_time = time()
            if (bot_response):
                await message.add_reaction("<:complition_done:1214170055210967090>")
                async with message.channel.typing(): await message.reply(f"The response to your message from <@1152586031149883423> was this [Which was Generated in: {end_time - start_time} seconds]:", mention_author = False)
                async with message.channel.typing(): 
                    for part in MessageStuff(text = bot_response).split_text(): await message.channel.send(part)
            else: await message.add_reaction("<:complition_undone:1214170316801179648>")
        except ValueError:
            start_time = time()
            _, user_message = message.content.split(" ", 1)
            image_data = await ImageIO.copy_image_data(message.attachments[0].url)
            mime_type = await ImageIO.get_image_type(image_data)
            bot_response = await GeminiCompletion(model_name = GenerativeModelConfig.TEXT_AND_IMAGE_TO_TEXT_MODEL_NAME,
                                                  generation_config = GenerativeModelConfig.GENERATION_CONFIG,
                                                  safety_settings = GenerativeModelConfig.SAFETY_SETTINGS).text_image_to_text(query = f"<start_of_text>\n{user_message}\n<end_of_text>", mime_type = mime_type, image_data = image_data)
            end_time = time()
            if (bot_response):
                await message.add_reaction("<:complition_done:1214170055210967090>")
                async with message.channel.typing(): await message.reply(f"The response to your message from <@1152586031149883423> was this [Which was Generated in: {end_time - start_time} seconds]:", mention_author = False)
                async with message.channel.typing(): 
                    for part in MessageStuff(text = bot_response).split_text(): await message.channel.send(part)
            else: await message.add_reaction("<:complition_undone:1214170316801179648>")
        except errors.HTTPException: pass
        except UnboundLocalError: pass
        finally:
            server = BOT.client.get_guild(int(environ.get("MESSGAE_LOGGER_SERVER_ID")))
            channel = server.get_channel(int(environ.get("MESSGAE_LOGGER_CHANNEL_ID")))
            await channel.send(f"User: <@{message.author.id}>")
            await channel.send("Complition type: `Text-and-Image-To-Text`")
            await channel.send(f"User Message: {user_message}")
            await channel.send(f"User Image: [User Image link.]( {message.attachments[0].url} )")
            await channel.send(f"<@1152586031149883423> Responce to the Message:")
            async with channel.typing(): 
                for part in MessageStuff(text = bot_response).split_text(): await channel.send(part)

    elif message.content.startswith("<@1152586031149883423>"):
        await message.add_reaction("<:Gemini:1209104350832762922>")
        # Reply to the message with the bot's response
        try:
            start_time = time()
            _, user_message = message.content.split(" ", 1)
            bot_response = await GeminiCompletion(model_name = GenerativeModelConfig.TEXT_TO_TEXT_MODEL_NAME,
                                                  generation_config = GenerativeModelConfig.GENERATION_CONFIG,
                                                  safety_settings = GenerativeModelConfig.SAFETY_SETTINGS).text_to_text(query = f"<start_of_text>\n{user_message}\n<end_of_text>")
            await message.add_reaction("<:complition_done:1214170055210967090>")
            end_time = time()
            if (bot_response):
                await message.add_reaction("<:complition_done:1214170055210967090>")
                async with message.channel.typing(): await message.reply(f"The response to your message from <@1152586031149883423> was this [Which was Generated in: {end_time - start_time} seconds]:", mention_author = False)
                async with message.channel.typing(): 
                    for part in MessageStuff(text = bot_response).split_text(): await message.channel.send(part)
            else: await message.add_reaction("<:complition_undone:1214170316801179648>")
        except ValueError:
            start_time = time()
            _, user_message = message.content.split(" ", 1)
            bot_response = await GeminiCompletion(model_name = GenerativeModelConfig.TEXT_TO_TEXT_MODEL_NAME,
                                                  generation_config = GenerativeModelConfig.GENERATION_CONFIG,
                                                  safety_settings = GenerativeModelConfig.SAFETY_SETTINGS).text_to_text(query = f"<start_of_text>\n{user_message}\n<end_of_text>")
            await message.add_reaction("<:complition_done:1214170055210967090>")
            end_time = time()
            if (bot_response):
                await message.add_reaction("<:complition_done:1214170055210967090>")
                async with message.channel.typing(): await message.reply(f"The response to your message from <@1152586031149883423> was this [Which was Generated in: {end_time - start_time} seconds]:", mention_author = False)
                async with message.channel.typing(): 
                    for part in MessageStuff(text = bot_response).split_text(): await message.channel.send(part)
            else: await message.add_reaction("<:complition_undone:1214170316801179648>")
        except errors.HTTPException: pass
        except UnboundLocalError: pass
        finally:
            server = BOT.client.get_guild(int(environ.get("MESSGAE_LOGGER_SERVER_ID")))
            channel = server.get_channel(int(environ.get("MESSGAE_LOGGER_CHANNEL_ID")))
            await channel.send(f"User: <@{message.author.id}>")
            await channel.send("Complition type: `Text-To-Text`")
            await channel.send(f"User Message: {user_message}")
            await channel.send(f"<@1152586031149883423> Responce to the Message:")
            async with channel.typing(): 
                for part in MessageStuff(text = bot_response).split_text(): await channel.send(part)

# Run the bot
try: 
    if __name__ == "__main__": BOT.client.run(token = environ.get("GEMINI_Pro_Multi_Modal_TOKEN")) # Replace with your actual bot token

except errors.LoginFailure: print("Improper token for the BOT, `@Gemini Pro Multi-Modal#0747`.\n",
                                  "• Check the BOT token of `@Gemini Pro Multi-Modal#0747` at:\n",
                                  "• https://discord.com/developers/applications/1153053230377488456/bot")

except client_exceptions.ClientConnectionError: print("Can't connect your client to `discord.com`.\n",
                                                      "Maybe problem came for not Stable Net Connection.\n",
                                                      "Connect to a Stable Net Connection and try again later.")
