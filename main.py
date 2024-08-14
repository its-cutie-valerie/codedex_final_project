import discord
import io
from PIL import Image
import imageio

class MyClient(discord.Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.images_cache = {}  # Dictionary to cache images by channel ID
        self.user_prompts = {}  # Dictionary to store user prompts for duration and loop count

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        # Ignore messages from the bot itself
        if message.author == self.user:
            return
        
        channel_id = message.channel.id

        # Handle `$gif` command
        if message.content.startswith('$gif'):
            if channel_id in self.images_cache and self.images_cache[channel_id]:
                # Prompt user for duration and loop count
                await message.channel.send("Please provide the duration (in milliseconds) for each frame and loop count (0 for infinite loop, any other number for a specific loop count) in the format: `duration, loop`")

                # Store the prompt awaiting for a response
                self.user_prompts[channel_id] = message.author.id
            else:
                await message.channel.send('No images to create a GIF.')

        # Handle image attachments
        elif message.attachments:
            images = []
            for attachment in message.attachments:
                if attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_bytes = await attachment.read()
                    image = Image.open(io.BytesIO(image_bytes))
                    images.append(image)

            if images:
                if channel_id not in self.images_cache:
                    self.images_cache[channel_id] = []

                # Add images to cache
                self.images_cache[channel_id].extend(images)
                await message.channel.send('Image added. Use `$gif` to create the GIF.')
            else:
                await message.channel.send('Please attach valid images (png, jpg, jpeg).')

        # Handle user input for duration and loop count
        elif channel_id in self.user_prompts and message.author.id == self.user_prompts[channel_id]:
            try:
                # Expecting user input in the format: duration, loop
                duration, loop = map(int, message.content.split(','))
                if loop < 0:
                    await message.channel.send('Loop count must be a non-negative integer.')
                    return

                # Create a GIF from the images
                if channel_id in self.images_cache and self.images_cache[channel_id]:
                    images = self.images_cache[channel_id]
                    self.images_cache[channel_id] = []  # Clear cache

                    if images:
                        # Convert PIL images to in-memory file-like objects
                        image_files = []
                        for image in images:
                            img_byte_arr = io.BytesIO()
                            image.save(img_byte_arr, format='PNG')  # Save image as PNG in-memory
                            img_byte_arr.seek(0)
                            image_files.append(img_byte_arr.read())

                        # Create a GIF from the images
                        gif_bytes = io.BytesIO()
                        with imageio.get_writer(gif_bytes, format='GIF', mode='I', duration=duration, loop=loop) as writer:
                            for img_data in image_files:
                                img = imageio.imread(io.BytesIO(img_data))
                                writer.append_data(img)
                        gif_bytes.seek(0)

                        # Send the GIF
                        await message.channel.send(file=discord.File(fp=gif_bytes, filename='output.gif'))
                        # Remove user prompt
                        del self.user_prompts[channel_id]
                    else:
                        await message.channel.send('No images found to create a GIF.')
                else:
                    await message.channel.send('No images to create a GIF.')
            except ValueError:
                await message.channel.send('Invalid format. Please use `duration, loop` format with integer values.')
            except Exception as e:
                await message.channel.send(f'An error occurred: {e}')

# Set up the bot's intents
intents = discord.Intents.default()
intents.message_content = True

# Create an instance of the bot
client = MyClient(intents=intents)

# Run the bot with the token
client.run('DISCORD_TOKEN')  # Replace with your own token.
