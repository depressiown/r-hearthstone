'''
Sidebar configuration utility. Quickly get what you need.
'''

import sys
import os
from ConfigParser import SafeConfigParser


class SidebarConfiguration:

    def __init__(self):

        self.config = SafeConfigParser()
        configPath = os.path.abspath(os.path.dirname(sys.argv[0]))
        configPath = os.path.join(configPath, 'hearthstone.cfg')
        self.config.read(configPath)

    def getCalendarID(self):
        return self.config.get('calendar', 'id')

    def getCalendarKey(self):
        return self.config.get('google', 'token')

    def getTargetSubreddit(self):
        return self.config.get('reddit', 'subreddit')

    def getRedditOAuthClientID(self):
        return self.config.get('reddit', 'oauth_client_id')

    def getRedditOAuthClientSecret(self):
        return self.config.get('reddit', 'oauth_client_secret')

    def getRedditOAuthAccessCode(self):
        return self.config.get('reddit', 'oauth_access_code')

    def getLogFileLocation(self):
        return self.config.get('log', 'file')
