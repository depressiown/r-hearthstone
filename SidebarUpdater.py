'''
Sidebar updater for /r/hearthstone!

Current features:
- OAuth2 Login
- Calendar

Coming soon:
- Streams
- Tweets
'''

import HTMLParser
import logging
import OAuth2Util
import praw
import time
import traceback
from SidebarConfiguration import SidebarConfiguration
from HearthstoneCalendar import HearthstoneCalendar
from HearthstoneStreams import HearthstoneStreams


testMode = False
sleepTime = 300
config = SidebarConfiguration()

reddit = praw.Reddit('/r/hearthstone sidebar updater')

logger = logging.getLogger('sidebar.logger')
logger.setLevel(logging.INFO)

fileHandler = logging.FileHandler('bot.log')
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))

logger.addHandler(fileHandler)

if not testMode:
    reddit.set_oauth_app_info(client_id=config.getRedditOAuthClientID(),
                              client_secret=config.getRedditOAuthClientSecret(),
                              redirect_uri='http://127.0.0.1:65010/authorize_callback')
    oauth = OAuth2Util.OAuth2Util(reddit)
    #accessInfo = reddit.get_access_information(config.getRedditOAuthAccessCode())
    subreddit = reddit.get_subreddit(config.getTargetSubreddit())

while True:

    calendarMarkdown = ''
    try:
        calendar = HearthstoneCalendar(config, logger)
        calendarMarkdown = calendar.getCalendarMarkdown()
    except Exception as e:
        logger.error('Exception fetching Calendar: {0}'.format(e))
        logger.error(traceback.format_exc())
        logger.error('Sleeping then doing another iteration.')
        time.sleep(sleepTime)
        continue

    topStreamMarkdown = ''
    randomStreamMarkdown = ''
    try:
        streams = HearthstoneStreams(config, logger)
        streams.populate()
        topStreamMarkdown = streams.getTopStreamerMarkdown()
        randomStreamMarkdown = streams.getRandomStreamerMarkdown()
    except Exception as e:
        logger.error('Exception fetching Streams: {0}'.format(e))
        logger.error(traceback.format_exc())
        logger.error('Sleeping then doing another iteration.')
        time.sleep(sleepTime)
        continue

    if not testMode:
        try:
            h = HTMLParser.HTMLParser()
            sidebarTemplate = h.unescape(subreddit.get_wiki_page("sidebar").content_md).encode()

            sidebarTemplate = sidebarTemplate.replace("{{events}}", calendarMarkdown)
            sidebarTemplate = sidebarTemplate.replace("{{top_streams}}", topStreamMarkdown)
            sidebarTemplate = sidebarTemplate.replace("{{random_streams}}", randomStreamMarkdown)
            subreddit.edit_wiki_page("config/sidebar", sidebarTemplate)
        except Exception as e:
            logger.error('Exception posting sidebar: {0}'.format(e))
            logger.error(traceback.format_exc())
            logger.error('Sleeping then doing another iteration.')
            time.sleep(sleepTime)
            continue

    logger.info('Snoozing for ' + str(sleepTime) + ' seconds until next update...\n')

    try:
        time.sleep(sleepTime)
    except Exception as e:
        logger.error('Exception while sleeping: {0}'.format(e))
        logger.error(traceback.format_exc())

    try:
        if not testMode:
            oauth.refresh()
            #reddit.refresh_access_information(accessInfo['refresh_token'])
    except Exception as e:
        logger.error('Exception refreshing reddit access: {0}'.format(e))
        logger.error(traceback.format_exc())
