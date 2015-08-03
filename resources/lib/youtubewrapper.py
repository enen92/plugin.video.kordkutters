#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
 Author: enen92 

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
"""
import urllib
import json
import re
import os
import sys
import math
from common_variables import *
from directory import *

#get list of playlists
def get_playlists():
	url = 'https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId='+channel_id+'&maxResults=50&key='+youtube_api_key
	raw = urllib.urlopen(url)
	resp = json.load(raw)
	raw.close()
	totalplaylists = len(resp["items"])
	for playlist in resp["items"]:
		playlist_id = playlist["id"]
		thumb = playlist["snippet"]["thumbnails"]["high"]["url"]
		label = playlist["snippet"]["title"]
		addDir('[B]'+label+'[/B]',playlist_id,1,thumb,1,totalplaylists,token='')
	return

#get list of live videos
def get_live_videos():
	url = 'https://www.googleapis.com/youtube/v3/search?eventType=live&part=snippet&channelId='+channel_id+'&type=video&maxResults=50&key='+youtube_api_key
	raw = urllib.urlopen(url)
	resp = json.load(raw)
	raw.close()
	if resp["items"]:
		totallive = len(resp["items"])
		for item in resp["items"]:
			title = item["snippet"]["title"]
			plot = item["snippet"]["description"]
			thumb = item["snippet"]["thumbnails"]["high"]["url"]
			videoid = item["id"]["videoId"]
			episode = re.findall('(\d+)',title)
			infolabels = {'plot':plot,'tvshowtitle':'KordKutters','title':title,'originaltitle':title,'status':'Continuing','cast':('Nathan Betzen','Ned Scott'),'castandrole':('Nathan Betzen','Ned Scott'),'episode':episode,'playcount':0}
			if totallive >= 1:
				addEpisode(title,videoid,5,thumb,1,totallive,infolabels,folder=False)
				xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
	else:
		msgok(translate(30000),translate(30002))
		sys.exit(0)

#Get list of offline videos
def return_youtubevideos(name,url,token,page):
	items_per_page = int(selfAddon.getSetting('items_per_page'))

	if page != 1:
		url_api = 'https://www.googleapis.com/youtube/v3/playlistItems?part=id,snippet,contentDetails&maxResults='+str(items_per_page)+'&playlistId='+url+'&key='+youtube_api_key +'&pageToken='+token
	else:
		url_api = 'https://www.googleapis.com/youtube/v3/playlistItems?part=id,snippet,contentDetails&maxResults='+str(items_per_page)+'&playlistId='+url+'&key='+youtube_api_key 
	
	raw = urllib.urlopen(url_api)
	resp = json.load(raw)
	raw.close()
	try: nextpagetoken = resp["nextPageToken"]
	except: nextpagetoken = ''
	try: availablevideos = resp["pageInfo"]["totalResults"]
	except: availablevideos = 1
	returnedVideos = resp["items"]
	totalvideos = len(returnedVideos)
	totalpages = int(math.ceil((float(availablevideos)/items_per_page)))
	for video in returnedVideos:
		title = video["snippet"]["title"]
		plot = video["snippet"]["description"]
		aired = video["snippet"]["publishedAt"]
		thumb = video["snippet"]["thumbnails"]["high"]["url"]
		videoid = video["contentDetails"]["videoId"]
		try: 
			date = re.compile('(.+?)-(.+?)-(.+?)T').findall(aired)[0]
			date = date[0]+'-'+date[1]+'-'+date[2]
		except: date = ''
		try:
			if 'episode' in title.lower() or '#' in title.lower() or re.findall('KordKutters (\d+)\:',title.lower()):
				episode = re.compile('(\d+)').findall(title)[0]
			else: episode = ''
		except: episode = ''
		if os.path.exists(os.path.join(watchedfolder,str(videoid)+'.txt')) : playcount = 1
		else: playcount = 0
		
		infolabels = {'plot':plot,'aired':date,'tvshowtitle':'KordKutters','title':title,'originaltitle':title,'status':'Continuing','cast':('Nathan Betzen','Ned Scott'),'castandrole':('Nathan Betzen','Ned Scott'),'episode':episode,'playcount':playcount}
		
		addEpisode(title,videoid,5,thumb,page,totalvideos,infolabels,folder=False)
	
	if totalpages > 1 and (page+1) <= totalpages:
		addDir('[B]'+translate(30010)+'[/B] '+str(page)+'/'+str(totalpages),url,1,os.path.join(artfolder,'next.png'),page+1,1,token=nextpagetoken)
	xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
	return

#Play a youtube video given the video_id	
def play_youtube_video(url):
	video_url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid='+url
	item = xbmcgui.ListItem(path=video_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	player = KKPlayer(mainurl=url)
	player.play(video_url,item)
	while player._playbackLock:
		player._trackPosition()
		xbmc.sleep(1000)
	return

