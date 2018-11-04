;known bugs
;setting destination from home station to second entry in people and places sometimes doesn't open the right click menu
;incorrect warp waypoint is selected if script is started while ship is in warp


;needed features
;add method for confirming a new destination has been set by pixelsearching for a red/yellow/green square in the 'route' gui
;add 'logout of client' functionality
;add ability to login to client from desktop and resume script
;write guide for configuring eve gui properly so script can read it
;add support for both standard ship cargo hold and 'special' ship cargo bays like ore holds

;how to configure client settings for NEOBOT TRAVELER
;reset all client window settings
;turn off window transparency completley
;do not pin any windows in your client as they will become transparent
;open 'wallet' and shrink window hori

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
	Random, mousemove, 5, 80
	MouseMove, varyby40+1781, varyby18+142, mousemove ;undock button in station sidebar
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
	Docked := 0
	SelectWaypoint()
	}

SelectWaypoint() ;click on yellow-tinted icon in overview to select next waypoint
	{ 
	;look for waypoint in overview
	Global
	Guicontrol, Text, Debugger, looking for waypoint
	WinActivate, EVE
	Loop, 300
		{
		PixelSearch, WaypointX, WaypointY, 1162, 170, 1176, 1074, 0x033535, 16, Fast ;overview icons
			if ErrorLevel = 0
				{
				Guicontrol, Text, Debugger, found waypoint
				Winset, AlwaysOnTop, On, NEOBOT TRAVELER, Accounts
				Goto, ClickWaypointinOverview
				}
			else
				Sleep, 100
		}
		Guicontrol, Text, Debugger, found waypoint
	
	;click on waypoint in overview to highlight it in selection box
	ClickWaypointinOverview:
	Random, varyby250, 0, 250
	Random, varyby9, 0, 9
	Random, mousemove, 5, 80
	MouseMove, varyby250+WaypointX, varyby9+WaypointY, mousemove ;waypoint icon in overview
		Random, wait200to2000milis, 200, 2000
		Sleep, wait200to2000milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, DoubleClickRoll, 1, 20 ;chance to double-click
				if DoubleClickRoll = 1
					{
					Random, wait5to250milis, 5, 250
					Sleep, wait5to250milis
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
	Loop, 60
		{
		PixelSearch, WarpButtonX, WarpButtonY, 1214, 71, 1229, 85, 0xdbdbdb, 7, Fast ;white warp icon in selection box above overview
			if ErrorLevel = 0
				{
				Guicontrol, Text, Debugger, found warp button
				Goto, Warp
				}
			else
				Sleep, 1000	
		}
	
	;click on warp button
	Warp:
	Random, wait200to2000milis, 200, 2000
	Sleep, wait200to2000milis
	
	Random, varyby12, 0, 12
	Random, varyby11, 0, 11
	Random, mousemove, 6, 60
	MouseMove, varyby12+1215, varyby11+70, mousemove ;warp icon in selection box
		Random, wait200to1600milis, 200, 1600
		Sleep, wait200to1600milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, DoubleClickRoll, 1, 20 ;chance to double-click
				if DoubleClickRoll = 1
					{
					Random, wait5to250milis, 5, 250
					Sleep, wait5to250milis
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
	Random, mousemove, 6, 60
	MouseMove, varyX, varyY, mousemove, R
	
	;wait a minimum period of time for warp to begin
		Random, wait5000to15000milis, 5000, 15000
		Sleep, wait5000to15000milis
	JumpOrDockDetect()
	}

JumpOrDockDetect() ;search for colors indicating either a jump has been made or ship has docked
	{
	;search for evidence of a jump
	Global
	Guicontrol, Text, Debugger, looking for dock or warp
	Loop, 8000 
		{	
		;search for evidence of a dock
		PixelSearch, DockMadeX, DockMadeY, 1781, 142, 1782, 143, 0x027a98, 15, Fast ;yellow undock icon
			if ErrorLevel = 0
				{
				Guicontrol, Text, Debugger, docking detected
					Docked := 1
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
			;search for evidence of a jump
			else
				{
				PixelSearch, JumpMadeX, JumpMadeY, 1174, 49, 1175, 51, 0x555555, 5, Fast ;grey 'no object selected' text in selection box
					if ErrorLevel = 0
						{
						Guicontrol, Text, Debugger, jump detected
							Random, wait1000to5000milis, 1000, 5000
							Sleep, wait1000to5000milis
							ClickOnWaypoint() ;if a jump has been detected, look for warp button
						}
					else
						Sleep, 50
				
				}
		}
		
	;if cannot detect jump or dock after timer expires, look for waypoint again with a larger search area
	Loop, 3
		{
		Guicontrol, Text, Debugger, looking for waypoint (backup)
		Loop, 50
			{
			PixelSearch, WaypointX, WaypointY, 1100, 50, 1300, 1080, 0x033535, 16, Fast ;icons in overview, wider area
				if ErrorLevel = 0
					{
					Guicontrol, Text, Debugger, found waypoint (backup)
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
		Random, mousemove2, 5, 80
		MouseMove, varyby250+WaypointX, varyby12+WaypointY, mousemove2 ;yellow waypoint icon in overview
			Random, wait200to2000milis, 200, 2000
			Sleep, wait200to2000milis
				Click, down
					Random, wait5to200milis, 5, 200
					Sleep, wait5to200milis
				Click, up
					Random, DoubleClickRoll, 1, 20 ;chance to double-click
					if DoubleClickRoll = 1
						{
						Random, wait5to250milis, 5, 250
						Sleep, wait5to250milis
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
			Random, mousemove, 6, 60
			MouseMove, varyby12+1215, varyby11+70, mousemove ;warp button in selection box
				Random, wait200to2000milis, 200, 2000
				Sleep, wait200to2000milis
					Click, down
						Random, wait5to200milis, 5, 200
						Sleep, wait5to200milis
					Click, up
						Random, DoubleClickRoll, 1, 20 ;chance to double-click
						if DoubleClickRoll = 1
							{
							Random, wait5to250milis, 5, 250
							Sleep, wait5to250milis
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
			Random, mousemove, 6, 60
			MouseMove, varyX, varyY, mousemove, R

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
		Guicontrol, Text, Debugger, focusing inventory
		Random, varyby650, 0, 650
		Random, varyby20, 0, 20
		Random, mousemove, 6, 60
		MouseMove, varyby650+647, varyby20+1046, mousemove ;bottom edge of inventory window
			Random, wait50to500milis, 50, 500
			Sleep, wait50to500milis
				Click, down
					Random, wait5to200milis, 5, 200
					Sleep, wait5to200milis
				Click, up
					Random, wait50to500milis, 50, 500
					Sleep, wait50to500milis
		
		;use hotkey to open station hangar inventory window
		Guicontrol, Text, Debugger, opening station hangar
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
		Guicontrol, Text, Debugger, focusing station hangar
		Random, varyby400, 0, 400
		Random, varyby300, 0, 300	
		Random, mousemove, 6, 60			
		MouseMove, varyby400+1208, varyby300+320, mousemove ;random location in station hangar inventory below first item
			Random, wait50to500milis, 50, 500
			Sleep, wait50to500milis
		Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
		Click, up
				Random, wait50to500milis, 50, 500
				Sleep, wait50to500milis
		
		;check to see if any items are present in station hangar inventory
		Loop, 50
			{
			PixelSearch, StationItemsX, StationItemsY, 661, 90, 1100, 100, 0xababab, 5, Fast ;white text label of items in first row of station hangar
				if ErrorLevel = 0
					{
					Guicontrol, Text, Debugger, found items in station hangar
						Random, wait50to500milis, 50, 500
						Sleep, wait50to500milis
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
	Guicontrol, Text, Debugger, selecting items
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
	Guicontrol, Text, Debugger, moving items to cargo hold
	Random, varyby300, 0, 300
	Random, varyby16, 0, 16
	Random, mousemove2, 6, 60
	MouseMove, varyby300+663, varyby16+85, mousemove2 ;first item in station hangar
		Random, wait50to500milis, 50, 500
		Sleep, wait50to500milis
		Click, down
			Random, wait5to200milis, 5, 200
			Sleep, wait5to200milis
				Random, varyby38, 0, 38
				Random, varyby13, 0, 13	
				Random, mousemove, 6, 60			
				MouseMove, varyby38+599, varyby13+67, mousemove ;ship ore cargo bay icon in inventory sidebar		
					Random, wait200to1000milis, 200, 1000
					Sleep, wait200to1000milis
		Click, up
			Random, wait500to1500milis, 500, 1500
			Sleep, wait500to1500milis
		
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
					Guicontrol, Text, Debugger, deselecting items
					Random, varyby400, 0, 400
					Random, varyby300, 0, 300	
					Random, mousemove, 6, 60			
					MouseMove, varyby400+1208, varyby300+320, mousemove ;random location in station hangar inventory below first item
						Random, wait200to500milis, 200, 500
						Sleep, wait200to500milis+500
					Click, down
							Random, wait5to200milis, 5, 200
							Sleep, wait5to200milis
					Click, up
						Random, wait50to500milis, 50, 500
						Sleep, wait50to500milis		
					;if not all items will fit at once, try placing items into ship cargo hold one at a time
					Guicontrol, Text, Debugger, moving items one at a time
					ItemsOneAtATime()
					}
				else
					{
					Random, wait300to800milis, 300, 800
					Sleep, wait300to800milis	
					}
			}
	
	;close station hangar inventory window with hotkey	
	CloseStationHangar:
	Guicontrol, Text, Debugger, closing station hangar
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
	Random, wait50to500milis, 50, 500
	Sleep, wait50to500milis
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
	Guicontrol, Text, Debugger, looking for first item
	Loop, 50
		{
		Random, varyby600, 0, 600
		Random, varyby13, 0, 20
		Random, mousemove, 6, 60
		MouseMove, varyby600+652, varyby13+87, mousemove ;first item slot in station hangar when using list view with icons
			Random, wait50to500milis, 50, 500
			Sleep, wait50to500milis
				PixelSearch, ItemSlot1X, ItemSlot1Y, 1653, 86, 1686, 102, 0x1c1c1c, 1, Fast ;far right side of first item slot turning light grey
					if ErrorLevel = 0
						{
						;if item is present in that slot, click and drag it to ship cargo bay
						Guicontrol, Text, Debugger, moving item to cargo hold
						Click, down
							Random, wait5to200milis, 5, 200
							Sleep, wait5to200milis
								Random, varyby40, 0, 40
								Random, varyby16, 0, 16	
								Random, mousemove, 6, 60			
								MouseMove, varyby40+598, varyby16+67, mousemove ;ship cargo bay icon in inventory sidebar	
									Random, wait200to1000milis, 200, 1000
									Sleep, wait200to1000milis								
						Click, up
							Random, wait1000to1500milis, 1000, 1500
							Sleep, wait1000to1500milis

						;wait to see if a pop-up menu appears indicating cargo hold full or not enough space for every item
						Guicontrol, Text, Debugger, checking for full cargo hold
						Loop, 3
							{
							PixelSearch, ShipFullX, ShipFullY, 1782, 142, 1789, 150, 0x014555, 3, Fast ;yellow undock icon becoming darker
								if ErrorLevel = 0
									{
									;if alert appears, close pop-up and return home
									Guicontrol, Text, Debugger, detected full cargo hold
									SendMode Input
									Send {ENTER down}
										Random, wait15to300milis, 15, 300
										Sleep, wait15to300milis
									Send {Enter up}
										Random, wait20to150milis, 20, 150
										Sleep, wait20to150milis
										
									;close station hangar inventory window
									Guicontrol, Text, Debugger, closing station hangar
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
									;set destination to 'home base' (first item in people & places alphabetically)
									Guicontrol, Text, Debugger, returning home
									ReturnHome()
									}
								else
									{
									Guicontrol, Text, Debugger, more items remaining
									Random, wait800to1300milis, 800, 1300
									Sleep, wait800to1300milis
									}
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
	Random, mousemove, 5, 80
	MouseMove, varyby25+3, varyby24+137, mousemove
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
	*/
	
	;right click on first entry in 'personal locations'
	Guicontrol, Text, Debugger, setting home destination
	Random, varyby500, 0, 500
	Random, varyby18, 0, 18
	Random, mousemove, 6, 60
	MouseMove, varyby500+79, varyby18+547, mousemove ;first entry in 'personal locations' within 'people & places' window
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down, right
				Random, wait150to200milis, 150, 200
				Sleep, wait150to200milis
			Click, up, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
				
	;click on 'set destination' in drop-down menu
	Random, varyby110, 0, 110
	Random, varyby12, 0, 12
	Random, mousemove, 5, 80
	MouseMove, varyby110+12, varyby12+23, mousemove, R ;'set destination' entry in right click drop-down menu
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
	Random, mousemove, 5, 80
	MouseMove, varyby5+580, varyby6+4, mousemove 'x button in top right corner of 'people & places' window
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
				Guicontrol, Text, Debugger, arrived home
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
	Guicontrol, Text, Debugger, focusing inventory window
	Random, varyby650, 0, 650
	Random, varyby20, 0, 20
	Random, mousemove, 5, 80
	MouseMove, varyby650+647, varyby20+1046, mousemove ;bottom edge of inventory window
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, wait200to500milis, 200, 500
				Sleep, wait200to500milis+500
				
	;make sure ship cargo bay is selected
	Guicontrol, Text, Debugger, selecting cargo bay
	Random, varyby25, 0, 25
	Random, varyby19, 0, 19
	Random, mousemove, 5, 80
	MouseMove, varyby25+611, varyby19+68, mousemove ;ship ore bay icon in inventory sidebar
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
			Click, up
				Random, wait200to500milis, 200, 500
				Sleep, wait200to500milis+500
	
	;focus window
	Guicontrol, Text, Debugger, focusing cargo bay	
	Random, varyby400, 0, 400
	Random, varyby300, 0, 300	
	Random, mousemove, 6, 60			
	MouseMove, varyby400+1208, varyby300+320, mousemove ;random location in inventory below first item
		Random, wait200to500milis, 200, 500
		Sleep, wait200to500milis+500
	Click, down
			Random, wait5to200milis, 5, 200
			Sleep, wait5to200milis
	Click, up
			Random, wait200to500milis, 200, 500
			Sleep, wait200to500milis+500	
	
	;select all items in ship cargo bay
	Guicontrol, Text, Debugger, selecting all items
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
	Guicontrol, Text, Debugger, moving items to station hangar
	Random, varyby300, 0, 300
	Random, varyby16, 0, 16
	Random, mousemove2, 6, 60
	MouseMove, varyby300+663, varyby16+85, mousemove2 ;first item in ship cargo bay
		Random, wait200to1000milis, 200, 1000
		Sleep, wait200to1000milis
			Click, down
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
					Random, varyby38, 0, 38
					Random, varyby13, 0, 13	
					Random, mousemove, 6, 60			
					MouseMove, varyby38+599, varyby13+119, mousemove	 ;station hangar icon in inventory sidebar		
						Random, wait200to1000milis, 200, 1000
						Sleep, wait200to1000milis
			Click, up
				Random, wait1000to5000milis, 1000, 5000
				Sleep, wait1000to5000milis
			ReturnToTarget()
	}
	
ReturnToTarget() ;return to second entry in personal locations to create loop
	{
	;focus 'people & places window'
	Global
	Guicontrol, Text, Debugger, returning to set location
	Random, varyby500, 0, 500
	Random, varyby18, 0, 14
	Random, mousemove, 6, 60
	MouseMove, varyby500+79, varyby18+569, mousemove ;second entry in 'personal locations' within 'people & places' window
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
	Random, mousemove, 6, 60
	MouseMove, varyby500+42, varyby13+569, mousemove ;second entry in 'personal locations' within 'people & places' window
		Random, wait900to1500milis, 900, 1500
		Sleep, wait900to1500milis+500
			Click, down, right
				Random, wait150to200milis, 150, 200
				Sleep, wait150to200milis
			Click, up, right
				Random, wait5to200milis, 5, 200
				Sleep, wait5to200milis
				
	;click on 'set destination' in drop-down menu
	Random, varyby110, 0, 110
	Random, varyby12, 0, 12
	Random, mousemove, 5, 80
	MouseMove, varyby110+12, varyby12+23, mousemove, R ;'set destination' entry in right click drop-down menu
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
	;click on menu icon in top left corner of screen
	Global	
	Guicontrol, Text, Debugger, logging out
	Random, varyby27, 0, 27
	Random, varyby26, 0, 26
	Random, mousemove, 6, 60
	MouseMove, varyby27+0, varyby26+0, mousemove ;menu icon in top left corner
		Random, wait200to1000milis, 200, 1000
		Sleep, wait200to1000milis
			Click, down
				Random, wait50to200milis, 50, 200
				Sleep, wait50to200milis
			Click, up	
				Random, wait200to1000milis, 200, 1000
				Sleep, wait200to1000milis
				
	;click 'settings' icon
	Random, varyby200, 0, 200
	Random, varyby24, 0, 24
	Random, mousemove, 6, 60
	MouseMove, varyby200+40, varyby24+675, mousemove ;settings icon in main menu sidebar
		Random, wait200to1000milis, 200, 1000
		Sleep, wait200to1000milis
			Click, down
				Random, wait50to200milis, 50, 200
				Sleep, wait50to200milis
			Click, up	
				Random, wait200to1000milis, 200, 1000
				Sleep, wait200to1000milis
				
	;if not docked, click 'log out safely'
	if (Docked < 1)
		{	
		Random, varyby50, 0, 50
		Random, varyby12, 0, 12
		Random, mousemove, 6, 60
		MouseMove, varyby50+1220, varyby12+805, mousemove ;log out safely button in settings menu
			Random, wait200to1000milis, 200, 1000
			Sleep, wait200to1000milis
				Click, down
					Random, wait50to200milis, 50, 200
					Sleep, wait50to200milis
				Click, up	
					Random, wait200to1000milis, 200, 1000
					Sleep, wait200to1000milis			
		}
	;if docked, click 'log out'
	else 
		{
		Random, varyby35, 0, 35
		Random, varyby12, 0, 12
		Random, mousemove, 6, 60
		MouseMove, varyby35+1305, varyby12+802, mousemove ;log out button in settings menu
			Random, wait200to1000milis, 200, 1000
			Sleep, wait200to1000milis
				Click, down
					Random, wait50to200milis, 50, 200
					Sleep, wait50to200milis
				Click, up	
					Random, wait200to1000milis, 200, 1000
					Sleep, wait200to1000milis		
					
		}
	;confirm selection if prompted
	Send {ENTER down}
		Random, wait15to300milis, 15, 300
		Sleep, wait15to300milis
	Send {Enter up}
		Random, wait150to300milis, 150, 300
		Sleep, wait150to300milis
	ListLines
	Pause
	}
	
ShowGUI()
	{
	Global
		Winset, AlwaysOnTop, On, NEOBOT TRAVELER, Accounts ;window stays on stop
	Gui, Add, Button, x252 y9 w90 h30 vSTART, START
	Gui, Add, Button, x192 y9 w60 h30 vSTOP, STOP
		Guicontrol, Disable, STOP
		
	Gui, Add, GroupBox, x12 y-1 w170 h40 , 
	Gui, Add, Text, x12 y9 w170 h30 +Center vDebugger, ready

	Gui, Add, GroupBox, x12 y49 w330 h180 , Settings
	Gui, Add, CheckBox, x42 y69 w90 h20 gTakeBreaks vBreaks, Take Breaks
	Gui, Add, ComboBox, x112 y119 w50 h20 vStationBreakMin, ComboBox
	Gui, Add, Text, x112 y89 w130 h20 +Center, Frequency
	Gui, Add, Text, x52 y119 w60 h20 +Center, Every
	Gui, Add, Text, x162 y119 w40 h20 +Center, to
	Gui, Add, ComboBox, x202 y119 w50 h20 vStationBreakMax, ComboBox
	Gui, Add, Text, x252 y119 w60 h20 +Center, Stations

	Gui, Add, Text, x52 y179 w60 h20 +Center, For
	Gui, Add, Text, x112 y149 w130 h20 +Center, Duration
	Gui, Add, ComboBox, x112 y179 w50 h21 vStationBreakSleepMin, ComboBox
	Gui, Add, Text, x162 y179 w40 h20 +Center, to
	Gui, Add, ComboBox, x202 y179 w50 h20 vStationBreakSleepMax, ComboBox
	Gui, Add, Text, x252 y179 w60 h20 +Center, Minutes

	Gui, Add, GroupBox, x2 y239 w340 h90 , Accounts
	Gui, Add, Button, x12 y279 w20 h30 , +
	Gui, Add, Button, x222 y279 w60 h30 , Add Key
	Gui, Add, Button, x292 y279 w40 h30 , View
	Gui, Add, Button, x32 y279 w20 h30 , -
	Gui, Add, DropDownList, x62 y279 w150 h40 , DropDownList
	
	;disable break settings by default until 'take breaks' checkbox is checked
	Guicontrol, Disable, StationBreakSleepMin
	Guicontrol, Disable, StationBreakSleepMax
	Guicontrol, Disable, StationBreakMin
	Guicontrol, Disable, StationBreakMax

	Gui, Show, x292 y-794 h341 w356, NEOBOT TRAVELER v%version%
	Return

	ButtonSTART:
		Guicontrol, Disable, START
		Guicontrol, Enable, STOP
			Gui, Submit, NoHide ;submit parameters specified in the gui
			Guicontrol, Text, Debugger, starting script
				WinMove, NEOBOT, START, (A_Screenwidth-352), (A_Screenheight-72), 352, 72 ;move gui to bottom right corner of screen
			;AtHomeCheck()
			;/*
				;check if ship is docked when script starts
				Loop, 10
					{
					PixelSearch, DockMadeX, DockMadeY, 1781, 142, 1834, 171, 0x027a98, 15, Fast ;yellow undock icon
						if ErrorLevel = 0
							{
							Docked := 1
							Undock()
							}
						else
							Sleep, 100
					}
					;if not docked, look for waypoint marker since ship must be in space
					Guicontrol, Text, Debugger, no docking found
					Docked := 0
					SelectWaypoint()
			;*/		
	Return

	ButtonSTOP:
		Reload
		;Guicontrol, Text, Debugger, stopping script
		;Guicontrol, Enable, START
		;ShowGui()
	Return

	ButtonView:
		msgbox %test%
	
	GuiClose:
		ExitApp

	TakeBreaks:
		Gui, Submit, NoHide	
			if (Breaks = 0)
				{
				Guicontrol, Disable, StationBreakSleepMin
				Guicontrol, Disable, StationBreakSleepMax
				Guicontrol, Disable, StationBreakMin
				Guicontrol, Disable, StationBreakMax
				}
			else
				{
				Guicontrol, Enable, StationBreakSleepMin
				Guicontrol, Enable, StationBreakSleepMax
				Guicontrol, Enable, StationBreakMin
				Guicontrol, Enable, StationBreakMax
				}
	Return
	
	test:
	ExitApp
	}
	
	;MsgBox, end of script
	;ExitApp	

shift:: ;manual kill switch, show logs
	{
	ListLines
	Pause
	}	

z:: ;reload
	{
	Reload
	}

x:: ;show variables
	{
	ListVars
	Pause
	}
 