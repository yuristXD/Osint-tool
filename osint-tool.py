#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import phonenumbers
import whois
import socket
import dns.resolver
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, quote
import time
from datetime import datetime
import re
import webbrowser

class OSINTTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        self.results = {}
        
        # Российские государственные сервисы
        self.russian_services = {
            'Налоговая ИНН': 'https://service.nalog.ru/inn.do',
            'Реестр банкротств': 'http://bankrot.fedresurs.ru/',
            'ЕГРЮЛ': 'http://egrul.nalog.ru/',
            'Проверка водительского удостоверения': 'https://xn--90adear.xn--p1ai/check/driver/',
            'Счетная палата': 'http://results.audit.gov.ru/',
            'Судебные акты': 'http://sudact.ru/',
            'ЦБ РФ кредитные организации': 'http://www.cbr.ru/credit/main.asp',
            'Блокировка счетов': 'https://service.nalog.ru/bi.do',
            'Проверка паспортов ФМС': 'http://services.fms.gov.ru/',
            'Недобросовестные поставщики': 'http://zakupki.gov.ru/223/dishonest/public/supplier-search.html',
            'Реестр террористов': 'http://fedsfm.ru/documents/terrorists-catalog-portal-act',
            'Черный список строителей': 'http://www.stroi-baza.ru/forum/index.php?showforum=46',
            'Решения судов': 'http://xn--90afdbaav0bd1afy6eub5d.xn--p1ai/',
            'Центр долгов': 'http://www.centerdolgov.ru/',
            'Арбитражный суд': 'http://ras.arbitr.ru/',
            'Росреестр': 'https://rosreestr.ru/wps/portal/cc_information_online',
            'База водителей': 'http://www.voditeli.ru/',
            'Суды общей юрисдикции': 'http://www.gcourts.ru/',
            'Раскрытие информации': 'http://www.e-disclosure.ru/',
            'ФССП': 'http://www.fssprus.ru/',
            'ФАС недобросовестные поставщики': 'http://rnp.fas.gov.ru/',
            'Услуги Росреестра': 'https://rosreestr.ru/wps/portal/p/cc_present/EGRN_1',
            'Нотариусы': 'http://www.notary.ru/notary/bd.html',
            'ЧОП': 'http://allchop.ru/',
            'Расшифровка кодов': 'http://enotpoiskun.ru/tools/codedecode/',
            'Проверка ОСАГО': 'http://polis.autoins.ru/',
            'Расшифровка VIN': 'http://www.vinformer.su/ident/vin.php?setLng=ru',
            'ФССП исполнительные производства': 'http://fssprus.ru/iss/ip',
            'ФССП розыск': 'http://fssprus.ru/iss/ip_search',
            'Розыск преступников': 'http://fssprus.ru/iss/suspect_info',
            'Реестр коллекторов': 'http://fssprus.ru/gosreestr_jurlic/',
            'Открытые данные ФССП': 'http://opendata.fssprus.ru/',
            'Саморегулируемые организации': 'http://sro.gosnadzor.ru/',
            'Реестр залогов': 'https://www.reestr-zalogov.ru/search/index',
            'Розыск МВД': 'https://мвд.рф/wanted',
            'Реестр студентов Москвы': 'https://www.mos.ru/karta-moskvicha/services-proverka-grazhdanina-v-reestre-studentov/',
            'Федеральное имущество': 'http://esugi.rosim.ru',
            'Реестр операторов персданных': 'pd.rkn.gov.ru/operators-registry'
        }
        
        # Международные OSINT сервисы
        self.international_services = {
            'Namechk (username)': 'https://namechk.com/',
            'HaveIBeenPwned (email)': 'https://haveibeenpwned.com/',
            'Hacked-Emails': 'https://hacked-emails.com/',
            'GhostProject': 'https://ghostproject.fr/',
            'WeLeakInfo': 'https://weleakinfo.com/',
            'Pipl': 'https://pipl.com/',
            'LeakedSource': 'https://leakedsource.ru/',
            'PhoneNumber': 'https://phonenumber.to',
            'OSINT Framework': 'http://osintframework.com/',
            'FindClone': 'https://findclone.ru/',
            'UnwiredLabs (базовые станции)': 'http://unwiredlabs.com',
            'Xinit базовые станции': 'http://xinit.ru/bs/',
            'PhotoMap по геометкам': 'http://sanstv.ru/photomap',
            'MarineTraffic': 'https://www.marinetraffic.com',
            'SeaTracker': 'https://seatracker.ru/ais.php',
            'ShipFinder': 'http://shipfinder.co/',
            'PlaneFinder': 'https://planefinder.net/',
            'RadarBox': 'https://www.radarbox24.com/',
            'FlightAware': 'https://de.flightaware.com/',
            'FlightRadar24': 'https://www.flightradar24.com'
        }

    def open_web_service(self, service_name, query=None):
        """Открытие веб-сервиса в браузере"""
        services = {**self.russian_services, **self.international_services}
        
        if service_name in services:
            url = services[service_name]
            if query:
                # Добавляем запрос к URL если нужно
                if '{}' in url:
                    url = url.format(quote(query))
                elif 'search' in url or 'query' in url:
                    url = f"{url}?q={quote(query)}"
            
            print(f"[+] Открываю: {service_name}")
            print(f"[+] URL: {url}")
            
            # Пытаемся открыть в браузере Termux
            try:
                webbrowser.open(url)
                return True
            except:
                print(f"[!] Не удалось открыть браузер. Перейдите по ссылке вручную.")
                return False
        else:
            print(f"[-] Сервис '{service_name}' не найден")
            return False

    def check_phone_number(self, phone_number):
        """Проверка телефонного номера"""
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            return {
                'valid': phonenumbers.is_valid_number(parsed_number),
                'country': phonenumbers.region_code_for_number(parsed_number),
                'type': phonenumbers.number_type(parsed_number),
                'international': phonenumbers.format_number(parsed_number, 
                                                          phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def check_domain(self, domain):
        """Проверка домена"""
        try:
            # WHOIS информация
            domain_info = whois.whois(domain)
            
            # DNS информация
            ip_address = socket.gethostbyname(domain)
            
            # Проверка доступности
            try:
                response = requests.get(f"http://{domain}", timeout=10)
                status_code = response.status_code
            except:
                status_code = "Unreachable"
            
            return {
                'whois': dict(domain_info),
                'ip_address': ip_address,
                'status': status_code
            }
        except Exception as e:
            return {'error': str(e)}
    
    def search_username(self, username):
        """Поиск username в социальных сетях"""
        sites = {
            'GitHub': f'https://github.com/{username}',
            'Twitter': f'https://twitter.com/{username}',
            'Instagram': f'https://instagram.com/{username}',
            'Facebook': f'https://facebook.com/{username}',
            'LinkedIn': f'https://linkedin.com/in/{username}',
            'Reddit': f'https://reddit.com/user/{username}',
            'Telegram': f'https://t.me/{username}',
            'VK': f'https://vk.com/{username}',
            'Odnoklassniki': f'https://ok.ru/{username}'
        }
        
        results = {}
        for site, url in sites.items():
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    results[site] = {
                        'url': url,
                        'exists': True,
                        'status': 'Found'
                    }
                else:
                    results[site] = {
                        'url': url,
                        'exists': False,
                        'status': 'Not found'
                    }
            except Exception as e:
                results[site] = {
                    'url': url,
                    'exists': False,
                    'status': f'Error: {str(e)}'
                }
            time.sleep(1)  # Задержка между запросами
        
        return results
    
    def email_analysis(self, email):
        """Анализ email адреса"""
        try:
            # Проверка формата
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            is_valid = bool(re.match(email_regex, email))
            
            # Извлечение домена
            domain = email.split('@')[1] if '@' in email else None
            
            # Проверка disposable email
            disposable_domains = ['tempmail', 'fake', 'trash', 'guerrillamail']
            is_disposable = any(dom in domain for dom in disposable_domains) if domain else False
            
            return {
                'valid_format': is_valid,
                'domain': domain,
                'is_disposable': is_disposable,
                'breach_check': 'Manual check recommended'
            }
        except Exception as e:
            return {'error': str(e)}
    
    def ip_lookup(self, ip_address):
        """Поиск информации об IP адресе"""
        try:
            response = self.session.get(f'https://ipapi.co/{ip_address}/json/', timeout=10)
            data = response.json()
            
            return {
                'ip': data.get('ip'),
                'city': data.get('city'),
                'region': data.get('region'),
                'country': data.get('country_name'),
                'isp': data.get('org'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude')
            }
        except Exception as e:
            return {'error': str(e)}
    
    def list_services(self, service_type=None):
        """Показать список доступных сервисов"""
        if service_type == 'russian':
            services = self.russian_services
            title = "РОССИЙСКИЕ ГОСУДАРСТВЕННЫЕ СЕРВИСЫ"
        elif service_type == 'international':
            services = self.international_services
            title = "МЕЖДУНАРОДНЫЕ OSINT СЕРВИСЫ"
        else:
            services = {**self.russian_services, **self.international_services}
            title = "ВСЕ ДОСТУПНЫЕ СЕРВИСЫ"
        
        print(f"\n{title}")
        print("=" * 80)
        for i, (name, url) in enumerate(services.items(), 1):
            print(f"{i:2d}. {name:40s} {url}")
    
    def run_comprehensive_scan(self, target):
        """Комплексный анализ цели"""
        print(f"[+] Начинаем анализ: {target}")
        print("-" * 50)
        
        results = {}
        
        # Определяем тип цели
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
            print("[+] Обнаружен IP адрес")
            results['ip_lookup'] = self.ip_lookup(target)
        
        elif '@' in target:
            print("[+] Обнаружен email адрес")
            results['email_analysis'] = self.email_analysis(target)
            username = target.split('@')[0]
            results['username_search'] = self.search_username(username)
        
        elif re.match(r'^\+?[\d\s\-\(\)]+$', target.replace(' ', '')):
            print("[+] Обнаружен телефонный номер")
            results['phone_analysis'] = self.check_phone_number(target)
        
        elif re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', target):
            print("[+] Обнаружен домен")
            results['domain_analysis'] = self.check_domain(target)
            results['website_analysis'] = self.website_analysis(f"http://{target}")
        
        elif re.match(r'^[a-zA-Z0-9_\-\.]+$', target):
            print("[+] Обнаружен username")
            results['username_search'] = self.search_username(target)
        
        else:
            print("[-] Не удалось определить тип цели")
            return None
        
        return results

def main():
    print("""
    ██████╗ ███████╗██╗███╗   ██╗████████╗
    ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝
    ██║   ██╗███████╗██║██╔██╗ ██║   ██║   
    ██║   ██║╚════██║██║██║╚██╗██║   ██║   
    ╚██████╔╝███████║██║██║ ╚████║   ██║   
     ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝   
                                           
    OSINT Tool for Termux v2.0
    """)
    
    tool = OSINTTool()
    
    while True:
        print("\n" + "="*80)
        print("Выберите опцию:")
        print("1. Поиск по username")
        print("2. Анализ домена")
        print("3. Проверка email")
        print("4. Поиск по IP")
        print("5. Проверка телефона")
        print("6. Комплексный анализ")
        print("7. Российские гос. сервисы")
        print("8. Международные OSINT сервисы")
        print("9. Открыть веб-сервис")
        print("10. Выход")
        print("="*80)
        
        choice = input("Ваш выбор (1-10): ").strip()
        
        if choice == '1':
            username = input("Введите username: ").strip()
            results = tool.search_username(username)
            print(json.dumps(results, indent=2, ensure_ascii=False))
            
        elif choice == '2':
            domain = input("Введите домен: ").strip()
            results = tool.check_domain(domain)
            print(json.dumps(results, indent=2, ensure_ascii=False))
            
        elif choice == '3':
            email = input("Введите email: ").strip()
            results = tool.email_analysis(email)
            print(json.dumps(results, indent=2, ensure_ascii=False))
            
        elif choice == '4':
            ip = input("Введите IP адрес: ").strip()
            results = tool.ip_lookup(ip)
            print(json.dumps(results, indent=2, ensure_ascii=False))
            
        elif choice == '5':
            phone = input("Введите телефонный номер: ").strip()
            results = tool.check_phone_number(phone)
            print(json.dumps(results, indent=2, ensure_ascii=False))
            
        elif choice == '6':
            target = input("Введите цель для анализа: ").strip()
            results = tool.run_comprehensive_scan(target)
            if results:
                print(json.dumps(results, indent=2, ensure_ascii=False))
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"osint_results_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"\n[+] Результаты сохранены в файл: {filename}")
            
        elif choice == '7':
            tool.list_services('russian')
            
        elif choice == '8':
            tool.list_services('international')
            
        elif choice == '9':
            print("Доступные сервисы:")
            tool.list_services()
            service_name = input("Введите название сервиса: ").strip()
            query = input("Введите запрос (или оставьте пустым): ").strip()
            tool.open_web_service(service_name, query if query else None)
            
        elif choice == '10':
            print("До свидания!")
            break
            
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
