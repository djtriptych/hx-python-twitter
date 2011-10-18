#!/usr/bin/env python

import urllib
import urllib2

try:
   import json
except ImportError:
   import simplejson as json


class TwitterApiMethod(object):
   def __init__(self, api):
      self.api = api

   def __call__(self, params):
      url = self.url
      if self.method == 'get':
         url += '?' + urllib.urlencode(params)
         response = urllib2.urlopen(url)
      elif self.method == 'post':
         response = urllib2.urlopen(url, params)

      return response

   @property
   def url(self):
      url = 'http://api.twitter.com/%(version)s/%(method)s.%(format)s'
      api_params = {
         'version': self.api.version,
         'format': self.api.format,
      }
      params = {'method':self.name}
      params.update(api_params)
      return url % params


class StatusesPublicTimeline(TwitterApiMethod):
   name = 'statuses/public_timeline'
   formats = 'json, xml, rss, atom'
   method = 'get'
   requires_auth = False
   rate_limited = True

   params = [
      'trim_user', 
      'include_entities',
   ]


class StatusesHomeTimeline(TwitterApiMethod):
   name = 'statuses/home_timeline'
   formats = 'json, xml, rss, atom'
   method = 'get'
   requires_auth = True
   rate_limited = True

   params = [
      'since_id',
      'max_id',
      'count',
      'page', 
      'trim_user', 
      'include_entities',
   ]


class StatusesFriendsTimeline(TwitterApiMethod):
   name = 'statuses/friends_timeline'
   formats = 'json, xml, rss, atom'
   method = 'get'
   requires_auth = True
   rate_limited = True

   params = [
      'since_id',
      'max_id',
      'count',
      'page', 
      'trim_user', 
      'include_rts',
      'include_entities',
   ]


class StatusesUserTimeline(TwitterApiMethod):
   name = 'statuses/user_timeline'
   formats = 'json, xml, rss, atom'
   method = 'get'
   requires_auth = False
   rate_limited = True

   params = [
      'user_id',
      'screen_name', 
      'since_id', 
      'max_id', 
      'count', 
      'page', 
      'trim_user',
      'include_rts', 
      'include_entities'
   ]


class StatusesMentions(TwitterApiMethod):
   name = 'statuses/mentions'
   formats = 'json, xml, rss, atom'
   method = 'get'
   requires_auth = True
   rate_limited = True

   params = [
      'since_id',
      'max_id',
      'count',
      'page', 
      'trim_user', 
      'include_rts',
      'include_entities',
   ]


class StatusesRetweetedByMe(TwitterApiMethod):
   name = 'statuses/retweeted_by_me'
   formats = 'json, xml, atom'
   method = 'get'
   requires_auth = True
   rate_limited = True

   params = [
      'since_id',
      'max_id',
      'count',
      'page', 
      'trim_user', 
      'include_entities',
   ]


class StatusesRetweetedToMe(TwitterApiMethod):
   name = 'statuses/retweeted_to_me'
   formats = 'json, xml, atom'
   method = 'get'
   requires_auth = True
   rate_limited = True

   params = [
      'since_id',
      'max_id',
      'count',
      'page', 
      'trim_user', 
      'include_entities',
   ]


class StatusesRetweetsOfMe(TwitterApiMethod):
   name = 'statuses/retweets_of_me'
   formats = 'json, xml, atom'
   method = 'get'
   requires_auth = True
   rate_limited = True

   params = [
      'since_id',
      'max_id',
      'count',
      'page', 
      'trim_user', 
      'include_entities',
   ]


class TwitterApi(object):
   methods = [
      StatusesPublicTimeline, 
      StatusesHomeTimeline, 
      StatusesFriendsTimeline, 
      StatusesUserTimeline, 
      StatusesMentions, 
      StatusesRetweetedByMe,
      StatusesRetweetedToMe, 
      StatusesRetweetsOfMe
   ]

   formats = {
      'application/json': 'json',
      'application/rss+xml': 'rss',
      'text/xml': 'xml',
      'application/atom+xml': 'atom',
   }

   def __init__(self, version='1', format='json'):
      self.version = version
      self.format = format
      self.methods = dict((m.name, m) for m in self.methods)

   def __call__(self, method):
      if method not in self.methods:
         return None
      return self.methods[method](api=self)


if __name__ == '__main__':
   api = TwitterApi(version='1', format='json')

   statuses = api('statuses/public_timeline')({
      'trim_user': '1',
      'include_entities': 't',
   })

