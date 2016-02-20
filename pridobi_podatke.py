import requests
import re
import orodja

for sezona in range(2006, 2017):
    r = requests.get('http://data.fis-ski.com/global-links/all-fis-results.html?place_search=&seasoncode_search={}&sector_search=JP&date_search=&gender_search=m&category_search=WC&codex_search=&nation_search=&disciplinecode_search=&date_from=01&search=Search&limit=50'.format(sezona))
    podatki = r.text
    linki=re.findall(r'\s*?<tr class="tr-sep">\s*?<td colspan="12">\s*?'
                     r'</td>\s*?</tr>\s*?<tr data-line="\d\d?">\s*?'
                     r'<td class="i\d status">\s*?<div class="wrapimg">'
                     r'<a class="sprite-tab btn-r tooltip" href="(.*?)" title='
                     r'"Results available"></a></div><div class="wrapimg">'
                     , podatki)
        # v seznamu linki so shranjeni linki do posameznih tekem,
        # ki pa jih bo treba še vsakega odpreti
    vse_tekme = []
    for link in linki:
        s = requests.get(link)
        izberi = s.text # iz teh spletnih strani moramo sedaj pobrati povezavo do pravih razultatov
        izberi.replace('\'', '"',)
        vse_tekme += re.findall(r"""<td class='i\d'align="left"><span class='txt-blue'><a href="(.*?)">.*?</a></span>""", izberi)
    for i in range(len(vse_tekme)):
        orodja.shrani_tekmo(vse_tekme[i], 'podatki/tekme/tekma{}_{}.html'.format(i,sezona))

        
