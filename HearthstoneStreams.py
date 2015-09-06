'''
Class for generating markdown of the top (and random) Hearthstone streams.

Implemented:
- Twitch

To-do:
- Everything else
'''

import random
import requests
import string


class HearthstoneStreams:

    numberOfTopStreams = 3
    numberOfRandomStreams = 3

    def __init__(self, config, logger):

        self.twitchID = config.getTwitchClientID()
        self.twitchSecret = config.getTwitchClientSecret()
        self.logger = logger
        self.streamList = []

    def __addTwitchStreams(self):

        self.logger.info('Fetching streams from Twitch API...')
        twitchTop50 = requests.get(
            "https://api.twitch.tv/kraken/streams",
            params={
                "limit": 50,
                "game": "Hearthstone: Heroes of Warcraft"
            })

        self.streamList = []
        for stream in twitchTop50.json()["streams"]:
            self.streamList.append({
                'streamer': stream['channel']['display_name'],
                'viewers': stream['viewers'],
                'url': stream['channel']['url'],
                'title': stream['channel']['status']
                })

    def __sortStreamList(self):

        sortedList = sorted(self.streamList, key=lambda k: k['viewers'], reverse=True)
        self.streamList = sortedList

    def __buildFormattedStream(self, streamIndex):

        streamer = self.streamList[streamIndex]['streamer'].encode('utf-8').rstrip()
        viewers = str(self.streamList[streamIndex]['viewers'])
        url = self.streamList[streamIndex]['url'].encode('utf-8') + '#stream'

        title = self.streamList[streamIndex]['title'].rstrip().lstrip()
        charactersToEscape = [']', '[', '~']
        for characterToEscape in charactersToEscape:
            title = string.replace(title, characterToEscape, '\\' + characterToEscape)

        if len(title) > 80:
            title = title[:80] + '...'

        title = title.encode('utf-8')

        return ">[~~{}~~\n>~~{} viewers~~\n>~~{}~~]({})\n\n".format(streamer, viewers, title, url)

    def populate(self):

        self.__addTwitchStreams()

        self.__sortStreamList()

    def getTopStreamerMarkdown(self):

        markdown = ''
        for streamIndex in range(0, HearthstoneStreams.numberOfTopStreams):
            markdown += self.__buildFormattedStream(streamIndex)

        self.logger.info('---------- TOP STREAM MARKDOWN ----------')
        self.logger.info('\n' + markdown)
        self.logger.info('-----------------------------------------')

        return markdown

    def getRandomStreamerMarkdown(self):

        random.seed()
        randomIndexes = random.sample(
            range(HearthstoneStreams.numberOfTopStreams, len(self.streamList) - 1),
            HearthstoneStreams.numberOfRandomStreams)

        markdown = ''
        for streamIndex in randomIndexes:
            markdown += self.__buildFormattedStream(streamIndex)

        self.logger.info('---------- RANDOM STREAM MARKDOWN ----------')
        self.logger.info('\n' + markdown)
        self.logger.info('--------------------------------------------')

        return markdown
