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
import xbmc,xbmcgui,xbmcaddon,xbmcvfs,os

addon_id = 'plugin.video.kordkutters'

selfAddon = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile')).decode('utf-8')
addonfolder = xbmc.translatePath(selfAddon.getAddonInfo('path')).decode('utf-8')
artfolder = os.path.join(addonfolder,'resources','img')
watchedfolder = os.path.join(datapath,'watched')

msgok = xbmcgui.Dialog().ok

def makefolders():
	if not os.path.exists(datapath): xbmcvfs.mkdir(datapath)
	if not os.path.exists(watchedfolder):xbmcvfs.mkdir(watchedfolder)
	return


def translate(text):
	return selfAddon.getLocalizedString(text).encode('utf-8')
