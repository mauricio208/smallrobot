import requests
import time
import csv
import re
import string
# from flask import Flask,send_file,request
from bs4 import BeautifulSoup
# app = Flask(__name__)
session = requests.Session()
timeout = 180
import random

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
session.headers.update({'user-agent': ua})

# gio-botsupply
# bellaz1O

subMenuArray = {
        'https://www.danlon.dk/appl?menu1=2&menu2=1',
        'https://www.danlon.dk/appl?menu1=2&menu2=2',
        'https://www.danlon.dk/appl?menu1=2&menu2=3',
        'https://www.danlon.dk/appl?menu1=2&menu2=8',
        'https://www.danlon.dk/appl?menu1=2&menu2=4',
        'https://www.danlon.dk/appl?menu1=2&menu2=6',
        'https://www.danlon.dk/appl?menu1=2&menu2=7',
        'https://www.danlon.dk/appl?menu1=2&menu2=12',
        'https://www.danlon.dk/appl?menu1=2&menu2=26',
        'https://www.danlon.dk/appl?menu1=3&menu2=1',
        'https://www.danlon.dk/appl?menu1=3&menu2=2',
        'https://www.danlon.dk/appl?menu1=3&menu2=3',
        'https://www.danlon.dk/appl?menu1=3&menu2=4',
        'https://www.danlon.dk/appl?menu1=3&menu2=5',
        'https://www.danlon.dk/appl?menu1=3&menu2=6',
        'https://www.danlon.dk/appl?menu1=3&menu2=16',
        'https://www.danlon.dk/appl?menu1=3&menu2=7',
        'https://www.danlon.dk/appl?menu1=3&menu2=8',
        'https://www.danlon.dk/appl?menu1=3&menu2=9',
        'https://www.danlon.dk/appl?menu1=3&menu2=10',
        'https://www.danlon.dk/appl?menu1=3&menu2=11',
        'https://www.danlon.dk/appl?menu1=3&menu2=12',
        'https://www.danlon.dk/appl?menu1=3&menu2=13',
        'https://www.danlon.dk/appl?menu1=3&menu2=14',
        'https://www.danlon.dk/appl?menu1=3&menu2=15',
        'https://www.danlon.dk/appl?menu1=3&menu2=19',
        'https://www.danlon.dk/appl?menu1=3&menu2=17',
        'https://www.danlon.dk/appl?menu1=3&menu2=18',
}

# @app.route('/get_file', methods=['GET', 'POST'])
# def crawl():
#     username = request.args.get('username')
#     password = request.args.get('password')
#     file_path = start(username,password)
#     return send_file(file_path,mimetype='text/csv',attachment_filename='Output.csv',as_attachment=True)

def start(user_name,password):

    main_url = 'https://www.danlon.dk/'
    login_page = 'https://www.danlon.dk/log-ind/'

    response = session.get(main_url,timeout=timeout)
    if response.status_code == 200:

        time.sleep(2)

        response_login = session.get(login_page,timeout=timeout)
        if response_login.status_code == 200:

            time.sleep(2)

            login_post = session.post(
                url='https://www.danlon.dk/DanlonFront',
                data={
                    'BRUGERID':user_name,
                    'PASSWORD':password,
                    'op':'login'
                },
                timeout=timeout
            )
            if login_post.status_code == 200:
                
                time.sleep(4)

                response_emp = session.get('https://www.danlon.dk/appl?menu1=2&menu2=1',timeout=timeout)
                if response_emp:
                    soup = BeautifulSoup(response_emp.text, 'html.parser')
                    select = soup.find(id='EmployeeSelectorForm_selection')
                    count = len(select.find_all('option'))

                    
                    time.sleep(3)
                    
                    results = list()

                    for i in range(2,count + 2):

                        response_select = session.post(
                            url='https://www.danlon.dk/appl',
                            data={
                                'command':'framework.MakeSelection',
                                'selector':'EmployeeSelector',
                                'selection':str(i)
                            },
                            timeout=timeout
                        )
                        if response_select.status_code == 200:
                            
                            time.sleep(3)

                            print("\tSuccess\n")

                            CT =''
                            for Submenu_Url in subMenuArray:
                                responseSub = session.get(Submenu_Url,timeout=timeout)
                                time.sleep(1)
                                if responseSub.status_code == 200:
                                    print("\tSuccess!..")
                                    print("\t\tURL: %s" % Submenu_Url)

                                    CT += responseSub.text + '<hr><hr><hr>'

                            # with open("CT-"+str(i)+".html",'at', encoding='utf-8') as FF:
                            #     FF.write(CT+'<hr><hr>')

                            NAVN = re.search(r'<input name="NAVN" value="([^"]+)"', CT, re.I|re.S)
                            if NAVN:
                                NAVN =NAVN.group(1)
                                print("NAVN: %s" % NAVN)
                                

                            ADRESSE1 = re.search(r'<input name="ADRESSE1" value="([^"]+)"', CT, re.I|re.S)
                            if ADRESSE1:
                                ADRESSE1 =ADRESSE1.group(1)
                                print("ADRESSE1: %s" % ADRESSE1)

                            ADRESSE2 = re.search(r'<input name="ADRESSE2" value="([^"]+)"', CT, re.I|re.S)
                            if ADRESSE2:
                                ADRESSE2 =ADRESSE2.group(1)
                                print("ADRESSE2: %s" % ADRESSE2)

                            POSTNUMMER = re.search(r'<input name="POSTNUMMER" value="([^"]+)"', CT, re.I|re.S)
                            if POSTNUMMER:
                                POSTNUMMER =POSTNUMMER.group(1)
                                print("POSTNUMMER: %s" % POSTNUMMER)

                            CITY = re.search(r'<input name="CITY" value="([^"]+)"', CT, re.I|re.S)
                            if CITY:
                                CITY =CITY.group(1)
                                print("CITY: %s" % CITY)

                            CPRNUMMER = re.search(r'<input type="hidden" name="CPRNUMMER" value="([^"]+)">', CT, re.I|re.S)
                            if CPRNUMMER:
                                CPRNUMMER =CPRNUMMER.group(1)
                                print("CPRNUMMER: %s" % CPRNUMMER)

                            REGNR = re.search(r'<input name="REGNR" value="([^"]+)"', CT, re.I|re.S)
                            if REGNR:
                                REGNR =REGNR.group(1)
                                print("REGNR: %s" % REGNR)

                            KONTONUMMER = re.search(r'<input name="KONTONUMMER" value="([^"]+)"', CT, re.I|re.S)
                            if KONTONUMMER:
                                KONTONUMMER =KONTONUMMER.group(1)
                                print("KONTONUMMER: %s" % KONTONUMMER)

                            BIC = re.search(r'<input name="BIC" value="([^"]+)"', CT, re.I|re.S)
                            if BIC:
                                BIC =BIC.group(1)
                                print("BIC: %s" % BIC)

                            IBAN = re.search(r'<input name="IBAN" value="([^"]+)"', CT, re.I|re.S)
                            if IBAN:
                                IBAN =IBAN.group(1)
                                print("IBAN: %s" % IBAN)

                            AKTIV = re.search(r'<input type="checkbox" name="AKTIV" tabindex="[^"]*" value="true" (checked) id="[^"]*">', CT, re.I|re.S)
                            if AKTIV:
                                AKTIV = "Checked"
                                print("AKTIV: %s" % AKTIV)
                            else:
                                AKTIV = "Not Checked"
                                print("AKTIV: %s" % AKTIV)

                            ANSATDATO = re.search(r'<input type="hidden" name="ANSATDATO" value="([^"]+)"', CT, re.I|re.S)
                            if ANSATDATO:
                                ANSATDATO =ANSATDATO.group(1)
                                print("ANSATDATO: %s" % ANSATDATO)

                            FRATRAADTDATO = re.search(r'<input name="FRATRAADTDATO" value="([^"]+)"', CT, re.I|re.S)
                            if FRATRAADTDATO:
                                FRATRAADTDATO =FRATRAADTDATO.group(1)
                                print("FRATRAADTDATO: %s" % FRATRAADTDATO)

                            TITEL = re.search(r'<input name="TITEL" value="([^"]+)"', CT, re.I|re.S)
                            if TITEL:
                                TITEL =TITEL.group(1)
                                print("TITEL: %s" % TITEL)

                            Ferieordning = re.search(r'>\s*Ferieordning\s*</a>\s*</p>\s*</td>\s*<td\s*>\s*<p class="noinput">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Ferieordning:
                                Ferieordning =Ferieordning.group(1)
                                print("Ferieordning: %s" % Ferieordning)

                            Feriepengemodtager = re.search(r'>\s*Feriepengemodtager\s*</a>\s*</p>\s*</td>\s*<td\s*>\s*<p class="noinput">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Feriepengemodtager:
                                Feriepengemodtager =Feriepengemodtager.group(1)
                                print("Feriepengemodtager: %s" % Feriepengemodtager)

                            Ferie_per_år = re.search(r'>\s*Ferie per &aring;r\s*</a>\s*</p>\s*</td>\s*<td\s*>\s*<p class="noinput">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Ferie_per_år:
                                Ferie_per_år =Ferie_per_år.group(1)
                                print("Ferie_per_år: %s" % Ferie_per_år)

                            Status_eIndkomst = re.search(r'>\s*Status eIndkomst\s*</a>\s*</p>\s*</td>\s*<td\s*>\s*<p class="noinput">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Status_eIndkomst:
                                Status_eIndkomst =Status_eIndkomst.group(1)
                                print("Status_eIndkomst: %s" % Status_eIndkomst)

                            PRODUKTIONSENHED = re.search(r'<input name="PRODUKTIONSENHED" value="([^"]+)"', CT, re.I|re.S)
                            if PRODUKTIONSENHED:
                                PRODUKTIONSENHED =PRODUKTIONSENHED.group(1)
                                print("PRODUKTIONSENHED: %s" % PRODUKTIONSENHED)

                            ANVENDREKLAME = re.search(r'<input type="checkbox" name="ANVENDREKLAME" tabindex="[^"]*" value="true" (checked)\s*id="[^"]*">', CT, re.I|re.S)
                            if ANVENDREKLAME:
                                ANVENDREKLAME ="Checked"
                                print("ANVENDREKLAME: %s" % ANVENDREKLAME)
                            else:
                                ANVENDREKLAME ="Not Checked"
                                print("ANVENDREKLAME: %s" % ANVENDREKLAME)

                            DanlønID = re.search(r'>\s*DanlÃ¸nID\s*</a>\s*</p>\s*</td>\s*<td\s*>\s*<p class="noinput">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if DanlønID:
                                DanlønID =DanlønID.group(1)
                                print("DanlønID: %s" % DanlønID)

                            TELEFON = re.search(r'<input name="TELEFON" value="([^"]+)"', CT, re.I|re.S)
                            if TELEFON:
                                TELEFON =TELEFON.group(1)
                                print("TELEFON: %s" % TELEFON)

                            MOBILTELEFON = re.search(r'<input name="MOBILTELEFON" value="([^"]+)"', CT, re.I|re.S)
                            if MOBILTELEFON:
                                MOBILTELEFON =MOBILTELEFON.group(1)
                                print("MOBILTELEFON: %s" % MOBILTELEFON)

                            EPOST = re.search(r'<input name="EPOST" value="([^"]+)"', CT, re.I|re.S)
                            if EPOST:
                                EPOST =EPOST.group(1)
                                print("EPOST: %s" % EPOST)

                            LOKALTELEFON = re.search(r'<input name="LOKALTELEFON" value="([^"]+)"', CT, re.I|re.S)
                            if LOKALTELEFON:
                                LOKALTELEFON =LOKALTELEFON.group(1)
                                print("LOKALTELEFON: %s" % LOKALTELEFON)

                            SENDNETTOLONSMS = re.search(r'<input type="checkbox" name="SENDNETTOLONSMS" tabindex="[^"]*" value="true" (checked)?\s*id="[^"]*">', CT, re.I|re.S)
                            if SENDNETTOLONSMS:
                                SENDNETTOLONSMS= "Checked"
                                print("SENDNETTOLONSMS: %s" % SENDNETTOLONSMS)
                            else:
                                SENDNETTOLONSMS= "Not Checked"
                                print("SENDNETTOLONSMS: %s" % SENDNETTOLONSMS)

                            SENDNETTOLONEPOST = re.search(r'<input type="checkbox" name="SENDNETTOLONEPOST" tabindex="[^"]*" value="true" (checked)?\s*id="[^"]*">', CT, re.I|re.S)
                            if SENDNETTOLONEPOST:
                                SENDNETTOLONEPOST= "Checked"
                                print("SENDNETTOLONEPOST: %s" % SENDNETTOLONEPOST)
                            else:
                                SENDNETTOLONEPOST= "Not Checked"
                                print("SENDNETTOLONEPOST: %s" % SENDNETTOLONEPOST)

                            FERIEPROCENT = re.search(r'<input name="FERIEPROCENT" value="([^"]+)"', CT, re.I|re.S)
                            if FERIEPROCENT:
                                FERIEPROCENT =FERIEPROCENT.group(1)
                                print("FERIEPROCENT: %s" % FERIEPROCENT)

                            FERIETILLAEGPROCENT = re.search(r'<input name="FERIETILLAEGPROCENT" value="([^"]+)"', CT, re.I|re.S)
                            if FERIETILLAEGPROCENT:
                                FERIETILLAEGPROCENT =FERIETILLAEGPROCENT.group(1)
                                print("FERIETILLAEGPROCENT: %s" % FERIETILLAEGPROCENT)

                            SHPROCENT = re.search(r'<input name="SHPROCENT" value="([^"]+)"', CT, re.I|re.S)
                            if SHPROCENT:
                                SHPROCENT =SHPROCENT.group(1)
                                print("SHPROCENT: %s" % SHPROCENT)

                            FRITVALGSPROCENT = re.search(r'<input name="FRITVALGSPROCENT" value="([^"]+)"', CT, re.I|re.S)
                            if FRITVALGSPROCENT:
                                FRITVALGSPROCENT =FRITVALGSPROCENT.group(1)
                                print("FRITVALGSPROCENT: %s" % FRITVALGSPROCENT)

                            Ferieoptjening = re.search(r'>\s*Ferieoptjening\s*</a>\s*</p>\s*</td>\s*<td\s*>\s*<p class="noinput">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Ferieoptjening:
                                Ferieoptjening =Ferieoptjening.group(1)
                                print("Ferieoptjening: %s" % Ferieoptjening)

                            Ferieregnskab_i = re.search(r'>\s*Ferieregnskab i\s*</a>\s*</p>\s*</td>\s*<td\s*>\s*<p class="noinput">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Ferieregnskab_i:
                                Ferieregnskab_i =Ferieregnskab_i.group(1)
                                print("Ferieregnskab_i: %s" % Ferieregnskab_i)

                            OMSORGSDAGEPRAAR = re.search(r'<input name="OMSORGSDAGEPRAAR" value="([^"]+)"', CT, re.I|re.S)
                            if OMSORGSDAGEPRAAR:
                                OMSORGSDAGEPRAAR =OMSORGSDAGEPRAAR.group(1)
                                print("OMSORGSDAGEPRAAR: %s" % OMSORGSDAGEPRAAR)

                            FERIEFRIDAGEPRAAR = re.search(r'<input name="FERIEFRIDAGEPRAAR" value="([^"]+)"', CT, re.I|re.S)
                            if FERIEFRIDAGEPRAAR:
                                FERIEFRIDAGEPRAAR =FERIEFRIDAGEPRAAR.group(1)
                                print("FERIEFRIDAGEPRAAR: %s" % FERIEFRIDAGEPRAAR)

                            EXTRATRAEKPROCENT = re.search(r'<input name="EXTRATRAEKPROCENT" value="([^"]+)"', CT, re.I|re.S)
                            if EXTRATRAEKPROCENT:
                                EXTRATRAEKPROCENT =EXTRATRAEKPROCENT.group(1)
                                print("EXTRATRAEKPROCENT: %s" % EXTRATRAEKPROCENT)

                            AM_indkomst = re.search(r'>\s*AM-indkomst\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if AM_indkomst:
                                AM_indkomst =AM_indkomst.group(1)
                                print("AM_indkomst: %s" % AM_indkomst)

                            Bidragsfri_A_indkomst = re.search(r'>\s*Bidragsfri A-indkomst\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Bidragsfri_A_indkomst:
                                Bidragsfri_A_indkomst =Bidragsfri_A_indkomst.group(1)
                                print("Bidragsfri_A_indkomst: %s" % Bidragsfri_A_indkomst)

                            Engangsindkomst = re.search(r'>\s*Engangsindkomst\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Engangsindkomst:
                                Engangsindkomst =Engangsindkomst.group(1)
                                print("Engangsindkomst: %s" % Engangsindkomst)

                            B_indkomst_uden_AM_bidrag = re.search(r'>\s*B-indkomst uden AM-bidrag\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if B_indkomst_uden_AM_bidrag:
                                B_indkomst_uden_AM_bidrag =B_indkomst_uden_AM_bidrag.group(1)
                                print("B_indkomst_uden_AM_bidrag: %s" % B_indkomst_uden_AM_bidrag)

                            B_indkomst_med_AM_bidrag = re.search(r'>\s*B-indkomst med AM-bidrag\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if B_indkomst_med_AM_bidrag:
                                B_indkomst_med_AM_bidrag =B_indkomst_med_AM_bidrag.group(1)
                                print("B_indkomst_med_AM_bidrag: %s" % B_indkomst_med_AM_bidrag)

                            Timer = re.search(r'>\s*Timer\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Timer:
                                Timer =Timer.group(1)
                                print("Timer: %s" % Timer)

                            ATP = re.search(r'>\s*ATP\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if ATP:
                                ATP =ATP.group(1)
                                print("ATP: %s" % ATP)

                            AM_bidrag = re.search(r'>\s*AM-bidrag\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if AM_bidrag:
                                AM_bidrag =AM_bidrag.group(1)
                                print("AM_bidrag: %s" % AM_bidrag)

                            A_skat = re.search(r'>\s*A-skat\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if A_skat:
                                A_skat =A_skat.group(1)
                                print("A_skat: %s" % A_skat)

                            Fri_bil = re.search(r'>\s*Fri bil\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Fri_bil:
                                Fri_bil =Fri_bil.group(1)
                                print("Fri_bil: %s" % Fri_bil)

                            Fri_kost_og_logi = re.search(r'>\s*Fri kost og logi\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Fri_kost_og_logi:
                                Fri_kost_og_logi =Fri_kost_og_logi.group(1)
                                print("Fri_kost_og_logi: %s" % Fri_kost_og_logi)

                            Fri_telefon = re.search(r'>\s*Fri telefon\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Fri_telefon:
                                Fri_telefon =Fri_telefon.group(1)
                                print("Fri_telefon: %s" % Fri_telefon)

                            Sundhedsforsikring = re.search(r'>\s*Sundhedsforsikring\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Sundhedsforsikring:
                                Sundhedsforsikring =Sundhedsforsikring.group(1)
                                print("Sundhedsforsikring: %s" % Sundhedsforsikring)

                            Antal_kilometer = re.search(r'>\s*Antal kilometer\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Antal_kilometer:
                                Antal_kilometer =Antal_kilometer.group(1)
                                print("Antal_kilometer: %s" % Antal_kilometer)

                            REJSEGODTGORELSE = re.search(r'>\s*RejsegodtgÃ¸relse\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if REJSEGODTGORELSE:
                                REJSEGODTGORELSE =REJSEGODTGORELSE.group(1)
                                print("REJSEGODTGORELSE: %s" % REJSEGODTGORELSE)

                            Eget_bidrag = re.search(r'>\s*Eget bidrag\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Eget_bidrag:
                                Eget_bidrag =Eget_bidrag.group(1)
                                print("Eget_bidrag: %s" % Eget_bidrag)

                            Firma_bidrag = re.search(r'>\s*Firma bidrag\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Firma_bidrag:
                                Firma_bidrag =Firma_bidrag.group(1)
                                print("Firma_bidrag: %s" % Firma_bidrag)

                            Eget_bidrag__AMP = re.search(r'>\s*Eget bidrag, AMP\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Eget_bidrag__AMP:
                                Eget_bidrag__AMP =Eget_bidrag__AMP.group(1)
                                print("Eget_bidrag__AMP: %s" % Eget_bidrag__AMP)

                            Firma_bidrag__AMP = re.search(r'>\s*Firma bidrag, AMP\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Firma_bidrag__AMP:
                                Firma_bidrag__AMP =Firma_bidrag__AMP.group(1)
                                print("Firma_bidrag__AMP: %s" % Firma_bidrag__AMP)

                            Gruppeliv = re.search(r'>\s*Gruppeliv\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Gruppeliv:
                                Gruppeliv =Gruppeliv.group(1)
                                print("Gruppeliv: %s" % Gruppeliv)

                            Gruppeliv__2 = re.search(r'>\s*Gruppeliv, 2\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Gruppeliv__2:
                                Gruppeliv__2 =Gruppeliv__2.group(1)
                                print("Gruppeliv__2: %s" % Gruppeliv__2)

                            Afholdte_G_dage = re.search(r'>\s*Afholdte G-dage\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Afholdte_G_dage:
                                Afholdte_G_dage =Afholdte_G_dage.group(1)
                                print("Afholdte_G_dage: %s" % Afholdte_G_dage)

                            Afholdte_omsorgsdage = re.search(r'>\s*Afholdte omsorgsdage\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Afholdte_omsorgsdage:
                                Afholdte_omsorgsdage =Afholdte_omsorgsdage.group(1)
                                print("Afholdte_omsorgsdage: %s" % Afholdte_omsorgsdage)

                            Afholdte_feriefridage = re.search(r'>\s*Afholdte feriefridage\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Afholdte_feriefridage:
                                Afholdte_feriefridage =Afholdte_feriefridage.group(1)
                                print("Afholdte_feriefridage: %s" % Afholdte_feriefridage)

                            Afspadsering__timer_til_gode = re.search(r'>\s*Afspadsering, timer til gode\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Afspadsering__timer_til_gode:
                                Afspadsering__timer_til_gode =Afspadsering__timer_til_gode.group(1)
                                print("Afspadsering__timer_til_gode: %s" % Afspadsering__timer_til_gode)

                            Afspadsering__beløb_til_gode = re.search(r'>\s*Afspadsering, belÃ¸b til gode\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Afspadsering__beløb_til_gode:
                                Afspadsering__beløb_til_gode =Afspadsering__beløb_til_gode.group(1)
                                print("Afspadsering__beløb_til_gode: %s" % Afspadsering__beløb_til_gode)

                            Flexsaldo = re.search(r'>\s*Flexsaldo\s*</a>\s*</p>\s*</td>\s*<td class="contentDetail-right">\s*([^<]*)\s*<', CT, re.I|re.S)
                            if Flexsaldo:
                                Flexsaldo =Flexsaldo.group(1)
                                print("Flexsaldo: %s" % Flexsaldo)

                            NORMTIMER = re.search(r'<input name="NORMTIMER" value="([^"]+)"', CT, re.I|re.S)
                            if NORMTIMER:
                                NORMTIMER =NORMTIMER.group(1)
                                print("NORMTIMER: %s" % NORMTIMER)

                            GAGE = re.search(r'<input name="GAGE" value="([^"]+)"', CT, re.I|re.S)
                            if GAGE:
                                GAGE =GAGE.group(1)
                                print("GAGE: %s" % GAGE)

                            PERSONLIGTTILLAEG = re.search(r'<input name="PERSONLIGTTILLAEG" value="([^"]+)"', CT, re.I|re.S)
                            if PERSONLIGTTILLAEG:
                                PERSONLIGTTILLAEG =PERSONLIGTTILLAEG.group(1)
                                print("PERSONLIGTTILLAEG: %s" % PERSONLIGTTILLAEG)

                            UGELON = re.search(r'<input name="UGELON" value="([^"]+)"', CT, re.I|re.S)
                            if UGELON:
                                UGELON =UGELON.group(1)
                                print("UGELON: %s" % UGELON)

                            KORSELSTILSKUD = re.search(r'<input name="KORSELSTILSKUD" value="([^"]+)"', CT, re.I|re.S)
                            if KORSELSTILSKUD:
                                KORSELSTILSKUD =KORSELSTILSKUD.group(1)
                                print("KORSELSTILSKUD: %s" % KORSELSTILSKUD)

                            TILLAEGFASTENHED1 = re.search(r'<input name="TILLAEGFASTENHED1" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTENHED1:
                                TILLAEGFASTENHED1 =TILLAEGFASTENHED1.group(1)
                                print("TILLAEGFASTENHED1: %s" % TILLAEGFASTENHED1)

                            TILLAEGFASTSATS1 = re.search(r'<input name="TILLAEGFASTSATS1" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTSATS1:
                                TILLAEGFASTSATS1 =TILLAEGFASTSATS1.group(1)
                                print("TILLAEGFASTSATS1: %s" % TILLAEGFASTSATS1)

                            TILLAEGFASTBELOB1 = re.search(r'<input name="TILLAEGFASTBELOB1" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTBELOB1:
                                TILLAEGFASTBELOB1 =TILLAEGFASTBELOB1.group(1)
                                print("TILLAEGFASTBELOB1: %s" % TILLAEGFASTBELOB1)

                            TILLAEGFASTENHED2 = re.search(r'<input name="TILLAEGFASTENHED2" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTENHED2:
                                TILLAEGFASTENHED2 =TILLAEGFASTENHED2.group(1)
                                print("TILLAEGFASTENHED2: %s" % TILLAEGFASTENHED2)

                            TILLAEGFASTSATS2 = re.search(r'<input name="TILLAEGFASTSATS2" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTSATS2:
                                TILLAEGFASTSATS2 =TILLAEGFASTSATS2.group(1)
                                print("TILLAEGFASTSATS2: %s" % TILLAEGFASTSATS2)

                            TILLAEGFASTBELOB2 = re.search(r'<input name="TILLAEGFASTBELOB2" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTBELOB2:
                                TILLAEGFASTBELOB2 =TILLAEGFASTBELOB2.group(1)
                                print("TILLAEGFASTBELOB2: %s" % TILLAEGFASTBELOB2)

                            TILLAEGFASTENHED3 = re.search(r'<input name="TILLAEGFASTENHED3" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTENHED3:
                                TILLAEGFASTENHED3 =TILLAEGFASTENHED3.group(1)
                                print("TILLAEGFASTENHED3: %s" % TILLAEGFASTENHED3)

                            TILLAEGFASTSATS3 = re.search(r'<input name="TILLAEGFASTSATS3" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTSATS3:
                                TILLAEGFASTSATS3 =TILLAEGFASTSATS3.group(1)
                                print("TILLAEGFASTSATS3: %s" % TILLAEGFASTSATS3)

                            TILLAEGFASTBELOB3 = re.search(r'<input name="TILLAEGFASTBELOB3" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTBELOB3:
                                TILLAEGFASTBELOB3 =TILLAEGFASTBELOB3.group(1)
                                print("TILLAEGFASTBELOB3: %s" % TILLAEGFASTBELOB3)

                            TILLAEGFASTENHED4 = re.search(r'<input name="TILLAEGFASTENHED4" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTENHED4:
                                TILLAEGFASTENHED4 =TILLAEGFASTENHED4.group(1)
                                print("TILLAEGFASTENHED4: %s" % TILLAEGFASTENHED4)

                            TILLAEGFASTSATS4 = re.search(r'<input name="TILLAEGFASTSATS4" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTSATS4:
                                TILLAEGFASTSATS4 =TILLAEGFASTSATS4.group(1)
                                print("TILLAEGFASTSATS4: %s" % TILLAEGFASTSATS4)

                            TILLAEGFASTBELOB4 = re.search(r'<input name="TILLAEGFASTBELOB4" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTBELOB4:
                                TILLAEGFASTBELOB4 =TILLAEGFASTBELOB4.group(1)
                                print("TILLAEGFASTBELOB4: %s" % TILLAEGFASTBELOB4)

                            TILLAEGFASTENHED5 = re.search(r'<input name="TILLAEGFASTENHED5" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTENHED5:
                                TILLAEGFASTENHED5 =TILLAEGFASTENHED5.group(1)
                                print("TILLAEGFASTENHED5: %s" % TILLAEGFASTENHED5)

                            TILLAEGFASTSATS5 = re.search(r'<input name="TILLAEGFASTSATS5" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTSATS5:
                                TILLAEGFASTSATS5 =TILLAEGFASTSATS5.group(1)
                                print("TILLAEGFASTSATS5: %s" % TILLAEGFASTSATS5)

                            TILLAEGFASTBELOB5 = re.search(r'<input name="TILLAEGFASTBELOB5" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGFASTBELOB5:
                                TILLAEGFASTBELOB5 =TILLAEGFASTBELOB5.group(1)
                                print("TILLAEGFASTBELOB5: %s" % TILLAEGFASTBELOB5)

                            Vis_lønafregning = re.search(r'<a href="appl[^"]+" title="Vis lÃ¸nafregning">\s*([^<]+)\s*</a>', CT, re.I|re.S)
                            if Vis_lønafregning:
                                Vis_lønafregning =Vis_lønafregning.group(1)
                                print("Vis_lønafregning: %s" % Vis_lønafregning)

                            ATP_af_løn = re.search(r'>\s*ATP af lÃ¸n\s*</p>\s*</td>\s*<td>\s*<p class="contentAmount">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if ATP_af_løn:
                                ATP_af_løn =ATP_af_løn.group(1)
                                print("ATP_af_løn: %s" % ATP_af_løn)

                            AM_indkomst = re.search(r'>\s*AM-indkomst\s*</p>\s*</td>\s*<td>\s*<p class="contentAmount">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if AM_indkomst:
                                AM_indkomst =AM_indkomst.group(1)
                                print("AM_indkomst: %s" % AM_indkomst)

                            AM_bidrag = re.search(r'>\s*AM-bidrag\s*</p>\s*</td>\s*<td>\s*<p class="contentAmount">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if AM_bidrag:
                                AM_bidrag =AM_bidrag.group(1)
                                print("AM_bidrag: %s" % AM_bidrag)

                            A_skat = re.search(r'>\s*A-skat\s*</p>\s*</td>\s*<td>\s*<p class="contentAmount">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if A_skat:
                                A_skat =A_skat.group(1)
                                print("A_skat: %s" % A_skat)

                            Til_udbetaling = re.search(r'>\s*Til udbetaling\s*</p>\s*</td>\s*<td>\s*<p class="contentAmount">\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Til_udbetaling:
                                Til_udbetaling =Til_udbetaling.group(1)
                                print("Til_udbetaling: %s" % Til_udbetaling)

                            FRADRAGFAST1 = re.search(r'<input name="FRADRAGFAST1" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGFAST1:
                                FRADRAGFAST1 =FRADRAGFAST1.group(1)
                                print("FRADRAGFAST1: %s" % FRADRAGFAST1)

                            FRADRAGFAST2 = re.search(r'<input name="FRADRAGFAST2" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGFAST2:
                                FRADRAGFAST2 =FRADRAGFAST2.group(1)
                                print("FRADRAGFAST2: %s" % FRADRAGFAST2)

                            FRADRAGFAST3 = re.search(r'<input name="FRADRAGFAST3" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGFAST3:
                                FRADRAGFAST3 =FRADRAGFAST3.group(1)
                                print("FRADRAGFAST3: %s" % FRADRAGFAST3)

                            FRADRAGFAST4 = re.search(r'<input name="FRADRAGFAST4" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGFAST4:
                                FRADRAGFAST4 =FRADRAGFAST4.group(1)
                                print("FRADRAGFAST4: %s" % FRADRAGFAST4)

                            FRADRAGFAST5 = re.search(r'<input name="FRADRAGFAST5" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGFAST5:
                                FRADRAGFAST5 =FRADRAGFAST5.group(1)
                                print("FRADRAGFAST5: %s" % FRADRAGFAST5)

                            TILLAEGPERIODEENHED1 = re.search(r'<input name="TILLAEGPERIODEENHED1" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEENHED1:
                                TILLAEGPERIODEENHED1 =TILLAEGPERIODEENHED1.group(1)
                                print("TILLAEGPERIODEENHED1: %s" % TILLAEGPERIODEENHED1)

                            TILLAEGPERIODESATS1 = re.search(r'<input name="TILLAEGPERIODESATS1" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODESATS1:
                                TILLAEGPERIODESATS1 =TILLAEGPERIODESATS1.group(1)
                                print("TILLAEGPERIODESATS1: %s" % TILLAEGPERIODESATS1)

                            TILLAEGPERIODEBELOB1 = re.search(r'<input name="TILLAEGPERIODEBELOB1" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEBELOB1:
                                TILLAEGPERIODEBELOB1 =TILLAEGPERIODEBELOB1.group(1)
                                print("TILLAEGPERIODEBELOB1: %s" % TILLAEGPERIODEBELOB1)

                            TILLAEGPERIODEENHED2 = re.search(r'<input name="TILLAEGPERIODEENHED2" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEENHED2:
                                TILLAEGPERIODEENHED2 =TILLAEGPERIODEENHED2.group(1)
                                print("TILLAEGPERIODEENHED2: %s" % TILLAEGPERIODEENHED2)

                            TILLAEGPERIODESATS2 = re.search(r'<input name="TILLAEGPERIODESATS2" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODESATS2:
                                TILLAEGPERIODESATS2 =TILLAEGPERIODESATS2.group(1)
                                print("TILLAEGPERIODESATS2: %s" % TILLAEGPERIODESATS2)

                            TILLAEGPERIODEBELOB2 = re.search(r'<input name="TILLAEGPERIODEBELOB2" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEBELOB2:
                                TILLAEGPERIODEBELOB2 =TILLAEGPERIODEBELOB2.group(1)
                                print("TILLAEGPERIODEBELOB2: %s" % TILLAEGPERIODEBELOB2)

                            TILLAEGPERIODEENHED3 = re.search(r'<input name="TILLAEGPERIODEENHED3" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEENHED3:
                                TILLAEGPERIODEENHED3 =TILLAEGPERIODEENHED3.group(1)
                                print("TILLAEGPERIODEENHED3: %s" % TILLAEGPERIODEENHED3)

                            TILLAEGPERIODESATS3 = re.search(r'<input name="TILLAEGPERIODESATS3" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODESATS3:
                                TILLAEGPERIODESATS3 =TILLAEGPERIODESATS3.group(1)
                                print("TILLAEGPERIODESATS3: %s" % TILLAEGPERIODESATS3)

                            TILLAEGPERIODEBELOB3 = re.search(r'<input name="TILLAEGPERIODEBELOB3" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEBELOB3:
                                TILLAEGPERIODEBELOB3 =TILLAEGPERIODEBELOB3.group(1)
                                print("TILLAEGPERIODEBELOB3: %s" % TILLAEGPERIODEBELOB3)

                            TILLAEGPERIODEENHED4 = re.search(r'<input name="TILLAEGPERIODEENHED4" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEENHED4:
                                TILLAEGPERIODEENHED4 =TILLAEGPERIODEENHED4.group(1)
                                print("TILLAEGPERIODEENHED4: %s" % TILLAEGPERIODEENHED4)

                            TILLAEGPERIODESATS4 = re.search(r'<input name="TILLAEGPERIODESATS4" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODESATS4:
                                TILLAEGPERIODESATS4 =TILLAEGPERIODESATS4.group(1)
                                print("TILLAEGPERIODESATS4: %s" % TILLAEGPERIODESATS4)

                            TILLAEGPERIODEBELOB4 = re.search(r'<input name="TILLAEGPERIODEBELOB4" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEBELOB4:
                                TILLAEGPERIODEBELOB4 =TILLAEGPERIODEBELOB4.group(1)
                                print("TILLAEGPERIODEBELOB4: %s" % TILLAEGPERIODEBELOB4)

                            TILLAEGPERIODEENHED5 = re.search(r'<input name="TILLAEGPERIODEENHED5" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEENHED5:
                                TILLAEGPERIODEENHED5 =TILLAEGPERIODEENHED5.group(1)
                                print("TILLAEGPERIODEENHED5: %s" % TILLAEGPERIODEENHED5)

                            TILLAEGPERIODESATS5 = re.search(r'<input name="TILLAEGPERIODESATS5" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODESATS5:
                                TILLAEGPERIODESATS5 =TILLAEGPERIODESATS5.group(1)
                                print("TILLAEGPERIODESATS5: %s" % TILLAEGPERIODESATS5)

                            TILLAEGPERIODEBELOB5 = re.search(r'<input name="TILLAEGPERIODEBELOB5" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGPERIODEBELOB5:
                                TILLAEGPERIODEBELOB5 =TILLAEGPERIODEBELOB5.group(1)
                                print("TILLAEGPERIODEBELOB5: %s" % TILLAEGPERIODEBELOB5)

                            FRADRAGPERIODE1 = re.search(r'<input name="FRADRAGPERIODE1" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGPERIODE1:
                                FRADRAGPERIODE1 =FRADRAGPERIODE1.group(1)
                                print("FRADRAGPERIODE1: %s" % FRADRAGPERIODE1)

                            FRADRAGPERIODE2 = re.search(r'<input name="FRADRAGPERIODE2" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGPERIODE2:
                                FRADRAGPERIODE2 =FRADRAGPERIODE2.group(1)
                                print("FRADRAGPERIODE2: %s" % FRADRAGPERIODE2)

                            FRADRAGPERIODE3 = re.search(r'<input name="FRADRAGPERIODE3" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGPERIODE3:
                                FRADRAGPERIODE3 =FRADRAGPERIODE3.group(1)
                                print("FRADRAGPERIODE3: %s" % FRADRAGPERIODE3)

                            FRADRAGPERIODE4 = re.search(r'<input name="FRADRAGPERIODE4" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGPERIODE4:
                                FRADRAGPERIODE4 =FRADRAGPERIODE4.group(1)
                                print("FRADRAGPERIODE4: %s" % FRADRAGPERIODE4)

                            FRADRAGPERIODE5 = re.search(r'<input name="FRADRAGPERIODE5" value="([^"]+)"', CT, re.I|re.S)
                            if FRADRAGPERIODE5:
                                FRADRAGPERIODE5 =FRADRAGPERIODE5.group(1)
                                print("FRADRAGPERIODE5: %s" % FRADRAGPERIODE5)

                            EGENPCTPENSION3 = re.search(r'<input name="EGENPCTPENSION3" value="([^"]+)"', CT, re.I|re.S)
                            if EGENPCTPENSION3:
                                EGENPCTPENSION3 =EGENPCTPENSION3.group(1)
                                print("EGENPCTPENSION3: %s" % EGENPCTPENSION3)

                            FIRMAPCTPENSION3 = re.search(r'<input name="FIRMAPCTPENSION3" value="([^"]+)"', CT, re.I|re.S)
                            if FIRMAPCTPENSION3:
                                FIRMAPCTPENSION3 =FIRMAPCTPENSION3.group(1)
                                print("FIRMAPCTPENSION3: %s" % FIRMAPCTPENSION3)

                            EGENBELOBPENSION3 = re.search(r'<input name="EGENBELOBPENSION3" value="([^"]+)"', CT, re.I|re.S)
                            if EGENBELOBPENSION3:
                                EGENBELOBPENSION3 =EGENBELOBPENSION3.group(1)
                                print("EGENBELOBPENSION3: %s" % EGENBELOBPENSION3)

                            FIRMABELOBPENSION3 = re.search(r'<input name="FIRMABELOBPENSION3" value="([^"]+)"', CT, re.I|re.S)
                            if FIRMABELOBPENSION3:
                                FIRMABELOBPENSION3 =FIRMABELOBPENSION3.group(1)
                                print("FIRMABELOBPENSION3: %s" % FIRMABELOBPENSION3)

                            OVERENSKOMSTKODE = re.search(r'<input name="OVERENSKOMSTKODE" value="([^"]+)"', CT, re.I|re.S)
                            if OVERENSKOMSTKODE:
                                OVERENSKOMSTKODE =OVERENSKOMSTKODE.group(1)
                                print("OVERENSKOMSTKODE: %s" % OVERENSKOMSTKODE)

                            FRITVALGTILPENSION = re.search(r'<input name="FRITVALGTILPENSION" value="([^"]+)"', CT, re.I|re.S)
                            if FRITVALGTILPENSION:
                                FRITVALGTILPENSION =FRITVALGTILPENSION.group(1)
                                print("FRITVALGTILPENSION: %s" % FRITVALGTILPENSION)

                            GRUPPELIV = re.search(r'<input name="GRUPPELIV" value="([^"]+)"', CT, re.I|re.S)
                            if GRUPPELIV:
                                GRUPPELIV =GRUPPELIV.group(1)
                                print("GRUPPELIV: %s" % GRUPPELIV)

                            FRIBIL = re.search(r'<input name="FRIBIL" value="([^"]+)"', CT, re.I|re.S)
                            if FRIBIL:
                                FRIBIL =FRIBIL.group(1)
                                print("FRIBIL: %s" % FRIBIL)

                            FRIKOSTENHED = re.search(r'<input name="FRIKOSTENHED" value="([^"]+)"', CT, re.I|re.S)
                            if FRIKOSTENHED:
                                FRIKOSTENHED =FRIKOSTENHED.group(1)
                                print("FRIKOSTENHED: %s" % FRIKOSTENHED)

                            FRIKOSTSATS = re.search(r'<input name="FRIKOSTSATS" value="([^"]+)"', CT, re.I|re.S)
                            if FRIKOSTSATS:
                                FRIKOSTSATS =FRIKOSTSATS.group(1)
                                print("FRIKOSTSATS: %s" % FRIKOSTSATS)

                            FRIKOSTBELOB = re.search(r'<input name="FRIKOSTBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if FRIKOSTBELOB:
                                FRIKOSTBELOB =FRIKOSTBELOB.group(1)
                                print("FRIKOSTBELOB: %s" % FRIKOSTBELOB)

                            FRIHELAARSBOLIG = re.search(r'<input name="FRIHELAARSBOLIG" value="([^"]+)"', CT, re.I|re.S)
                            if FRIHELAARSBOLIG:
                                FRIHELAARSBOLIG =FRIHELAARSBOLIG.group(1)
                                print("FRIHELAARSBOLIG: %s" % FRIHELAARSBOLIG)

                            FRISOMMERBOLIG = re.search(r'<input name="FRISOMMERBOLIG" value="([^"]+)"', CT, re.I|re.S)
                            if FRISOMMERBOLIG:
                                FRISOMMERBOLIG =FRISOMMERBOLIG.group(1)
                                print("FRISOMMERBOLIG: %s" % FRISOMMERBOLIG)

                            FRILYSTBAAD = re.search(r'<input name="FRILYSTBAAD" value="([^"]+)"', CT, re.I|re.S)
                            if FRILYSTBAAD:
                                FRILYSTBAAD =FRILYSTBAAD.group(1)
                                print("FRILYSTBAAD: %s" % FRILYSTBAAD)

                            FRILICENS = re.search(r'<input name="FRILICENS" value="([^"]+)"', CT, re.I|re.S)
                            if FRILICENS:
                                FRILICENS =FRILICENS.group(1)
                                print("FRILICENS: %s" % FRILICENS)

                            FRIANDREGODER = re.search(r'<input name="FRIANDREGODER" value="([^"]+)"', CT, re.I|re.S)
                            if FRIANDREGODER:
                                FRIANDREGODER =FRIANDREGODER.group(1)
                                print("FRIANDREGODER: %s" % FRIANDREGODER)

                            FRIANDREGODERUDENBUNDGRAENSE = re.search(r'<input name="FRIANDREGODERUDENBUNDGRAENSE" value="([^"]+)"', CT, re.I|re.S)
                            if FRIANDREGODERUDENBUNDGRAENSE:
                                FRIANDREGODERUDENBUNDGRAENSE =FRIANDREGODERUDENBUNDGRAENSE.group(1)
                                print("FRIANDREGODERUDENBUNDGRAENSE: %s" % FRIANDREGODERUDENBUNDGRAENSE)

                            MULTIMEDIESKAT = re.search(r'<input name="MULTIMEDIESKAT" value="([^"]+)"', CT, re.I|re.S)
                            if MULTIMEDIESKAT:
                                MULTIMEDIESKAT =MULTIMEDIESKAT.group(1)
                                print("MULTIMEDIESKAT: %s" % MULTIMEDIESKAT)

                            MEDARBEJDERBREDBAAND = re.search(r'<input name="MEDARBEJDERBREDBAAND" value="([^"]+)"', CT, re.I|re.S)
                            if MEDARBEJDERBREDBAAND:
                                MEDARBEJDERBREDBAAND =MEDARBEJDERBREDBAAND.group(1)
                                print("MEDARBEJDERBREDBAAND: %s" % MEDARBEJDERBREDBAAND)

                            BRUTTOTRAEKMEDFPREDUKTION = re.search(r'<input name="BRUTTOTRAEKMEDFPREDUKTION" value="([^"]+)"', CT, re.I|re.S)
                            if BRUTTOTRAEKMEDFPREDUKTION:
                                BRUTTOTRAEKMEDFPREDUKTION =BRUTTOTRAEKMEDFPREDUKTION.group(1)
                                print("BRUTTOTRAEKMEDFPREDUKTION: %s" % BRUTTOTRAEKMEDFPREDUKTION)

                            BRUTTOTRAEKUDENFPREDUKTION = re.search(r'<input name="BRUTTOTRAEKUDENFPREDUKTION" value="([^"]+)"', CT, re.I|re.S)
                            if BRUTTOTRAEKUDENFPREDUKTION:
                                BRUTTOTRAEKUDENFPREDUKTION =BRUTTOTRAEKUDENFPREDUKTION.group(1)
                                print("BRUTTOTRAEKUDENFPREDUKTION: %s" % BRUTTOTRAEKUDENFPREDUKTION)

                            HEALTHINSURANCE = re.search(r'<input name="HEALTHINSURANCE" value="([^"]+)"', CT, re.I|re.S)
                            if HEALTHINSURANCE:
                                HEALTHINSURANCE =HEALTHINSURANCE.group(1)
                                print("HEALTHINSURANCE: %s" % HEALTHINSURANCE)

                            SALDOFRADRAGSALDO = re.search(r'<input name="SALDOFRADRAGSALDO" value="([^"]+)"', CT, re.I|re.S)
                            if SALDOFRADRAGSALDO:
                                SALDOFRADRAGSALDO =SALDOFRADRAGSALDO.group(1)
                                print("SALDOFRADRAGSALDO: %s" % SALDOFRADRAGSALDO)

                            SALDOFRADRAGBELOB = re.search(r'<input name="SALDOFRADRAGBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if SALDOFRADRAGBELOB:
                                SALDOFRADRAGBELOB =SALDOFRADRAGBELOB.group(1)
                                print("SALDOFRADRAGBELOB: %s" % SALDOFRADRAGBELOB)

                            FIRMALAANSALDO = re.search(r'<input name="FIRMALAANSALDO" value="([^"]+)"', CT, re.I|re.S)
                            if FIRMALAANSALDO:
                                FIRMALAANSALDO =FIRMALAANSALDO.group(1)
                                print("FIRMALAANSALDO: %s" % FIRMALAANSALDO)

                            FIRMALAANRENTEPCT = re.search(r'<input name="FIRMALAANRENTEPCT" value="([^"]+)"', CT, re.I|re.S)
                            if FIRMALAANRENTEPCT:
                                FIRMALAANRENTEPCT =FIRMALAANRENTEPCT.group(1)
                                print("FIRMALAANRENTEPCT: %s" % FIRMALAANRENTEPCT)

                            FIRMALAANBELOB = re.search(r'<input name="FIRMALAANBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if FIRMALAANBELOB:
                                FIRMALAANBELOB =FIRMALAANBELOB.group(1)
                                print("FIRMALAANBELOB: %s" % FIRMALAANBELOB)

                            TIMELONTIMER1 = re.search(r'<input name="TIMELONTIMER1" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONTIMER1:
                                TIMELONTIMER1 =TIMELONTIMER1.group(1)
                                print("TIMELONTIMER1: %s" % TIMELONTIMER1)

                            TIMELONSATS1 = re.search(r'<input name="TIMELONSATS1" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONSATS1:
                                TIMELONSATS1 =TIMELONSATS1.group(1)
                                print("TIMELONSATS1: %s" % TIMELONSATS1)

                            TIMELONBELOB1 = re.search(r'<input name="TIMELONBELOB1" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONBELOB1:
                                TIMELONBELOB1 =TIMELONBELOB1.group(1)
                                print("TIMELONBELOB1: %s" % TIMELONBELOB1)

                            TIMELONTIMER2 = re.search(r'<input name="TIMELONTIMER2" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONTIMER2:
                                TIMELONTIMER2 =TIMELONTIMER2.group(1)
                                print("TIMELONTIMER2: %s" % TIMELONTIMER2)

                            TIMELONSATS2 = re.search(r'<input name="TIMELONSATS2" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONSATS2:
                                TIMELONSATS2 =TIMELONSATS2.group(1)
                                print("TIMELONSATS2: %s" % TIMELONSATS2)
                            
                            TIMELONBELOB2 = re.search(r'<input name="TIMELONBELOB2" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONBELOB2:
                                TIMELONBELOB2 =TIMELONBELOB2.group(1)
                                print("TIMELONBELOB2: %s" % TIMELONBELOB2)

                            TIMELONTIMER3 = re.search(r'<input name="TIMELONTIMER3" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONTIMER3:
                                TIMELONTIMER3 =TIMELONTIMER3.group(1)
                                print("TIMELONTIMER3: %s" % TIMELONTIMER3)

                            TIMELONSATS3 = re.search(r'<input name="TIMELONSATS3" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONSATS3:
                                TIMELONSATS3 =TIMELONSATS3.group(1)
                                print("TIMELONSATS3: %s" % TIMELONSATS3)

                            TIMELONBELOB3 = re.search(r'<input name="TIMELONBELOB3" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONBELOB3:
                                TIMELONBELOB3 =TIMELONBELOB3.group(1)
                                print("TIMELONBELOB3: %s" % TIMELONBELOB3)

                            TIMELONTIMER4 = re.search(r'<input name="TIMELONTIMER4" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONTIMER4:
                                TIMELONTIMER4 =TIMELONTIMER4.group(1)
                                print("TIMELONTIMER4: %s" % TIMELONTIMER4)

                            TIMELONSATS4 = re.search(r'<input name="TIMELONSATS4" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONSATS4:
                                TIMELONSATS4 =TIMELONSATS4.group(1)
                                print("TIMELONSATS4: %s" % TIMELONSATS4)

                            TIMELONBELOB4 = re.search(r'<input name="TIMELONBELOB4" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONBELOB4:
                                TIMELONBELOB4 =TIMELONBELOB4.group(1)
                                print("TIMELONBELOB4: %s" % TIMELONBELOB4)

                            TIMELONTIMER5 = re.search(r'<input name="TIMELONTIMER5" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONTIMER5:
                                TIMELONTIMER5 =TIMELONTIMER5.group(1)
                                print("TIMELONTIMER5: %s" % TIMELONTIMER5)

                            TIMELONSATS5 = re.search(r'<input name="TIMELONSATS5" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONSATS5:
                                TIMELONSATS5 =TIMELONSATS5.group(1)
                                print("TIMELONSATS5: %s" % TIMELONSATS5)

                            TIMELONBELOB5 = re.search(r'<input name="TIMELONBELOB5" value="([^"]+)"', CT, re.I|re.S)
                            if TIMELONBELOB5:
                                TIMELONBELOB5 =TIMELONBELOB5.group(1)
                                print("TIMELONBELOB5: %s" % TIMELONBELOB5)

                            OVERTID1TIMER = re.search(r'<input name="OVERTID1TIMER" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID1TIMER:
                                OVERTID1TIMER =OVERTID1TIMER.group(1)
                                print("OVERTID1TIMER: %s" % OVERTID1TIMER)

                            OVERTID1SATS = re.search(r'<input name="OVERTID1SATS" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID1SATS:
                                OVERTID1SATS =OVERTID1SATS.group(1)
                                print("OVERTID1SATS: %s" % OVERTID1SATS)

                            OVERTID1BELOB = re.search(r'<input name="OVERTID1BELOB" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID1BELOB:
                                OVERTID1BELOB =OVERTID1BELOB.group(1)
                                print("OVERTID1BELOB: %s" % OVERTID1BELOB)

                            OVERTID2TIMER = re.search(r'<input name="OVERTID2TIMER" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID2TIMER:
                                OVERTID2TIMER =OVERTID2TIMER.group(1)
                                print("OVERTID2TIMER: %s" % OVERTID2TIMER)

                            OVERTID2SATS = re.search(r'<input name="OVERTID2SATS" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID2SATS:
                                OVERTID2SATS =OVERTID2SATS.group(1)
                                print("OVERTID2SATS: %s" % OVERTID2SATS)

                            OVERTID2BELOB = re.search(r'<input name="OVERTID2BELOB" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID2BELOB:
                                OVERTID2BELOB =OVERTID2BELOB.group(1)
                                print("OVERTID2BELOB: %s" % OVERTID2BELOB)

                            OVERTID3TIMER = re.search(r'<input name="OVERTID3TIMER" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID3TIMER:
                                OVERTID3TIMER =OVERTID3TIMER.group(1)
                                print("OVERTID3TIMER: %s" % OVERTID3TIMER)

                            OVERTID3SATS = re.search(r'<input name="OVERTID3SATS" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID3SATS:
                                OVERTID3SATS =OVERTID3SATS.group(1)
                                print("OVERTID3SATS: %s" % OVERTID3SATS)

                            OVERTID3BELOB = re.search(r'<input name="OVERTID3BELOB" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID3BELOB:
                                OVERTID3BELOB =OVERTID3BELOB.group(1)
                                print("OVERTID3BELOB: %s" % OVERTID3BELOB)

                            OVERTID4TIMER = re.search(r'<input name="OVERTID4TIMER" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID4TIMER:
                                OVERTID4TIMER =OVERTID4TIMER.group(1)
                                print("OVERTID4TIMER: %s" % OVERTID4TIMER)

                            OVERTID4SATS = re.search(r'<input name="OVERTID4SATS" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID4SATS:
                                OVERTID4SATS =OVERTID4SATS.group(1)
                                print("OVERTID4SATS: %s" % OVERTID4SATS)

                            OVERTID4BELOB = re.search(r'<input name="OVERTID4BELOB" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID4BELOB:
                                OVERTID4BELOB =OVERTID4BELOB.group(1)
                                print("OVERTID4BELOB: %s" % OVERTID4BELOB)

                            OVERTID5TIMER = re.search(r'<input name="OVERTID5TIMER" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID5TIMER:
                                OVERTID5TIMER =OVERTID5TIMER.group(1)
                                print("OVERTID5TIMER: %s" % OVERTID5TIMER)

                            OVERTID5SATS = re.search(r'<input name="OVERTID5SATS" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID5SATS:
                                OVERTID5SATS =OVERTID5SATS.group(1)
                                print("OVERTID5SATS: %s" % OVERTID5SATS)

                            OVERTID5BELOB = re.search(r'<input name="OVERTID5BELOB" value="([^"]+)"', CT, re.I|re.S)
                            if OVERTID5BELOB:
                                OVERTID5BELOB =OVERTID5BELOB.group(1)
                                print("OVERTID5BELOB: %s" % OVERTID5BELOB)

                            TANTIEME = re.search(r'<input name="TANTIEME" value="([^"]+)"', CT, re.I|re.S)
                            if TANTIEME:
                                TANTIEME =TANTIEME.group(1)
                                print("TANTIEME: %s" % TANTIEME)

                            BESTYRELSESHONORAR = re.search(r'<input name="BESTYRELSESHONORAR" value="([^"]+)"', CT, re.I|re.S)
                            if BESTYRELSESHONORAR:
                                BESTYRELSESHONORAR =BESTYRELSESHONORAR.group(1)
                                print("BESTYRELSESHONORAR: %s" % BESTYRELSESHONORAR)

                            HONORARBIDRAGSPLIGT = re.search(r'<input name="HONORARBIDRAGSPLIGT" value="([^"]+)"', CT, re.I|re.S)
                            if HONORARBIDRAGSPLIGT:
                                HONORARBIDRAGSPLIGT =HONORARBIDRAGSPLIGT.group(1)
                                print("HONORARBIDRAGSPLIGT: %s" % HONORARBIDRAGSPLIGT)

                            HONORARBIDRAGSFRI = re.search(r'<input name="HONORARBIDRAGSFRI" value="([^"]+)"', CT, re.I|re.S)
                            if HONORARBIDRAGSFRI:
                                HONORARBIDRAGSFRI =HONORARBIDRAGSFRI.group(1)
                                print("HONORARBIDRAGSFRI: %s" % HONORARBIDRAGSFRI)

                            ANDENINDKOMST = re.search(r'<input name="ANDENINDKOMST" value="([^"]+)"', CT, re.I|re.S)
                            if ANDENINDKOMST:
                                ANDENINDKOMST =ANDENINDKOMST.group(1)
                                print("ANDENINDKOMST: %s" % ANDENINDKOMST)

                            JUBILAEUMSGRATIALE = re.search(r'<input name="JUBILAEUMSGRATIALE" value="([^"]+)"', CT, re.I|re.S)
                            if JUBILAEUMSGRATIALE:
                                JUBILAEUMSGRATIALE =JUBILAEUMSGRATIALE.group(1)
                                print("JUBILAEUMSGRATIALE: %s" % JUBILAEUMSGRATIALE)

                            FRATRAEDELSEGODTGORELSE = re.search(r'<input name="FRATRAEDELSEGODTGORELSE" value="([^"]+)"', CT, re.I|re.S)
                            if FRATRAEDELSEGODTGORELSE:
                                FRATRAEDELSEGODTGORELSE =FRATRAEDELSEGODTGORELSE.group(1)
                                print("FRATRAEDELSEGODTGORELSE: %s" % FRATRAEDELSEGODTGORELSE)

                            REJSEENHED = re.search(r'<input name="REJSEENHED" value="([^"]+)"', CT, re.I|re.S)
                            if REJSEENHED:
                                REJSEENHED =REJSEENHED.group(1)
                                print("REJSEENHED: %s" % REJSEENHED)

                            REJSESATS = re.search(r'<input name="REJSESATS" value="([^"]+)"', CT, re.I|re.S)
                            if REJSESATS:
                                REJSESATS =REJSESATS.group(1)
                                print("REJSESATS: %s" % REJSESATS)

                            REJSEBELOB = re.search(r'<input name="REJSEBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if REJSEBELOB:
                                REJSEBELOB =REJSEBELOB.group(1)
                                print("REJSEBELOB: %s" % REJSEBELOB)

                            UDLANDREJSE = re.search(r'<input name="UDLANDREJSE" value="([^"]+)"', CT, re.I|re.S)
                            if UDLANDREJSE:
                                UDLANDREJSE =UDLANDREJSE.group(1)
                                print("UDLANDREJSE: %s" % UDLANDREJSE)

                            KMENHEDER = re.search(r'<input name="KMENHEDER" value="([^"]+)"', CT, re.I|re.S)
                            if KMENHEDER:
                                KMENHEDER =KMENHEDER.group(1)
                                print("KMENHEDER: %s" % KMENHEDER)

                            REJSEGODTGORELSEENHED = re.search(r'<input name="REJSEGODTGORELSEENHED" value="([^"]+)"', CT, re.I|re.S)
                            if REJSEGODTGORELSEENHED:
                                REJSEGODTGORELSEENHED =REJSEGODTGORELSEENHED.group(1)
                                print("REJSEGODTGORELSEENHED: %s" % REJSEGODTGORELSEENHED)

                            REJSEGODTGORELSESATS = re.search(r'<input name="REJSEGODTGORELSESATS" value="([^"]+)"', CT, re.I|re.S)
                            if REJSEGODTGORELSESATS:
                                REJSEGODTGORELSESATS =REJSEGODTGORELSESATS.group(1)
                                print("REJSEGODTGORELSESATS: %s" % REJSEGODTGORELSESATS)

                            REJSEGODTGORELSEBELOB = re.search(r'<input name="REJSEGODTGORELSEBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if REJSEGODTGORELSEBELOB:
                                REJSEGODTGORELSEBELOB =REJSEGODTGORELSEBELOB.group(1)
                                print("REJSEGODTGORELSEBELOB: %s" % REJSEGODTGORELSEBELOB)

                            TILLAEGEJFB = re.search(r'<input name="TILLAEGEJFB" value="([^"]+)"', CT, re.I|re.S)
                            if TILLAEGEJFB:
                                TILLAEGEJFB =TILLAEGEJFB.group(1)
                                print("TILLAEGEJFB: %s" % TILLAEGEJFB)

                            RETFRADRAGDAGE = re.search(r'<input name="RETFRADRAGDAGE" value="([^"]+)"', CT, re.I|re.S)
                            if RETFRADRAGDAGE:
                                RETFRADRAGDAGE =RETFRADRAGDAGE.group(1)
                                print("RETFRADRAGDAGE: %s" % RETFRADRAGDAGE)

                            RETATPTIMER = re.search(r'<input name="RETATPTIMER" value="([^"]+)"', CT, re.I|re.S)
                            if RETATPTIMER:
                                RETATPTIMER =RETATPTIMER.group(1)
                                print("RETATPTIMER: %s" % RETATPTIMER)

                            RETATPBELOB = re.search(r'<input name="RETATPBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if RETATPBELOB:
                                RETATPBELOB =RETATPBELOB.group(1)
                                print("RETATPBELOB: %s" % RETATPBELOB)

                            RETATPSYGEDAGPENGEBELOB = re.search(r'<input name="RETATPSYGEDAGPENGEBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if RETATPSYGEDAGPENGEBELOB:
                                RETATPSYGEDAGPENGEBELOB =RETATPSYGEDAGPENGEBELOB.group(1)
                                print("RETATPSYGEDAGPENGEBELOB: %s" % RETATPSYGEDAGPENGEBELOB)

                            RETASKATBELOB = re.search(r'<input name="RETASKATBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if RETASKATBELOB:
                                RETASKATBELOB =RETASKATBELOB.group(1)
                                print("RETASKATBELOB: %s" % RETASKATBELOB)

                            GAGEREDUKTION = re.search(r'<input name="GAGEREDUKTION" value="([^"]+)"', CT, re.I|re.S)
                            if GAGEREDUKTION:
                                GAGEREDUKTION =GAGEREDUKTION.group(1)
                                print("GAGEREDUKTION: %s" % GAGEREDUKTION)

                            RETASKATFPBELOB = re.search(r'<input name="RETASKATFPBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if RETASKATFPBELOB:
                                RETASKATFPBELOB =RETASKATFPBELOB.group(1)
                                print("RETASKATFPBELOB: %s" % RETASKATFPBELOB)

                            RETOPTJENTFERIEDAGEDETTE = re.search(r'<input name="RETOPTJENTFERIEDAGEDETTE" value="([^"]+)"', CT, re.I|re.S)
                            if RETOPTJENTFERIEDAGEDETTE:
                                RETOPTJENTFERIEDAGEDETTE =RETOPTJENTFERIEDAGEDETTE.group(1)
                                print("RETOPTJENTFERIEDAGEDETTE: %s" % RETOPTJENTFERIEDAGEDETTE)

                            RETOPTJENTFERIEDAGEFORRIGE_2015 = re.search(r'<input name="RETOPTJENTFERIEDAGEFORRIGE" value="([^"]+)"', CT, re.I|re.S)
                            if RETOPTJENTFERIEDAGEFORRIGE_2015:
                                RETOPTJENTFERIEDAGEFORRIGE_2015 =RETOPTJENTFERIEDAGEFORRIGE_2015.group(1)
                                print("RETOPTJENTFERIEDAGEFORRIGE_2015: %s" % RETOPTJENTFERIEDAGEFORRIGE_2015)

                            RETOPTJENTFERIEDAGESIDSTE_2016 = re.search(r'<input name="RETOPTJENTFERIEDAGESIDSTE" value="([^"]+)"', CT, re.I|re.S)
                            if RETOPTJENTFERIEDAGESIDSTE_2016:
                                RETOPTJENTFERIEDAGESIDSTE_2016 =RETOPTJENTFERIEDAGESIDSTE_2016.group(1)
                                print("RETOPTJENTFERIEDAGESIDSTE_2016: %s" % RETOPTJENTFERIEDAGESIDSTE_2016)

                            RETAFHOLDTFERIEDAGEFORRIGE_2015 = re.search(r'<input name="RETAFHOLDTFERIEDAGEFORRIGE" value="([^"]+)"', CT, re.I|re.S)
                            if RETAFHOLDTFERIEDAGEFORRIGE_2015:
                                RETAFHOLDTFERIEDAGEFORRIGE_2015 =RETAFHOLDTFERIEDAGEFORRIGE_2015.group(1)
                                print("RETAFHOLDTFERIEDAGEFORRIGE_2015: %s" % RETAFHOLDTFERIEDAGEFORRIGE_2015)

                            RETAFHOLDTFERIEDAGESIDSTE_2016 = re.search(r'<input name="RETAFHOLDTFERIEDAGESIDSTE" value="([^"]+)"', CT, re.I|re.S)
                            if RETAFHOLDTFERIEDAGESIDSTE_2016:
                                RETAFHOLDTFERIEDAGESIDSTE_2016 =RETAFHOLDTFERIEDAGESIDSTE_2016.group(1)
                                print("RETAFHOLDTFERIEDAGESIDSTE_2016: %s" % RETAFHOLDTFERIEDAGESIDSTE_2016)

                            RETFERIEBERETTIGENDELON_2017 = re.search(r'<input name="RETFERIEBERETTIGENDELON" value="([^"]+)"', CT, re.I|re.S)
                            if RETFERIEBERETTIGENDELON_2017:
                                RETFERIEBERETTIGENDELON_2017 =RETFERIEBERETTIGENDELON_2017.group(1)
                                print("RETFERIEBERETTIGENDELON_2017: %s" % RETFERIEBERETTIGENDELON_2017)

                            RETNETTOFERIEPENGEFORRIGE_2015 = re.search(r'<input name="RETNETTOFERIEPENGEFORRIGE" value="([^"]+)"', CT, re.I|re.S)
                            if RETNETTOFERIEPENGEFORRIGE_2015:
                                RETNETTOFERIEPENGEFORRIGE_2015 =RETNETTOFERIEPENGEFORRIGE_2015.group(1)
                                print("RETNETTOFERIEPENGEFORRIGE_2015: %s" % RETNETTOFERIEPENGEFORRIGE_2015)

                            RETNETTOFERIEPENGESIDSTE_2016 = re.search(r'<input name="RETNETTOFERIEPENGESIDSTE" value="([^"]+)"', CT, re.I|re.S)
                            if RETNETTOFERIEPENGESIDSTE_2016:
                                RETNETTOFERIEPENGESIDSTE_2016 =RETNETTOFERIEPENGESIDSTE_2016.group(1)
                                print("RETNETTOFERIEPENGESIDSTE_2016: %s" % RETNETTOFERIEPENGESIDSTE_2016)

                            RETNETTOFERIEPENGEDETTE_2017 = re.search(r'<input name="RETNETTOFERIEPENGEDETTE" value="([^"]+)"', CT, re.I|re.S)
                            if RETNETTOFERIEPENGEDETTE_2017:
                                RETNETTOFERIEPENGEDETTE_2017 =RETNETTOFERIEPENGEDETTE_2017.group(1)
                                print("RETNETTOFERIEPENGEDETTE_2017: %s" % RETNETTOFERIEPENGEDETTE_2017)

                            RETUDBETALTNETTOFPFORRIGE_2015 = re.search(r'<input name="RETUDBETALTNETTOFPFORRIGE" value="([^"]+)"', CT, re.I|re.S)
                            if RETUDBETALTNETTOFPFORRIGE_2015:
                                RETUDBETALTNETTOFPFORRIGE_2015 =RETUDBETALTNETTOFPFORRIGE_2015.group(1)
                                print("RETUDBETALTNETTOFPFORRIGE_2015: %s" % RETUDBETALTNETTOFPFORRIGE_2015)

                            RETUDBETALTNETTOFPSIDSTE_2016 = re.search(r'<input name="RETUDBETALTNETTOFPSIDSTE" value="([^"]+)"', CT, re.I|re.S)
                            if RETUDBETALTNETTOFPSIDSTE_2016:
                                RETUDBETALTNETTOFPSIDSTE_2016 =RETUDBETALTNETTOFPSIDSTE_2016.group(1)
                                print("RETUDBETALTNETTOFPSIDSTE_2016: %s" % RETUDBETALTNETTOFPSIDSTE_2016)

                            RETFRITVALGOPSPARET = re.search(r'<input name="RETFRITVALGOPSPARET" value="([^"]+)"', CT, re.I|re.S)
                            if RETFRITVALGOPSPARET:
                                RETFRITVALGOPSPARET =RETFRITVALGOPSPARET.group(1)
                                print("RETFRITVALGOPSPARET: %s" % RETFRITVALGOPSPARET)

                            RETFRITVALGBRUGT = re.search(r'<input name="RETFRITVALGBRUGT" value="([^"]+)"', CT, re.I|re.S)
                            if RETFRITVALGBRUGT:
                                RETFRITVALGBRUGT =RETFRITVALGBRUGT.group(1)
                                print("RETFRITVALGBRUGT: %s" % RETFRITVALGBRUGT)

                            SYGEDAGPENGETIMER = re.search(r'<input name="SYGEDAGPENGETIMER" value="([^"]+)"', CT, re.I|re.S)
                            if SYGEDAGPENGETIMER:
                                SYGEDAGPENGETIMER =SYGEDAGPENGETIMER.group(1)
                                print("SYGEDAGPENGETIMER: %s" % SYGEDAGPENGETIMER)

                            SYGEDAGPENGESATS = re.search(r'<input name="SYGEDAGPENGESATS" value="([^"]+)"', CT, re.I|re.S)
                            if SYGEDAGPENGESATS:
                                SYGEDAGPENGESATS =SYGEDAGPENGESATS.group(1)
                                print("SYGEDAGPENGESATS: %s" % SYGEDAGPENGESATS)

                            SYGEDAGPENGEBELOB = re.search(r'<input name="SYGEDAGPENGEBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if SYGEDAGPENGEBELOB:
                                SYGEDAGPENGEBELOB =SYGEDAGPENGEBELOB.group(1)
                                print("SYGEDAGPENGEBELOB: %s" % SYGEDAGPENGEBELOB)

                            SYGELONTIMER = re.search(r'<input name="SYGELONTIMER" value="([^"]+)"', CT, re.I|re.S)
                            if SYGELONTIMER:
                                SYGELONTIMER =SYGELONTIMER.group(1)
                                print("SYGELONTIMER: %s" % SYGELONTIMER)

                            SYGELONSATS = re.search(r'<input name="SYGELONSATS" value="([^"]+)"', CT, re.I|re.S)
                            if SYGELONSATS:
                                SYGELONSATS =SYGELONSATS.group(1)
                                print("SYGELONSATS: %s" % SYGELONSATS)

                            SYGELONBELOB = re.search(r'<input name="SYGELONBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if SYGELONBELOB:
                                SYGELONBELOB =SYGELONBELOB.group(1)
                                print("SYGELONBELOB: %s" % SYGELONBELOB)

                            SYGEFERIEPENGE = re.search(r'<input name="SYGEFERIEPENGE" value="([^"]+)"', CT, re.I|re.S)
                            if SYGEFERIEPENGE:
                                SYGEFERIEPENGE =SYGEFERIEPENGE.group(1)
                                print("SYGEFERIEPENGE: %s" % SYGEFERIEPENGE)

                            SYGEDAGE = re.search(r'<input name="SYGEDAGE" value="([^"]+)"', CT, re.I|re.S)
                            if SYGEDAGE:
                                SYGEDAGE =SYGEDAGE.group(1)
                                print("SYGEDAGE: %s" % SYGEDAGE)

                            Ferie_fra_2015_som_kan_afholdes_nu = re.search(r'>\s*Ferie fra 2015 som kan afholdes nu\s*</p>\s*</td>\s*<td\s*>\s*<p[^>]*>\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Ferie_fra_2015_som_kan_afholdes_nu:
                                Ferie_fra_2015_som_kan_afholdes_nu =Ferie_fra_2015_som_kan_afholdes_nu.group(1)
                                print("Ferie_fra_2015_som_kan_afholdes_nu: %s" % Ferie_fra_2015_som_kan_afholdes_nu)

                            Ferie_fra_2016_som_kan_afholdes_nu = re.search(r'>\s*Ferie fra 2016 som kan afholdes nu\s*</p>\s*</td>\s*<td\s*>\s*<p[^>]*>\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Ferie_fra_2016_som_kan_afholdes_nu:
                                Ferie_fra_2016_som_kan_afholdes_nu =Ferie_fra_2016_som_kan_afholdes_nu.group(1)
                                print("Ferie_fra_2016_som_kan_afholdes_nu: %s" % Ferie_fra_2016_som_kan_afholdes_nu)

                            Ferie_som_kan_afholdes_nu_i_alt = re.search(r'>\s*Ferie som kan afholdes nu i alt\s*</a>\s*</p>\s*</td>\s*<td\s*>\s*<p[^>]*>\s*([^<]+)\s*<', CT, re.I|re.S)
                            if Ferie_som_kan_afholdes_nu_i_alt:
                                Ferie_som_kan_afholdes_nu_i_alt =Ferie_som_kan_afholdes_nu_i_alt.group(1)
                                print("Ferie_som_kan_afholdes_nu_i_alt: %s" % Ferie_som_kan_afholdes_nu_i_alt)

                            AFHOLDTFERIEDAGE = re.search(r'<input name="AFHOLDTFERIEDAGE" value="([^"]+)"', CT, re.I|re.S)
                            if AFHOLDTFERIEDAGE:
                                AFHOLDTFERIEDAGE =AFHOLDTFERIEDAGE.group(1)
                                print("AFHOLDTFERIEDAGE: %s" % AFHOLDTFERIEDAGE)

                            AFSPADSERINGHENSATTIMER = re.search(r'<input name="AFSPADSERINGHENSATTIMER" value="([^"]+)"', CT, re.I|re.S)
                            if AFSPADSERINGHENSATTIMER:
                                AFSPADSERINGHENSATTIMER =AFSPADSERINGHENSATTIMER.group(1)
                                print("AFSPADSERINGHENSATTIMER: %s" % AFSPADSERINGHENSATTIMER)

                            AFSPADSERINGHENSATBELOB = re.search(r'<input name="AFSPADSERINGHENSATBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if AFSPADSERINGHENSATBELOB:
                                AFSPADSERINGHENSATBELOB =AFSPADSERINGHENSATBELOB.group(1)
                                print("AFSPADSERINGHENSATBELOB: %s" % AFSPADSERINGHENSATBELOB)

                            AFSPADSERINGAFHOLDTTIMER = re.search(r'<input name="AFSPADSERINGAFHOLDTTIMER" value="([^"]+)"', CT, re.I|re.S)
                            if AFSPADSERINGAFHOLDTTIMER:
                                AFSPADSERINGAFHOLDTTIMER =AFSPADSERINGAFHOLDTTIMER.group(1)
                                print("AFSPADSERINGAFHOLDTTIMER: %s" % AFSPADSERINGAFHOLDTTIMER)

                            AFSPADSERINGAFHOLDTBELOB = re.search(r'<input name="AFSPADSERINGAFHOLDTBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if AFSPADSERINGAFHOLDTBELOB:
                                AFSPADSERINGAFHOLDTBELOB =AFSPADSERINGAFHOLDTBELOB.group(1)
                                print("AFSPADSERINGAFHOLDTBELOB: %s" % AFSPADSERINGAFHOLDTBELOB)

                            FLEXPLANLAGTTIMER = re.search(r'<input name="FLEXPLANLAGTTIMER" value="([^"]+)"', CT, re.I|re.S)
                            if FLEXPLANLAGTTIMER:
                                FLEXPLANLAGTTIMER =FLEXPLANLAGTTIMER.group(1)
                                print("FLEXPLANLAGTTIMER: %s" % FLEXPLANLAGTTIMER)

                            FLEXTILSTEDETIMER = re.search(r'<input name="FLEXTILSTEDETIMER" value="([^"]+)"', CT, re.I|re.S)
                            if FLEXTILSTEDETIMER:
                                FLEXTILSTEDETIMER =FLEXTILSTEDETIMER.group(1)
                                print("FLEXTILSTEDETIMER: %s" % FLEXTILSTEDETIMER)

                            UDBETALTOMSORGSDAGE = re.search(r'<input name="UDBETALTOMSORGSDAGE" value="([^"]+)"', CT, re.I|re.S)
                            if UDBETALTOMSORGSDAGE:
                                UDBETALTOMSORGSDAGE =UDBETALTOMSORGSDAGE.group(1)
                                print("UDBETALTOMSORGSDAGE: %s" % UDBETALTOMSORGSDAGE)

                            OMSORGSDAGESATS = re.search(r'<input name="OMSORGSDAGESATS" value="([^"]+)"', CT, re.I|re.S)
                            if OMSORGSDAGESATS:
                                OMSORGSDAGESATS =OMSORGSDAGESATS.group(1)
                                print("OMSORGSDAGESATS: %s" % OMSORGSDAGESATS)

                            UDBETALTOMSORGSDAGEBELOB = re.search(r'<input name="UDBETALTOMSORGSDAGEBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if UDBETALTOMSORGSDAGEBELOB:
                                UDBETALTOMSORGSDAGEBELOB =UDBETALTOMSORGSDAGEBELOB.group(1)
                                print("UDBETALTOMSORGSDAGEBELOB: %s" % UDBETALTOMSORGSDAGEBELOB)

                            UDBETALTFERIEFRIDAGE = re.search(r'<input name="UDBETALTFERIEFRIDAGE" value="([^"]+)"', CT, re.I|re.S)
                            if UDBETALTFERIEFRIDAGE:
                                UDBETALTFERIEFRIDAGE =UDBETALTFERIEFRIDAGE.group(1)
                                print("UDBETALTFERIEFRIDAGE: %s" % UDBETALTFERIEFRIDAGE)

                            FERIEFRIDAGESATS = re.search(r'<input name="FERIEFRIDAGESATS" value="([^"]+)"', CT, re.I|re.S)
                            if FERIEFRIDAGESATS:
                                FERIEFRIDAGESATS =FERIEFRIDAGESATS.group(1)
                                print("FERIEFRIDAGESATS: %s" % FERIEFRIDAGESATS)

                            UDBETALTFERIEFRIDAGEBELOB = re.search(r'<input name="UDBETALTFERIEFRIDAGEBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if UDBETALTFERIEFRIDAGEBELOB:
                                UDBETALTFERIEFRIDAGEBELOB =UDBETALTFERIEFRIDAGEBELOB.group(1)
                                print("UDBETALTFERIEFRIDAGEBELOB: %s" % UDBETALTFERIEFRIDAGEBELOB)

                            LEDIGHEDSDAGEENHED = re.search(r'<input name="LEDIGHEDSDAGEENHED" value="([^"]+)"', CT, re.I|re.S)
                            if LEDIGHEDSDAGEENHED:
                                LEDIGHEDSDAGEENHED =LEDIGHEDSDAGEENHED.group(1)
                                print("LEDIGHEDSDAGEENHED: %s" % LEDIGHEDSDAGEENHED)

                            LEDIGHEDSDAGESATS = re.search(r'<input name="LEDIGHEDSDAGESATS" value="([^"]+)"', CT, re.I|re.S)
                            if LEDIGHEDSDAGESATS:
                                LEDIGHEDSDAGESATS =LEDIGHEDSDAGESATS.group(1)
                                print("LEDIGHEDSDAGESATS: %s" % LEDIGHEDSDAGESATS)

                            LEDIGHEDSDAGEBELOB = re.search(r'<input name="LEDIGHEDSDAGEBELOB" value="([^"]+)"', CT, re.I|re.S)
                            if LEDIGHEDSDAGEBELOB:
                                LEDIGHEDSDAGEBELOB =LEDIGHEDSDAGEBELOB.group(1)
                                print("LEDIGHEDSDAGEBELOB: %s" % LEDIGHEDSDAGEBELOB)

                            random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
                            file_name = 'FinalFile-{0}.csv'.format(random_string)
                            with open(file_name, 'a', newline='',encoding="utf-8") as csvfile:
                                fieldnames = [
                                                'NAVN',
                                                'ADRESSE1',
                                                'ADRESSE2',
                                                'POSTNUMMER',
                                                'CITY',
                                                'CPRNUMMER',
                                                'REGNR',
                                                'KONTONUMMER',
                                                'BIC',
                                                'IBAN',
                                                'AKTIV',
                                                'ANSATDATO',
                                                'FRATRAADTDATO',
                                                'TITEL',
                                                'Ferieordning',
                                                'Feriepengemodtager',
                                                'Ferie_per_år',
                                                'Status_eIndkomst',
                                                'PRODUKTIONSENHED',
                                                'ANVENDREKLAME',
                                                'DanlønID',
                                                'TELEFON',
                                                'MOBILTELEFON',
                                                'EPOST',
                                                'LOKALTELEFON',
                                                'SENDNETTOLONSMS',
                                                'SENDNETTOLONEPOST',
                                                'FERIEPROCENT',
                                                'FERIETILLAEGPROCENT',
                                                'SHPROCENT',
                                                'FRITVALGSPROCENT',
                                                'Ferieoptjening',
                                                'Ferieregnskab_i',
                                                'OMSORGSDAGEPRAAR',
                                                'FERIEFRIDAGEPRAAR',
                                                'EXTRATRAEKPROCENT',
                                                'AM_indkomst',
                                                'Bidragsfri_A_indkomst',
                                                'Engangsindkomst',
                                                'B_indkomst_uden_AM_bidrag',
                                                'B_indkomst_med_AM_bidrag',
                                                'Timer',
                                                'ATP',
                                                'AM_bidrag',
                                                'A_skat',
                                                'Fri_bil',
                                                'Fri_kost_og_logi',
                                                'Fri_telefon',
                                                'Sundhedsforsikring',
                                                'Antal_kilometer',
                                                'REJSEGODTGORELSE',
                                                'Eget_bidrag',
                                                'Firma_bidrag',
                                                'Eget_bidrag__AMP',
                                                'Firma_bidrag__AMP',
                                                'Gruppeliv',
                                                'Gruppeliv__2',
                                                'Afholdte_G_dage',
                                                'Afholdte_omsorgsdage',
                                                'Afholdte_feriefridage',
                                                'Afspadsering__timer_til_gode',
                                                'Afspadsering__beløb_til_gode',
                                                'Flexsaldo',
                                                'NORMTIMER',
                                                'GAGE',
                                                'PERSONLIGTTILLAEG',
                                                'UGELON',
                                                'KORSELSTILSKUD',
                                                'TILLAEGFASTENHED1',
                                                'TILLAEGFASTSATS1',
                                                'TILLAEGFASTBELOB1',
                                                'TILLAEGFASTENHED2',
                                                'TILLAEGFASTSATS2',
                                                'TILLAEGFASTBELOB2',
                                                'TILLAEGFASTENHED3',
                                                'TILLAEGFASTSATS3',
                                                'TILLAEGFASTBELOB3',
                                                'TILLAEGFASTENHED4',
                                                'TILLAEGFASTSATS4',
                                                'TILLAEGFASTBELOB4',
                                                'TILLAEGFASTENHED5',
                                                'TILLAEGFASTSATS5',
                                                'TILLAEGFASTBELOB5',
                                                'Vis_lønafregning',
                                                'ATP_af_løn',
                                                'Til_udbetaling',
                                                'FRADRAGFAST1',
                                                'FRADRAGFAST2',
                                                'FRADRAGFAST3',
                                                'FRADRAGFAST4',
                                                'FRADRAGFAST5',
                                                'TILLAEGPERIODEENHED1',
                                                'TILLAEGPERIODESATS1',
                                                'TILLAEGPERIODEBELOB1',
                                                'TILLAEGPERIODEENHED2',
                                                'TILLAEGPERIODESATS2',
                                                'TILLAEGPERIODEBELOB2',
                                                'TILLAEGPERIODEENHED3',
                                                'TILLAEGPERIODESATS3',
                                                'TILLAEGPERIODEBELOB3',
                                                'TILLAEGPERIODEENHED4',
                                                'TILLAEGPERIODESATS4',
                                                'TILLAEGPERIODEBELOB4',
                                                'TILLAEGPERIODEENHED5',
                                                'TILLAEGPERIODESATS5',
                                                'TILLAEGPERIODEBELOB5',
                                                'FRADRAGPERIODE1',
                                                'FRADRAGPERIODE2',
                                                'FRADRAGPERIODE3',
                                                'FRADRAGPERIODE4',
                                                'FRADRAGPERIODE5',
                                                'EGENPCTPENSION3',
                                                'FIRMAPCTPENSION3',
                                                'EGENBELOBPENSION3',
                                                'FIRMABELOBPENSION3',
                                                'OVERENSKOMSTKODE',
                                                'FRITVALGTILPENSION',
                                                'GRUPPELIV',
                                                'FRIBIL',
                                                'FRIKOSTENHED',
                                                'FRIKOSTSATS',
                                                'FRIKOSTBELOB',
                                                'FRIHELAARSBOLIG',
                                                'FRISOMMERBOLIG',
                                                'FRILYSTBAAD',
                                                'FRILICENS',
                                                'FRIANDREGODER',
                                                'FRIANDREGODERUDENBUNDGRAENSE',
                                                'MULTIMEDIESKAT',
                                                'MEDARBEJDERBREDBAAND',
                                                'BRUTTOTRAEKMEDFPREDUKTION',
                                                'BRUTTOTRAEKUDENFPREDUKTION',
                                                'HEALTHINSURANCE',
                                                'SALDOFRADRAGSALDO',
                                                'SALDOFRADRAGBELOB',
                                                'FIRMALAANSALDO',
                                                'FIRMALAANRENTEPCT',
                                                'FIRMALAANBELOB',
                                                'TIMELONTIMER1',
                                                'TIMELONSATS1',
                                                'TIMELONBELOB1',
                                                'TIMELONTIMER2',
                                                'TIMELONSATS2',
                                                'TIMELONBELOB2',
                                                'TIMELONTIMER3',
                                                'TIMELONSATS3',
                                                'TIMELONBELOB3',
                                                'TIMELONTIMER4',
                                                'TIMELONSATS4',
                                                'TIMELONBELOB4',
                                                'TIMELONTIMER5',
                                                'TIMELONSATS5',
                                                'TIMELONBELOB5',
                                                'OVERTID1TIMER',
                                                'OVERTID1SATS',
                                                'OVERTID1BELOB',
                                                'OVERTID2TIMER',
                                                'OVERTID2SATS',
                                                'OVERTID2BELOB',
                                                'OVERTID3TIMER',
                                                'OVERTID3SATS',
                                                'OVERTID3BELOB',
                                                'OVERTID4TIMER',
                                                'OVERTID4SATS',
                                                'OVERTID4BELOB',
                                                'OVERTID5TIMER',
                                                'OVERTID5SATS',
                                                'OVERTID5BELOB',
                                                'TANTIEME',
                                                'BESTYRELSESHONORAR',
                                                'HONORARBIDRAGSPLIGT',
                                                'HONORARBIDRAGSFRI',
                                                'ANDENINDKOMST',
                                                'JUBILAEUMSGRATIALE',
                                                'FRATRAEDELSEGODTGORELSE',
                                                'REJSEENHED',
                                                'REJSESATS',
                                                'REJSEBELOB',
                                                'UDLANDREJSE',
                                                'KMENHEDER',
                                                'REJSEGODTGORELSEENHED',
                                                'REJSEGODTGORELSESATS',
                                                'REJSEGODTGORELSEBELOB',
                                                'TILLAEGEJFB',
                                                'RETFRADRAGDAGE',
                                                'RETATPTIMER',
                                                'RETATPBELOB',
                                                'RETATPSYGEDAGPENGEBELOB',
                                                'RETASKATBELOB',
                                                'GAGEREDUKTION',
                                                'RETASKATFPBELOB',
                                                'RETOPTJENTFERIEDAGEDETTE',
                                                'RETOPTJENTFERIEDAGEFORRIGE_2015',
                                                'RETOPTJENTFERIEDAGESIDSTE_2016',
                                                'RETAFHOLDTFERIEDAGEFORRIGE_2015',
                                                'RETAFHOLDTFERIEDAGESIDSTE_2016',
                                                'RETFERIEBERETTIGENDELON_2017',
                                                'RETNETTOFERIEPENGEFORRIGE_2015',
                                                'RETNETTOFERIEPENGESIDSTE_2016',
                                                'RETNETTOFERIEPENGEDETTE_2017',
                                                'RETUDBETALTNETTOFPFORRIGE_2015',
                                                'RETUDBETALTNETTOFPSIDSTE_2016',
                                                'RETFRITVALGOPSPARET',
                                                'RETFRITVALGBRUGT',
                                                'SYGEDAGPENGETIMER',
                                                'SYGEDAGPENGESATS',
                                                'SYGEDAGPENGEBELOB',
                                                'SYGELONTIMER',
                                                'SYGELONSATS',
                                                'SYGELONBELOB',
                                                'SYGEFERIEPENGE',
                                                'SYGEDAGE',
                                                'Ferie_fra_2015_som_kan_afholdes_nu',
                                                'Ferie_fra_2016_som_kan_afholdes_nu',
                                                'Ferie_som_kan_afholdes_nu_i_alt',
                                                'AFHOLDTFERIEDAGE',
                                                'AFSPADSERINGHENSATTIMER',
                                                'AFSPADSERINGHENSATBELOB',
                                                'AFSPADSERINGAFHOLDTTIMER',
                                                'AFSPADSERINGAFHOLDTBELOB',
                                                'FLEXPLANLAGTTIMER',
                                                'FLEXTILSTEDETIMER',
                                                'UDBETALTOMSORGSDAGE',
                                                'OMSORGSDAGESATS',
                                                'UDBETALTOMSORGSDAGEBELOB',
                                                'UDBETALTFERIEFRIDAGE',
                                                'FERIEFRIDAGESATS',
                                                'UDBETALTFERIEFRIDAGEBELOB',
                                                'LEDIGHEDSDAGEENHED',
                                                'LEDIGHEDSDAGESATS',
                                                'LEDIGHEDSDAGEBELOB'
                                            ]
                                writer = csv.DictWriter(csvfile, delimiter=",", fieldnames=fieldnames)
                                writer.writeheader()
                                writer.writerow({
                                            'NAVN':NAVN,
                                            'ADRESSE1':ADRESSE1,
                                            'ADRESSE2':ADRESSE2,
                                            'POSTNUMMER':POSTNUMMER,
                                            'CITY':CITY,
                                            'CPRNUMMER':CPRNUMMER,
                                            'REGNR':REGNR,
                                            'KONTONUMMER':KONTONUMMER,
                                            'BIC':BIC,
                                            'IBAN':IBAN,
                                            'AKTIV':AKTIV,
                                            'ANSATDATO':ANSATDATO,
                                            'FRATRAADTDATO':FRATRAADTDATO,
                                            'TITEL':TITEL,
                                            'Ferieordning':Ferieordning,
                                            'Feriepengemodtager':Feriepengemodtager,
                                            'Ferie_per_år':Ferie_per_år,
                                            'Status_eIndkomst':Status_eIndkomst,
                                            'PRODUKTIONSENHED':PRODUKTIONSENHED,
                                            'ANVENDREKLAME':ANVENDREKLAME,
                                            'DanlønID':DanlønID,
                                            'TELEFON':TELEFON,
                                            'MOBILTELEFON':MOBILTELEFON,
                                            'EPOST':EPOST,
                                            'LOKALTELEFON':LOKALTELEFON,
                                            'SENDNETTOLONSMS':SENDNETTOLONSMS,
                                            'SENDNETTOLONEPOST':SENDNETTOLONEPOST,
                                            'FERIEPROCENT':FERIEPROCENT,
                                            'FERIETILLAEGPROCENT':FERIETILLAEGPROCENT,
                                            'SHPROCENT':SHPROCENT,
                                            'FRITVALGSPROCENT':FRITVALGSPROCENT,
                                            'Ferieoptjening':Ferieoptjening,
                                            'Ferieregnskab_i':Ferieregnskab_i,
                                            'OMSORGSDAGEPRAAR':OMSORGSDAGEPRAAR,
                                            'FERIEFRIDAGEPRAAR':FERIEFRIDAGEPRAAR,
                                            'EXTRATRAEKPROCENT':EXTRATRAEKPROCENT,
                                            'AM_indkomst':AM_indkomst,
                                            'Bidragsfri_A_indkomst':Bidragsfri_A_indkomst,
                                            'Engangsindkomst':Engangsindkomst,
                                            'B_indkomst_uden_AM_bidrag':B_indkomst_uden_AM_bidrag,
                                            'B_indkomst_med_AM_bidrag':B_indkomst_med_AM_bidrag,
                                            'Timer':Timer,
                                            'ATP':ATP,
                                            'AM_bidrag':AM_bidrag,
                                            'A_skat':A_skat,
                                            'Fri_bil':Fri_bil,
                                            'Fri_kost_og_logi':Fri_kost_og_logi,
                                            'Fri_telefon':Fri_telefon,
                                            'Sundhedsforsikring':Sundhedsforsikring,
                                            'Antal_kilometer':Antal_kilometer,
                                            'REJSEGODTGORELSE':REJSEGODTGORELSE,
                                            'Eget_bidrag':Eget_bidrag,
                                            'Firma_bidrag':Firma_bidrag,
                                            'Eget_bidrag__AMP':Eget_bidrag__AMP,
                                            'Firma_bidrag__AMP':Firma_bidrag__AMP,
                                            'Gruppeliv':Gruppeliv,
                                            'Gruppeliv__2':Gruppeliv__2,
                                            'Afholdte_G_dage':Afholdte_G_dage,
                                            'Afholdte_omsorgsdage':Afholdte_omsorgsdage,
                                            'Afholdte_feriefridage':Afholdte_feriefridage,
                                            'Afspadsering__timer_til_gode':Afspadsering__timer_til_gode,
                                            'Afspadsering__beløb_til_gode':Afspadsering__beløb_til_gode,
                                            'Flexsaldo':Flexsaldo,
                                            'NORMTIMER':NORMTIMER,
                                            'GAGE':GAGE,
                                            'PERSONLIGTTILLAEG':PERSONLIGTTILLAEG,
                                            'UGELON':UGELON,
                                            'KORSELSTILSKUD':KORSELSTILSKUD,
                                            'TILLAEGFASTENHED1':TILLAEGFASTENHED1,
                                            'TILLAEGFASTSATS1':TILLAEGFASTSATS1,
                                            'TILLAEGFASTBELOB1':TILLAEGFASTBELOB1,
                                            'TILLAEGFASTENHED2':TILLAEGFASTENHED2,
                                            'TILLAEGFASTSATS2':TILLAEGFASTSATS2,
                                            'TILLAEGFASTBELOB2':TILLAEGFASTBELOB2,
                                            'TILLAEGFASTENHED3':TILLAEGFASTENHED3,
                                            'TILLAEGFASTSATS3':TILLAEGFASTSATS3,
                                            'TILLAEGFASTBELOB3':TILLAEGFASTBELOB3,
                                            'TILLAEGFASTENHED4':TILLAEGFASTENHED4,
                                            'TILLAEGFASTSATS4':TILLAEGFASTSATS4,
                                            'TILLAEGFASTBELOB4':TILLAEGFASTBELOB4,
                                            'TILLAEGFASTENHED5':TILLAEGFASTENHED5,
                                            'TILLAEGFASTSATS5':TILLAEGFASTSATS5,
                                            'TILLAEGFASTBELOB5':TILLAEGFASTBELOB5,
                                            'Vis_lønafregning':Vis_lønafregning,
                                            'ATP_af_løn':ATP_af_løn,
                                            'Til_udbetaling':Til_udbetaling,
                                            'FRADRAGFAST1':FRADRAGFAST1,
                                            'FRADRAGFAST2':FRADRAGFAST2,
                                            'FRADRAGFAST3':FRADRAGFAST3,
                                            'FRADRAGFAST4':FRADRAGFAST4,
                                            'FRADRAGFAST5':FRADRAGFAST5,
                                            'TILLAEGPERIODEENHED1':TILLAEGPERIODEENHED1,
                                            'TILLAEGPERIODESATS1':TILLAEGPERIODESATS1,
                                            'TILLAEGPERIODEBELOB1':TILLAEGPERIODEBELOB1,
                                            'TILLAEGPERIODEENHED2':TILLAEGPERIODEENHED2,
                                            'TILLAEGPERIODESATS2':TILLAEGPERIODESATS2,
                                            'TILLAEGPERIODEBELOB2':TILLAEGPERIODEBELOB2,
                                            'TILLAEGPERIODEENHED3':TILLAEGPERIODEENHED3,
                                            'TILLAEGPERIODESATS3':TILLAEGPERIODESATS3,
                                            'TILLAEGPERIODEBELOB3':TILLAEGPERIODEBELOB3,
                                            'TILLAEGPERIODEENHED4':TILLAEGPERIODEENHED4,
                                            'TILLAEGPERIODESATS4':TILLAEGPERIODESATS4,
                                            'TILLAEGPERIODEBELOB4':TILLAEGPERIODEBELOB4,
                                            'TILLAEGPERIODEENHED5':TILLAEGPERIODEENHED5,
                                            'TILLAEGPERIODESATS5':TILLAEGPERIODESATS5,
                                            'TILLAEGPERIODEBELOB5':TILLAEGPERIODEBELOB5,
                                            'FRADRAGPERIODE1':FRADRAGPERIODE1,
                                            'FRADRAGPERIODE2':FRADRAGPERIODE2,
                                            'FRADRAGPERIODE3':FRADRAGPERIODE3,
                                            'FRADRAGPERIODE4':FRADRAGPERIODE4,
                                            'FRADRAGPERIODE5':FRADRAGPERIODE5,
                                            'EGENPCTPENSION3':EGENPCTPENSION3,
                                            'FIRMAPCTPENSION3':FIRMAPCTPENSION3,
                                            'EGENBELOBPENSION3':EGENBELOBPENSION3,
                                            'FIRMABELOBPENSION3':FIRMABELOBPENSION3,
                                            'OVERENSKOMSTKODE':OVERENSKOMSTKODE,
                                            'FRITVALGTILPENSION':FRITVALGTILPENSION,
                                            'GRUPPELIV':GRUPPELIV,
                                            'FRIBIL':FRIBIL,
                                            'FRIKOSTENHED':FRIKOSTENHED,
                                            'FRIKOSTSATS':FRIKOSTSATS,
                                            'FRIKOSTBELOB':FRIKOSTBELOB,
                                            'FRIHELAARSBOLIG':FRIHELAARSBOLIG,
                                            'FRISOMMERBOLIG':FRISOMMERBOLIG,
                                            'FRILYSTBAAD':FRILYSTBAAD,
                                            'FRILICENS':FRILICENS,
                                            'FRIANDREGODER':FRIANDREGODER,
                                            'FRIANDREGODERUDENBUNDGRAENSE':FRIANDREGODERUDENBUNDGRAENSE,
                                            'MULTIMEDIESKAT':MULTIMEDIESKAT,
                                            'MEDARBEJDERBREDBAAND':MEDARBEJDERBREDBAAND,
                                            'BRUTTOTRAEKMEDFPREDUKTION':BRUTTOTRAEKMEDFPREDUKTION,
                                            'BRUTTOTRAEKUDENFPREDUKTION':BRUTTOTRAEKUDENFPREDUKTION,
                                            'HEALTHINSURANCE':HEALTHINSURANCE,
                                            'SALDOFRADRAGSALDO':SALDOFRADRAGSALDO,
                                            'SALDOFRADRAGBELOB':SALDOFRADRAGBELOB,
                                            'FIRMALAANSALDO':FIRMALAANSALDO,
                                            'FIRMALAANRENTEPCT':FIRMALAANRENTEPCT,
                                            'FIRMALAANBELOB':FIRMALAANBELOB,
                                            'TIMELONTIMER1':TIMELONTIMER1,
                                            'TIMELONSATS1':TIMELONSATS1,
                                            'TIMELONBELOB1':TIMELONBELOB1,
                                            'TIMELONTIMER2':TIMELONTIMER2,
                                            'TIMELONSATS2':TIMELONSATS2,
                                            'TIMELONBELOB2':TIMELONBELOB2,
                                            'TIMELONTIMER3':TIMELONTIMER3,
                                            'TIMELONSATS3':TIMELONSATS3,
                                            'TIMELONBELOB3':TIMELONBELOB3,
                                            'TIMELONTIMER4':TIMELONTIMER4,
                                            'TIMELONSATS4':TIMELONSATS4,
                                            'TIMELONBELOB4':TIMELONBELOB4,
                                            'TIMELONTIMER5':TIMELONTIMER5,
                                            'TIMELONSATS5':TIMELONSATS5,
                                            'TIMELONBELOB5':TIMELONBELOB5,
                                            'OVERTID1TIMER':OVERTID1TIMER,
                                            'OVERTID1SATS':OVERTID1SATS,
                                            'OVERTID1BELOB':OVERTID1BELOB,
                                            'OVERTID2TIMER':OVERTID2TIMER,
                                            'OVERTID2SATS':OVERTID2SATS,
                                            'OVERTID2BELOB':OVERTID2BELOB,
                                            'OVERTID3TIMER':OVERTID3TIMER,
                                            'OVERTID3SATS':OVERTID3SATS,
                                            'OVERTID3BELOB':OVERTID3BELOB,
                                            'OVERTID4TIMER':OVERTID4TIMER,
                                            'OVERTID4SATS':OVERTID4SATS,
                                            'OVERTID4BELOB':OVERTID4BELOB,
                                            'OVERTID5TIMER':OVERTID5TIMER,
                                            'OVERTID5SATS':OVERTID5SATS,
                                            'OVERTID5BELOB':OVERTID5BELOB,
                                            'TANTIEME':TANTIEME,
                                            'BESTYRELSESHONORAR':BESTYRELSESHONORAR,
                                            'HONORARBIDRAGSPLIGT':HONORARBIDRAGSPLIGT,
                                            'HONORARBIDRAGSFRI':HONORARBIDRAGSFRI,
                                            'ANDENINDKOMST':ANDENINDKOMST,
                                            'JUBILAEUMSGRATIALE':JUBILAEUMSGRATIALE,
                                            'FRATRAEDELSEGODTGORELSE':FRATRAEDELSEGODTGORELSE,
                                            'REJSEENHED':REJSEENHED,
                                            'REJSESATS':REJSESATS,
                                            'REJSEBELOB':REJSEBELOB,
                                            'UDLANDREJSE':UDLANDREJSE,
                                            'KMENHEDER':KMENHEDER,
                                            'REJSEGODTGORELSEENHED':REJSEGODTGORELSEENHED,
                                            'REJSEGODTGORELSESATS':REJSEGODTGORELSESATS,
                                            'REJSEGODTGORELSEBELOB':REJSEGODTGORELSEBELOB,
                                            'TILLAEGEJFB':TILLAEGEJFB,
                                            'RETFRADRAGDAGE':RETFRADRAGDAGE,
                                            'RETATPTIMER':RETATPTIMER,
                                            'RETATPBELOB':RETATPBELOB,
                                            'RETATPSYGEDAGPENGEBELOB':RETATPSYGEDAGPENGEBELOB,
                                            'RETASKATBELOB':RETASKATBELOB,
                                            'GAGEREDUKTION':GAGEREDUKTION,
                                            'RETASKATFPBELOB':RETASKATFPBELOB,
                                            'RETOPTJENTFERIEDAGEDETTE':RETOPTJENTFERIEDAGEDETTE,
                                            'RETOPTJENTFERIEDAGEFORRIGE_2015':RETOPTJENTFERIEDAGEFORRIGE_2015,
                                            'RETOPTJENTFERIEDAGESIDSTE_2016':RETOPTJENTFERIEDAGESIDSTE_2016,
                                            'RETAFHOLDTFERIEDAGEFORRIGE_2015':RETAFHOLDTFERIEDAGEFORRIGE_2015,
                                            'RETAFHOLDTFERIEDAGESIDSTE_2016':RETAFHOLDTFERIEDAGESIDSTE_2016,
                                            'RETFERIEBERETTIGENDELON_2017':RETFERIEBERETTIGENDELON_2017,
                                            'RETNETTOFERIEPENGEFORRIGE_2015':RETNETTOFERIEPENGEFORRIGE_2015,
                                            'RETNETTOFERIEPENGESIDSTE_2016':RETNETTOFERIEPENGESIDSTE_2016,
                                            'RETNETTOFERIEPENGEDETTE_2017':RETNETTOFERIEPENGEDETTE_2017,
                                            'RETUDBETALTNETTOFPFORRIGE_2015':RETUDBETALTNETTOFPFORRIGE_2015,
                                            'RETUDBETALTNETTOFPSIDSTE_2016':RETUDBETALTNETTOFPSIDSTE_2016,
                                            'RETFRITVALGOPSPARET':RETFRITVALGOPSPARET,
                                            'RETFRITVALGBRUGT':RETFRITVALGBRUGT,
                                            'SYGEDAGPENGETIMER':SYGEDAGPENGETIMER,
                                            'SYGEDAGPENGESATS':SYGEDAGPENGESATS,
                                            'SYGEDAGPENGEBELOB':SYGEDAGPENGEBELOB,
                                            'SYGELONTIMER':SYGELONTIMER,
                                            'SYGELONSATS':SYGELONSATS,
                                            'SYGELONBELOB':SYGELONBELOB,
                                            'SYGEFERIEPENGE':SYGEFERIEPENGE,
                                            'SYGEDAGE':SYGEDAGE,
                                            'Ferie_fra_2015_som_kan_afholdes_nu':Ferie_fra_2015_som_kan_afholdes_nu,
                                            'Ferie_fra_2016_som_kan_afholdes_nu':Ferie_fra_2016_som_kan_afholdes_nu,
                                            'Ferie_som_kan_afholdes_nu_i_alt':Ferie_som_kan_afholdes_nu_i_alt,
                                            'AFHOLDTFERIEDAGE':AFHOLDTFERIEDAGE,
                                            'AFSPADSERINGHENSATTIMER':AFSPADSERINGHENSATTIMER,
                                            'AFSPADSERINGHENSATBELOB':AFSPADSERINGHENSATBELOB,
                                            'AFSPADSERINGAFHOLDTTIMER':AFSPADSERINGAFHOLDTTIMER,
                                            'AFSPADSERINGAFHOLDTBELOB':AFSPADSERINGAFHOLDTBELOB,
                                            'FLEXPLANLAGTTIMER':FLEXPLANLAGTTIMER,
                                            'FLEXTILSTEDETIMER':FLEXTILSTEDETIMER,
                                            'UDBETALTOMSORGSDAGE':UDBETALTOMSORGSDAGE,
                                            'OMSORGSDAGESATS':OMSORGSDAGESATS,
                                            'UDBETALTOMSORGSDAGEBELOB':UDBETALTOMSORGSDAGEBELOB,
                                            'UDBETALTFERIEFRIDAGE':UDBETALTFERIEFRIDAGE,
                                            'FERIEFRIDAGESATS':FERIEFRIDAGESATS,
                                            'UDBETALTFERIEFRIDAGEBELOB':UDBETALTFERIEFRIDAGEBELOB,
                                            'LEDIGHEDSDAGEENHED':LEDIGHEDSDAGEENHED,
                                            'LEDIGHEDSDAGESATS':LEDIGHEDSDAGESATS,
                                            'LEDIGHEDSDAGEBELOB':LEDIGHEDSDAGEBELOB
                                        })
                                
                                NAVN = ''
                                ADRESSE1 = ''
                                ADRESSE2 = ''
                                POSTNUMMER = ''
                                CITY = ''
                                CPRNUMMER = ''
                                REGNR = ''
                                KONTONUMMER = ''
                                BIC = ''
                                IBAN = ''
                                AKTIV = ''
                                ANSATDATO = ''
                                FRATRAADTDATO = ''
                                TITEL = ''
                                Ferieordning = ''
                                Feriepengemodtager = ''
                                Ferie_per_år = ''
                                Status_eIndkomst = ''
                                PRODUKTIONSENHED = ''
                                ANVENDREKLAME = ''
                                DanlønID = ''
                                TELEFON = ''
                                MOBILTELEFON = ''
                                EPOST = ''
                                LOKALTELEFON = ''
                                SENDNETTOLONSMS = ''
                                SENDNETTOLONEPOST = ''
                                FERIEPROCENT = ''
                                FERIETILLAEGPROCENT = ''
                                SHPROCENT = ''
                                FRITVALGSPROCENT = ''
                                Ferieoptjening = ''
                                Ferieregnskab_i = ''
                                OMSORGSDAGEPRAAR = ''
                                FERIEFRIDAGEPRAAR = ''
                                EXTRATRAEKPROCENT = ''
                                AM_indkomst = ''
                                Bidragsfri_A_indkomst = ''
                                Engangsindkomst = ''
                                B_indkomst_uden_AM_bidrag = ''
                                B_indkomst_med_AM_bidrag = ''
                                Timer = ''
                                ATP = ''
                                AM_bidrag = ''
                                A_skat = ''
                                Fri_bil = ''
                                Fri_kost_og_logi = ''
                                Fri_telefon = ''
                                Sundhedsforsikring = ''
                                Antal_kilometer = ''
                                REJSEGODTGORELSE = ''
                                Eget_bidrag = ''
                                Firma_bidrag = ''
                                Eget_bidrag__AMP = ''
                                Firma_bidrag__AMP = ''
                                Gruppeliv = ''
                                Gruppeliv__2 = ''
                                Afholdte_G_dage = ''
                                Afholdte_omsorgsdage = ''
                                Afholdte_feriefridage = ''
                                Afspadsering__timer_til_gode = ''
                                Afspadsering__beløb_til_gode = ''
                                Flexsaldo = ''
                                NORMTIMER = ''
                                GAGE = ''
                                PERSONLIGTTILLAEG = ''
                                UGELON = ''
                                KORSELSTILSKUD = ''
                                TILLAEGFASTENHED1 = ''
                                TILLAEGFASTSATS1 = ''
                                TILLAEGFASTBELOB1 = ''
                                TILLAEGFASTENHED2 = ''
                                TILLAEGFASTSATS2 = ''
                                TILLAEGFASTBELOB2 = ''
                                TILLAEGFASTENHED3 = ''
                                TILLAEGFASTSATS3 = ''
                                TILLAEGFASTBELOB3 = ''
                                TILLAEGFASTENHED4 = ''
                                TILLAEGFASTSATS4 = ''
                                TILLAEGFASTBELOB4 = ''
                                TILLAEGFASTENHED5 = ''
                                TILLAEGFASTSATS5 = ''
                                TILLAEGFASTBELOB5 = ''
                                Vis_lønafregning = ''
                                ATP_af_løn = ''
                                Til_udbetaling = ''
                                FRADRAGFAST1 = ''
                                FRADRAGFAST2 = ''
                                FRADRAGFAST3 = ''
                                FRADRAGFAST4 = ''
                                FRADRAGFAST5 = ''
                                TILLAEGPERIODEENHED1 = ''
                                TILLAEGPERIODESATS1 = ''
                                TILLAEGPERIODEBELOB1 = ''
                                TILLAEGPERIODEENHED2 = ''
                                TILLAEGPERIODESATS2 = ''
                                TILLAEGPERIODEBELOB2 = ''
                                TILLAEGPERIODEENHED3 = ''
                                TILLAEGPERIODESATS3 = ''
                                TILLAEGPERIODEBELOB3 = ''
                                TILLAEGPERIODEENHED4 = ''
                                TILLAEGPERIODESATS4 = ''
                                TILLAEGPERIODEBELOB4 = ''
                                TILLAEGPERIODEENHED5 = ''
                                TILLAEGPERIODESATS5 = ''
                                TILLAEGPERIODEBELOB5 = ''
                                FRADRAGPERIODE1 = ''
                                FRADRAGPERIODE2 = ''
                                FRADRAGPERIODE3 = ''
                                FRADRAGPERIODE4 = ''
                                FRADRAGPERIODE5 = ''
                                EGENPCTPENSION3 = ''
                                FIRMAPCTPENSION3 = ''
                                EGENBELOBPENSION3 = ''
                                FIRMABELOBPENSION3 = ''
                                OVERENSKOMSTKODE = ''
                                FRITVALGTILPENSION = ''
                                GRUPPELIV = ''
                                FRIBIL = ''
                                FRIKOSTENHED = ''
                                FRIKOSTSATS = ''
                                FRIKOSTBELOB = ''
                                FRIHELAARSBOLIG = ''
                                FRISOMMERBOLIG = ''
                                FRILYSTBAAD = ''
                                FRILICENS = ''
                                FRIANDREGODER = ''
                                FRIANDREGODERUDENBUNDGRAENSE = ''
                                MULTIMEDIESKAT = ''
                                MEDARBEJDERBREDBAAND = ''
                                BRUTTOTRAEKMEDFPREDUKTION = ''
                                BRUTTOTRAEKUDENFPREDUKTION = ''
                                HEALTHINSURANCE = ''
                                SALDOFRADRAGSALDO = ''
                                SALDOFRADRAGBELOB = ''
                                FIRMALAANSALDO = ''
                                FIRMALAANRENTEPCT = ''
                                FIRMALAANBELOB = ''
                                TIMELONTIMER1 = ''
                                TIMELONSATS1 = ''
                                TIMELONBELOB1 = ''
                                TIMELONTIMER2 = ''
                                TIMELONSATS2 = ''
                                TIMELONBELOB2 = ''
                                TIMELONTIMER3 = ''
                                TIMELONSATS3 = ''
                                TIMELONBELOB3 = ''
                                TIMELONTIMER4 = ''
                                TIMELONSATS4 = ''
                                TIMELONBELOB4 = ''
                                TIMELONTIMER5 = ''
                                TIMELONSATS5 = ''
                                TIMELONBELOB5 = ''
                                OVERTID1TIMER = ''
                                OVERTID1SATS = ''
                                OVERTID1BELOB = ''
                                OVERTID2TIMER = ''
                                OVERTID2SATS = ''
                                OVERTID2BELOB = ''
                                OVERTID3TIMER = ''
                                OVERTID3SATS = ''
                                OVERTID3BELOB = ''
                                OVERTID4TIMER = ''
                                OVERTID4SATS = ''
                                OVERTID4BELOB = ''
                                OVERTID5TIMER = ''
                                OVERTID5SATS = ''
                                OVERTID5BELOB = ''
                                TANTIEME = ''
                                BESTYRELSESHONORAR = ''
                                HONORARBIDRAGSPLIGT = ''
                                HONORARBIDRAGSFRI = ''
                                ANDENINDKOMST = ''
                                JUBILAEUMSGRATIALE = ''
                                FRATRAEDELSEGODTGORELSE = ''
                                REJSEENHED = ''
                                REJSESATS = ''
                                REJSEBELOB = ''
                                UDLANDREJSE = ''
                                KMENHEDER = ''
                                REJSEGODTGORELSEENHED = ''
                                REJSEGODTGORELSESATS = ''
                                REJSEGODTGORELSEBELOB = ''
                                TILLAEGEJFB = ''
                                RETFRADRAGDAGE = ''
                                RETATPTIMER = ''
                                RETATPBELOB = ''
                                RETATPSYGEDAGPENGEBELOB = ''
                                RETASKATBELOB = ''
                                GAGEREDUKTION = ''
                                RETASKATFPBELOB = ''
                                RETOPTJENTFERIEDAGEDETTE = ''
                                RETOPTJENTFERIEDAGEFORRIGE_2015 = ''
                                RETOPTJENTFERIEDAGESIDSTE_2016 = ''
                                RETAFHOLDTFERIEDAGEFORRIGE_2015 = ''
                                RETAFHOLDTFERIEDAGESIDSTE_2016 = ''
                                RETFERIEBERETTIGENDELON_2017 = ''
                                RETNETTOFERIEPENGEFORRIGE_2015 = ''
                                RETNETTOFERIEPENGESIDSTE_2016 = ''
                                RETNETTOFERIEPENGEDETTE_2017 = ''
                                RETUDBETALTNETTOFPFORRIGE_2015 = ''
                                RETUDBETALTNETTOFPSIDSTE_2016 = ''
                                RETFRITVALGOPSPARET = ''
                                RETFRITVALGBRUGT = ''
                                SYGEDAGPENGETIMER = ''
                                SYGEDAGPENGESATS = ''
                                SYGEDAGPENGEBELOB = ''
                                SYGELONTIMER = ''
                                SYGELONSATS = ''
                                SYGELONBELOB = ''
                                SYGEFERIEPENGE = ''
                                SYGEDAGE = ''
                                Ferie_fra_2015_som_kan_afholdes_nu = ''
                                Ferie_fra_2016_som_kan_afholdes_nu = ''
                                Ferie_som_kan_afholdes_nu_i_alt = ''
                                AFHOLDTFERIEDAGE = ''
                                AFSPADSERINGHENSATTIMER = ''
                                AFSPADSERINGHENSATBELOB = ''
                                AFSPADSERINGAFHOLDTTIMER = ''
                                AFSPADSERINGAFHOLDTBELOB = ''
                                FLEXPLANLAGTTIMER = ''
                                FLEXTILSTEDETIMER = ''
                                UDBETALTOMSORGSDAGE = ''
                                OMSORGSDAGESATS = ''
                                UDBETALTOMSORGSDAGEBELOB = ''
                                UDBETALTFERIEFRIDAGE = ''
                                FERIEFRIDAGESATS = ''
                                UDBETALTFERIEFRIDAGEBELOB = ''
                                LEDIGHEDSDAGEENHED = ''
                                LEDIGHEDSDAGESATS = ''
                                LEDIGHEDSDAGEBELOB = ''
                                return file_name
    print('done all.')




# if __name__ == "__main__":
#     try:
#         app.run(host='0.0.0.0')
#     except Exception as e:
#         print(e)

