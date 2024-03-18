#!/usr/bin/env python3

import ctypes
import sys
import requests
import time
import tkinter
from playsound import playsound

MOCK = False
sfp = 'Flash.mp3'

if MOCK:
	GAMESTATE_URL = 'https://static.developer.riotgames.com/docs/lol/liveclientdata_sample.json'
else:
	GAMESTATE_URL = 'https://127.0.0.1:2999/liveclientdata/allgamedata'

def get_gamestate():
	try:
                ret = requests.get(GAMESTATE_URL, verify=False)
	except Exception as e:
		print(e)
		return None
	if ret.status_code != 200:
		return None
	js = ret.json()

	return js

def press_keys(*keys):
    for key in keys:
        ctypes.windll.user32.keybd_event(key, 0, 0, 0)  # Press key
    time.sleep(0.1)  # Add a short delay to ensure the keys are pressed in order
    for key in keys:
        ctypes.windll.user32.keybd_event(key, 0, 2, 0)  # Release key

def main(args):
	done = False
	kills = 0 if not MOCK else -1
	assists = 0

	while not done:
		gs = get_gamestate()
		if gs is None:
			print('Failed to query gamestate')
			continue

		summoner_name = gs['activePlayer']['summonerName']
		summoner_name = summoner_name[0:summoner_name.rfind('#')]
		#print(summoner_name,gs['allPlayers'])
		
		[ summoner_stats ] = list(filter(lambda p: p['summonerName'] == summoner_name, gs['allPlayers']))
		#print(summoner_name, summoner_stats)

		if summoner_stats['scores']['kills'] > kills:
			kills = summoner_stats['scores']['kills']
			#playsound(sfp)
                        
                        #every 4 kills strobe 
			'''if summoner_stats['scores']['kills'] %4 == 0:
				flash(0.05)
				time.sleep(0.05)
				flash(0.05)
				time.sleep(0.05)
				flash(0.05)
				time.sleep(0.05)'''
			
			#every 4 kills invert my colors	
			'''if summoner_stats['scores']['creepScore']%10 == 0:
                                                        #inver the colors
				VK_LWIN = 0x5B          #windows key press
				VK_CONTROL = 0x11       #control key pressed 
				VK_C = 0x43             #c key pressed
				press_keys(VK_LWIN, VK_CONTROL, VK_C) #press all at once'''
                                
			#print['creepScore']
			flash(1)
			


		if summoner_stats['scores']['assists'] > assists:
			flash(1)
		assists = summoner_stats['scores']['assists']
		

		#if MOCK:
			#done = True
		time.sleep(1)
		
		
	return 0

def flash(t):
	win = tkinter.Tk()
	win.title('FLASHBANG!')
	win.attributes('-fullscreen', True)
	win.attributes('-topmost', True)
	win.configure(bg='white')
	win.after(t * 1000, win.destroy)
	win.mainloop()



if __name__ == '__main__':
	sys.exit(main(sys.argv))

