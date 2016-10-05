#!/usr/bin/python
import discord
import asyncio

client = discord.Client()

@client.async_event
async def on_message(message):
    try:
        print(str(message.channel.server.name) + " -> " + str(message.channel.name) + ' - ' + str(message.author) + ': ' + str(message.content))
    except:
        print("Private message - " + str(message.author) + ': ' + str(message.content))

#loop = asyncio.get_event_loop()
    if message.author.id == client.user.id and '!yank' in message.content:
        try:
            await client.send_message(message.channel,"Getting the logs for {}".format(message.channel.name))

            with open("{0}.txt".format(message.channel.name),'w') as f:
                async for line in client.logs_from(message.channel, limit=10000000):
                    for i in line.attachments:
                        try:
                            f.write('{0}::file:{1}\n'.format(line.author.name,i['url']))
                        except:
                            continue
                        
                    try:
                        f.write('{0}: {1}\n'.format(line.author.name,line.content)) #line is of the message type
                    except:
                        continue

            await client.send_message(message.channel,'The logs for this channel have been saved.')
        except Exception as e:
            await client.send_message(message.channel,'Failed saving logs: {}'.format(e))

@client.async_event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    
client.run('<username>', '<password>')

