from pprint import pprint
import os
import csv
import sys
import bs4
import requests
from bs4 import BeautifulSoup

global url


def polivka(odkaz: str) -> BeautifulSoup:
	"""
	Funkce posila dotaz na server pomoci odkazu zadaneho v prvnim parametru fce main().
	Funkce vraci objekt BeautifulSoup.
	"""
	response = requests.get(odkaz)
	return BeautifulSoup(response.text, 'html.parser')


def seznam_vsech_obci() -> list:
	"""
	Fuknce vyuziva nekolika funkci:
	pomoci polivka() skrapuje stranku, jejiz odkaz byl zadan v prvnim argumentu fce main();
	extrahuj_kody_obci() vytvori seznam kodu vsech obci;
	extrahuj_nazvy_obci() vytvori seznam nazvu vsech obci;
	extrahuj_odkazy_obci() vytvori seznam odkazu, ktere se budou pouzivat dal.
	Nakonec se vse zazipuje do jednoho seznamu.
	"""
	global url
	url = sys.argv[1]  # 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103'
	parsed_soup = polivka(url)

	kod_obce = extrahuj_kody_obci(parsed_soup)
	# pprint(kod_obce)
	nazev_obce = extrahuj_nazvy_obci(parsed_soup)
	# pprint(nazev_obce)
	odkazy_na_obce = extrahuj_odkazy_obci(parsed_soup)
	# pprint(odkazy_na_obce)
	return list(zip(kod_obce, nazev_obce, odkazy_na_obce))


def vsechny_td_tagy(soup: bs4.BeautifulSoup, *args) -> list:
	"""
	Vstup je parsed_soup a stringy, ktere charakterizuji hodnoty atributu headers pro tabulky, napr:
	tabulka 1 => 't1sa1 t1sb1',
	tabulka 2 => 't2sa1 t2sb1',
	tabulka 3 => 't3sa1 t3sb1'  a tak dal...
	https://www.w3schools.com/cssref/css_selectors.asp
	Vraci list vsech td radku.
	"""
	radky = []
	for arg in args:
		radky += soup.select(f'td[headers="{arg}"]')
	return radky


def extrahuj_kody_obci(soup: bs4.BeautifulSoup) -> list:
	"""
	Vstup fce je parsed_soup.
	Pomoci fce vsechny_td_tagy projdeme vsechny radky a ty, ktere maji a_tag, ulozime do listu.
	Vytahneme pouze jejich popis pomoci .text
	Vraci list kodu vsech obci.
	"""
	radky = vsechny_td_tagy(soup, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')
	# kody_obci = []
	# for td in radky:
	# 	if td.find('a'):
	# 		kody_obci.append(td.find('a').text)
	# return kody_obci
	# list comprehension
	return [td.find('a').text for td in radky if td.find('a')]


def extrahuj_nazvy_obci(soup: bs4.BeautifulSoup) -> list:
	"""
	Vstup fce je parsed_soup
	Pomoci fce vsechny_td_tagy projdeme vsechny radky a vypiseme jejich jmena.
	Vytahneme pouze jejich popis pomoci .text
	Vraci list nazvu vsech obci.
	"""
	radky = vsechny_td_tagy(soup, 't1sa1 t1sb2', 't2sa1 t2sb2', 't3sa1 t3sb2')
	# nazvy = []
	# for td in radky:
	# 	nazvy.append(td.text)
	# return nazvy
	# list comprehension
	return [td.text for td in radky]


def extrahuj_odkazy_obci(soup: bs4.BeautifulSoup) -> list:
	"""
	Vstup fce je parsed_soup
	Pomoci fce vsechny_td_tagy projdeme vsechny radky a ty, ktere maji a_tag, ulozime do listu.
	Chceme ale jejich hodnotu atributu href.
	Vraci list odkazu na vsechny obce.
	"""
	radky = vsechny_td_tagy(soup, 't1sa1 t1sb1', 't2sa1 t2sb1', 't3sa1 t3sb1')
	# odkazy = []
	# for td in radky:
	# 	if td.find('a')
	# 		odkazy.append(td.find('a').get('href'))
	# return odkazy
	# list comprehension
	return [td.find('a').get('href') for td in radky if td.find('a')]


def volici_obalky_hlasy(soup) -> list:
	"""
	Vstup fce je parsed_soup
	Podle hlavicek najde hodnoty pro Volice, Obalky a Hlasy.
	Vraci list s hodnotami pro Volice, Obalky a Hlasy.
	"""
	headers = ['sa2', 'sa3', 'sa6']
	v_o_h = []
	for header in headers:
		hodnota = soup.find('td', {'headers': f'{header}'})
		#  POZOR na ValueError: invalid literal for int() with base 10: '1\xa0224'
		hodnota = hodnota.text.replace('\xa0', '')  # nahrazuje mezeru za tisicovkou
		v_o_h.append(int(hodnota))
	return v_o_h


def hlasy_pro_stranu(soup) -> list:
	"""
	Vstupem fce je soup.
	Pomoci fce vsechny_td_tagy projdeme radky a vybereme hodnoty podle hlavicek.
	Vraci list s pocty platnych hlasu.
	"""
	radky = vsechny_td_tagy(soup, 't1sa2 t1sb3', 't2sa2 t2sb3')
	# pocty_hlasu = []
	# for td in radky:
	# 	if td.text != '-':
	# 		td = td.text.replace('\xa0', '')
	# 		pocty_hlasu.append(int(td.text))
	# return pocty_hlasu
	# list comprehension
	return [(int(td.text.replace('\xa0', ''))) for td in radky if td.text != '-']


def spoj_vysledky(soup) -> list:
	"""
	Vstupem fce je soup.
	Spoji listy s vysledky pro Volice, Obalky, Hlasy a Hlasy pro strany.
	Vraci list.
	"""
	return volici_obalky_hlasy(soup) + hlasy_pro_stranu(soup)


def extrahuj_jmena_stran(soup) -> list:
	"""
	Vstupem fce je soup.
	Pomoci fce vsechny_td_tagy projdeme radky a vybereme hodnoty podle hlavicek.
	Hledame jmena polit. stran. Metodou .text ziskame nazvy.
	Vraci list se jmen polit. stran.
	"""
	radky = vsechny_td_tagy(soup, 't1sa1 t1sb2', 't2sa1 t2sb2')
	# list comprehension
	return [td.text for td in radky if td.text != '-']


def hlavicka(soup) -> list:
	"""
	Vstupem fce je soup.
	Spoji listy hlavicka1 a hlavicka2.
	Vraci list.
	"""
	hlavicka1 = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
	hlavicka2 = extrahuj_jmena_stran(soup)
	return hlavicka1 + hlavicka2


def zapis_csv_souboru(kody_nazvy_odkazy) -> csv:
	"""
	Vstupem fce je list kodu, nazvu a odkazu obci.
	Funkce zapisuje do csv souboru data vyskrapovana ze zadane adresy v 1. argumentu fce main()
	a naslednych odkazech na obce.
	Vraci csv soubor pojmenovany podle druheho argumentu fce main().
	"""
	jmeno_souboru = sys.argv[2]
	url_odkaz = 'https://www.volby.cz/pls/ps2017nss/' + kody_nazvy_odkazy[0][2]
	odkaz_soup = polivka(url_odkaz)
	csv_hlavicka = hlavicka(odkaz_soup)

	# kontrolni printy, jestli funkce vraci pozadovane vystupy.
	# print(volici_obalky_hlasy(odkaz_soup))
	# print(hlasy_pro_stranu(odkaz_soup))
	# print(spoj_vysledky(odkaz_soup))
	# print(extrahuj_jmena_stran(odkaz_soup))

	with open(f'{jmeno_souboru}.csv', mode='w', encoding="UTF-8", newline='') as soubor:
		writer = csv.writer(soubor)
		writer.writerow(csv_hlavicka)
		counter = 0
		soucet_obci = len(kody_nazvy_odkazy)
		for polozka_v_seznamu in kody_nazvy_odkazy:
			kolecko(counter)
			print(f'{(counter/soucet_obci*100):.0f} % VYSLEDKU ULOZENO')
			url2 = 'https://www.volby.cz/pls/ps2017nss/' + polozka_v_seznamu[2]
			soup = polivka(url2)
			results = spoj_vysledky(soup)
			writer.writerow([polozka_v_seznamu[0], polozka_v_seznamu[1]] + results)
			counter += 1
			os.system('cls')
		finalni_zprava(counter, soucet_obci, jmeno_souboru)
		exit()


def finalni_zprava(counter, soucet_obci, jmeno_souboru):
	print(f'ULOZENO {(counter / soucet_obci * 100):.0f} % VYSLEDKU')
	print(f'Vsechny vysledky z adresy: \n{url}')
	print(f'Byly zapsany do souboru {jmeno_souboru}.csv')
	print()
	print('Ukoncuji program...')


def kolecko(counter: int) -> None:
	"""
	Jenom legracni fce na zobrazeni otacejiciho se "kolecka"
	pri zpracovavani dat :-D
	"""
	cisla = [cislo for cislo in range(0, 101)]
	znacky = ['|', '/', '--', '\\']
	znacky = znacky * 25
	znaky = dict(zip(cisla, znacky))
	print(f'{znaky[counter]:4} ZPRACOVAVAM DATA')


def main():
	"""
	HLAVNI FUNKCE
	Pri spusteni v terminalu vyzaduje dva argumenty:
	1. url stranky okresu, ktery chceme skrapovat
	2. jmeno souboru, ktery bude zapsan (bez koncovky).
	"""
	kody_nazvy_odkazy = seznam_vsech_obci()
	# pprint(kody_nazvy_odkazy)
	zapis_csv_souboru(kody_nazvy_odkazy)


if __name__ == '__main__':
	try:
		main()
	except Exception as exception:
		print(f'Vyskytl se problem typu {exception}, ukoncuji program...')
