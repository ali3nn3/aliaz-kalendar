import asyncio
from playwright.async_api import async_playwright
import os

# --- KONFIGURACE ---
# Vlož sem URL tvého nasazeného Google Apps Scriptu (končící na /exec)
URL_GOOGLE_SCRIPTU = "https://script.google.com/macros/s/AKfycbxCqK-2hycXEZY6Mgrboq_iHt0Cf3rjhu9SzDuvQmsJq58U1bAQ3S6e9MQfE761nb1w/exec" 
VYSTUPNI_SOUBOR = "kalendar.png"
SIRKA = 800
VYSKA = 600
# -------------------

async def make_screenshot():
    async with async_playwright() as p:
        # Spustíme prohlížeč (Chromium) v "headless" režimu (bez okna)
        browser = await p.chromium.launch()
        
        # Nastavíme velikost okna odpovídající displeji PocketBooku
        page = await browser.new_page(viewport={'width': SIRKA, 'height': VYSKA})
        
        print(f"Otevírám URL: {URL_GOOGLE_SCRIPTU}")
        # Přejdeme na URL a počkáme, až se načte síťový provoz (networkidle)
        # To je jistota, že se načetly všechny kalendáře z GAS.
        await page.goto(URL_GOOGLE_SCRIPTU, wait_until="networkidle")
        
        # Volitelné: Počkáme ještě chvíli pro jistotu (např. 2 sekundy)
        await page.wait_for_timeout(2000)

        print(f"Dělám screenshot do: {VYSTUPNI_SOUBOR}")
        # Uděláme screenshot. 'colorspace: "gray"' se pokusí o převod do šedi už v prohlížeči.
        await page.screenshot(path=VYSTUPNI_SOUBOR, full_page=False)
        
        await browser.close()
        print("Hotovo.")

if __name__ == "__main__":
    asyncio.run(make_screenshot())
