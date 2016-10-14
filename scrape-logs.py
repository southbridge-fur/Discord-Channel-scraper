#!/usr/bin/python
import discord
import asyncio
import getpass
import argparse
import re

parser = argparse.ArgumentParser(description='Scrapes the logs from a Discord channel.')
parser.add_argument('--username','-u', action='store', help='Username to login under. If not specified, username will be prompted for.')
parser.add_argument('--password','-p', action='store', help='Password to login under. If not specified, password will be prompted for.')
parser.add_argument('--flag','-f', action='store', default="!yank", help='An alternative to specifing the server and channel, specify a piece of regex which when matched against a message sent by the target user, will trigger scraping of the channel the message was posted in. Useful for private messages and private chats. Default value is "!yank", activates by default if no server is specified.')
parser.add_argument('--quiet','-q', action='store_true', help='Supress messages in Discord')
parser.add_argument('--server','--guild','-s', action='store', help='Discord server name to scrape from (user must be a member of the server and have history privileges). If channel is not specified the entire server will be scraped.')
parser.add_argument('--channel','-c', action='store', help='Discord channel name to scrape from (user must have history privileges for the particular channel)')
parser.add_argument('--limit','-l', action='store', default=1000000, type=int, help='Number of messages to save. Default is 1000000')
parser.add_argument('--output','-o', action='store', help="Outputs all logs into a single file. If not specified, logs are saved under the format: <server name>-<channel name>.txt.") 

args = parser.parse_args()

#prompt for username
if (not args.username):
    args.username = input("username: ")

if (not args.password):
    args.password = getpass.getpass("password: ")

print(args)
    
client = discord.Client()

async def getLogs(channel):
    try:
        if not args.quiet:
            await client.send_message(channel,"Getting the logs for {}".format(channel.name))
            
        #with open(((channel.server != None) ? "{0}-{1}.txt".format(channel.server.name,channel.name): "{0}.txt".format(channel.name)),'w') as f:
        with open("{0}.txt".format(channel.name),'w') as f:
            for line in client.logs_from(channel, limit=args.limit):
                for i in line.attachments:
                    try:
                        f.write('{0}::file:{1}\n'.format(line.author.name,i['url']))
                    except:
                        continue
                try:
                    f.write('{0}: {1}\n'.format(line.author.name,line.content)) #line is of the message type
                except:
                    continue
        if not args.quiet:
            await client.send_message(channel,'The logs for this channel have been saved.')
    except Exception as e:
        if not args.quiet:
            await client.send_message(channel,'Failed saving logs: {}'.format(e))


#Strangely, this will work once we are logged in
@client.async_event
async def on_message(message):
    try:
       print(str(message.channel.server.name) + " -> " + str(message.channel.name) + ' - ' + str(message.author) + ': ' + str(message.content))
    except:
       print("Private message - " + str(message.author) + ': ' + str(message.content))

    # if (not args.server) and message.author.id == client.user.id and re.compile(args.flag).match(message.content):
    #     print("Matched {}".format(args.flag))
    #     await getLogs(message.channel)


#on login this does not execute
#issues like this have happened before when issues with asyncio arrise
@client.async_event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

    #even with the rest of this function commented out it will not be called when we are logged in despite messages propegating to on_message
    if (args.server):
        print("cheching server")
        server = discord.utils.get(client.servers, server__name=args.server)
        if (not server):
            print("Invalid server name: {}".format(args.server))
            await client.logout()
            exit()
        print("good server")
        if (args.channel):
            print("checking channel")
            channel = discord.utils.get(client.get_all_channels, server=server, name=args.channel)
            if (not channel):
                print("Invalid channel name: {}".format(args.channel))
                await client.logout()
                exit()
            print("good channel")
            getLogs(channel)
        else:
            for channel in server.channels:
                getLogs(channel)
        await client.logout()
        exit()

        
try:
    client.run(args.username, args.password)
except KeyboardInterrupt:
    client.logout()
    exit()
except Exception as e:
    print("{}".format(e))
    exit()
