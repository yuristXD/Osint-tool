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

class MegaOSINTTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
        # МЕГА БАЗА ДАННЫХ - все предоставленные ресурсы
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
            'База водителей': 'https://www.voditeli.ru/',
            'Суды общей юрисдикции': 'https://www.gcourts.ru/',
            'Раскрытие информации': 'https://www.e-disclosure.ru/',
            'ФССП': 'https://www.fssprus.ru/',
            'ФАС недобросовестные поставщики': 'https://rnp.fas.gov.ru/',
            'Услуги Росреестра': 'https://rosreestr.ru/wps/portal/p/cc_present/EGRN_1',
            'Нотариусы': 'https://www.notary.ru/notary/bd.html',
            'ЧОП': 'https://allchop.ru/',
            'Расшифровка кодов': 'https://enotpoiskun.ru/tools/codedecode/',
            'Проверка ОСАГО': 'https://polis.autoins.ru/',
            'Расшифровка VIN': 'https://www.vinformer.su/ident/vin.php?setLng=ru',
            'ФССП исполнительные производства': 'https://fssprus.ru/iss/ip',
            'ФССП розыск': 'https://fssprus.ru/iss/ip_search',
            'Розыск преступников': 'https://fssprus.ru/iss/suspect_info',
            'Реестр коллекторов': 'https://fssprus.ru/gosreestr_jurlic/',
            'Открытые данные ФССП': 'https://opendata.fssprus.ru/',
            'Саморегулируемые организации': 'https://sro.gosnadzor.ru/',
            'Реестр залогов': 'https://www.reestr-zalogov.ru/search/index',
            'Розыск МВД': 'https://мвд.рф/wanted',
            'Реестр студентов Москвы': 'https://www.mos.ru/karta-moskvicha/services-proverka-grazhdanina-v-reestre-studentov/',
            'Федеральное имущество': 'https://esugi.rosim.ru',
            'Реестр операторов персданных': 'https://pd.rkn.gov.ru/operators-registry',
            
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
            'Multistat': 'https://www.multistat.ru/'
        }

    def search_database(self, db_name, query, query_type):
        """Поиск в конкретной базе данных"""
        results = {'database': db_name, 'query': query, 'type': query_type}
        
        if db_name in self.mega_databases:
            base_url = self.mega_databases[db_name]
            try:
                # Специфичные параметры для разных типов запросов
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
                        
                        # Извлекаем потенциально полезную информацию
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
        print(f"\n🔍 Поиск '{query}' ({query_type}) по базам данных...")
        print("=" * 70)
        
        all_results = {}
        
        databases_to_search = selected_dbs if selected_dbs else self.mega_databases.keys()
        
        for db_name in databases_to_search:
            print(f"📊 {db_name}...")
            result = self.search_database(db_name, query, query_type)
            
            if 'error' not in result or result.get('success'):
                all_results[db_name] = result
                status = "✅" if result.get('success') else "⚠️"
                print(f"   {status} {result.get('status', 'N/A')} - {result.get('url', '')}")
            else:
                print(f"   ❌ Ошибка: {result.get('error', 'Unknown')}")
            
            time.sleep(0.5)  # Задержка между запросами
        
        return all_results

    def auto_detect_query_type(self, query):
        """Автоматическое определение типа запроса"""
        query = str(query).strip()
        
        # ИНН (10-12 цифр)
        if re.match(r'^\d{10,12}$', query):
            return 'inn', 'ИНН'
        
        # Водительские права (серия номер)
        elif re.match(r'^\d{2} ?\d{2} ?\d{6}$', query):
            return 'driver_license', 'Водительское удостоверение'
        
        # Паспорт (серия номер)
        elif re.match(r'^\d{4} ?\d{6}$', query):
            return 'passport', 'Паспорт'
        
        # Email
        elif '@' in query and re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', query):
            return 'email', 'Email'
        
        # Телефон
        elif re.match(r'^\+?[78]?[ -]?\(?\d{3}\)?[ -]?\d{3}[ -]?\d{2}[ -]?\d{2}$', query.replace(' ', '')):
            return 'phone', 'Телефон'
        
        # Username (только буквы, цифры, точки, подчеркивания)
        elif re.match(r'^[a-zA-Z0-9._-]+$', query) and len(query) > 2:
            return 'username', 'Username'
        
        # Компания (содержит ООО, АО, ИП и т.д.)
        elif re.search(r'(ООО|АО|ЗАО|ОАО|ИП|ПАО|НКО)', query, re.IGNORECASE):
            return 'company', 'Компания'
        
        # ФИО (2-3 слова, первая буква заглавная)
        elif len(query.split()) in [2, 3] and all(word[0].isupper() for word in query.split() if word):
            return 'person', 'ФИО'
        
        else:
            return 'general', 'Общий запрос'

    def comprehensive_search(self, query, db_category=None):
        """Комплексный поиск по всем базам"""
        query_type, type_name = self.auto_detect_query_type(query)
        print(f"🎯 Обнаружен тип: {type_name}")
        
        # Выбор категорий баз для поиска
        if db_category == 'russian':
            dbs_to_search = [k for k in self.mega_databases.keys() if any(x in k for x in ['ФНС', 'Рос', 'Суд', 'МВД', 'ФССП'])]
        elif db_category == 'international':
            dbs_to_search = [k for k in self.mega_databases.keys() if k not in ['ФНС', 'Рос', 'Суд', 'МВД', 'ФССП']]
        else:
            dbs_to_search = None
        
        results = self.mass_search(query, query_type, dbs_to_search)
        
        # Сохранение результатов
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mega_osint_search_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'query': query,
                'query_type': query_type,
                'type_name': type_name,
                'timestamp': timestamp,
                'results': results
            }, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Результаты сохранены в: {filename}")
        
        # Вывод статистики
        success_count = sum(1 for r in results.values() if r.get('success'))
        print(f"📈 Статистика: {success_count}/{len(results)} баз ответили успешно")
        
        return results

    def show_categories(self):
        """Показать категории баз данных"""
        categories = {
            '🇷🇺 Российские гос. реестры': [k for k in self.mega_databases if any(x in k for x in ['ФНС', 'Рос', 'Суд', 'МВД', 'ФССП'])],
            '🌐 Международные OSINT': [k for k in self.mega_databases if k not in ['ФНС', 'Рос', 'Суд', 'МВД', 'ФССП']],
            '📊 Бизнес и компании': [k for k in self.mega_databases if any(x in k for x in ['компан', 'бизнес', 'реестр', 'база'])],
            '👤 Персональные данные': [k for k in self.mega_databases if any(x in k for x in ['паспорт', 'водитель', 'ФИО', 'ИНН'])]
        }
        
        for category, dbs in categories.items():
            print(f"\n{category} ({len(dbs)}):")
            for db in dbs[:5]:  # Показываем первые 5
                print(f"  • {db}")
            if len(dbs) > 5:
                print(f"  • ... и еще {len(dbs)-5}")

def main():
    print("""
    🚀 MEGA OSINT SEARCH TOOL
    =========================
    🔍 200+ баз данных | Автоматический поиск | Полный пробив
    """)
    
    tool = MegaOSINTTool()
    
    while True:
        print("\n" + "="*60)
        print("Выберите опцию:")
        print("1. 🔎 Комплексный поиск по всем базам")
        print("2. 🇷🇺 Только российские гос. реестры")
        print("3. 🌐 Только международные OSINT базы")
        print("4. 📋 Показать все базы данных")
        print("5. 🗂️ Показать категории")
        print("6. 💾 Экспорт базы данных")
        print("7. 🚪 Выход")
        print("="*60)
        
        choice = input("Ваш выбор (1-7): ").strip()
        
        if choice in ['1', '2', '3']:
            query = input("Введите запрос (ИНН, телефон, email, ФИО и т.д.): ").strip()
            if query:
                if choice == '1':
                    tool.comprehensive_search(query)
                elif choice == '2':
                    tool.comprehensive_search(query, 'russian')
                elif choice == '3':
                    tool.comprehensive_search(query, 'international')
        
        elif choice == '4':
            print(f"\n📊 ВСЕ БАЗЫ ДАННЫХ ({len(tool.mega_databases)}):")
            for i, (name, url) in enumerate(tool.mega_databases.items(), 1):
                print(f"{i:3d}. {name}: {url}")
        
        elif choice == '5':
            tool.show_categories()
        
        elif choice == '6':
            # Экспорт базы данных в JSON
            with open('osint_databases_export.json', 'w', encoding='utf-8') as f:
                json.dump(tool.mega_databases, f, indent=2, ensure_ascii=False)
            print("💾 База данных экспортирована в osint_databases_export.json")
        
        elif choice == '7':
            print("До свидания! 👋")
            break
        
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
