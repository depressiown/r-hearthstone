'''
Calendar API accessor for /r/hearthstone.

This will hit the Google Calendar and be able to format the response in whatever form
of Markdown that we'd like.
'''

import calendar
import time
import requests
import string
import yaml


class HearthstoneCalendar:

    def __init__(self, config):

        self.id = config.getCalendarID()
        self.key = config.getCalendarKey()

    def __getUpcomingEvents(self):

        print 'Fetching calendar (' + self.id + ') from Google API...'
        googleCalendar = requests.get(
            "https://www.googleapis.com/calendar/v3/calendars/" + self.id + "/events",
            params={
                "maxResults": 5,
                "orderBy": "startTime",
                "singleEvents": "true",
                "fields": "items(location,start,summary,description),summary",
                "timeMin": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "key": self.key
            })

        for item in googleCalendar.json()["items"]:
            yield item

    def __formatTimestamp(self, event):

        current_time = time.time()
        event_time = calendar.timegm(time.strptime(event["start"]["dateTime"], "%Y-%m-%dT%H:%M:%SZ"))

        if current_time >= event_time - 60:
            return "LIVE"
        else:
            def format_segment(number, suffix=""):
                return "%d%s" % (number, suffix) if number else ""

            time_diff = event_time - current_time
            days = time_diff // 86400
            hours = (time_diff % 86400) // 3600
            minutes = (time_diff % 3600) // 60

            return " ".join([format_segment(days, "d"), format_segment(hours, "h"), format_segment(minutes, "m")]).strip()

    def __formatEventURL(self, event, event_type, timestamp):

        event_url = ""
        if "location" in event:
            event_url = event["location"]

        event_url += "#upcoming"

        if timestamp == "LIVE":
            event_url += "#live"

        event_url += "#" + event_type

        return event_url

    def __formatEvent(self, event):

        properties = {}

        timestamp = self.__formatTimestamp(event)

        if "description" in event:
            try:
                properties = yaml.safe_load(event["description"])
                if type(properties) != dict:
                    properties = {}
                    print "YAML ERROR: description is not a dictionary"
            except yaml.YAMLError as e:
                print "YAML ERROR: {0}".format(e)
            except Exception as e:
                print "ERROR: {0}".format(e)

        # Show the icon depending on the type of the event
        eventType = properties.get("type", "show")

        # Tagline
        eventDescription = "&nbsp;"
        if "description" in properties:
            eventDescription = properties["description"]

        title = event["summary"].rstrip().lstrip()
        description = eventDescription.rstrip().lstrip()
        charactersToEscape = [']', '[', '~']
        for characterToEscape in charactersToEscape:
            title = string.replace(title, characterToEscape, '\\' + characterToEscape)
            description = string.replace(description, characterToEscape, '\\' + characterToEscape)

        markdown = "[~~{}~~\n~~{}~~\n~~{}~~]({})".format(
            title,
            timestamp,
            description,
            self.__formatEventURL(event, eventType, timestamp))

        return markdown

    def getCalendarMarkdown(self):

        markdown = ''
        for event in self.__getUpcomingEvents():
            markdown += self.__formatEvent(event) + '\n\n'

        print '\n---------- CALENDAR MARKDOWN ----------'
        print markdown
        print '---------------------------------------\n'

        return markdown
