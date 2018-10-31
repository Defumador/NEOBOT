#include Traveler.ahk

Gui, Add, Text, x12 y9 w320 h20 +Center, EOBOT
Gui, Add, Button, x162 y59 w170 h50 , START
Gui, Add, Button, x72 y59 w80 h50 , STOP 
Gui, Add, GroupBox, x12 y119 w320 h70 , Debugger

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
Gui, Add, ComboBox, x92 y489 w50 h20 vEveryMinutes, ComboBox
Gui, Add, Text, x102 y459 w130 h20 +Center, Frequency
Gui, Add, Text, x32 y489 w60 h20 +Center , Every
Gui, Add, Text, x142 y489 w40 h20 +Center, to
Gui, Add, ComboBox, x182 y489 w50 h21 , ComboBox
Gui, Add, Text, x232 y489 w60 h20 +Center, Minutes

Gui, Add, Text, x32 y549 w60 h20 +Center, For
Gui, Add, Text, x102 y519 w130 h20 +Center, Duration
Gui, Add, ComboBox, x92 y549 w50 h21 , ComboBox
Gui, Add, Text, x142 y549 w40 h20 +Center, to
Gui, Add, ComboBox, x182 y549 w50 h21 , ComboBox
Gui, Add, Text, x232 y549 w60 h20 +Center, Minutes

Gui, Add, Text, x122 y29 w100 h20 +Center, version %version%
; Generated using SmartGUI Creator 4.0
Gui, Show, x794 y267 h592 w348, 
Return

ButtonSTART:
Gui, Submit, NoHide
;Undock()
msgbox, %EveryMinutes%
Return

ButtonSTOP:
ListLines
Return

ButtonView:
msgbox %test%

test:
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

GuiClose:
ExitApp