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
from urllib.parse import urlencode, quote, urlparse
from datetime import datetime
import colorama
from colorama import Fore, Style, Back
import subprocess
import webbrowser
import random
import threading

# Инициализация colorama
colorama.init(autoreset=True)

class MegaOSINTTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
        
        # Полная база данных OSINT ресурсов
        self.resources = {
            'государственные_сервисы_россии': [
                'https://service.nalog.ru/inn.do - сервис определения ИНН физического лица',
                'http://bankrot.fedresurs.ru/ - единый федеральный реестр сведений о банкротстве',
                'http://egrul.nalog.ru/ - сведения из ЕГРЮЛ',
                'https://xn--90adear.xn--p1ai/check/driver/ - проверка водительского удостоверения',
                'http://results.audit.gov.ru/ - портал открытых данных Счетной палаты РФ',
                'http://sudact.ru/ - судебные и нормативные акты',
                'http://www.cbr.ru/credit/main.asp - справочник по кредитным организациям ЦБ РФ',
                'https://service.nalog.ru/bi.do - проверка блокировки банковских счетов',
                'http://services.fms.gov.ru/ - проверка действительности паспортов ФМС',
                'http://zakupki.gov.ru/223/dishonest/public/supplier-search.html - реестр недобросовестных поставщиков',
                'http://fedsfm.ru/documents/terrorists-catalog-portal-act - реестр террористов и экстремистов',
                'http://www.stroi-baza.ru/forum/index.php?showforum=46 - черный список строительных компаний',
                'http://xn--90afdbaav0bd1afy6eub5d.xn--p1ai/ - база данных решений судов общей юрисдикции',
                'http://www.centerdolgov.ru/ - информация о недобросовестных компаниях-должниках',
                'http://ras.arbitr.ru/ - высший арбитражный суд РФ',
                'https://rosreestr.ru/wps/portal/cc_information_online - справочная информация по объектам недвижимости',
                'http://www.voditeli.ru/ - база данных о водителях грузовых автомашин',
                'http://www.gcourts.ru/ - поисковик по судам общей юрисдикции',
                'http://www.e-disclosure.ru/ - сервер раскрытия информации по эмитентам ценных бумаг',
                'http://www.fssprus.ru/ - федеральная служба судебных приставов',
                'http://rnp.fas.gov.ru/ - реестр недобросовестных поставщиков ФАС РФ',
                'https://rosreestr.ru/wps/portal/p/cc_present/EGRN_1 - портал услуг Росреестра',
                'http://www.notary.ru/notary/bd.html - нотариальный портал',
                'http://allchop.ru/ - база частных охранных предприятий',
                'http://enotpoiskun.ru/tools/codedecode/ - расшифровка кодов ИНН, КПП, ОГРН',
                'http://polis.autoins.ru/ - проверка полисов ОСАГО',
                'http://www.vinformer.su/ident/vin.php?setLng=ru - расшифровка VIN транспортных средств',
                'http://fssprus.ru/iss/ip - банк данных исполнительных производств',
                'http://fssprus.ru/iss/ip_search - реестр розыска по исполнительным производствам',
                'http://fssprus.ru/iss/suspect_info - лица в розыске по подозрению в преступлениях',
                'http://fssprus.ru/gosreestr_jurlic/ - реестр юридических лиц по возврату задолженности',
                'http://opendata.fssprus.ru/ - открытые данные ФССП',
                'http://sro.gosnadzor.ru/ - государственный реестр саморегулируемых организаций',
                'https://rosreestr.ru/wps/portal/online_request - справочная информация по объектам недвижимости',
                'https://rosreestr.ru/wps/portal/p/cc_present/EGRN_1 - запрос сведений ЕГРН',
                'https://rosreestr.ru/wps/portal/cc_ib_opendata - открытые данные Росреестра',
                'https://pkk5.rosreestr.ru/ - публичная кадастровая карта',
                'https://www.reestr-zalogov.ru/search/index - реестр уведомлений о залоге движимого имущества',
                'https://мвд.рф/wanted - розыск МВД',
                'https://www.mos.ru/karta-moskvicha/services-proverka-grazhdanina-v-reestre-studentov/ - проверка в реестре студентов',
                'http://esugi.rosim.ru - реестр федерального имущества РФ',
                'pd.rkn.gov.ru/operators-registry - реестр операторов обработки персональных данных',
                'bankrot.fedresurs.ru - единый федеральный реестр сведений о банкротстве',
                'https://service.nalog.ru/zd.do - юрлица с налоговой задолженностью',
                'https://service.nalog.ru/addrfind.do - адреса нескольких юрлиц',
                'https://service.nalog.ru/uwsfind.do - сведения о юрлицах и ИП',
                'https://service.nalog.ru/disqualified.do - реестр дисквалифицированных лиц',
                'https://service.nalog.ru/disfind.do - юрлица с дисквалифицированными лицами',
                'https://service.nalog.ru/svl.do - лица с невозможностью участия в организации',
                'https://service.nalog.ru/mru.do - физлица - руководители нескольких юрлиц'
            ],
            'международные_ресурсы': [
                'http://www.chinacheckup.com/ - верификация китайских компаний',
                'http://www.dnb.com/products.html - Dun and Bradstreet (бизнес-информация)',
                'http://www.imena.ua/blog/ukraine-database/ - базы данных Украины',
                'https://www.marinetraffic.com - карта движения судов в реальном времени',
                'https://seatracker.ru/ais.php - карта движения судов',
                'http://shipfinder.co/ - карта движения судов',
                'https://planefinder.net/ - отслеживание самолетов',
                'https://www.radarbox24.com/ - отслеживание самолетов',
                'https://de.flightaware.com/ - отслеживание самолетов',
                'https://www.flightradar24.com - отслеживание самолетов'
            ],
            'соцсети_и_поиск_людей': [
                'https://namechk.com/ - поиск по username/nickname',
                'https://vk.com/people/ - поиск по ВКонтакте',
                'https://ok.ru/search?q= - Одноклассники',
                'https://www.facebook.com/search/people/?q= - Facebook',
                'https://www.instagram.com/ - Instagram',
                'https://t.me/ - Telegram',
                'https://my.mail.ru/people/search - Mail.ru',
                'https://twitter.com/search?q= - Twitter/X',
                'https://www.linkedin.com/search/results/people/?keywords= - LinkedIn',
                'https://sanstv.ru/photomap - поиск фото по геометкам',
                'https://findclone.ru/ - распознавание лиц (ВКонтакте)'
            ],
            'поиск_по_email': [
                'https://haveibeenpwned.com/ - проверка утечек email',
                'https://hacked-emails.com/ - проверка взломанных email',
                'https://ghostproject.fr/ - поиск утечек',
                'https://weleakinfo.com/ - поиск утечек информации',
                'https://pipl.com/ - поиск людей по email',
                'https://leakedsource.ru/ - проверка утечек'
            ],
            'поиск_по_телефону': [
                'https://phonenumber.to - поиск по номеру телефона',
                'https://pipl.com/ - поиск людей по телефону',
                '@get_kontakt_bot - Telegram-бот для поиска'
            ],
            'osint_фреймворки_и_инструменты': [
                'http://osintframework.com/ - фреймворк OSINT инструментов',
                'http://unwiredlabs.com - поиск местоположения базовой станции',
                'http://xinit.ru/bs/ - поиск базовых станций сотовых операторов'
            ],
            'бизнес_аналитика_и_базы_данных': [
                'http://www.fciit.ru/ - единая информационная система нотариата России',
                'http://gradoteka.ru/ - статистическая информация по городам РФ',
                'http://www.egrul.ru/ - поиск сведений о компаниях и директорах',
                'http://disclosure.skrin.ru - раскрытие информации на рынке ценных бумаг',
                'http://1prime.ru/docs/product/disclosure.html - раскрытие информации Прайм-ТАСС',
                'https://www.cbr.ru/ - информация ЦБ по бюро кредитных историй',
                'http://www.gks.ru/accounting_report - данные бухгалтерской отчетности',
                'http://www.tks.ru/db/ - таможенные онлайн базы данных',
                'http://tipodop.ru/ - каталог предприятий и организаций России',
                'http://www.catalogfactory.org/ - организации России с финансовыми результатами',
                'http://pravo.ru/ - справочно-информационная система нормативных актов',
                'http://azstatus.ru/ - база данных предпринимателей РФ',
                'http://seldon.ru/ - система работы с закупками',
                'http://www.reestrtpprf.ru/ - реестр надежных партнеров ТПП',
                'http://iskr-a.com/ - сообщество безопасников',
                'http://www.ruscentr.com/ - реестр базовых организаций экономики',
                'https://www.aips-ariadna.com/ - антикриминальная онлайн система',
                'http://188.254.71.82/rds_ts_pub/ - реестр зарегистрированных деклараций',
                'http://croinform.ru/index.php?page=index - сервис проверки клиентов и контрагентов',
                'http://www.zakupki.gov.ru/epz/main/public/home.html - официальный сайт госзакупок',
                'http://rostender.info/ - рассылка новых тендеров',
                'http://pravo.fso.gov.ru/ - государственная система правовой информации',
                'http://www.bicotender.ru/ - поисковая система тендеров',
                'http://sophist.hse.ru/ - архив экономических и социологических данных',
                'http://www.tenderguru.ru/ - национальный тендерный портал',
                'http://www.moscowbase.ru/ - адресно-телефонные базы данных',
                'http://www.credinform.ru/ru-RU/globas - информационно-аналитическая система ГЛОБАС',
                'http://www.actinfo.ru/ - отраслевой бизнес-справочник предприятий',
                'http://www.sudrf.ru/ - государственная система Правосудие',
                'http://docs.pravo.ru/ - справочно-правовая система Право.ру',
                'http://www.egrul.com/ - поиск по ЕГРЮЛ, ЕГРИП, ФИО',
                'http://www.fedresurs.ru/ - единый федеральный реестр сведений',
                'http://www.findsmi.ru/ - поиск по региональным СМИ',
                'http://hub.opengovdata.ru/ - открытые государственные данные',
                'http://www.ruward.ru/ - агрегатор рейтингов Рунета',
                'http://www.b2b-energo.ru/firm_dossier/ - система рынка электроэнергетики',
                'http://opengovdata.ru/ - открытые базы данных государственных ресурсов',
                'http://bir.1prime.ru/ - информационно-аналитическая система Бир-аналитик',
                'http://www.prima-inform.ru/ - доступ к информационным ресурсам',
                'http://www.integrum.ru/ - портал для конкурентной разведки',
                'www.spark-interfax.ru - информационный портал',
                'https://fira.ru/ - база данных предприятий и организаций',
                'www.skrin.ru - информация об эмитентах ценных бумаг',
                'http://www.magelan.pro/ - портал по тендерам и закупкам',
                'http://www.kontragent.info/ - информация о реквизитах контрагентов',
                'http://www.ist-budget.ru/ - веб-сервис по тендерам',
                'http://www.vuve.su/ - портал информации об организациях',
                'http://www.disclosure.ru/index.shtml - система раскрытия информации',
                'http://www.mosstat.ru/index.html - базы данных по ЕГРПО и ЕГРЮЛ',
                'http://www.torg94.ru/ - ресурс по госзакупкам',
                'http://www.k-agent.ru/ - база данных Контрагент',
                'http://www.is-zakupki.ru/ - система государственных и коммерческих закупок',
                'http://salespring.ru/ - база данных деловых контактов',
                'www.multistat.ru - многофункциональный статистический портал'
            ]
        }

        # Соцсети для поиска по ФИО
        self.social_networks = {
            'VKontakte': {
                'url': 'https://vk.com/people/{}',
                'search_url': 'https://vk.com/search?c%5Bq%5D={}&c%5Bsection%5D=people'
            },
            'Odnoklassniki': {
                'url': 'https://ok.ru/profile/{}',
                'search_url': 'https://ok.ru/search?q={}'
            },
            'Facebook': {
                'url': 'https://www.facebook.com/{}',
                'search_url': 'https://www.facebook.com/search/people/?q={}'
            },
            'Instagram': {
                'url': 'https://www.instagram.com/{}',
                'search_url': 'https://www.instagram.com/web/search/topsearch/?query={}'
            },
            'Telegram': {
                'url': 'https://t.me/{}',
                'search_url': 'https://t.me/{}'
            },
            'Twitter/X': {
                'url': 'https://twitter.com/{}',
                'search_url': 'https://twitter.com/search?q={}'
            },
            'LinkedIn': {
                'url': 'https://www.linkedin.com/in/{}',
                'search_url': 'https://www.linkedin.com/search/results/people/?keywords={}'
            },
            'Mail.ru': {
                'url': 'https://my.mail.ru/{}',
                'search_url': 'https://my.mail.ru/people/search?q={}'
            }
        }

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def print_banner(self):
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════╗
{Fore.RED}║{Fore.YELLOW}                  MEGA OSINT TOOL v2.0                   {Fore.RED}║
{Fore.RED}║{Fore.CYAN}         Комплексный инструмент для поиска информации      {Fore.RED}║
{Fore.RED}║{Fore.MAGENTA}           База данных: 200+ OSINT ресурсов             {Fore.RED}║
{Fore.RED}╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def show_resources_by_category(self):
        """Показать ресурсы по категориям"""
        print(f"\n{Fore.GREEN}📚 КАТЕГОРИИ OSINT РЕСУРСОВ:{Style.RESET_ALL}\n")
        
        categories = list(self.resources.keys())
        for i, category in enumerate(categories, 1):
            print(f"{Fore.YELLOW}{i}. {category.replace('_', ' ').title()}{Style.RESET_ALL}")
        
        try:
            choice = int(input(f"\n{Fore.YELLOW}➜ Выберите категорию (1-{len(categories)}): {Style.RESET_ALL}"))
            if 1 <= choice <= len(categories):
                selected_category = categories[choice-1]
                self.show_category_resources(selected_category)
            else:
                print(f"{Fore.RED}❌ Неверный выбор!{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}❌ Введите число!{Style.RESET_ALL}")

    def show_category_resources(self, category):
        """Показать ресурсы выбранной категории"""
        print(f"\n{Fore.GREEN}📖 РЕСУРСЫ: {category.replace('_', ' ').upper()}{Style.RESET_ALL}\n")
        
        if category in self.resources:
            for i, resource in enumerate(self.resources[category], 1):
                print(f"{Fore.CYAN}{i:2d}. {resource}{Style.RESET_ALL}")
            
            # Опция открытия ресурса
            try:
                choice = input(f"\n{Fore.YELLOW}➜ Введите номер ресурса для открытия (или Enter для возврата): {Style.RESET_ALL}")
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(self.resources[category]):
                        url = self.resources[category][idx].split(' - ')[0].strip()
                        print(f"{Fore.GREEN}🔗 Открываю: {url}{Style.RESET_ALL}")
                        webbrowser.open(url)
            except:
                pass
        else:
            print(f"{Fore.RED}❌ Категория не найдена!{Style.RESET_ALL}")

    def search_social_networks(self, fio):
        """Поиск по ФИО в социальных сетях"""
        print(f"\n{Fore.GREEN}🔍 Поиск по ФИО в соцсетях: {fio}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}⏳ Генерируем ссылки для поиска...{Style.RESET_ALL}\n")
        
        encoded_fio = quote(fio)
        
        for platform, data in self.social_networks.items():
            search_url = data['search_url'].format(encoded_fio)
            print(f"{Fore.GREEN}🔗 {platform}: {search_url}{Style.RESET_ALL}")

    def deep_search_fio(self, fio):
        """Глубокий поиск по ФИО"""
        print(f"\n{Fore.GREEN}🔍 Глубокий поиск по ФИО: {fio}{Style.RESET_ALL}")
        
        # Поиск в соцсетях
        self.search_social_networks(fio)
        
        # Поиск в поисковых системах
        print(f"\n{Fore.CYAN}🌐 Поиск в поисковых системах:{Style.RESET_ALL}")
        
        search_engines = [
            ('Google', f'https://www.google.com/search?q="{fio}"'),
            ('Yandex', f'https://yandex.ru/search/?text="{fio}"'),
            ('Bing', f'https://www.bing.com/search?q="{fio}"'),
            ('DuckDuckGo', f'https://duckduckgo.com/?q="{fio}"')
        ]
        
        for engine, url in search_engines:
            print(f"{Fore.BLUE}🔗 {engine}: {url}{Style.RESET_ALL}")
        
        # Специализированные сервисы
        print(f"\n{Fore.MAGENTA}📊 Специализированные сервисы:{Style.RESET_ALL}")
        
        special_services = [
            ('Новости', f'https://news.google.com/search?q={fio}'),
            ('Форумы', f'https://www.google.com/search?q={fio}+site:forum.ru'),
            ('Блоги', f'https://www.google.com/search?q={fio}+site:blogspot.com')
        ]
        
        for service, url in special_services:
            print(f"{Fore.CYAN}🔗 {service}: {url}{Style.RESET_ALL}")

    def search_phone(self, phone):
        print(f"\n{Fore.GREEN}🔍 Поиск информации по номеру: {phone}{Style.RESET_ALL}")
        
        try:
            parsed = phonenumbers.parse(phone, "RU")
            if not phonenumbers.is_valid_number(parsed):
                print(f"{Fore.RED}❌ Неверный номер телефона{Style.RESET_ALL}")
                return
            
            print(f"{Fore.CYAN}📞 Форматированный номер: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}{Style.RESET_ALL}")
            
            services = [
                f"https://phonenumber.to/{phone}",
                f"https://www.truecaller.com/search/ru/{phone}",
                f"https://telegram.me/{phone}"
            ]
            
            for service in services:
                print(f"{Fore.YELLOW}🔗 Проверить: {service}{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Ошибка: {e}{Style.RESET_ALL}")

    def search_email(self, email):
        print(f"\n{Fore.GREEN}📧 Поиск информации по email: {email}{Style.RESET_ALL}")
        
        services = [
            f"https://haveibeenpwned.com/account/{email}",
            f"https://ghostproject.fr/search/{email}",
            f"https://www.google.com/search?q=%22{email}%22",
            f"https://yandex.ru/search/?text=%22{email}%22"
        ]
        
        for service in services:
            print(f"{Fore.YELLOW}🔗 Проверить: {service}{Style.RESET_ALL}")

    def search_username(self, username):
        print(f"\n{Fore.GREEN}👤 Поиск по username: {username}{Style.RESET_ALL}")
        
        services = [
            f"https://namechk.com/{username}",
            f"https://www.google.com/search?q=%22{username}%22",
            f"https://yandex.ru/search/?text=%22{username}%22",
            f"https://t.me/{username}"
        ]
        
        for service in services:
            print(f"{Fore.YELLOW}🔗 Проверить: {service}{Style.RESET_ALL}")

    def show_statistics(self):
        """Показать статистику по базе данных"""
        total_resources = sum(len(resources) for resources in self.resources.values())
        print(f"\n{Fore.GREEN}📊 СТАТИСТИКА БАЗЫ ДАННЫХ:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Всего категорий: {len(self.resources)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Всего ресурсов: {total_resources}{Style.RESET_ALL}")
        
        for category, resources in self.resources.items():
            print(f"{Fore.YELLOW}│ {category.replace('_', ' ').title():25s}: {len(resources):3d} ресурсов{Style.RESET_ALL}")

    def main_menu(self):
        self.clear_screen()
        self.print_banner()
        
        while True:
            print(f"\n{Fore.GREEN}🎯 ОСНОВНОЕ МЕНЮ:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}1. 🔍 Поиск по ФИО (соцсети + интернет)")
            print(f"2. 📞 Поиск по номеру телефона")
            print(f"3. 📧 Поиск по email")
            print(f"4. 🏷️ Поиск по username")
            print(f"5. 📚 Просмотр базы OSINT ресурсов")
            print(f"6. 📊 Статистика базы данных")
            print(f"7. 🚪 Выход{Style.RESET_ALL}")
            
            choice = input(f"\n{Fore.YELLOW}➜ Выберите опцию: {Style.RESET_ALL}").strip()
            
            if choice == '1':
                fio = input(f"{Fore.YELLOW}Введите ФИО: {Style.RESET_ALL}").strip()
                if fio:
                    self.deep_search_fio(fio)
                else:
                    print(f"{Fore.RED}❌ Введите ФИО!{Style.RESET_ALL}")
            elif choice == '2':
                phone = input(f"{Fore.YELLOW}Введите номер телефона: {Style.RESET_ALL}").strip()
                if phone:
                    self.search_phone(phone)
                else:
                    print(f"{Fore.RED}❌ Введите номер телефона!{Style.RESET_ALL}")
            elif choice == '3':
                email = input(f"{Fore.YELLOW}Введите email: {Style.RESET_ALL}").strip()
                if email:
                    self.search_email(email)
                else:
                    print(f"{Fore.RED}❌ Введите email!{Style.RESET_ALL}")
            elif choice == '4':
                username = input(f"{Fore.YELLOW}Введите username: {Style.RESET_ALL}").strip()
                if username:
                    self.search_username(username)
                else:
                    print(f"{Fore.RED}❌ Введите username!{Style.RESET_ALL}")
            elif choice == '5':
                self.show_resources_by_category()
            elif choice == '6':
                self.show_statistics()
            elif choice == '7':
                print(f"{Fore.GREEN}👋 До свидания!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}❌ Неверный выбор!{Style.RESET_ALL}")

def main():
    tool = MegaOSINTTool()
    
    # Проверка зависимостей
    try:
        import colorama
    except ImportError:
        print("Устанавливаем colorama...")
        subprocess.run([sys.executable, "-m", "pip", "install", "colorama"])
        import colorama
        colorama.init(autoreset=True)
    
    try:
        import phonenumbers
    except ImportError:
        print("Устанавливаем phonenumbers...")
        subprocess.run([sys.executable, "-m", "pip", "install", "phonenumbers"])
        import phonenumbers
    
    tool.main_menu()

if __name__ == "__main__":
    main()
