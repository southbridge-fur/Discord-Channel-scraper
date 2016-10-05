Meant for use with the discord chat program available here: [Discord](https://discordapp.com/)

**Requires**
	* [Rapptz's discord python API](https://github.com/Rapptz/discord.py)
		* Note: can be installed by running the following command as root:
		```python3 -m pip install -U discord.py```
		**See official documentation for further customization.*

**Usage**

1. Modify the final line in the script to include both your discord email and password
2. Run the script
	* Note: a rather cryptic error can occur if you have 2 factor authentication enabled, [bug report here](https://github.com/Rapptz/discord.py/issues/235))
3. As the same user which was used to log into the script, go to the desired channel you wish to save and type ```!yank``` which will start the scraping process
4. If successful, the file should be saved in the directory you ran the script in as <channel name>.txt
	* Note: This works with both server channels and private channels, however private conversions will save under the filename 'None.txt', while everything else will save under the name of the channel.

**Future plans**

- [ ]: Solve the 2FAuth issue.
- [ ]: More robust than the hacked-together mess it currently is
- [ ]: *Quiet mode* - doesn't require messages
- [ ]: Command line arguments
- [ ]: Remake discord API in C so it works more than half the time.