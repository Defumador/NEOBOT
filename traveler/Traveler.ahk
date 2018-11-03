;;known bugs
;setting destination from home station to second entry in people and places sometimes doesn't open the right click menu

;add method for confirming a new destination has been set by pielsearching for a red/yellow/green square in the 'route' gui

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
#Warn  ; Enable warnings to assist with detecting common errors.
SendMode Event  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir% 
CoordMode, Pixel, Screen
CoordMode, Mouse, Screen
#Persistent

version = 0.01 ;variable declaration
DockedCount := 0

;Undock()
;SelectWaypoint()
;ClickOnWaypoint()
;JumpOrDockDetect()
;ItemsInInventory()
;ReturnHome()
;AtHomeCheck()
ShowGUI()

Undock() ;undock from station
	{
	;click on undocking button in station window
	Global
	Random, varyby40, 0, 40
	Random, varyby18, 0, 18
	Random, mousemove1, 5, 80
	MouseMove, varyby40+1781, varyby18+142, mousemove1 ;undock button in station sidebar
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
	
	;wait until undocking finishes
	Guicontrol, Text, Debugger, undocking
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
		PixelSearch, WaypointX, WaypointY, 1162, 170, 1176, 1074, 0x033535, 12, Fast ;overview icons
			if ErrorLevel = 0
				{
				Guicontrol, Text, Debugger, found waypoint
				Goto, ClickWaypointinOverview
				}
			else
				Sleep, 100
		}
		Guicontrol, Text, Debugger, found waypoint
	
	;click on waypoint in overview to highlight it in selection box
	ClickWaypointinOverview:
	Random, varyby250, 0, 250
	Random, varyby12, 0, 12
	Random, mousemove2, 5, 80
	MouseMove, varyby250+WaypointX, varyby12+WaypointY, mousemove2 ;waypoint icon in overview
		Random, wait200to2000milis, 200, 2000
		Sleep, wait200to2000milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, DoubleClickRoll, 1, 20 ;chance to double-click
				if DoubleClickRoll = 1
					{
					Random, wait20to250milis, 20, 250
					Sleep, wait20to250milis
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
		PixelSearch, WarpButtonX, WarpButtonY, 1214, 71, 1229, 85, 0xdbdbdb, 7, Fast ;white warp icon in selection box above overview
			if ErrorLevel = 0
				{
				Guicontrol, Text, Debugger, found warp button
				Goto, Warp
				}
			else
				Sleep, 100	
		}
	
	;click on warp button
	Warp:
	Random, wait200to2000milis, 200, 2000
	Sleep, wait200to2000milis
	
	Random, varyby12, 0, 12
	Random, varyby11, 0, 11
	Random, mousemove3, 3, 100
	MouseMove, varyby12+1215, varyby11+70, mousemove3 ;warp icon in selection box
		Random, wait200to1600milis, 200, 1600
		Sleep, wait200to1600milis
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
	Guicontrol, Text, Debugger, warping
		Random, wait200to2000milis, 200, 2000
		Sleep, wait200to2000milis
				
	;move mouse away from button so button can be easily seen
	Random, varyX, -300, 300
	Random, varyY, 60, 300
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
	Guicontrol, Text, Debugger, looking for dock or warp
	Loop, 15000 
		{
		PixelSearch, JumpMadeX, JumpMadeY, 1174, 49, 1175, 51, 0x4c4c4c, 9, Fast ;grey 'no object selected' text in selection box
			if ErrorLevel = 0
				{
				Guicontrol, Text, Debugger, jump detected
					Random, wait200to800milis, 200, 800
					Sleep, wait200to800milis
					ClickOnWaypoint() ;if a jump has been detected, click on the next waypoint
				}
			else
				{
				;if a jump has not been detected, search for evidence of a dock
				PixelSearch, DockMadeX, DockMadeY, 1781, 142, 1782, 143, 0x027a98, 15, Fast ;yellow undock icon
					if ErrorLevel = 0
						{
						Guicontrol, Text, Debugger, docking detected
							DockedCount += 1
								if (StationBreakMin > 0) ;if break parameters have been specified, run function using those parameters
									{
									DockBreakSpecified()
									ItemsInInventory()
									}
								if (StationBreakMin = 0) ;if break parameters have not been specified, run function with preset default values
									{
									DockBreakDefault()
									ItemsInInventory()
									}
								else
									ItemsInInventory() ;if script doesn't break, continue as normal
						}
					else
						Sleep, 100	
				}
		}
		
	;if cannot detect jump or dock after timer expires, look for waypoint again with a larger search area
	Loop, 3
		{
		Loop, 50
			{
			PixelSearch, WaypointX, WaypointY, 1100, 50, 1300, 1080, 0x033535, 16, Fast ;icons in overview, wider area
				if ErrorLevel = 0
					{
					Guicontrol, Text, Debugger, found waypoint
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
		MouseMove, varyby250+WaypointX, varyby12+WaypointY, mousemove12 ;yellow waypoint icon in overview
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
		
		Loop, 50
			{
			PixelSearch, WarpButtonX, WarpButtonY, 1214, 71, 1229, 85, 0x020202, 1, Fast ;white warp button in selection box
				if ErrorLevel = 0
					{
					Guicontrol, Text, Debugger, found warp button
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
			MouseMove, varyby12+1215, varyby11+70, mousemove13 ;warp button in selection box
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
			Guicontrol, Text, Debugger, warping
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

DockBreakSpecified() ;roll for chance of sleeping script while docked at a station along route if user has specified break parameters
	{
	;if ship has docked at least the minimum number of times specified in the gui and taking breaks is enabled, roll to determine if script will sleep
	Global
	if ((DockedCount >= StationBreakMin) and (Breaks = 1))
		{
		Random, StationBreakRoll, StationBreakMin, StationBreakMax ;roll for chance of sleeping
			if (StationBreakRoll = StationBreakMin)
				{
				Random, StationSleepRoll, (StationBreakSleepMin*60*1000), (StationBreakSleepMax*60*1000) ;if roll sucessful, roll for sleep duration as specified in gui, convert minutes to miliseconds
					StationSleepRollShow := StationSleepRoll ;convert back into seconds for display purposes within gui
					StationSleepRollShow /= 1000
						Guicontrol, Text, Debugger, sleeping for %StationSleepRollShow% seconds
				Sleep, StationSleepRoll 
					DockedCount := 0 ;after sleeping, reset docked count variable so sleep isn't forced when StationBreakMax is reached
				Return
				}
			else
				Return
		}
		
	;if ship has docked equal to or more than the maximum number of times specified in the gui and script hasn't already slept yet, force the script to sleep
	if ((DockedCount >= StationBreakMax) and (Breaks = 1))
		{
		Random, StationSleepRoll, (StationBreakSleepMin*60*1000), (StationBreakSleepMax*60*1000) ;if roll sucessful, roll for sleep duration as specified in gui, convert minutes to miliseconds
			StationSleepRollShow := StationSleepRoll ;convert back into seconds for display purposes within gui
			StationSleepRollShow /= 1000
				Guicontrol, Text, Debugger, sleeping for %StationSleepRollShow% seconds
		Sleep, StationSleepRoll
			DockedCount := 0 ;after sleeping, reset docked count variable so sleep isn't forced on next dock
		Return	
		}
	else
		Return
	}

DockBreakDefault() ;roll for chance of sleeping script while docked at a station along route using default values if user hasn't specified break parameters
	{
	;if ship has docked at least the minimum number of times specified in the gui, roll to determine if script will sleep
	Global
	if ((DockedCount >= 1) and (Breaks = 1))
		{
		Random, StationBreakRollDefault, 0, 10 ;roll for chance of sleeping
			if StationBreakRoll = 0
				{
				Random, StationSleepRollDefault, 60000, 120000 ;if roll sucessful, roll for sleep
					StationSleepRollDefaultShow = (StationSleepRollDefault / 1000) ;convert back into seconds for display purposes within gui
						Guicontrol, Text, Debugger, sleeping for %StationSleepRollDefaultShow% seconds
				Sleep, StationSleepRollDefault
					DockedCount = 0 ;after sleeping, reset docked count variable so sleep isn't forced when 
				Return
				}
			else
				Return
				
		}
	;if ship has docked equal to or more than the maximum number of times by default and script hasn't already slept yet, force the script to sleep
	if ((DockedCount >= 5) and (Breaks = 1))
		{
		Random, StationSleepRollDefault, 60000, 120000 ;if roll sucessful, roll for sleep duration
			StationSleepRollDefaultShow = (StationSleepRollDefault / 1000) ;convert back into seconds for display purposes within gui
				Guicontrol, Text, Debugger, sleeping for %StationSleepRollDefaultShow% seconds
		Sleep, StationSleepRollDefault
			DockedCount = 0 ;after sleeping, reset docked count variable so sleep isn't forced on next dock
		Return	
		}
	else
		Return
	}

ItemsInInventory() ;move items from station hangar to ship cargo bay
	{
	;first, check if ship has reached home station
	Global
	AtHomeCheck()
	
	Random, wait1000to5000milis, 1000, 5000
	Sleep, wait1000to5000milis	
	Loop, 2 ;open and close station hangar window multiple times to make sure items are/aren't present
		{
		;focus main inventory window
		Random, varyby650, 0, 650
		Random, varyby20, 0, 20
		Random, mousemove9, 5, 80
		MouseMove, varyby650+647, varyby20+1046, mousemove9 ;bottom edge of inventory window
			Random, wait200to500milis, 200, 500
			Sleep, wait200to500milis+500
				Click, down
					Random, wait5to200milis, 5, 200
					Sleep, wait5to200milis
				Click, up
					Random, wait200to500milis, 200, 500
					Sleep, wait200to500milis+500
		
		;use hotkey to open station hangar inventory window
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
		
		;focus station hangar window	
		Random, varyby400, 0, 400
		Random, varyby300, 0, 300	
		Random, mousemove19, 5, 100			
		MouseMove, varyby400+1208, varyby300+320, mousemove19 ;random location in station hangar inventory below first item
			Random, wait200to500milis, 200, 500
			Sleep, wait200to500milis+500
		Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
		Click, up
				Random, wait200to500milis, 200, 500
				Sleep, wait200to500milis+500	
		
		;check to see if any items are present in station hangar inventory
		Loop, 50
			{
			PixelSearch, StationItemsX, StationItemsY, 661, 90, 1100, 100, 0xababab, 5, Fast ;white text label of items in first row of station hangar
				if ErrorLevel = 0
					{
					Guicontrol, Text, Debugger, found items in station hangar
					Random, wait200to500milis, 200, 500
					Sleep, wait200to500milis
						Goto, SelectInventory
					}
				else
					Sleep, 10
			}
		}
	
	;if no items are present in station inventory, undock and continue
	Guicontrol, Text, Debugger, station hangar empty
	Goto, CloseStationHangar
	
	;use hotkey to select all items
	SelectInventory:
	SendMode Input
	Send {Ctrl down} 
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {A down}
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {A up}
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {Ctrl up}
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis
	SendMode Event

	;click and drag items to ship cargo hold
	Random, varyby300, 0, 300
	Random, varyby16, 0, 16
	Random, mousemove12, 5, 100
	MouseMove, varyby300+663, varyby16+85, mousemove12 ;first item in station hangar
		Random, wait200to1000milis, 200, 1000
		Sleep, wait200to1000milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
					Random, varyby38, 0, 38
					Random, varyby13, 0, 13	
					Random, mousemove13, 5, 100			
					MouseMove, varyby38+599, varyby13+67, mousemove13 ;ship ore cargo bay icon in inventory sidebar		
						Random, wait200to1000milis, 200, 1000
						Sleep, wait200to1000milis
			Click, up
				Random, wait1000to5000milis, 1000, 5000
				Sleep, wait1000to5000milis
		
		;check to see if 'not enough cargo space' alert appears	
		Loop, 10 
			{
			PixelSearch, ShipFullX, ShipFullY, 1782, 142, 1789, 150, 0x014555, 3, Fast ;check if undock icon becomes darker due to pop-up window
				if ErrorLevel = 0
					{
					;close alert
					Send {ENTER down}
						Random, wait15to300milis, 15, 300
						Sleep, wait15to300milis
					Send {Enter up}
						Random, wait150to300milis, 150, 300
						Sleep, wait150to300milis
					
					;deselect items
					Random, varyby400, 0, 400
					Random, varyby300, 0, 300	
					Random, mousemove19, 5, 100			
					MouseMove, varyby400+1208, varyby300+320, mousemove19 ;random location in station hangar inventory below first item
						Random, wait200to500milis, 200, 500
						Sleep, wait200to500milis+500
					Click, down
							Random, wait5to200milis, 5, 200
							Sleep, wait5to200milis
					Click, up
							Random, wait200to500milis, 200, 500
							Sleep, wait200to500milis+500			
					;if not all items will fit at once, try placing items into ship cargo hold one at a time
					ItemsOneAtATime()
					}
				else
					Sleep, 10	
			}
	
	;close station hangar inventory window with hotkey	
	CloseStationHangar:
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

ItemsOneAtATime() ;if not all items can be added to ship at once, try adding them one at a time
	{
	;double-check items are still present
	Global
	Loop, 50
	{
	PixelSearch, StationItemsX, StationItemsY, 661, 90, 1177, 100, 0xababab, 5, Fast ;white text label of items in first row of station hangar
		if ErrorLevel = 0
			{
			Guicontrol, Text, Debugger, found items in station hangar
			Goto, SelectInventoryOneAtATime
			}
		else
			Sleep, 80
	}
	
	;move mouse over first item slot and check if background has changed color to determine if item is there
	SelectInventoryOneAtATime:
	Guicontrol, Text, Debugger, moving items one at a time
	Loop, 100
		{
		Random, varyby600, 0, 600
		Random, varyby13, 0, 20
		Random, mousemove15, 5, 100
		MouseMove, varyby600+652, varyby13+87, mousemove15 ;first item slot in station hangar when using list view with icons
			Random, wait200to1000milis, 200, 1000
			Sleep, wait200to1000milis
				PixelSearch, ItemSlot1X, ItemSlot1Y, 1653, 86, 1686, 102, 0x1c1c1c, 1, Fast ;far right side of first item slot turning light grey
					if ErrorLevel = 0
						{
						;if item is present in that slot, click and drag it to ship cargo bay
						Guicontrol, Text, Debugger, found item in first slot
						Click, down
							Random, wait5to200milis, 5, 200
							Sleep, wait5to200milis
								Random, varyby40, 0, 40
								Random, varyby16, 0, 16	
								Random, mousemove16, 5, 100			
								MouseMove, varyby40+598, varyby16+67, mousemove16 ;ship cargo bay icon in inventory sidebar	
									Random, wait200to1000milis, 200, 1000
									Sleep, wait200to1000milis								
						Click, up
							Random, wait800to3000milis, 800, 3000
							Sleep, wait800to3000milis

						;wait to see if a pop-up menu appears indicating cargo hold full or not enough space for every item
						Loop, 15 
							{
							PixelSearch, ShipFullX, ShipFullY, 1782, 142, 1789, 150, 0x014555, 3, Fast ;yellow undock icon becoming darker
								if ErrorLevel = 0
									{
									;if alert appears, close pop-up and return home
									Guicontrol, Text, Debugger, detected full cargo hold, returning home
									SendMode Input
									Send {ENTER down}
										Random, wait15to300milis, 15, 300
										Sleep, wait15to300milis
									Send {Enter up}
									SendMode Event
										Random, wait20to150milis, 20, 150
										Sleep, wait20to150milis

									;set destination to 'home base' (first item in people & places alphabetically)
									ReturnHome()
									}
								else
									Guicontrol, Text, Debugger, more items remaining
									Sleep, 50	
							}
						;if pop-up doesn't appear, repeat loop and continue moving first item in station hangar into ship cargo bay
						}
		}
		;if loop finishes without pop-up appearing, the script likely made an error
		Guicontrol, Text, Debugger, ItemsOneAtATime loop finished
		ListLines
		Pause
	}
	
ReturnHome() ;open 'people & places' menu and set whichever item is listed first as the next destination
	{
	Global
	
	/*
	;click on 'people & places' icon
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
	MouseMove, varyby500+42, varyby16+547, mousemove6 ;first entry in 'personal locations' within 'people & places' window
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down, right
				Random, wait150to200milis, 150, 200
				Sleep, wait150to200milis
			Click, up, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
				
	;click on 'set destination' in drop-down menu
	Random, varyby50, 0, 50
	Random, varyby12, 0, 12
	Random, mousemove7, 5, 80
	MouseMove, varyby50+10, varyby12+23, mousemove7, R ;'set destination' entry in right click drop-down menu
		Random, wait800to1500milis, 800, 1500
		Sleep, wait800to1500milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up	
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
	
	/*	
	;close 'people & places' window
	Random, varyby5, 0, 5
	Random, varyby6, 0, 6
	Random, mousemove8, 5, 80
	MouseMove, varyby5+580, varyby6+4, mousemove8 'x button in top right corner of 'people & places' window
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up	
				Random, wait5to800milis, 5, 800
				Sleep, wait5to800milis	
					Undock()
	*/
	
	Undock()
	}
			
AtHomeCheck() ;check the 'people & places' menu for color change to determine if ship has arrived at destination
	{
	;check if first entry in 'people & places' menu has turned green, indicating it is the current system
	Global
	Loop, 3
		{
		PixelSearch, AtDestX, AtDestY, 76, 550, 95, 561, 0x53a553, 11, Fast ;green text of first 'personal locations' entry
			if ErrorLevel = 0
				{
				Guicontrol, Text, Debugger, arrived at destination
				UnloadCargoBay()
				}
			else
				Sleep, 100	
		}
	Return
	}

UnloadCargoBay() ;unload items from ship cargo bay and place items into station hangar
	{
	;focus main inventory window
	Global
	Random, varyby650, 0, 650
	Random, varyby20, 0, 20
	Random, mousemove9, 5, 80
	MouseMove, varyby650+647, varyby20+1046, mousemove9 ;bottom edge of inventory window
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, wait200to500milis, 200, 500
				Sleep, wait200to500milis+500
				
	;make sure ship cargo bay is selected
	Random, varyby25, 0, 25
	Random, varyby19, 0, 19
	Random, mousemove9, 5, 80
	MouseMove, varyby25+611, varyby19+68, mousemove9 ;ship ore bay icon in inventory sidebar
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, wait200to500milis, 200, 500
				Sleep, wait200to500milis+500
	
	;focus window	
	Random, varyby400, 0, 400
	Random, varyby300, 0, 300	
	Random, mousemove19, 5, 100			
	MouseMove, varyby400+1208, varyby300+320, mousemove19 ;random location in inventory below first item
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
	Click, down
			Random, wait5to200milis, 5, 200
			Sleep, wait5to200milis
	Click, up
			Random, wait200to500milis, 200, 500
			Sleep, wait200to500milis+500	
	
	;select all items in ship cargo bay
	SendMode Input
	Send {Ctrl down} 
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {A down}
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {A up}
		Random, wait20to150milis, 20, 150
		Sleep, wait20to150milis
	Send {Ctrl up}
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis
	SendMode Event

	;drag items to station hangar
	Random, varyby300, 0, 300
	Random, varyby16, 0, 16
	Random, mousemove12, 5, 100
	MouseMove, varyby300+663, varyby16+85, mousemove12 ;first item in ship cargo bay
		Random, wait200to1000milis, 200, 1000
		Sleep, wait200to1000milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
					Random, varyby38, 0, 38
					Random, varyby13, 0, 13	
					Random, mousemove13, 5, 100			
					MouseMove, varyby38+599, varyby13+119, mousemove13					;station hangar icon in inventory sidebar		
						Random, wait200to1000milis, 200, 1000
						Sleep, wait200to1000milis
			Click, up
				Random, wait1000to5000milis, 1000, 5000
				Sleep, wait1000to5000milis
	
	;return to second entry in personal locations to create loop
	
	;focus 'people & places window'
	Random, varyby500, 0, 500
	Random, varyby14, 0, 14
	Random, mousemove6, 5, 100
	MouseMove, varyby500+42, varyby14+569, mousemove6 ;second entry in 'personal locations' within 'people & places' window
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
				
	;right click on first entry in 'personal locations'
	Random, varyby500, 0, 500
	Random, varyby13, 0, 16
	Random, mousemove6, 5, 100
	MouseMove, varyby500+42, varyby13+569, mousemove6 ;second entry in 'personal locations' within 'people & places' window
		Random, wait900to1500milis, 900, 1500
		Sleep, wait900to1500milis+500
			Click, down, right
				Random, wait150to200milis, 150, 200
				Sleep, wait150to200milis
			Click, up, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
				
	;click on 'set destination' in drop-down menu
	Random, varyby50, 0, 50
	Random, varyby12, 0, 12
	Random, mousemove7, 5, 80
	MouseMove, varyby50+10, varyby12+23, mousemove7, R ;'set destination' entry in right click drop-down menu
		Random, wait200to1000milis, 200, 1000
		Sleep, wait200to1000milis
			Click, down
				Random, wait50to200milis, 50, 200
				Sleep, wait50to200milis
			Click, up	
				Random, wait200to1000milis, 200, 1000
				Sleep, wait200to1000milis
			Undock()
	ExitApp
	}
	
Logout() ;logout of client
	{
	Global
		
	
	}

ShowGUI()
	{
	Global
	Gui, Add, Text, x12 y9 w320 h20 +Center, NEOBOT TRAVELER
	Gui, Add, Button, x162 y59 w170 h50 vSTART, START
	Gui, Add, Button, x72 y59 w80 h50 , STOP 

	Gui, Add, GroupBox, x12 y119 w320 h70 , Debugger
	Gui, Add, Text, x20 y145 w250 h20 +Center vDebugger, ready

	Gui, Add, GroupBox, x12 y199 w320 h200 , Accounts

	Gui, Add, Button, x22 y229 w20 h30 , +
	Gui, Add, Button, x22 y269 w20 h30 , +
	Gui, Add, Button, x22 y309 w20 h30 , +
	Gui, Add, Button, x22 y349 w20 h30 , +
	Gui, Add, Button, x42 y229 w20 h30 , -
	Gui, Add, Button, x42 y269 w20 h30 , -
	Gui, Add, Button, x42 y309 w20 h30 , -
	Gui, Add, Button, x42 y349 w20 h30 , -
	Gui, Add, Button, x212 y269 w60 h30 , Add Key
	Gui, Add, Button, x212 y229 w60 h30 , Add Key
	Gui, Add, Button, x212 y349 w60 h30 , Add Key
	Gui, Add, Button, x212 y309 w60 h30 , Add Key
	Gui, Add, Button, x282 y269 w40 h30 , View
	Gui, Add, Button, x282 y229 w40 h30 , View
	Gui, Add, Button, x282 y349 w40 h30 , View
	Gui, Add, Button, x282 y309 w40 h30 , View

	Gui, Add, Radio, x72 y229 w140 h30 vAccount , Account 1
	Gui, Add, Radio, x72 y269 w140 h30 , Account 2
	Gui, Add, Radio, x72 y309 w140 h30 , Account 3
	Gui, Add, Radio, x72 y349 w140 h30 , Account 4

	Gui, Add, GroupBox, x12 y409 w320 h170 , Settings

	Gui, Add, CheckBox, x42 y439 w90 h20 vBreaks, Take Breaks
	Gui, Add, ComboBox, x92 y489 w50 h20 vStationBreakMin, ComboBox
	Gui, Add, Text, x102 y459 w130 h20 +Center, Frequency
	Gui, Add, Text, x32 y489 w60 h20 +Center , Every
	Gui, Add, Text, x142 y489 w40 h20 +Center, to
	Gui, Add, ComboBox, x182 y489 w50 h21 vStationBreakMax, ComboBox
	Gui, Add, Text, x232 y489 w60 h20 +Center, Stations

	Gui, Add, Text, x32 y549 w60 h20 +Center, For
	Gui, Add, Text, x102 y519 w130 h20 +Center, Duration
	Gui, Add, ComboBox, x92 y549 w50 h21 vStationBreakSleepMin, ComboBox
	Gui, Add, Text, x142 y549 w40 h20 +Center, to
	Gui, Add, ComboBox, x182 y549 w50 h21 vStationBreakSleepMax, ComboBox
	Gui, Add, Text, x232 y549 w60 h20 +Center, Minutes

	Gui, Add, Text, x122 y29 w100 h20 +Center, version %version%
	Gui, Show, x794 y267 h596 w352, NEOBOT TRAVELER v%version%
	Return

	ButtonSTART:
	Guicontrol, Disable, START
	Gui, Submit, NoHide ;submit parameters specified in the gui
	Winset, Alwaysontop, , A ;window stays on stop
	Guicontrol, Text, Debugger, starting script
	;AtHomeCheck()
	;/*
		;check if ship is docked when script starts
		PixelSearch, DockMadeX, DockMadeY, 1781, 142, 1834, 171, 0x027a98, 15, Fast ;yellow undock icon
			if ErrorLevel = 0
				Undock()
			else ;if not docked, look for waypoint marker since ship must be in space
				SelectWaypoint()
	;*/		
	Return

	ButtonSTOP:
	Guicontrol, Text, Debugger, stopping script
	Guicontrol, Enable, START
	ListLines
	Pause
	Return

	ButtonView:
	msgbox %test%
	
	GuiClose:
	ExitApp

	;ButtonTake\ Breaks:
	
	
	test:
	ExitApp
	}
	
;MsgBox, end of script
;ExitApp	

shift:: ;manual kill switch
	{
	ListLines
	Pause
	}	

z:: ;show logs
	{
	ListLines
	Pause
	}

x:: ;show variables
	{
	ListVars
	Pause
	}
