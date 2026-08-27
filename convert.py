import re
import urllib.request

# Nastavenie správnej URL adresy pre zdroj
EASYLIST_URL = "https://raw.githubusercontent.com/tomasko126/easylistczechandslovak/master/filters.txt"
OUTPUT_FILE = "cz-sk-adlist.txt"

def main():
    # Opravený print príkaz (premenná EASYLIST_URL je správne dosadená do reťazca)
    print(f"Sťahujem EasyList z: {EASYLIST_URL}")
    try:
        req = urllib.request.Request(EASYLIST_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Chyba pri sťahovaní: {e}")
        return

    domains = set()
    # Regulárny výraz, ktorý hľadá zápis ||domena.sk^
    pattern = re.compile(r"^\|\|([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\^")

    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('!') or line.startswith('['):
            continue
            
        match = pattern.match(line)
        if match:
            domain = match.group(1).lower()
            # Vyradenie IP adries z adlistu
            if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", domain):
                domains.add(domain)

    # Zápis vyčistených domén do súboru
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for domain in sorted(domains):
            f.write(f"0.0.0.0 {domain}\n")

    print(f"Hotovo. Úspešne uložených {len(domains)} domén.")

if __name__ == "__main__":
    main()
