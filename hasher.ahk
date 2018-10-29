﻿#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.


SetBatchLines, -1

;DllCall("QueryPerformanceFrequency", "int64P", perffreq)
;DllCall("QueryPerformanceCounter", "int64P", perfcount0)

sData := "testtesttest1"
sHash := Hash(sData, StrLen(sData))

;DllCall("QueryPerformanceCounter", "int64P", perfcount1)
;MsgBox % (perfcount1 - perfcount0) / perffreq

MsgBox % sHash


Hash(ByRef sData, nLen, SID = 4)	; SID: 3 for MD5, 4 for SHA
{
	DllCall("advapi32\CryptAcquireContextA", "UintP", hProv, "Uint", 0, "Uint", 0, "Uint", 1, "Uint", 0xF0000000)
	DllCall("advapi32\CryptCreateHash", "Uint", hProv, "Uint", 0x8000|0|SID , "Uint", 0, "Uint", 0, "UintP", hHash)

	DllCall("advapi32\CryptHashData", "Uint", hHash, "Uint", &sData, "Uint", nLen, "Uint", 0)

	DllCall("advapi32\CryptGetHashParam", "Uint", hHash, "Uint", 2, "Uint", 0, "UintP", nSize, "Uint", 0)
	VarSetCapacity(HashVal, nSize, 0)
	DllCall("advapi32\CryptGetHashParam", "Uint", hHash, "Uint", 2, "Uint", &HashVal, "UintP", nSize, "Uint", 0)

	DllCall("advapi32\CryptDestroyHash", "Uint", hHash)
	DllCall("advapi32\CryptReleaseContext", "Uint", hProv, "Uint", 0)

	SetFormat, Integer, H
	Loop, %nSize%
	{
	nValue := *(&HashVal + A_Index - 1)
	StringReplace, nValue, nValue, 0x, % (nValue < 16 ? 0 :)
	sHash .= nValue
	}

	Return sHash
}