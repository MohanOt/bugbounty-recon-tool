import os
import subprocess
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

target = input("Enter target domain: ")

# Subdomain enumeration
print("[*] Finding subdomains...")
subdomains_file = "reports/subdomains.txt"
os.system(f"subfinder -d {target} -o {subdomains_file}")

# Checking live hosts
print("[*] Checking live hosts...")
live_file = "reports/live_subdomains.txt"
os.system(f"cat {subdomains_file} | httpx -silent > {live_file}")
# Vulnerability scanning
print("[*] Running Nuclei scans...")
os.system(f"nuclei -l {live_file} -o reports/vulnerabilities.txt")

# Take screenshots
print("[*] Taking screenshots of live hosts...")
options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

with open(live_file) as f:
    for url in f.read().splitlines():
        try:
            driver.get("http://" + url)
            time.sleep(2)
            screenshot_file = f"screenshots/{url.replace('.', '_')}.png"
            driver.save_screenshot(screenshot_file)
            print(f"[+] Screenshot saved: {screenshot_file}")
        except Exception as e:
            print(f"[-] Could not capture {url}: {e}")

driver.quit()
print("[*] Recon complete!")