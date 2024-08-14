# Discord GIF Bot

The sole purpose of this bot is to practice Python, the libraries in it and build a final project for [Codédex](https://codedex.io) Python curriculum.\
It uses '**discord**' for interacting with the Discord platform, '**io**' for handling in-memory file operations, '**PIL**' (Pillow) for image processing and '**imageio**'for reading and writing images (GIFs in this case).\
Code waits for user to upload images and adds a prompt `$gif` to create the gif, then it asks for delay between each image and if it should be looped (0) or if it's supposed to have fixed amount of repetitions, and then it uploads the gif to the channel.\
It needs [Discord Developers](https://discord.com/developers/) account and created bot for the token that replaces `DISCORD_TOKEN` in the very bottom of the code