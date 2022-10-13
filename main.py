from discord_webhook import DiscordWebhook, DiscordEmbed
from colorama import Fore
import threading, yaml, random, string, requests, ctypes

config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)

def log(msg):
    print(msg)

invalid = 0
valid = 0
shit = 0

class checker:
    def __init__(self):
        try:
            self.session = requests.Session()
            self.webhook = config["webhook"]
            self.proxyless = config["proxyless"]
            self.success = open("./output/valid.txt", 'a')
            self.invalid = open("./output/invalid.txt", 'a')
            self.webhook = DiscordWebhook(url=config["webhook"])
            self.threads = config["threads"]
        except StopIteration:
            log("No proxies, try proxyless mode")

    def gen(self):
        while True:
            global invalid, valid, shit
            ctypes.windll.kernel32.SetConsoleTitleW(f"Total: {valid + invalid} | Valid: {valid} | Invalid: {invalid} | Shit Proxies: {shit}")
            try:
                proxies = random.choice(open("proxies.txt", "r").read().splitlines())
                code = ''.join(random.choices((string.digits + string.ascii_letters), k=16))#random.randint(12, 18)))
                gift = f"https://discord.gift/{code}"
                r = self.session.get(f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true", proxies=None if self.proxyless else {'http': f'http://{proxies}', 'https': f'http://{proxies}'})
                if r.status_code == 200:
                    log(f"{Fore.GREEN}Valid Code: {gift}")
                    self.success.write(gift + '\n')
                    self.webhook.add_embed(DiscordEmbed(title="New hit", description=gift))
                    self.webhook.execute()
                    valid += 1
                if r.status_code == 429:
                    log(f"{Fore.YELLOW}Ratelimited, please use proxies")
                    break
                else:
                    log(f"{Fore.RED}Invalid Code {gift}")
                    self.invalid.write(gift + '\n')
                    invalid += 1
            except OSError:
                print('bad proxy: '+ proxies)
                shit += 1
                continue

    def main(self):
        for i in range(self.threads):
            threading.Thread(target=self.gen).start()
        
if __name__ == "__main__":
    checker().main()