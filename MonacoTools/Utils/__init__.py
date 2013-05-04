import _winreg as winreg

def filepath():
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
        "Software\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Steam App 113000")

    path = winreg.QueryValueEx(key, "InstallLocation")
    key.Close()
    return path[0]