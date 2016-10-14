#!/usr/bin/python
import discord
import asyncio
import getpass
import argparse

parser = argparse.ArgumentParser(description='Scrapes the logs from a Discord channel.')
parser.add_argument('--username','-u', action='store', help='Username to login under. Note: If not specified, username and/or password will be prompted for.')
parser.add_argument('--password','-p', action='store', help='Password to login under')
parser.add_argument('--server','--guild','-s', action='store', help='Discord server name to scrape from (user must be a member of the server and have history privileges). If channel is not specified the entire server will be scraped.')
parser.add_argument('--channel','-c', action='store', help='Discord channel name to scrape from (user must have history privileges for the particular channel)')
parser.add_argument('--flag','-f', action='store', help='An alternative to specifing the server and channel, specify a piece of regex which when matched against a message sent by the target user, will trigger scaping of the channel the message was posted in. Useful for private messages and private chats.')
parser.add_argument('--limit','-l', action='store', default=1000000, type=int, help='Number of messages to save')
parser.add_argument('--output','-o', action='store', help="Outputs all logs into a single file. If not specified, logs are saved under the format: <server name>-<channel name>.txt.") 

args = parser.parse_args()

#prompt for username
if (not args.username):
    args.username = input("username: ")

if (not args.password):
    args.password = getpass.getpass("password: ")

client = discord.Client()

@client.async_event
async def on_message(message):
    #try:
    #    print(str(message.channel.server.name) + " -> " + str(message.channel.name) + ' - ' + str(message.author) + ': ' + str(message.content))
    #except:
    #    print("Private message - " + str(message.author) + ': ' + str(message.content))

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
    if (args.server):
        

    
client.run(args.username, args.password)

