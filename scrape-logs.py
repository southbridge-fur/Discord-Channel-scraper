#!/usr/bin/python
import discord
import asyncio
import getpass
import argparse
import re
import logging

logging.basicConfig(
    level = "WARNING",
    style = "{",
    format="[{asctime}] [{process}] [{levelname}] {filename}:{lineno} {msg}"
    )

log = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='Scrapes the logs from a Discord channel.')
parser.add_argument('--username','-u', action='store', help='Username to login under. If not specified, username will be prompted for.')
#parser.add_argument('--password','-p', action='store', help='Password to login under. If not specified, password will be prompted for.')
parser.add_argument('--flag','-f', action='store', default="!yank", help='An alternative to specifing the server and channel, specify a piece of regex which when matched against a message sent by the target user, will trigger scraping of the channel the message was posted in. Useful for private messages and private chats. Default value is "!yank", activates by default if no server is specified.')
parser.add_argument('--quiet','-q', action='store_true', help='Supress messages in Discord')
parser.add_argument('--server','--guild','-s', action='store', help='Discord server name to scrape from (user must be a member of the server and have history privileges). This field is case sensitive. If channel is not specified the entire server will be scraped.')
parser.add_argument('--channel','-c', action='store', help='Discord channel name to scrape from (user must have history privileges for the particular channel). This field is case sensitive.')
parser.add_argument('--limit','-l', action='store', default=1000000, type=int, help='Number of messages to save. Default is 1000000')
parser.add_argument('--output','-o', action='store', help="Outputs all logs into a single file. If not specified, logs are saved under the format: <server name>-<channel name>.txt.") 
parser.add_argument('--logging', action='store', choices=[10,20,30,40,50], default=20, help='Change the logging level. Defaults to 20, info.')

args = parser.parse_args()

log.setLevel(args.logging)

#prompt for username
if (not args.username):
    args.username = input("Username: ")

password = getpass.getpass("Password for user {0}: ".format(args.username))

client = discord.Client()

async def getLogs(channel):
    try:
        if not args.quiet:
            await client.send_message(channel,"Getting the logs for channel {0}".format(channel.name))
        log.info("Getting the logs for channel {0}".format(channel.name))
        with open("{0}.txt".format(channel.name),'w') as f:
            async for line in client.logs_from(channel, limit=args.limit):
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
            await client.send_message(channel,'The messages for this channel have been saved.')
        log.info("Messages for channel {0} finished downloading".format(channel.name))
    except Exception as e:
        if not args.quiet:
            await client.send_message(channel,'Failed saving logs: {}'.format(e.message))
        log.error("Error while downloading channel {0}: {1}".format(channel.name,e.message))


#Strangely, this will work once we are logged in
@client.async_event
async def on_message(message):
    try:
       log.debug(str(message.channel.server.name) + " -> " + str(message.channel.name) + ' - ' + str(message.author) + ': ' + str(message.content))
    except:
       log.debug("Private message - " + str(message.author) + ': ' + str(message.content))

    if not args.server and not args.channel:
        if args.flag == message.content[:len(args.flag)]:
            await getLogs(message.channel)
    # if (not args.server) and message.author.id == client.user.id and re.compile(args.flag).match(message.content):
    #     print("Matched {}".format(args.flag))
    #     await getLogs(message.channel)


@client.async_event
async def on_ready():
    log.info("Logged in as user {0}".format(client.user.name))

    if args.server and args.channel:
        channel = ""
        try:
            channel = discord.utils.get(client.get_all_channels(), server__name=args.server, name=args.channel)
        except:
            channel = ""
        if channel:
            await getLogs(channel)
        else:
            log.error("Could not find channel {0} in server {1}".format(args.channel, args.server))
        await client.logout()
    elif args.server:
        log.info("Downloading messages for all channels in server {0}".format(arg.server))
        for channel in server.channels:
            await getLogs(channel)
        await client.logout()
    else:
        log.info('Entering flag mode with flag "{0}"'.format(args.flag))
        
try:
    log.info("Logging in...")
    client.run(args.username, password)
except KeyboardInterrupt:
    log.info("Logging out...")
except Exception as e:
    log.error(e.message)
