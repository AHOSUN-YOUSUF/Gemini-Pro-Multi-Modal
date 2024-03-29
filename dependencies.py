# Import necessary libraries
from google.generativeai import (configure, GenerativeModel)
from google.api_core import (exceptions)
from requests import (get as get_image, Response)
from discord import (Client, Intents)
from PIL import (Image)
from re import (split, DOTALL)
from io import (BytesIO)

# Define a class to encapsulate Discord bot setup
class BOT:
    # Set up Discord client with default intents
    intents = Intents.default()
    intents.message_content = True
    client: Client = Client(intents=intents)

    # Function to get the number of guilds the bot is in
    def in_guilds() -> int: return len(BOT.client.guilds)

# Class to handle message splitting
class MessageStuff:
    def __init__(self, text: str) -> None:
        self.text = text

    # Function to split text into chunks of 2000 characters or less
    def split_text(self) -> list[str]:
        parts = split(pattern = r'(```.*?```)', string = self.text, flags = DOTALL)
        result: list[str] = []
        for part in parts:
            while len(part) > 2000:
                split_index = part.rfind('\n', 0, 2000)
                if split_index == -1: split_index = 2000
                result.append(part[:split_index])
                part = part[split_index:]
            result.append(part)
        return result

    def remove_tags(text: str) -> str:
        text = text.replace("<start_of_text>", "")
        text = text.replace("<end_of_text>", "")
        return text

# Class to encapsulate model configuration and safety settings
class GenerativeModelConfig:
    TEXT_TO_TEXT_MODEL_NAME: str = "models/gemini-1.0-pro-latest"
    TEXT_AND_IMAGE_TO_TEXT_MODEL_NAME: str = "models/gemini-1.0-pro-vision-latest"
    GENERATION_CONFIG: dict[str, int] = {"temperature": 1,
                                         "top_p": 1,
                                         "top_k": 1,
                                         "max_output_tokens": 2048}
    SAFETY_SETTINGS: list = [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                             {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                             {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                             {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}]

# Class to handle text and image to text generation
class GeminiCompletion:
    def __init__(self, model_name: str, generation_config: dict[str, int], safety_settings: list) -> None:
        self.model_name = model_name
        self.generation_config = generation_config
        self.safety_settings = safety_settings

    # Authenticate with the Generative AI service
    @staticmethod
    def gemini_auth(auth_key: str) -> None:
        configure(api_key = auth_key)

    # Generate text based on text input
    async def text_to_text(self, query: str) -> str:
        try:
            model = GenerativeModel(model_name = self.model_name,
                                    generation_config = self.generation_config,
                                    safety_settings = self.safety_settings)
            text_parts = ["""Your a AI built by Google Deep Mind and Gooele AI Team, and your work is to help other people with your Text and Image Understanding and Text generation ability.""",
                          """But people can or will get help from you as a Discord BOT.""",
                         f"""Generate an answer to this prompt in Markdown format: <start_of_text>\n{query}\n<end_of_text>\nFormatting guidelines: For bold text, use **<The Text>**,""",
                          """for lists, use * <The Text>, and for sublists, use * <The Text>. For code blocks, use triple backticks followed by the language and the code.""",
                          """Example Code:\n```cpp\n#include <iostream>\n\nint main()\n{\n    std::cout << "Hello World!";\n    return 0;\n}\n```.""",
                          """Also, try to be friendly and humorous. Feel free to use emoticons like :), :(, :D, ¯\_(ツ)_/¯, :D, :/, :P and :].""",
                          """Notes:\n¯\_(ツ)_/¯ indicates to I don't know,\n:/  indicates to Mild annoyance, indecision, or awkwardness, and\n:P to Playfulness and teasing purpose.""",
                          """However, avoid excessive use of emoticons for a more professional tone."""]
            prompt_parts = ["\n".join(text_parts)]
            answer = model.generate_content(contents = prompt_parts)
            return answer.text
        except exceptions.InternalServerError: return "Before swearing at me! You need to know that it's Googles fault xDD.\nOkay, seriously, I'm not able to process Text to Text with Google for now!\nSorry about that! Check back later! Please?\n:3 oh and did you know you can't process anything in me after a long message as well owo!\nThis message is already SUPERlong so....."
        except exceptions.InvalidArgument: return "Invalid API Key for Google Gemini Pro."

    # Generate text based on text and image input
    async def text_image_to_text(self, query: str, mime_type: str, image_data: bytes) -> str:
        try:
            model = GenerativeModel(model_name = self.model_name,
                                    generation_config = self.generation_config,
                                    safety_settings = self.safety_settings)
            image_parts: list[dict] = [{"mime_type": mime_type,
                                        "data": image_data}]
            prompt_parts: list[str] = [f"<start_of_text>\n{query}\n<end_of_text>",
                                       image_parts[0]]
            answer = model.generate_content(contents = prompt_parts)
            return answer.text

        except exceptions.InternalServerError: return "Before swearing at me! You need to know that it's Googles fault xDD.\nOkay, seriously, I'm not able to process Text to Text with Google for now!\nSorry about that! Check back later! Please?\n:3 oh and did you know you can't process anything in me after a long message as well owo!\nThis message is already SUPERlong so....."
        except exceptions.InvalidArgument: return "Invalid API Key for Google Gemini Pro."

# Class to handle image related operations
class ImageConfig:
    GET_IMAGE: Response = get_image
    IMAGE_FORMATS: dict[str, str] = {"jpeg": "image/jpeg",
                                     "webp": "image/webp",
                                     "jpg": "image/jpeg",
                                     "png": "image/png"}

# Class to handle image input and output
class ImageIO:
    @staticmethod
    async def copy_image_data(url: str | bytes) -> bytes:
        response = ImageConfig.GET_IMAGE(url)
        if response.status_code == 200: return response.content
        return None

    @staticmethod
    async def get_image_type(image_data: bytes) -> str:
        image = Image.open(BytesIO(image_data))
        mime_type = ImageConfig.IMAGE_FORMATS.get(image.format.lower())
        return mime_type
