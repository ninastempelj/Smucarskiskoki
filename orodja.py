import csv
import os
import requests
import sys
import re


def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)


def shrani(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    try:
        print('Shranjujem {}...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding = 'utf8') as datoteka:
        datoteka.write(r.text)
        print('shranjeno!')

def shrani_tekmo(url, ime_datoteke, vsili_prenos=False):
    '''Vsebino strani na danem naslovu shrani v datoteko z danim imenom.'''
    # Med tekmami se pojavljajo tudi kvalifikacije, nekatere ženske tekme in ekipne tekme,
    # ki jih želim izbrisati, zato še ena funkcija
    try:
        print('Shranjujem {}...'.format(url), end='')
        sys.stdout.flush()
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')

    vzorec_prave = re.compile(r'<div class="padding-content">[\S\s]*?'
                                  r'<h4>\s*(?P<kvalifikacije>.*?) - Men.s(?P<ekipna> Team)? HS\d\d\d?'
                                  r'[\S\s]*?<div class="right text-right">Race codex : \d+?\s*?<br />')
    podatki = re.findall(vzorec_prave, r.text)
    if not ('World Cup', '') in podatki:
        print('Ni prava tekma za naš projekt.')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding = 'utf8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')

def vsebina_datoteke(ime_datoteke):
    '''Vrne niz z vsebino datoteke z danim imenom.'''
    with open(ime_datoteke, encoding = 'utf8') as datoteka:
        vsebina = datoteka.read()
    return vsebina


def datoteke(imenik):
    '''Vrne imena vseh datotek v danem imeniku skupaj z imenom imenika.'''
    return [os.path.join(imenik, datoteka) for datoteka in os.listdir(imenik)]


def zapisi_tabelo(slovarji, imena_polj, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding = 'utf8') as csv_dat:
        writer = csv.DictWriter(csv_dat, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)
