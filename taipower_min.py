import os
import json
from lib.crawler import MinuteCrawler, DayCrawler, DayAppendCrawler, CrawlerCollector, DataMissingException 

BASE_PATH = '~/data/TaiPower'
MAX_TIME = 1440
WAITING_SEC = 60

def format_usage_json(jfile):
    '''
    Format a total usage .csv file to csv tuple for recording
    Input:
        List of contents crawl from taipower read as .csv
    Output:
        List of a string and the first column must be the record time
    '''
    needed = [l.replace('"','').replace('\n','').replace(',','')
                for l in jfile[2:6]]
    seperate = needed[-1].split(':')
    hr = seperate[0][-2:]
    minute = seperate[1][:2]
    # print(hr, minute)
    del needed[-1]
    needed.insert(0,'{}:{}'.format(hr,minute))
    needed = [','.join(needed)+'\n']
    # print(needed)

    return needed

def format_genary_json(jfile):
    '''
    Format a genary .csv file to csv contents for recording
    Input:
        List of contents crawl from taipower read as .csv
    Output:
        List of csv tuple for recording and the first line must be the record time
    '''
    contents = json.loads(jfile[0])
    rtime = contents['']
    contents = [','.join(l[1:]).strip().replace('-','')
                 + '\n' for l in contents['aaData']]
    contents.insert(0, rtime+ '\n')
    return contents

if __name__ == '__main__':
    genaryCrawler = MinuteCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.txt',
                        os.path.join(BASE_PATH, 'genary/'),
                        format_genary_json)
    fuelTypeCrawler = DayCrawler(
                    'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadfueltype.csv',
                    os.path.join(BASE_PATH, 'fueltype/'))
    areasCrawler = DayCrawler(
                    'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadareas.csv',
                    os.path.join(BASE_PATH, 'area/day_usage/'))
    areasGenCrawler = DayAppendCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genloadareaperc.csv',
                        os.path.join(BASE_PATH, 'area/gen_usage/'))
    totalUsageCrawler = DayAppendCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadpara.txt',
                        os.path.join(BASE_PATH, 'total/'),
                        format_usage_json)
    
    # Type DayAppendCrawler Must Seperate collect
    crawl_list = [genaryCrawler, fuelTypeCrawler, areasCrawler]
    append_crawl_list = [areasGenCrawler, totalUsageCrawler]

    acc = CrawlerCollector(1, 0)
    acc.add(append_crawl_list)
    acc.all_crawl()

    cc = CrawlerCollector(MAX_TIME, WAITING_SEC)
    cc.add(crawl_list)
    cc.all_crawl()
