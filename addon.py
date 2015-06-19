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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,xbmcvfs
import os,sys
from resources.lib.common_variables import *
from resources.lib.directory import *
from resources.lib.getvideolist import *
from resources.lib.watched import * 
from resources.lib.kkplayer import *


def main_menu():
	if selfAddon.getSetting('navigate_toall') == 'true':
		return_youtubevideos(1,"","all")
	else:
		addDir('[B]'+translate(30001)+'[/B]','',1, '',1,1)
		addDir('[B]'+translate(30002)+'[/B]','',2, '',1,1)
		addDir('[B]'+translate(30003)+'[/B]','',3, '',1,1)	
	
"""

Addon navigation is below
 
"""	
			
            
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


params=get_params()
url=None
name=None
mode=None
iconimage=None
page = None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except:
	try: 
		mode=params["mode"]
	except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: page=int(params["page"])
except: page = 1

print ("Mode: "+str(mode))
print ("URL: "+str(url))
print ("Name: "+str(name))
print ("iconimage: "+str(iconimage))
print ("Page: "+str(page))


if mode==None: main_menu()
elif mode==1: return_youtubevideos(page,url,"all")
elif mode==2: return_youtubevideos(page,url,"episodes")
elif mode==3: return_youtubevideos(page,url,"howto")
elif mode==5: 
	video_url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid='+url
	item = xbmcgui.ListItem(path=video_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	player = KKPlayer(mainurl=url)
	player.play(video_url,item)
	while player._playbackLock:
		player._trackPosition()
		xbmc.sleep(1000)
elif mode==6: mark_as_watched(url)
elif mode==7: removed_watched(url)
elif mode==8: add_to_bookmarks(url)
elif mode==9: remove_from_bookmarks(url)
	
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
