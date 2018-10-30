#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Event  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% 
CoordMode, Pixel, Screen
CoordMode, Mouse, Screen
#Persistent

;Undock()
SelectWaypoint()
;ClickOnWaypoint()
;JumpOrDockDetect()
;ItemsInInventory()
;ReturnToJita()
;AtJitaCheck

Undock() ;undock from station
	{
	;click on undocking button in station window
	Global
	Random, varyby40, 0, 40
	Random, varyby18, 0, 18
	Random, mousemove1, 5, 80
	MouseMove, varyby40+1781, varyby18+142, mousemove1
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
	;look for waypoint in overview
	Global
	Loop, 300
		{
		PixelSearch, WaypointX, WaypointY, 1162, 170, 1176, 1074, 0x033535, 12, Fast
			if ErrorLevel = 0
				{
				Gui, Destroy
				Gui, Add, Text, ,found waypoint
				Gui, Show, Y15, Msgbox
				Goto, ClickWaypointinOverview
				}
			else
				Sleep, 100
		}
		MsgBox, cant find waypoint!
	
	;click on waypoint in overview to highlight it in selection box
	ClickWaypointinOverview:
	Random, varyby250, 0, 250
	Random, varyby12, 0, 12
	Random, mousemove2, 5, 80
	MouseMove, varyby250+WaypointX, varyby12+WaypointY, mousemove2
		Random, wait200to2000milis, 200, 2000
		Sleep, wait200to2000milis
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
	Loop, 300
		{
		PixelSearch, WarpButtonX, WarpButtonY, 1214, 71, 1229, 85, 0x020202, 1, Fast
			if ErrorLevel = 0
				{
				Gui, Destroy
				Gui, Add, Text, ,found warp button
				Gui, Show, Y15, Msgbox
				Goto, Warp
				}
			else
				Sleep, 100	
		}
	
	;click on warp button
	Warp:
	Random, wait200to3000milis, 2000, 3000
	Sleep, wait200to3000milis
	
	Random, varyby12, 0, 12
	Random, varyby11, 0, 11
	Random, mousemove3, 3, 100
	MouseMove, varyby12+1215, varyby11+70, mousemove3
		Random, wait200to2000milis, 200, 2000
		Sleep, wait200to2000milis
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
							Random, wait200to500milis, 200, 500
							Sleep, wait200to500milis
					}	
				Random, wait200to2000milis, 200, 2000
				Sleep, wait200to2000milis
				
		;move mouse away from button so button can be easily seen
		Random, varyX, -300, 300
		Random, varyY, -60, 300
		Random, mousemove4, 3, 100
		MouseMove, varyX, varyY, mousemove4, R
	
	;wait a minimum period of time for warp to begin
	Random, wait2000to15000milis, 2000, 15000
	Sleep, wait2000to15000milis
	JumpOrDockDetect()
	}

JumpOrDockDetect() ;search for colors indicating either a jump has been made or ship has docked
	{
	;search for evidence of a jump
	Global
	Loop, 15000 
		{
		PixelSearch, JumpMadeX, JumpMadeY, 1174, 49, 1175, 51, 0x4c4c4c, 10, Fast
			if ErrorLevel = 0
				{
				Gui, Destroy
				Gui, Add, Text, ,jump detected
				Gui, Show, Y15, Msgbox
				ClickOnWaypoint() ;if a jump has been detected, click on the next waypoint
				}
			else
				{
				;if a jump has not been detected, search for evidence of a dock
				PixelSearch, DockMadeX, DockMadeY, 1781, 142, 1782, 143, 0x027a98, 15, Fast
					if ErrorLevel = 0
						{
						Gui, Destroy
						Gui, Add, Text, ,docking detected
						Gui, Show, Y15, Msgbox	
						ItemsInInventory() ;if a dock has been detected, place items in inventory
						}
					else
						Sleep, 100	
				}
		}
		
	;if cannot detect jump or dock after timer expires, look for waypoint again with a larger search area
	Loop, 3
		{
		Loop, 300
			{
			PixelSearch, WaypointX, WaypointY, 1100, 50, 1300, 1080, 0x033535, 16, Fast
				if ErrorLevel = 0
					{
					Gui, Destroy
					Gui, Add, Text, ,found waypoint
					Gui, Show, Y15, Msgbox
					Goto, ClickWaypointinOverviewBackup
					}
				else
					Sleep, 10
			}
		MsgBox, cant find waypoint!
	
		;click on waypoint in overview to highlight it in selection box
		ClickWaypointinOverviewBackup:
		Random, varyby250, 0, 250
		Random, varyby12, 0, 12
		Random, mousemove12, 5, 80
		MouseMove, varyby250+WaypointX, varyby12+WaypointY, mousemove12
			Random, wait200to2000milis, 200, 2000
			Sleep, wait200to2000milis
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
		
		Loop, 300
			{
			PixelSearch, WarpButtonX, WarpButtonY, 1214, 71, 1229, 85, 0x020202, 1, Fast
				if ErrorLevel = 0
					{
					Gui, Destroy
					Gui, Add, Text, ,found warp button
					Gui, Show, Y15, Msgbox
					Goto, WarpBackup
					}
				else
					Sleep, 100	
			}
	
			;click on warp button
			WarpBackup:
			Random, wait200to3000milis, 2000, 3000
			Sleep, wait200to3000milis

			Random, varyby12, 0, 12
			Random, varyby11, 0, 11
			Random, mousemove13, 3, 100
			MouseMove, varyby12+1215, varyby11+70, mousemove13
				Random, wait200to2000milis, 200, 2000
				Sleep, wait200to2000milis
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
									Random, wait200to500milis, 200, 500
									Sleep, wait200to500milis
							}	
						Random, wait200to2000milis, 200, 2000
						Sleep, wait200to2000milis

			;move mouse away from button so button can be easily seen
			Random, varyX, -300, 300
			Random, varyY, -60, 300
			Random, mousemove14, 3, 100
			MouseMove, varyX, varyY, mousemove14, R

			;wait a minimum period of time for warp to begin
			Random, wait2000to15000milis, 2000, 15000
			Sleep, wait2000to15000milis
			JumpOrDockDetect()
		}
	Msgbox, cant find dock or jump!
	}
		
ItemsInInventory() ;move items from station hangar to ship cargo bay
	{
	;first, check if ship has reached jita
	Global
	AtJitaCheck()
	
	Random, wait2000to5000milis, 2000, 5000
	Sleep, wait2000to5000milis	
	
	;focus inventory window
	Random, varyby10, 0, 10
	Random, varyby200, 0, 200
	Random, mousemove9, 5, 80
	MouseMove, varyby10+648, varyby200+82, mousemove9
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, wait200to500milis, 200, 500
				Sleep, wait200to500milis+500
	
	;use hotkey to open station inventory in station
	SendMode Input
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
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis
	SendMode Event
	
	;check to see if any items are present in station hangar inventory
	Loop, 300 
		{
		PixelSearch, StationItemsX, StationItemsY, 550, 145, 1500, 180, 0x939393, 2, Fast
			if ErrorLevel = 0
				{
				Gui, Destroy
				Gui, Add, Text, ,items in station detected
				Gui, Show, Y15, Msgbox
				Goto, SelectInventory
				}
			else
				Sleep, 100	
		}
	
	;if no items are present in station inventory, undock and continue
	Gui, Destroy
	Gui, Add, Text, ,station empty
	Gui, Show, Y15, Msgbox
	Undock() 
	
	;right click on left edge of inventory screen and use drop-down menu to select all items in station hangar inventory
	SelectInventory:
	Random, varyby10, 0, 10
	Random, varyby200, 0, 200
	Random, mousemove10, 5, 80
	MouseMove, varyby10+648, varyby200+82, mousemove10
		Random, wait200to2000milis, 200, 2000
		Sleep, wait200to2000milis
			Click, down, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up, right

	;click on 'select all'
	Random, varyby90, 0, 90
	Random, varyby10, 3, 10
	Random, mousemove11, 5, 80
	MouseMove, varyby90, varyby10, mousemove11, R 
		Random, wait200to1000milis, 200, 1000
		Sleep, wait200to1000milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, wait200to1000milis, 200, 1000
				Sleep, wait200to1000milis

	;click and drag items to ship inventory
	Random, varyby50, 0, 50
	Random, varyby60, 0, 60
	Random, mousemove12, 5, 100
	MouseMove, varyby50+663, varyby60+81, mousemove12
		Random, wait200to1000milis, 200, 1000
		Sleep, wait200to1000milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
					Random, varyby28, 0, 28
					Random, varyby18, 0, 18	
					Random, mousemove13, 5, 100			
					MouseMove, varyby28+614, varyby18+46, mousemove13		
			Click, up
				Random, wait1000to5000milis, 1000, 5000
				Sleep, wait1000to5000milis
		
		;check to see if 'not enough cargo space' alert appears	
		Loop, 10 
			{
			PixelSearch, ShipFullX, ShipFullY, 791, 436, 793, 438, 0xCACACA, 3, Fast
				if ErrorLevel = 0
					{
					;if alert appears, return to Jita and stop script
					;hit enter key
					Send {ENTER down}
						Random, wait20to200milis, 20, 200
						Sleep, wait20to200milis
					Send {Enter up}
					
					;set destination to Jita 4-4
					Gui, Destroy
					Gui, Add, Text, ,detected full cargo hold
					Gui, Show, Y15, Msgbox
					ReturnToJita()
					}
				else
					Sleep, 10	
			}
		
	;close station inventory with hotkey	
	SendMode Input
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
	SendMode Event
	
	;undock from station
	Random, wait1000to5000milis, 1000, 5000
	Sleep, wait1000to5000milis
	Undock()
	}

ReturnToJita() ;open 'people & places' menu and set Jita 4-4 as destination
	{
	Global
	
	/*
	;click on 'people and places' icon
	Random, varyby25, 0, 25
	Random, varyby24, 0, 24
	Random, mousemove5, 5, 80
	MouseMove, varyby25+3, varyby24+137, mousemove5
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
	*/
	
	;right click on first entry in 'personal locations'
	Random, varyby500, 0, 500
	Random, varyby16, 0, 16
	Random, mousemove6, 5, 100
	MouseMove, varyby500+42, varyby16+547, mousemove6
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
				
	;click on 'set destination' in drop-down menu
	Random, varyby50, 0, 50
	Random, varyby12, 0, 12
	Random, mousemove7, 5, 80
	MouseMove, varyby50+10, varyby12+23, mousemove7, R
		Random, wait200to1000milis, 200, 1000
		Sleep, wait200to1000milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up	
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
	
	/*	
	;close 'people and places' window
	Random, varyby5, 0, 5
	Random, varyby6, 0, 6
	Random, mousemove8, 5, 80
	MouseMove, varyby5+580, varyby6+4, mousemove8
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up	
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis	
					Undock()
	*/
	
	}
			
AtJitaCheck() ;check the 'people & places' menu for color change to determine if ship has arrived at Jita 4-4	
	{
	;check if Jita entry in 'people & places' menu has turned green, indicating it is the current system
	Global
	Loop, 3
		{
		PixelSearch, AtJitaX, AtJitaY, 76, 550, 95, 561, 0x53a553, 11, Fast
			if ErrorLevel = 0
				{
				Gui, Destroy
				Gui, Add, Text, ,arrived at Jita system
				Gui, Show, Y15, Msgbox
				ExitApp 
				}
			else
				Sleep, 100	
		}
	Return
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
