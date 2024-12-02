import random 
import string 
import requests 

import json
import time
import os

from colorama import Fore, init

class VmztGenUsernames:
  def __init__(self):
    with open("utils/config.json", "r", encoding="utf-8") as configFile:
        self.config = json.load(configFile)
        
        self.token = self.config.get("token")
        self.webhooks = self.config.get("webhooks")

    with open("utils/proxies.txt", "r", encoding="utf-8") as proxyFile:
       self.proxies = proxyFile.read().split("\n")

  def randomUsernames(self):
        option = random.choice(["letters", "letters_numbers"])

        if option == "letters":
            return ''.join(random.choices(string.ascii_letters, k=random.choice([2, 3, 4]))).lower()
        else:
            return ''.join(random.choices(string.ascii_letters + string.digits, k=random.choice([2, 3, 4]))).lower()

  def startGen(self):
      username = self.randomUsernames()
      proxy = random.choice(self.proxies)

      headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9171 Chrome/128.0.6613.186 Electron/32.2.2 Safari/537.36",
        "Authorization": f"{self.token}"
      }

      response = requests.post("https://discord.com/api/v9/unique-username/username-attempt-unauthed", headers=headers, proxies={ "http": f"http://{proxy}", "https": f"http://{proxy}" }, json={ "username": username }, timeout=1500)
      if response.status_code == 200:
        data = response.json()
        print(f"                {Fore.RESET}{Fore.CYAN}Username:{Fore.RESET} {username} | {Fore.RESET}{Fore.YELLOW}Used:{Fore.RESET} {data["taken"]}")

        if not data["taken"]:
          if len(username) == 2: 
             requests.post(f"{self.webhooks["twoLetters"]}", json={"content": f"<:pawibow:1273050862566244396> ・ **Username available (RARE TWO LETTERS @everyone):** `{username} | Found there: <t:{int(time.time())}:R>`"})
          elif len(username) == 3:
              requests.post(f"{self.webhooks["threeLetters"]}", json={"content": f"<:pawibow:1273050862566244396> ・ **Username available (RARE THREE LETTERS @everyone):** `{username}` | Found there: <t:{int(time.time())}:R>"})
          else:
            requests.post(f"{self.webhooks["fourLetters"]}", json={"content": f"<:vermelho_laco:1301760407584772117> ・ **Username available:** `{username}` | Found there: <t:{int(time.time())}:R>"})
        else:
          webhook = self.webhooks["wasntThisTime"] 
          if webhook == "" | webhook == "Webhook to send usernames NOT AVAILABLE (NOT REQUIRED)":
             pass
          else:
            requests.post(f"{webhook}", json={"content": f"<:raiva:1258822537542893698> ・ **It wasn't this time:** `{username}` | Found there: <t:{int(time.time())}:R>"})
          pass

if __name__ == "__main__":
  init(autoreset=True)
  os.system("title Vmzt Username Generator")
  os.system("cls")

  print(f"""{Fore.RESET}{Fore.LIGHTCYAN_EX}
          ██╗   ██╗███╗   ███╗███████╗████████╗    
          ██║   ██║████╗ ████║╚══███╔╝╚══██╔══╝    
          ██║   ██║██╔████╔██║  ███╔╝    ██║       
          ╚██╗ ██╔╝██║╚██╔╝██║ ███╔╝     ██║       
           ╚████╔╝ ██║ ╚═╝ ██║███████╗   ██║       
            ╚═══╝  ╚═╝     ╚═╝╚══════╝   ╚═╝      
        
           discord.gg/vmzt | discord.gg/painel
                @pgwl      |  @desenvolvedor
  """)
  print(f"                {Fore.RESET}{Fore.BLUE}[*] Starting process...")
  time.sleep(1)
  
  vmztGenInstance = VmztGenUsernames()
  print(f"                {Fore.RESET}{Fore.GREEN}[#] Started successfully...\n")

  while True:
    try: 
      vmztGenInstance.startGen()
    except Exception as e:
      print(f"                {Fore.RESET}{Fore.RED}[!] Process crashed, waiting 1 second and continuing...")

      time.sleep(1)
