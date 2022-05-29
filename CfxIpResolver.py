import requests
import re
import os

request = None

class fivemServer():
    table = dict()
    def __init__(self,cfxlink):
        self.cfxlink = cfxlink

    def getIp(self):
        request = requests.get(f"https://cfx.re/join/{self.cfxlink}")
        ipWithHttp = request.headers["X-Citizenfx-Url"]
        ipWithNoHttp = re.sub(r'http://', '', ipWithHttp)
        ip = re.sub(r'/', '', ipWithNoHttp)
        self.ipPort = ip.split(":")
        return self.ipPort

    def getIpInfos(self):
        x = self.getIp()[0]
        request = requests.get(f"http://ip-api.com/json/{x}?fields=status,message,country,region,regionName,city,isp,org,as,asname")
        return request.json()

    def view(self):
        infos = self.getIpInfos()
        print(f"IP: " + self.ipPort[0])
        print(f"Port: " + self.ipPort[1])
        print(f"Locale: " + infos["city"] + "/" + infos["regionName"] +"/" +infos["country"])
        print(f"AS: " + infos["as"])
        print(f"ASName: " + infos["asname"])
        print(f"ISP: " + infos["isp"])
        print(f"Org: " + infos["org"] + "\n")
        y = input("Can you ping this server?\n1 - Yes\n2 - No\n~ ")
        if y == "1":
            clear()
            ping(self.ipPort[0])
        
def ping(ip):
    response = os.popen(f"ping {ip}").read()
    print(response)
    if "Received = 4" or "Recebido = 4" in response:
        print(f"[ONLINE] {ip} Ping Successful\n")
    else:
        print(f"[OFFLINE] {ip} Ping Unsuccessful\n")

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

clear()
r = ""
while r != "quit":
    r = input("1 - Query Server\n2 - Ping Server\n3 - Quit\n~ ")
    clear()
    if r == "1":
        cfxlink = input("Paste cfx.re link: ")
        server = fivemServer(cfxlink)
        server.view()
    elif r == "2":
        ip = input("Exemple: 127.0.0.1\nPaste IP with no port: ")
        ping(ip)
    elif r == "3":
        r = "quit"
