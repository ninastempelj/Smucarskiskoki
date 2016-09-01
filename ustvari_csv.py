import re
import orodja

def uredi_ime(oseba):
    # ŠTEMPELJ Novak Nina  -> Štempelj Novak Nina
    # ŠTEMPELJ-NOVAK Nina -> Štempelj-Novak Nina
    ime = oseba.split()
    nime = ''
    for imek in ime:
        nimek = ''
        for priimek in imek.split(sep = '-'):
            priimek = priimek[0] + priimek[1:].lower()
            nimek += '-' + priimek
        nime += ' ' + nimek[1:]
    return nime[1:]

def povprecje(a,b):
    # izracuna povprečje dveh števil, ki sta podani kot niz, drugi je
    # lahko prazen niz, in vrne niz v katerem je zapisano število
    if b == '':
        return a
    return str((float(a) + float(b))/2)
    
########## Ta del kode ustvari csv datoteke ##################    
tekme = orodja.datoteke('podatki/tekme')
idtekme = re.compile(r'<input type="hidden" name="raceid" id="raceid" value="(?P<id_tekme>\d{4})"/>')
vzorec_tekme = re.compile(r'<div class="padding-content">\s*<h3>\s*.*?<a href='\
                          r'".*?place=(?P<id_prizorisca>.*?)&gender=.*?">(?P<prizorisce>.*?)</a>\s*\((?P<drzava>\w{3})\)\s*<.*?">(?P<datum>\d\d\.\d\d.\d\d\d\d)</span>[\S\s]*?'
                          r'<div class="right text-right">Race codex')

vzorec_tekmovalca = re.compile(r'<td class=.i\d. align=.right.>&nbsp;(?P<uvrstitev>([12]?\d)|(30))</td>\s'\
                               r'<td .*?</td>\s'\
                               r'<td class=.i\d. align=.right.>&nbsp;(?P<id_tekmovalca>\d+?)</td>\s'\
                               r'<td class=.i\d.><a href=".*?">(?P<ime>.*?)</a>&nbsp;</td>\s'\
                               r'<td class=.*?>(?P<letnica>\d+?)&nbsp;</td>\s'\
                               r'<td class=.*?>(?P<nacionalnost>\w+?)&nbsp;</td>\s'\
                               r'<td class=.*?>&nbsp;(?P<dolzina1>.*?)</td>\s'\
                               r'<td .*?</td>\s<td class=.*?>&nbsp;(?P<dolzina2>.*?)</td>\s'\
                               r'<td .*?</td>\s<td class=.*?>&nbsp;(?P<tocke>.*?)</td>')

tekmovalci, prizorisca = {}, {}
uvrstitve, tekmovanja = [], []

for tekma in tekme:
    for opis in re.finditer(vzorec_tekme, orodja.vsebina_datoteke(tekma)): # na vsaki strani bo le eno ujemanje
        ta_tekma = re.findall(idtekme, orodja.vsebina_datoteke(tekma))[0]
        podatki_tekma = opis.groupdict()
        podatki_tekma['id_tekme']= (ta_tekma)
        podatki_tekma['id_prizorisca'] = podatki_tekma['id_prizorisca'][:5]
        podatki_tekma['sezona'] = tekma.split(sep = '_')[1][0:4]
        ime_prizorisca = podatki_tekma.pop('prizorisce')
        drzava_prizorisca = podatki_tekma.pop('drzava')
        prizorisca[podatki_tekma['id_prizorisca']] = {'id_prizorisca' : podatki_tekma['id_prizorisca'],
                                                'kraj' : ime_prizorisca,
                                                'država': drzava_prizorisca
                                                }

    tekmovanja += [podatki_tekma]

    for tekmovalec in re.finditer(vzorec_tekmovalca, orodja.vsebina_datoteke(tekma)):
        mesto = tekmovalec.groupdict()
        id_cloveka = mesto['id_tekmovalca']
        ime_cloveka = mesto.pop('ime')
        letnica_cloveka = mesto.pop('letnica')
        nacionalnost_cloveka = mesto.pop('nacionalnost')

        tekmovalci[id_cloveka] = {'id_tekmovalca' : id_cloveka,
                                  'ime' : uredi_ime(ime_cloveka),
                                  'nacionalnost' : nacionalnost_cloveka
                                  'letnica' : letnica_cloveka
                                  }
        mesto['id_tekme'] = ta_tekma
        uvrstitve += [mesto]

idji_tek = list(tekmovalci)
seznam_slovarjev_tekmovalcev =[tekmovalci[idjek] for idjek in idji_tek]

idji_priz = list(prizorisca)
seznam_slovarjev_prizorisc =[prizorisca[idjek] for idjek in idji_priz]


orodja.zapisi_tabelo(seznam_slovarjev_tekmovalcev, ['id_tekmovalca', 'ime', 'nacionalnost', 'letnica'], 'podatki/csv_tekmovalci.csv')
orodja.zapisi_tabelo(uvrstitve,['id_tekme', 'id_tekmovalca', 'uvrstitev', 'dolzina1', 'dolzina2', 'tocke'], 'podatki/csv_uvrstitve.csv')
orodja.zapisi_tabelo(tekmovanja,['id_tekme', 'id_prizorisca', 'datum', 'sezona'], 'podatki/csv_tekmovanja.csv')
orodja.zapisi_tabelo(seznam_slovarjev_prizorisc, ['id_prizorisca', 'kraj', 'država'], 'podatki/csv_prizorisca.csv')           
