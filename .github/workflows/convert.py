import re
import urllib.request

EASYLIST_URL = "https://githubusercontent.com"
OUTPUT_FILE = "cz-sk-adlist.txt"

def main():
    print(f"Sťahujem EasyList z: {EASYLIST_URL}")
    try:
        req = urllib.request.Request(EASYLIST_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Chyba pri sťahovaní: {e}")
        return

    domains = set()
    # Hľadáme pravidlá vo formáte ||domena.sk^ (kompatibilné s DNS blokovaním)
    pattern = re.compile(r"^\|\|([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\^")

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('!') or line.startswith('['):
            continue
            
        match = pattern.match(line)
        if match:
            domain = match.group(1).lower()
            # Ochrana pred zachytením IP adries alebo chybne parsovaných reťazcov
            if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
                domains.add(domain)

    # Uloženie očistených domén, každá na nový riadok
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for domain in sorted(domains):
            f.write(f"{domain}\n")

    print(f"Hotovo. Uložených {len(domains)} domén.")

if __name__ == "__main__":
    main()
