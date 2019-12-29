from crawler import Crawler
from args import get_args
import csv
from datetime import datetime


if __name__ == '__main__':
    args = get_args()
    crawler = Crawler()
    content = crawler.crawl(args.start_date, args.end_date)
    # TODO: write content to file according to spec
    with open(args.output,'w',newline='') as f:
        fieldnames = ['Post date','Title','Content']
        thewriter = csv.DictWriter(f, fieldnames = fieldnames)
        thewriter.writeheader()
        for i in range(0,int(len(content)/3)):
            thewriter.writerow({'Post date':content[i*3].strftime('%Y-%m-%d'),'Title':content[i*3+1],'Content':content[i*3+2]})
