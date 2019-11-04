import os
import urllib
import webapp2
import httplib2
from datetime import date,datetime,timedelta
httplib2.debuglevel = 4

from apiclient.discovery import build
from optparse import OptionParser

# Set DEVELOPER_KEY to the "API key" value from the "Access" tab of the
# Google APIs Console http://code.google.com/apis/console#access
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCLVBSJD0Zf6XwaVXtRbeapro7xPtvBkgc"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

class MainHandler(webapp2.RequestHandler):
  def get(self):
      hoy = datetime.utcnow()
      hoy = hoy -timedelta(days=1)
      hoy = hoy.isoformat("T") + "Z"

      youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY,
      )
      search_response = youtube.search().list(
        q="uruguay",
        part="id,snippet",
        maxResults=5,
        publishedAfter=hoy,
        regionCode="UY",
        order="rating",
      ).execute()
      
      videos = []
      channels = []
      playlists = []
      
      for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"], 
              search_result["id"]["videoId"]))
        elif search_result["id"]["kind"] == "youtube#channel":
            channels.append("%s (%s)" % (search_result["snippet"]["title"], 
              search_result["id"]["channelId"]))
        elif search_result["id"]["kind"] == "youtube#playlist":
            playlists.append("%s (%s)" % (search_result["snippet"]["title"], 
              search_result["id"]["playlistId"]))
    
      template_values = {
       'videos': videos,
       'channels': channels,
       'playlists': playlists
      }
      v = []
      for i in videos:
        a = i.split()
        a = a[-1]
        a = a.replace("(","").replace(")","")
        #a = "http://www.youtube.com/embed/" + a 
        v.append(a)
      print v
      return v
        