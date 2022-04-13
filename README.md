Engeto Project 3 — Elections Scraper

Tento program stahuje výsledky voleb pro vybrané území (okres) a ukládá je do csv souboru.
<br>

1. Instalace requirements

- v preferovaném IDE nainstalujte potřebné knihovny ze souboru requirements.txt 
- případně pomocí příkazového řádku zapište příkaz `pip install requests` a `pip install beautifulsoup4`
- pokud to v příkazovém řádku nefunguje, zkuste zapsat v altermativním tvaru:
  - `pip3 install beautifulsoup4`
  - `python -m pip install beautifulsoup4`
  - `python3 -m pip3 install beautifulsoup4`

2. Spuštění programu

Program se spouští pomocí souboru main.py. Pro bezproblémové spuštění a vygenerování csv souboru 
jsou na vstupu vyžadovány dva argumenty.
1. odkaz na stránku, ze které se bude skrapovat;
2. jméno souboru, do kterého se zapíší výsledky (bez koncovky)

Oba argumenty musí být zapsány ve formě stringu.

*POZN.: pokud spouštíme program v příkazovém řádku, je třeba použít dvojité uvozovky namísto jednoduchých.*

3. Výstup

V souboru (zadané_jméno).csv naleznete uložená data.

Ukázka spuštění programu

Do terminálu napište:<br>
python main.py 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103' 'Prostejov'
<br>

Do příkazového řádku (cmd) napište:<br>
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "Prostejov"
<br>
