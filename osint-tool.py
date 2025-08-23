#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import phonenumbers
import whois
import socket
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode, quote
from datetime import datetime
import colorama
from colorama import Fore, Style, Back
import subprocess

# Инициализация colorama
colorama.init(autoreset=True)

class MegaOSINTTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
        # МЕГА БАЗА ДАННЫХ - ВСЕ ПРЕДОСТАВЛЕННЫЕ РЕСУРСЫ
        self.mega_databases = {
            # 🇷🇺 Российские государственные реестры
            'ФНС ИНН физлица': 'https://service.nalog.ru/inn.do',
            'Реестр банкротств': 'https://bankrot.fedresurs.ru/',
            'ЕГРЮЛ': 'https://egrul.nalog.ru/',
            'Проверка водительского удостоверения': 'https://xn--90adear.xn--p1ai/check/driver/',
            'Счетная палата': 'https://results.audit.gov.ru/',
            'Судебные акты': 'https://sudact.ru/',
            'ЦБ РФ кредитные организации': 'https://www.cbr.ru/credit/main.asp',
            'Блокировка счетов': 'https://service.nalog.ru/bi.do',
            'Проверка паспортов ФМС': 'https://services.fms.gov.ru/',
            'Недобросовестные поставщики': 'https://zakupki.gov.ru/223/dishonest/public/supplier-search.html',
            'Реестр террористов': 'https://fedsfm.ru/documents/terrorists-catalog-portal-act',
            'Черный список строителей': 'https://www.stroi-baza.ru/forum/index.php?showforum=46',
            'Решения судов': 'https://xn--90afdbaav0bd1afy6eub5d.xn--p1ai/',
            'Центр долгов': 'https://www.centerdolgov.ru/',
            'Арбитражный суд': 'https://ras.arbitr.ru/',
            'Росреестр': 'https://rosreestr.ru/wps/portal/cc_information_online',
            'Суды общей юрисдикции': 'https://www.gcourts.ru/',
            'Раскрытие информации': 'https://www.e-disclosure.ru/',
            'ФАС недобросовестные поставщики': 'https://rnp.fas.gov.ru/',
            'Услуги Росреестра': 'https://rosreestr.ru/wps/portal/p/cc_present/EGRN_1',
            'Нотариусы': 'https://www.notary.ru/notary/bd.html',
            'ЧОП': 'https://allchop.ru/',
            'Расшифровка кодов': 'https://enotpoiskun.ru/tools/codedecode/',
            'Расшифровка VIN': 'https://www.vinformer.su/ident/vin.php?setLng=ru',
            'Розыск преступников': 'https://fssprus.ru/iss/suspect_info',
            'Реестр коллекторов': 'https://fssprus.ru/gosreestr_jurlic/',
            'Открытые данные ФССП': 'https://opendata.fssprus.ru/',
            'Саморегулируемые организации': 'https://sro.gosnadzor.ru/',
            'Реестр залогов': 'https://www.reestr-zalogov.ru/search/index',
            'Розыск МВД': 'https://мвд.рф/wanted',
            'Реестр студентов Москвы': 'https://www.mos.ru/karta-moskvicha/services-proverka-grazhdanina-v-reestre-studentov/',
            'Федеральное имущество': 'https://esugi.rosim.ru',
            'Реестр операторов персданных': 'https://pd.rkn.gov.ru/operators-registry',
            'Единый реестр банкротств': 'https://bankrot.fedresurs.ru/',
            
            # 🔍 Поиск контрагента
            'ФНС задолженность': 'https://service.nalog.ru/zd.do',
            'ФНС адреса юрлиц': 'https://service.nalog.ru/addrfind.do',
            'ФНС госрегистрация': 'https://service.nalog.ru/uwsfind.do',
            'ФНС дисквалифицированные': 'https://service.nalog.ru/disqualified.do',
            'ФНС дисквалифицированные руководители': 'https://service.nalog.ru/disfind.do',
            'ФНС невозможность руководства': 'https://service.nalog.ru/svl.do',
            'ФНС учредители нескольких юрлиц': 'https://service.nalog.ru/mru.do',
            'Федресурс': 'https://fedresurs.ru/',
            
            # 🌐 Международные OSINT базы
            'Namechk (username)': 'https://namechk.com/',
            'HaveIBeenPwned (email)': 'https://haveibeenpwned.com/',
            'Hacked-Emails': 'https://hacked-emails.com/',
            'GhostProject': 'https://ghostproject.fr/',
            'WeLeakInfo': 'https://weleakinfo.com/',
            'Pipl': 'https://pipl.com/',
            'LeakedSource': 'https://leakedsource.ru/',
            'PhoneNumber': 'https://phonenumber.to',
            'OSINT Framework': 'https://osintframework.com/',
            'FindClone': 'https://findclone.ru/',
            'UnwiredLabs (базовые станции)': 'https://unwiredlabs.com',
            'Xinit базовые станции': 'https://xinit.ru/bs/',
            'PhotoMap по геометкам': 'https://sanstv.ru/photomap',
            
            # 🚢 Транспорт и отслеживание
            'MarineTraffic': 'https://www.marinetraffic.com',
            'SeaTracker': 'https://seatracker.ru/ais.php',
            'ShipFinder': 'https://shipfinder.co/',
            'PlaneFinder': 'https://planefinder.net/',
            'RadarBox': 'https://www.radarbox24.com/',
            'FlightAware': 'https://de.flightaware.com/',
            'FlightRadar24': 'https://www.flightradar24.com',
            
            # 📊 Дополнительные бизнес-базы
            'Роскомнадзор реестры': 'https://rkn.gov.ru/mass-communications/reestr/',
            'ЕГРЮЛ международный': 'https://www.egrul.ru/',
            'СКРИН раскрытие информации': 'https://disclosure.skrin.ru',
            'Прайм-ТАСС': 'https://1prime.ru/docs/product/disclosure.html',
            'ЦБ кредитные истории': 'https://www.cbr.ru/',
            'Росстат отчетность': 'https://www.gks.ru/accounting_report',
            'Таможенные базы': 'https://www.tks.ru/db/',
            'Каталог предприятий': 'https://tipodop.ru/',
            'CatalogFactory': 'https://www.catalogfactory.org/',
            'Право.ру': 'https://pravo.ru/',
            'AzStatus': 'https://azstatus.ru/',
            'Seldon закупки': 'https://seldon.ru/',
            'ТПП надежные партнеры': 'https://www.reestrtpprf.ru/',
            'Кронос проверка': 'https://croinform.ru/index.php?page=index',
            'Госзакупки': 'https://www.zakupki.gov.ru/epz/main/public/home.html',
            'Rostender': 'https://rostender.info/',
            'Правовая информация': 'https://pravo.fso.gov.ru/',
            'BicoTender': 'https://www.bicotender.ru/',
            'ВШЭ архив': 'https://sophist.hse.ru/',
            'TenderGuru': 'https://www.tenderguru.ru/',
            'MoscowBase': 'https://www.moscowbase.ru/',
            'Credinform ГЛОБАС': 'https://www.credinform.ru/ru-RU/globas',
            'ActInfo справочник': 'https://www.actinfo.ru/',
            'Правосудие': 'https://www.sudrf.ru/',
            'Право.ру документы': 'https://docs.pravo.ru/',
            'Fedresurs факты деятельности': 'https://www.fedresurs.ru/',
            'FindSMI СМИ': 'https://www.findsmi.ru/',
            'OpenGovData': 'https://hub.opengovdata.ru/',
            'Ruward рейтинги': 'https://www.ruward.ru/',
            'B2B-Energo': 'https://www.b2b-energo.ru/firm_dossier/',
            'OpenData': 'https://opengovdata.ru/',
            'Бир-аналитик': 'https://bir.1prime.ru/',
            'Prima-Inform': 'https://www.prima-inform.ru/',
            'Integrum': 'https://www.integrum.ru/',
            'Spark-Interfax': 'https://www.spark-interfax.ru/',
            'Fira': 'https://fira.ru/',
            'SKRIN': 'https://www.skrin.ru/',
            'Magelan тендеры': 'https://www.magelan.pro/',
            'Контрагент': 'https://www.kontragent.info/',
            'IST-Budget': 'https://www.ist-budget.ru/',
            'Vuve': 'https://www.vuve.su/',
            'Disclosure': 'https://www.disclosure.ru/index.shtml',
            'Mosstat': 'https://www.mosstat.ru/index.html',
            'Torg94': 'https://www.torg94.ru/',
            'K-Agent': 'https://www.k-agent.ru/',
            'IS-Zakupki': 'https://www.is-zakupki.ru/',
            'SaleSpring': 'https://salespring.ru/',
            'Multistat': 'https://www.multistat.ru/',
            
            # 🔐 Дополнительные сервисы
            'Рокомнадзор операторы': 'https://rkn.gov.ru/mass-communications/reestr/',
            'Китайские компании': 'https://www.chinacheckup.com/',
            'Dun and Bradstreet': 'https://www.dnb.com/products.html',
            'Украинские базы': 'https://www.imena.ua/blog/ukraine-database/',
            'Нотариальная система': 'https://www.fciit.ru/',
            'Городская статистика': 'https://gradoteka.ru/',
            'Таможенные данные': 'https://www.tks.ru/db/',
            'Антикриминальная система': 'https://www.aips-ariadna.com/',
            'Реестр деклараций': 'https://188.254.71.82/rds_ts_pub/',
            'Сообщество безопасников': 'https://iskr-a.com/',
            'Российский центр': 'https://www.ruscentr.com/',
            'Правовая система': 'https://pravo.fso.gov.ru/',
            'Тендерный портал': 'https://www.tenderguru.ru/',
            'Биржа контактов': 'https://salespring.ru/'
        }

        # Удаление нерабочих баз данных
        self.remove_non_working_databases()

    def remove_non_working_databases(self):
        """Удаление нерабочих баз данных"""
        non_working_dbs = [
            'Проверка ОСАГО',  # polis.autoins.ru
            'ФССП',  # fssprus.ru
            'ФССП исполнительные производства',  # fssprus.ru
            'ФССП розыск',  # fssprus.ru
            'База водителей',  # www.voditeli.ru
        ]
        
        for db in non_working_dbs:
            if db in self.mega_databases:
                del self.mega_databases[db]
                print(f"{Fore.YELLOW}🗑️ Удалена нерабочая база: {db}")

    def clear_screen(self):
        """Очистка экрана с стилизацией"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"{Fore.RED}{'='*80}")
        print(f"{Fore.RED}{Back.BLACK}    ██████╗ ███████╗██╗███╗   ██╗████████╗")
        print(f"{Fore.RED}{Back.BLACK}    ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝")
        print(f"{Fore.RED}{Back.BLACK}    ██║   ██╗███████╗██║██╔██╗ ██║   ██║   ")
        print(f"{Fore.RED}{Back.BLACK}    ██║   ██║╚════██║██║██║╚██╗██║   ██║   ")
        print(f"{Fore.RED}{Back.BLACK}    ╚██████╔╝███████║██║██║ ╚████║   ██║   ")
        print(f"{Fore.RED}{Back.BLACK}     ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   ")
        print(f"{Fore.RED}{'='*80}")
        print(f"{Fore.RED}{Style.BRIGHT}    MEGA OSINT SEARCH TOOL v2.0")
        print(f"{Fore.RED}    🔍 {len(self.mega_databases)}+ баз данных | 🚀 Автоматический поиск")
        print(f"{Fore.RED}    ⚡ Полный пробив | 🛡️ Анонимный режим")
        print(f"{Fore.RED}{'='*80}")

    def show_loading(self, message):
        """Показать анимацию загрузки"""
        print(f"\n{Fore.RED}🔄 {message}", end='', flush=True)
        for i in range(3):
            time.sleep(0.3)
            print(f"{Fore.RED}.", end='', flush=True)
        print()

    def search_database(self, db_name, query, query_type):
        """Поиск в конкретной базе данных"""
        results = {'database': db_name, 'query': query, 'type': query_type}
        
        if db_name in self.mega_databases:
            base_url = self.mega_databases[db_name]
            try:
                params = {}
                
                if query_type == 'inn':
                    params = {'inn': query}
                elif query_type == 'phone':
                    params = {'phone': query, 'number': query}
                elif query_type == 'email':
                    params = {'email': query, 'q': query}
                elif query_type == 'username':
                    params = {'username': query, 'q': query}
                elif query_type == 'company':
                    params = {'company': query, 'q': query, 'name': query}
                elif query_type == 'person':
                    params = {'fio': query, 'name': query, 'q': query}
                else:
                    params = {'q': query, 'search': query}
                
                response = self.session.get(base_url, params=params, timeout=20)
                results['status'] = response.status_code
                results['url'] = response.url
                
                if response.status_code == 200:
                    if 'text/html' in response.headers.get('content-type', ''):
                        soup = BeautifulSoup(response.text, 'html.parser')
                        results['title'] = soup.title.string if soup.title else None
                        
                        text_content = soup.get_text()
                        results['content_preview'] = ' '.join(text_content[:300].split()) + '...'
                        
                    results['success'] = True
                else:
                    results['error'] = f"HTTP {response.status_code}"
                    
            except Exception as e:
                results['error'] = str(e)
        else:
            results['error'] = "База данных не найдена"
        
        return results

    def mass_search(self, query, query_type, selected_dbs=None):
        """Массовый поиск по всем базам данных"""
        print(f"\n{Fore.RED}🔍 Поиск '{query}' ({query_type}) по базам данных...")
        print(f"{Fore.RED}{'='*70}")
        
        all_results = {}
        
        databases_to_search = selected_dbs if selected_dbs else list(self.mega_databases.keys())
        
        for db_name in databases_to_search:
            print(f"{Fore.RED}📊 {db_name}...", end=' ', flush=True)
            result = self.search_database(db_name, query, query_type)
            
            if 'error' not in result or result.get('success'):
                all_results[db_name] = result
                status = f"{Fore.GREEN}✅" if result.get('success') else f"{Fore.YELLOW}⚠️"
                print(f"{status} {result.get('status', 'N/A')}")
                
                # Вывод подробной информации о результате
                if result.get('success'):
                    print(f"   {Fore.CYAN}URL: {result.get('url')}")
                    if result.get('title'):
                        print(f"   {Fore.CYAN}Заголовок: {result.get('title')}")
                    if result.get('content_preview'):
                        print(f"   {Fore.CYAN}Предпросмотр: {result.get('content_preview')}")
                elif result.get('error'):
                    print(f"   {Fore.RED}Ошибка: {result.get('error')}")
                print()
            else:
                print(f"{Fore.RED}❌ Ошибка: {result.get('error', 'Unknown')}")
            
            time.sleep(0.3)
        
        return all_results

    def auto_detect_query_type(self, query):
        """Автоматическое определение типа запроса"""
        query = str(query).strip()
        
        if re.match(r'^\d{10,12}$', query):
            return 'inn', 'ИНН'
        elif re.match(r'^\d{2} ?\d{2} ?\d{6}$', query):
            return 'driver_license', 'Водительское удостоверение'
        elif re.match(r'^\d{4} ?\d{6}$', query):
            return 'passport', 'Паспорт'
        elif '@' in query and re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', query):
            return 'email', 'Email'
        elif re.match(r'^\+?[78]?[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$', query.replace(' ', '')):
            return 'phone', 'Телефон'
        elif re.match(r'^[a-zA-Z0-9._-]+$', query) and len(query) > 2:
            return 'username', 'Username'
        elif re.search(r'(ООО|АО|ЗАО|ОАО|ИП|ПАО|НКО)', query, re.IGNORECASE):
            return 'company', 'Компания'
        elif len(query.split()) in [2, 3] and all(word[0].isupper() for word in query.split() if word):
            return 'person', 'ФИО'
        else:
            return 'general', 'Общий запрос'

    def comprehensive_search(self, query, db_category=None):
        """Комплексный поиск по всем базам"""
        query_type, type_name = self.auto_detect_query_type(query)
        print(f"{Fore.RED}🎯 Обнаружен тип: {Fore.WHITE}{type_name}")
        
        if db_category == 'russian':
            dbs_to_search = [k for k in self.mega_databases.keys() if any(x in k for x in ['ФНС', 'Рос', 'Суд', 'МВД', 'ФССП'])]
        elif db_category == 'international':
            dbs_to_search = [k for k in self.mega_databases.keys() if k not in ['ФНС', 'Рос', 'Суд', 'МВД', 'ФССП']]
        else:
            dbs_to_search = list(self.mega_databases.keys())
        
        self.show_loading("Сканирование баз данных")
        results = self.mass_search(query, query_type, dbs_to_search)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"osint_search_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'query': query,
                'query_type': query_type,
                'type_name': type_name,
                'timestamp': timestamp,
                'results': results
            }, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n{Fore.GREEN}💾 Результаты сохранены в: {Fore.WHITE}{filename}")
        
        success_count = sum(1 for r in results.values() if r.get('success'))
        total_count = len(results)
        print(f"{Fore.RED}📈 Статистика: {Fore.WHITE}{success_count}/{total_count} баз ответили успешно")
        print(f"{Fore.RED}📊 Объем базы данных: {Fore.WHITE}{len(self.mega_databases)} источников")
        
        # Детальная статистика
        print(f"\n{Fore.RED}📋 ДЕТАЛЬНАЯ СТАТИСТИКА:")
        print(f"{Fore.RED}✅ Успешные запросы: {Fore.GREEN}{success_count}")
        print(f"{Fore.RED}❌ Ошибки: {Fore.RED}{total_count - success_count}")
        print(f"{Fore.RED}🔗 Всего баз в системе: {Fore.BLUE}{len(self.mega_databases)}")
        
        return results

    def show_all_databases(self):
        """Показать все базы данных с подробной информацией"""
        print(f"\n{Fore.RED}{'='*80}")
        print(f"{Fore.RED}{Style.BRIGHT}ПОЛНЫЙ СПИСОК БАЗ ДАННЫХ")
        print(f"{Fore.RED}{'='*80}")
        print(f"{Fore.RED}📊 Общее количество: {len(self.mega_databases)} источников")
        print(f"{Fore.RED}{'='*80}")
        
        for i, (name, url) in enumerate(self.mega_databases.items(), 1):
            print(f"{Fore.RED}{i:3d}. {Fore.CYAN}{name}")
            print(f"    {Fore.YELLOW}URL: {url}")
            print()

    def show_menu(self):
        """Показать главное меню"""
        print(f"\n{Fore.RED}{'='*60}")
        print(f"{Fore.RED}{Style.BRIGHT}ВЫБЕРИТЕ ОПЦИЮ:")
        print(f"{Fore.RED}{'='*60}")
        print(f"{Fore.RED}1. 🔎 Комплексный поиск по всем базам")
        print(f"{Fore.RED}2. 🇷🇺 Только российские гос. реестры")
        print(f"{Fore.RED}3. 🌐 Только международные OSINT базы")
        print(f"{Fore.RED}4. 📋 Показать все базы данных ({len(self.mega_databases)})")
        print(f"{Fore.RED}5. 🗂️ Показать категории")
        print(f"{Fore.RED}6. 💾 Экспорт базы данных")
        print(f"{Fore.RED}7. 🚪 Выход")
        print(f"{Fore.RED}{'='*60}")

def main():
    tool = MegaOSINTTool()
    tool.clear_screen()
    
    while True:
        tool.show_menu()
        
        choice = input(f"{Fore.RED}Ваш выбор (1-7): ").strip()
        
        if choice in ['1', '2', '3']:
            query = input(f"{Fore.RED}Введите запрос (ИНН, телефон, email, ФИО и т.д.): ").strip()
            if query:
                if choice == '1':
                    tool.comprehensive_search(query)
                elif choice == '2':
                    tool.comprehensive_search(query, 'russian')
                elif choice == '3':
                    tool.comprehensive_search(query, 'international')
        
        elif choice == '4':
            tool.show_all_databases()
        
        elif choice == '5':
            print(f"\n{Fore.RED}🗂️ КАТЕГОРИИ БАЗ ДАННЫХ:")
            categories = {
                '🇷🇺 Российские гос. реестры': [k for k in tool.mega_databases if any(x in k for x in ['ФНС', 'Рос', 'Суд', 'МВД', 'ФССП'])],
                '🌐 Международные OSINT': [k for k in tool.mega_databases if k not in ['ФНС', 'Рос', 'Суд', 'МВД', 'ФССП']],
                '📊 Бизнес и компании': [k for k in tool.mega_databases if any(x in k.lower() for x in ['бизнес', 'компан', 'реестр'])],
                '👤 Персональные данные': [k for k in tool.mega_databases if any(x in k.lower() for x in ['паспорт', 'водитель', 'фио', 'инн'])]
            }
            
            for category, dbs in categories.items():
                print(f"\n{Fore.RED}{category} ({len(dbs)}):")
                for db in dbs[:5]:
                    print(f"{Fore.RED}  • {db}")
                if len(dbs) > 5:
                    print(f"{Fore.RED}  • ... и еще {len(dbs)-5}")
        
        elif choice == '6':
            with open('osint_databases_export.json', 'w', encoding='utf-8') as f:
                json.dump(tool.mega_databases, f, indent=2, ensure_ascii=False)
            print(f"{Fore.GREEN}💾 База данных экспортирована в osint_databases_export.json")
            print(f"{Fore.GREEN}📊 Количество баз: {len(tool.mega_databases)}")
        
        elif choice == '7':
            print(f"\n{Fore.RED}👋 До свидания!")
            break
        
        else:
            print(f"{Fore.RED}❌ Неверный выбор. Попробуйте снова.")
        
        input(f"\n{Fore.RED}Нажмите Enter для продолжения...")
        tool.clear_screen()

if __name__ == "__main__":
    # Убедимся что colorama установлена
    try:
        import colorama
    except ImportError:
        print("Устанавливаем colorama...")
        subprocess.run([sys.executable, "-m", "pip", "install", "colorama"])
        import colorama
        colorama.init(autoreset=True)
    
    main()
