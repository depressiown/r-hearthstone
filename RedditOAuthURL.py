'''
Utility to get the authorization URL and code from reddit.
'''

import praw
from SidebarConfiguration import SidebarConfiguration


config = SidebarConfiguration()

r = praw.Reddit('/r/hearthstone sidebar updater')
r.set_oauth_app_info(client_id=config.getRedditOAuthClientID(),
                     client_secret=config.getRedditOAuthClientSecret(),
                     redirect_uri='http://127.0.0.1:65010/authorize_callback')

print '\nThe URL to grant access to the application (make sure to be logged in as the appropriate user):'
print r.get_authorize_url('uniqueKey', ['identity', 'modwiki', 'wikiread', 'wikiedit'], True) + '\n'

print 'After granting access to the application, copy the "code" URL parameter from the resulting URL and put this in the configuration as the "oauth_access_code".\n'
print '!!!!!!!!!!!!!!!!!!!!WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!'
print 'THIS IS A ONE-TIME USE TOKEN. EACH TIME THE PROGRAM IS'
print 'RUN, YOU MUST RE-DO THIS STEP AND RE-ENTER THE ACCESS '
print 'CODE INTO THE CONFIG.'
print '!!!!!!!!!!!!!!!!!!!!WARNING!!!!!!!!!!!!!!!!!!!!!!!!!!!'

print '\n(yes, this is a giant pain in the ass)'
