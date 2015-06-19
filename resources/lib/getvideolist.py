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

from directory import *
import urllib, json,re,os

def return_youtubevideos(page,token,mode):

	items_per_page = int(selfAddon.getSetting('items_per_page'))

	if page != 1:
		url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=id,snippet,contentDetails&maxResults='+str(items_per_page)+'&playlistId=UUtp9s4L-kxIRy221VVtgjXg&key=AIzaSyAxaHJTQ5zgh86wk7geOwm-y0YyNMcEkSc&pageToken='+token
	else:
		url = 'https://www.googleapis.com/youtube/v3/playlistItems?part=id,snippet,contentDetails&maxResults='+str(items_per_page)+'&playlistId=UUtp9s4L-kxIRy221VVtgjXg&key=AIzaSyAxaHJTQ5zgh86wk7geOwm-y0YyNMcEkSc'
	raw = urllib.urlopen(url)
	resp = json.load(raw)
	raw.close()
	try: nextpagetoken = resp["nextPageToken"]
	except: nextpagetoken = ''
	try: availablevideos = resp["pageInfo"]["totalResults"]
	except: availablevideos = 1
	returnedVideos = resp["items"]
	totalvideos = len(returnedVideos)
	totalpages = int((float(availablevideos)/items_per_page))
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
			if 'episode' in title.lower() or '#' in title.lower():
				episode = re.compile('(\d+)').findall(title)[0]
			else: episode = ''
		except: episode = ''
		if os.path.exists(os.path.join(watchedfolder,str(videoid)+'.txt')) : playcount = 1
		else: playcount = 0
		
		infolabels = {'plot':plot,'aired':date,'tvshowtitle':'KordKutters','title':title,'originaltitle':title,'status':'Continuing','cast':('Nathan Betzen','Ned Scott'),'castandrole':('Nathan Betzen','Ned Scott'),'episode':episode,'playcount':playcount}
		
		
		if mode == 'all':
			addEpisode(title,videoid,5,thumb,page,totalvideos,infolabels,folder=False)
		elif mode == 'episodes':
			if 'episode' in title.lower() or '#' in title.lower():
				addEpisode(title,videoid,5,thumb,page,totalvideos,infolabels,folder=False)
		elif mode == 'howto':
			if 'episode' not in title.lower() and '#' not in title.lower():
				addEpisode(title,videoid,5,thumb,page,totalvideos,infolabels,folder=False)
	#check if more pages do exist
	if mode == 'all': mode = 1
	elif mode == 'episodes': mode = 2
	elif mode == 'howto': mode = 3
	
	
	if totalpages > 1 and (page+1) <= totalpages:
		addDir('[B]'+translate(30010)+'[/B] '+str(page)+'/'+str(totalpages),nextpagetoken,mode, '',page+1,1)
	xbmcplugin.setContent(int(sys.argv[1]), 'episodes')

