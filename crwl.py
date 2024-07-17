import argparse
import requests
import bs4
import logging
import hashlib
import sys
from datetime import datetime
from colorama import init
from termcolor import colored
import threading
from queue import Queue

logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

init()

# ARRAY LIST FOR CRAWLER
external = []
unknown = []

def extractor(soup, host):
    all_links = list()
    for link in soup.find_all('a', href=True):
        if link['href'].startswith('/'):
            if link['href'] not in all_links:
                all_links.append(host + link['href'])
        elif host in link['href']:
            if link['href'] not in all_links:
                all_links.append(link['href'])
        elif 'http://' in host:
            if 'https://' + host.split('http://')[1] in link['href'] and link['href'] not in all_links:
                all_links.append(link['href'])
        elif 'http' not in link['href'] and 'www' not in link['href'] and len(link['href']) > 2 and '#' not in link['href']:
            if link['href'] not in all_links:
                all_links.append(host + '/' + link['href'])
        elif len(link['href']) > 6:
            external.append(link['href'])
        else:
            unknown.append(link['href'])
    return all_links

def xploit(link, host=None):
    if host is None:
        host = link
    try:
        res = requests.get(link, allow_redirects=True)
        soup = bs4.BeautifulSoup(res.text, features="xml")
        return extractor(soup, host)
    except Exception as e:
        print(colored(f"[Error] Failed to exploit {link}: {e}", 'red'))
        return []

def xploit_worker(queue, host, results):
    while not queue.empty():
        link = queue.get()
        try:
            links = xploit(link, host)
            results.extend(links)
        except Exception as e:
            print(colored(f"[Error] Failed to exploit {link}: {e}", 'red'))
        finally:
            queue.task_done()

def level2(linklist, host, my_Thread):
    final_list = list()
    queue = Queue()
    results = []

    for link in linklist:
        queue.put(link)

    threads = []
    for _ in range(int(my_Thread)):
        t = threading.Thread(target=xploit_worker, args=(queue, host, results))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    final_list.extend(results)
    final_list = list(set(final_list))

    return final_list

def get_html_text(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        return None

def md5_hash(text):
    md5 = hashlib.md5()
    md5.update(text.encode('utf-8'))
    return md5.hexdigest()

def crawl_and_hash(url, all_md5, my_Thread):
    links = level2(xploit("https://" + url), "https://" + url,my_Thread)
    count_link = 1
    if len(links) > 1:
        for link in links:
            sys.stdout.write(colored(f"\r[*] Loading {count_link}/{len(links)} URL...",'light_green'))
            sys.stdout.flush()
            count_link+=1
            html_text = get_html_text(link)
            if html_text:
                soup = bs4.BeautifulSoup(html_text, 'html.parser')
                text_to_hash = '\n'.join([tag.get_text() for tag in soup.find_all('body')])
                hashed_text = md5_hash(text_to_hash)
                all_md5.add(f"{hashed_text}|{link}")
                # print(colored(f"[✔] {hashed_text}|{link}","light_green"))
        sys.stdout.flush()


def worker(queue, all_md5, my_Thread):
    while not queue.empty():
        url = queue.get()
        crawl_and_hash(url, all_md5, my_Thread)
        queue.task_done()



def matchHash(urlhash,md5hash):
    html_text = get_html_text(urlhash)
    if html_text:
        soup = bs4.BeautifulSoup(html_text, 'html.parser')
        text_to_hash = '\n'.join([tag.get_text() for tag in soup.find_all('body')])
        hashed_text = md5_hash(text_to_hash)
        if(hashed_text == md5hash):
            return True
        else:
            return False
        

def check_worker(queue):
    while not queue.empty():
        mdlink = queue.get()
        urlHash = mdlink.split('|')[1]
        md5Hash = mdlink.split('|')[0]
        check_match = matchHash(urlHash, md5Hash)
        if check_match:
            with open("./results/" + str(datetime.now().date()) + ".txt", 'a') as o:
                o.write(f"MATCH|{md5Hash}|{urlHash}\n")
                print(colored(f"MATCH|{md5Hash}|{urlHash}", 'light_green'))
        else:
            with open("./results/" + str(datetime.now().date()) + ".txt", 'a') as o:
                o.write(f"NOT MATCH|{md5Hash}|{urlHash}\n")
                print(colored(f"NOT MATCH|{md5Hash}|{urlHash}", 'light_red'))
        queue.task_done()




def main():
    print(colored("""
 ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
 ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓█████████████▓▒░░▒▓████████▓▒░ 

    __CRAWL AND SECURE YOUR WEBSITE__
    __MADE BY BUDIBLACK__
    x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x

    Usage : -h for help.                                                 
""", 'red'))

    parser = argparse.ArgumentParser(description=colored("List Commands :", 'white'))
    parser.add_argument('--crawl', type=str, help=colored("Crawl and save links into txt file - (.txt file without https/http contains).", 'blue'))
    parser.add_argument('--check', type=str, help=colored("Check if file has changed or not (md5 match) - (.txt file).", 'blue'))
    parser.add_argument('--thread', type=str, help=colored("Number of threads.", 'blue'))
    args = parser.parse_args()

    my_Thread=10

    if args.thread:
        my_Thread = args.thread

    if args.crawl:
        with open(args.crawl, 'r') as file:
            lines_link = file.read().split('\n')
        
        print(colored(f"\n\n[!] Waiting for crawling -> [{args.crawl}]...", 'red'))
        print(colored(f"[!] Thread Number -> [{my_Thread}]\n", 'red'))

        all_md5 = set()
        queue = Queue()

        for link in lines_link:
            queue.put(link)

        threads = []
        for _ in range(int(my_Thread)):
            t = threading.Thread(target=worker, args=(queue, all_md5, my_Thread))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        for linkz in all_md5:
            with open("./crawl/" + str(datetime.now().date()) + ".txt", 'a') as o:
                o.write(f"{linkz}\n")

        print(colored(f"\n[Success] All links have been crawled and hashed to md5, output file => ./crawl/{str(datetime.now().date())}.txt", 'green'))

    elif args.check:
        with open(args.check, 'r') as file:
            lines_link = file.read().split('\n')

        print(colored(f"\n\n[!] Waiting for checking and matching -> [{args.check}]...", 'red'))

        queue = Queue()

        for mdlink in lines_link:
            queue.put(mdlink)

        threads = []
        for _ in range(int(my_Thread)):
            t = threading.Thread(target=check_worker, args=(queue,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        print(colored(f"\n[Success] All links have been matched and checked, output file => ./results/{str(datetime.now().date())}.txt", 'green'))



if __name__ == "__main__":
    main()

