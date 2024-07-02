import requests
import urllib3
import sys

# InsecureRequestWarning xəbərdarlığını söndürürük
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Rəng kodları
RESET = '\033[0m'
GREEN = '\033[92m'
BLUE = '\033[94m'
RED = '\033[91m'
YELLOW = '\033[93m'

# Funksiyanı yazaq
def check_links():
    # Faylların tam yolunu daxil edin
    link_file_path = 'link.txt'
    param_file_path = 'param.txt'
    
    # Faylları oxuyuruq
    with open(link_file_path, 'r') as link_file:
        links = link_file.read().splitlines()

    with open(param_file_path, 'r') as param_file:
        params = param_file.read().splitlines()

    results = []
    counts = {
        'completed': 0,
        '200': 0,
        '300': 0,
        '400': 0,
        '500': 0
    }
    
    # Ümumi linklərin sayını hesablayırıq
    total_requests = len(links) * len(params)

    # Hər link üçün
    for link in links:
        for param in params:
            # Tam URL yığılır
            full_url = f"{link}{param}"
            try:
                response = requests.get(full_url, verify=False)  # SSL doğrulamasını ləğv edirik
                code = response.status_code
                length = len(response.content) # KB olaraq tam ədəd
                result = {
                    'code': code,
                    'length': length,
                    'url': full_url
                }
                results.append(result)
                
                # Sayğacları yeniləyirik
                counts['completed'] += 1
                if 200 <= code < 300:
                    counts['200'] += 1
                elif 300 <= code < 400:
                    counts['300'] += 1
                elif 400 <= code < 500:
                    counts['400'] += 1
                elif 500 <= code < 600:
                    counts['500'] += 1
                
                # Terminalda məlumatları göstəririk (tək sətirdə yeniləyirik)
                sys.stdout.write(f"\rCompleted: {counts['completed']}/{total_requests} | {GREEN}SUCCESS: {counts['200']}{RESET} | {BLUE}REDIRECT: {counts['300']}{RESET} | {RED}CLIENT ERR: {counts['400']}{RESET} | {YELLOW}SERVER ERR: {counts['500']}{RESET}")
                sys.stdout.flush()
            except requests.RequestException as e:
                print(f"\nError occurred for URL: {full_url} -> {e}")

    # İrəliləmə məlumatlarını göstərdikdən sonra iki sətir aşağı düşürük
    print("\n\n")

    # Nəticələri HTTP status koduna görə sıralayırıq
    sorted_results = sorted(results, key=lambda x: (x['code'], -x['length']))

    # Nəticələri qruplara ayırırıq
    grouped_results = {}
    for result in sorted_results:
        code = result['code']
        if code not in grouped_results:
            grouped_results[code] = []
        grouped_results[code].append(result)

    # Ekranda göstəririk və fayla yazırıq
    results_file_path = 'results.txt'
    with open(results_file_path, 'w') as result_file:
        for code in sorted(grouped_results.keys()):
            # İçəridə səhifə ölçüsünə görə azalan sıraya görə düzəldirik
            for result in sorted(grouped_results[code], key=lambda x: -x['length']):
                color_code = RESET
                if 200 <= code < 300:
                    color_code = GREEN
                elif 300 <= code < 400:
                    color_code = BLUE
                elif 400 <= code < 500:
                    color_code = RED
                elif 500 <= code < 600:
                    color_code = YELLOW
                
                hehe = '\t' if result['length'] < 1000 else ''
                result_str = f"CODE: {color_code}{code}{RESET} | LEN: {result['length']} KB{hehe}\t[*]\t{result['url']}"
                print(result_str)
                result_file.write(result_str + "\n")
            result_file.write("++++++++\n")
            print("++++++++")

# Funksiyanı çağırırıq
check_links()

