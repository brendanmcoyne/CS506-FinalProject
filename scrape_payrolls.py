import requests
from bs4 import BeautifulSoup
import csv
import re

URL = "https://www.stevetheump.com/Payrolls.htm"
OUTPUT_CSV = "mlb_2001_payrolls.csv"

def clean_money(s):
    """Remove extra characters and ensure proper format."""
    s = s.strip()
    s = s.replace(u'\xa0', '')  # remove non-breaking spaces
    s = re.sub(r'[^0-9$.,]', '', s)
    return s

def scrape_2001_payrolls():
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all <pre> blocks; payrolls are inside
    pre_blocks = soup.find_all('pre')
    
    payroll_lines = []
    for block in pre_blocks:
        text = block.get_text()
        # Grab the 2001 section only
        if "2001 Opening Day Payrolls" in text:
            lines = text.splitlines()
            start = False
            for line in lines:
                if "2001 Opening Day Payrolls" in line:
                    start = True
                    continue
                if start:
                    if not line.strip():  # skip empty lines
                        continue
                    payroll_lines.append(line.strip())
            break

    # Parse lines
    rows = []
    for idx, line in enumerate(payroll_lines):
        # Skip headers
        if 'Team' in line and 'Payroll' in line:
            continue
        # Remove rank numbers and colons
        line = re.sub(r'^\d+\s*[:.]?\s*', '', line)
        parts = re.split(r'\s{2,}', line)  # split by 2+ spaces
        if len(parts) >= 3:
            team = parts[0].replace(':', '').strip()
            payroll = clean_money(parts[1])
            avg = clean_money(parts[2])
            rows.append([idx + 1, team, payroll, avg])

    # Write CSV
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Rank', 'Team', 'Payroll', 'Average'])
        writer.writerows(rows)

    print(f"Scraped {len(rows)} teams for 2001. Saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    scrape_2001_payrolls()
