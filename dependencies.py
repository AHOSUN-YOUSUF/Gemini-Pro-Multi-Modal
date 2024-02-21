# Import necessary libraries
from google.generativeai import (configure, GenerativeModel)
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

# Class to encapsulate model configuration and safety settings
class GenerativeModelConfig:
    TEXT_TO_TEXT_MODEL_NAME: str = "models/gemini-pro"
    TEXT_AND_IMAGE_TO_TEXT_MODEL_NAME: str = "models/gemini-pro-vision"
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
    def gemini_auth(auth_key: str) -> None: configure(api_key = auth_key)

    # Generate text based on text input
    async def text_to_text(self, query: str) -> str:
        model = GenerativeModel(model_name = self.model_name,
                                generation_config=self.generation_config,
                                safety_settings=self.safety_settings)

        answer = model.generate_content(contents = [query])
        return answer.text

    # Generate text based on text and image input
    async def text_image_to_text(self, query: str, mime_type: str, image_data: bytes) -> str:
        model = GenerativeModel(model_name = self.model_name,
                                generation_config = self.generation_config,
                                safety_settings = self.safety_settings)

        answer = model.generate_content(contents=[query,
                                                  {"mime_type": mime_type,
                                                   "data": image_data}])
        return answer.text

# Class to handle image related operations
class ImageConfig:
    GET_IMAGE = get_image
    IMAGE_OPENER = Image
    IMAGE_READER = BytesIO
    IMAGE_FORMATS: dict[str, str] = {"jpeg": "image/jpeg",
                                     "webp": "image/webp",
                                     "jpg": "image/jpeg",
                                     "png": "image/png"}

# Class to handle image input and output
class ImageIO:
    @staticmethod
    async def copy_image_data(url: str | bytes) -> bytes:
        response: Response = ImageConfig.GET_IMAGE(url)
        if response.status_code == 200: return response.content
        return None

    @staticmethod
    async def get_image_type(image_data: bytes) -> str:
        image = ImageConfig.IMAGE_OPENER.open(ImageConfig.IMAGE_READER(image_data))
        mime_type = ImageConfig.IMAGE_FORMATS.get(image.format.lower())
        return mime_type
