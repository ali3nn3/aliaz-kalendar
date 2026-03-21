import asyncio
from playwright.async_api import async_playwright
import os

# --- KONFIGURACE ---
# Vlož sem URL tvého nasazeného Google Apps Scriptu (končící na /exec)
URL_GOOGLE_SCRIPTU = "https://script.google.com/macros/s/AKfycbxCqK-2hycXEZY6Mgrboq_iHt0Cf3rjhu9SzDuvQmsJq58U1bAQ3S6e9MQfE761nb1w/exec" 
# Najde absolutní cestu k aktuálnímu adresáři, kde běží skript
current_dir = os.path.dirname(os.path.abspath(__file__))
VYSTUPNI_SOUBOR = os.path.join(current_dir, "kalendar.png")
SIRKA = 800
# Vyfotíme trochu víc na výšku, abychom měli co ořezávat
VYSKA_VYFOCENI = 650 
# Finální rozměry pro PocketBook
SIRKA_FINÁLNÍ = 800
VYSKA_FINÁLNÍ = 600
# Kolik pixelů odshora oříznout (výška proužku + rezerva)
ORIZNUTE_ODSHORA = 50
# -------------------

async def make_screenshot():
    async with async_playwright() as p:
        # Spustíme prohlížeč (Chromium) v "headless" režimu (bez okna)
        browser = await p.chromium.launch()
        
        # Nastavíme velikost okna odpovídající displeji PocketBooku
        page = await browser.new_page(viewport={'width': SIRKA, 'height': VYSKA_VYFOCENI})
        
        print(f"Otevírám URL: {URL_GOOGLE_SCRIPTU}")
        # Přejdeme na URL a počkáme, až se načte síťový provoz (networkidle)
        await page.goto(URL_GOOGLE_SCRIPTU, wait_until="networkidle")
        
        # Volitelné: Počkáme ještě chvíli pro jistotu (např. 2 sekundy)
        await page.wait_for_timeout(2000)

        # ------------------------------------------------------------

        ### SKRÝT GOOGLE UPOZORNĚNÍ (AGRESIVNÍ VERZE) ###
        # Tento kód se pokusí najít a skrýt všechny podezřelé elementy.
        try:
            # Selektory pro různé verze Google proužku:
            # 1. Standardní CSS třída
            # 2. Jakýkoliv div s vysokým z-indexem (často používaný pro překryvy)
            # 3. Jakýkoliv iframe, který není v body (často používaný pro proužky)
            css_to_hide = """
                .apps-script-developer-banner { display: none !important; }
                iframe[src*="google.com/macros/static"] { display: none !important; }
                div[style*="z-index"] { display: none !important; }
                body > iframe { display: none !important; }
            """
            await page.add_style_tag(content=css_to_hide)
            print("Pokus o skrytí Google proužku (agresivní selektory).")
            
            # Volitelné: Počkáme sekundu, aby se změna projevila
            await page.wait_for_timeout(1000)
            
        except Exception as e:
            print(f"Nepodařilo se skrýt Google proužek: {e}")

        # ------------------------------------------------------------

        print(f"Dělám screenshot a ořezávám...")
        # Vyfotíme jen viditelnou část (ne full_page), ale s větší výškou
        # Poté ořízneme horní část (ORIZNUTE_ODSHORA)
        # a zbytek bude mít rozměr [SIRKA_FINÁLNÍ x VYSKA_FINÁLNÍ]
        await page.screenshot(
            path=VYSTUPNI_SOUBOR,
            full_page=False,
            clip={
                'x': 0,
                'y': ORIZNUTE_ODSHORA,
                'width': SIRKA_FINÁLNÍ,
                'height': VYSKA_FINÁLNÍ
            }
        )
        
        await browser.close()
        print("Hotovo.")

if __name__ == "__main__":
    asyncio.run(make_screenshot())
