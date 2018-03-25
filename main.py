import sekrets

import discord
import asyncio

client = discord.Client()

players = {}

# wenn gestartet
@client.event
@asyncio.coroutine
def on_ready():
    print(client.user.name + ' ist online')
    yield from client.send_message(client.get_channel('419136782173732865'),
                                   embed=discord.Embed(color=discord.Color.green(),
                                                       description='{name} meldet sich zum dienst.'.format(
                                                           name=client.user.name)))


# auf nachrichten reagieren
@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.lower().startswith('?moe'):
        yield from client.send_message(message.channel,
                                       embed=discord.Embed(color=discord.Color.green(),
                                                           description='Ja bitte?'))


# Musik
# auf nachrichten reagieren


@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith('?moe join'):
        try:
            channel = message.author.voice.voice_channel
            yield from client.join_voice_channel(channel)
        except discord.errors.InvalidArgument:
            yield from client.send_message(message.channel, "Kein Voice channel gefunden.")
        except Exception as error:
            yield from client.send_message(message.channel, "Ein Error: {error}".format(error=error))

    if message.content.startswith('?moe quit'):
        try:
            voice_client = client.voice_client_in(message.server)
            yield from voice_client.disconnect()
        except AttributeError:
            yield from client.send_message(message.channel, "Ich bin zur zeit nicht connected.")
        except Exception as Hugo:
            yield from client.send_message(message.channel, "Ein Error: {haus}".format(haus=Hugo))

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
                voice = yield from client.join_voice_channel(channel)
                player = yield from voice.create_ytdl_player(yt_url)
                players[message.server.id] = player
                player.start()
                print(voice.channel)
        except Exception as err:
            yield from client.send_message(message.channel,
                                           embed=discord.Embed(color=discord.Color.red(),
                                                               description="Fehler:\n{msg}".format(msg=err)))

    if message.content.startswith('?moe stop'):
        try:
            players[message.server.id].stop()
        except:
            pass

    if message.content.startswith('?moe pause'):
        try:
            players[message.server.id].pause()
        except:
            pass

    if message.content.startswith('?moe resume'):

        try:
            players[message.server.id].resume()
        except:
            pass


client.run(sekrets.botToken)
