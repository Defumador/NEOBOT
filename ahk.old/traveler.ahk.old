#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Event  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% 


CoordMode, Pixel, Screen
CoordMode, Mouse, Screen
#Persistent

SelectWaypoint()

Undock() ;undock from station
	{
	;click on undocking button in station window
	Global
	Random, varyby40, 0, 40
	Random, varyby18, 0, 18
	Random, mousemove, 5, 80
	MouseMove, varyby40+1781, varyby18+142, mousemove
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
	
	;wait until undocking finishes
	Random, wait5to10s, 5000, 10000
	Sleep, wait5to10s+5000
	SelectWaypoint()
	}


SelectWaypoint() ;click on yellow-tinted icon in overview to select next waypoint
	{ 
	;look for waypoint color in overview
	Global
	Loop, 300
		{
		PixelSearch, WaypointX, WaypointY, 1164, 163, 1177, 1074, 0x098383, 8, Fast
			if ErrorLevel = 0
				{
				;MsgBox, foundwaypoint
				Goto, ClickWaypointinOverview
				}
			else
				Sleep, 1000	
		}
		MsgBox, cant find waypoint!
	
	;click on waypoint in overview to highlight it in selection box
	ClickWaypointinOverview:
	Random, varyby250, 0, 250
	Random, varyby12, 0, 12
	Random, mousemove, 5, 80
	MouseMove, varyby250+WaypointX, varyby12+WaypointY, mousemove
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, DoubleClickRoll, 1, 20 ;chance to double-click
				if DoubleClickRoll = 1
					{
					Random, wait90to250milis, 90, 250
					Sleep, wait90to250milis
						Click, down
							Random, wait5to200milis, 5, 200
							Sleep, wait5to200milis
						Click, up
					}	
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
	ClickOnWaypoint()
	}
	
ClickOnWaypoint() ;click on warp button in selection box to warp to waypoint
	{
	;double-check warp button is present		
	Global
	Loop, 10
	{
	PixelSearch, WarpButtonX, WarpButtonY, 1214, 71, 1229, 85, 0x020202, 1, Fast
		if ErrorLevel = 0
			{
			;Msgbox, found jump!
			Goto, Warp ;if a jump has been detected, look for the next waypoint
			}
		else
			Sleep, 1000	
	}
	
	;warp
	Warp:
	Random, wait2000to5000milis, 2000, 5000
	Sleep, wait2000to5000milis
	
	Random, varyby12, 0, 12
	Random, varyby11, 0, 11
	Random, mousemove, 5, 80
	MouseMove, varyby12+1215, varyby11+70, mousemove
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, DoubleClickRoll, 1, 20 ;chance to double-click
				if DoubleClickRoll = 1
					{
					Random, wait90to250milis, 90, 250
					Sleep, wait90to250milis
						Click, down
							Random, wait5to200milis, 5, 200
							Sleep, wait5to200milis
						Click, up
					}	
		;move mouse away from button so color can be easily seen
		Random, varyby300, 0, 300
		Random, varyby301, 0, 301
		Random, mousemove, 3, 80
		MouseMove, varyby100, varyby101, mousemove, R
		
	Random, wait2000to10000milis, 2000, 10000
	Sleep, wait2000to10000milis
	JumpDock()
	}

JumpDock() ;search for colors indicating either a jump has been made or ship has docked
	{
	Global
		;search for evidence of a jump
		Loop, 5000 
		{
		PixelSearch, JumpMadeX, JumpMadeY, 1215, 78, 1227, 78, 0x020202, 1, Fast
			if ErrorLevel = 0
				{
				;Msgbox, found jump!
				ClickOnWaypoint() ;if a jump has been detected, look for the next waypoint
				}
			else
				Sleep, 200	
		}
		MsgBox, cant find evidence of a jump!

		;search for evidence of a dock
		Loop, 300
		{
		PixelSearch, DockMadeX, DockMadeY, 1780, 141, 1794, 147, 0x007997, 5, Fast
			if ErrorLevel = 0
				ItemsInInventory() ;if a dock has been detected, place items in inventory
			else
				Sleep, 1000	
		}
		MsgBox, cant find evidence of a dock!
	}	
		
ItemsInInventory() ;move items from station hangar to ship cargo bay
	{
	Global
	Random, wait2000to5000milis, 2000, 5000
	Sleep, wait2000to5000milis+5000	
	
	Send {Alt down} ;hotkey to open station inventory in station
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {G down}
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {G up}
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {Alt up}
			
	
	;check to see if items are actually present in station inventory
	Loop, 300 
	{
	PixelSearch, StationItemsX, StationItemsY, 550, 145, 1500, 180, 0x939393, 12, Fast
		if ErrorLevel = 0
			{
			;Msgbox, found items!
			Goto, SelectInventory
			}
		else
			Sleep, 100	
	}
	Undock() ;if no items are present in station inventory, undock
	
	;right click on left edge of inventory screen to select all
	SelectInventory:
	Random, varyby10, 0, 10
	Random, varyby200, 0, 200
	Random, mousemove, 5, 80
	MouseMove, varyby10+648, varyby200+82, mousemove
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up, right

	;click on 'select all'
	Random, varyby90, 0, 90
	Random, varyby10, 0, 10
	Random, mousemove, 5, 80
	MouseMove, varyby90, varyby10, mousemove, R 
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up

	;click and drag items to ship inventory
	Random, wait200to500milis, 200, 500
	Sleep, wait200to500milis+500
	Random, varyby50, 0, 50
	Random, varyby60, 0, 60
	Random, mousemove, 5, 80
	MouseMove, varyby50+663, varyby60+81, mousemove
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
				Random, varyby38, 0, 38
				Random, varyby18, 0, 18	
				Random, mousemove, 5, 80				
				MouseMove, varyby38+611, varyby18+46, mousemove			
			Click, up
			Random, wait2000to5000milis, 2000, 5000
			Sleep, wait2000to5000milis+500	
		
		;check to see if 'not enough cargo space' alert appears	
		Loop, 10 
		{
		PixelSearch, ShipFullX, ShipFullY, 791, 436, 793, 438, 0xCACACA, 3, Fast
			if ErrorLevel = 0
				{
				;if alert appears, return to Jita
				ReturnToJita()
				}
			else
				Sleep, 100	
		}
		
	;close station inventory	
	Send {Alt down} 
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {G down}
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {G up}
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {Alt up}

	Random, wait2000to5000milis, 2000, 5000
	Sleep, wait2000to5000milis+500	
	}

ReturnToJita() ;open 'people & places' menu and set Jita 4-4 as destination
	{
	;click on 'people and places' icon
	Global
	Random, varyby27, 0, 27
	Random, varyby26, 0, 26
	Random, mousemove, 5, 80
	MouseMove, varyby27+3, varyby26+137, mousemove
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
	
	;right click on first entry in 'personal locations'
	Random, varyby500, 0, 500
	Random, varyby16, 0, 26
	Random, mousemove, 5, 80
	MouseMove, varyby500+38, varyby16+147, mousemove
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
				
	;click on 'set destination'
	Random, varyby500, 0, 500
	Random, varyby12, 0, 12
	Random, mousemove, 5, 80
	MouseMove, varyby500+10, varyby12+23, mousemove, R
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up	
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
				
	;close 'people and places' window
	Random, varyby5, 0, 5
	Random, varyby6, 0, 6
	Random, mousemove, 5, 80
	MouseMove, varyby5+580, varyby6+4, mousemove
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up	
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis	
					Undock()
	}
			
	
	
	
MsgBox, end of script
ExitApp	
	
shift:: ;manual kill switch
	{
	Gui, Destroy
	ExitApp
	}	

z:: ;show logs
	{
	Gui, Destroy
	ListLines
	Pause
	}
