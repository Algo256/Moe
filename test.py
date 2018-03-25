import discord
import asyncio
import sekrets

client = discord.Client()

players = {}

@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith('?moe play'):
        yt_url = message.content[10:]
        try:
            if client.is_voice_connected(message.server):
                voice_client = client.voice_client_in(message.server)
                yield from voice_client.disconnect()

                channel = message.author.voice.voice_channel
                voice = yield from client.join_voice_channel(channel)
                player = yield from voice.create_ytdl_player(yt_url)
                players[message.server.id] = player
                player.start()
            else:
                channel = message.author.voice.voice_channel
                voice = yield from  client.join_voice_channel(channel)
                player = yield from voice.create_ytdl_player(yt_url)
                players[message.server.id] = player
                player.start()
                print(voice.channel)
        except Exception as Hugo:
            yield from client.send_message(message.channel, "Ein Error: ```{haus}```".format(haus=Hugo))

client.run(sekrets.botToken)