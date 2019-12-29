import requests
import lxml.html
from datetime import datetime
from time import sleep

class Crawler(object):
    def __init__(self,
                 base_url='https://www.csie.ntu.edu.tw/news/',
                 rel_url='news.php?class=101'):
        self.base_url = base_url
        self.rel_url = rel_url

    def crawl(self, start_date, end_date,
              date_thres=datetime(2012, 1, 1)):
        """Main crawl API

        1. Note that you need to sleep 0.1 seconds for any request.
        2. It is welcome to modify TA's template.
        """
        if end_date < date_thres:
            end_date = date_thres
        contents = list()
        page_num = 0
        while True:
            rets, last_date = self.crawl_page(
                start_date, end_date, page=f'&no={page_num}')
            page_num += 10
            if rets:
                contents += rets
            if last_date < start_date:
                break
        return contents

    def crawl_page(self, start_date, end_date, page=''):
        """Parse ten rows of the given page

        Parameters:
            start_date (datetime): the start date (included)
            end_date (datetime): the end date (included)
            page (str): the relative url specified page num

        Returns:
            content (list): a list of date, title, and content
            last_date (datetime): the smallest date in the page
        """
        html = requests.get(
            self.base_url + self.rel_url + page,
            headers={'Accept-Language':
                     'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6'}
        )
        doc = lxml.html.fromstring(html.content)
        sleep(0.1)
        # TODO: parse the response and get dates, titles and relative url with etree
        contents = list()
        table = doc.xpath('.//table[@id="RSS_Table_page_news_1"]')[0]
        body = table.xpath('tbody')[0]
        total_news = body.xpath('.//tr')
        rel_urls = []
        dates = []
        titles = []

        for news in total_news:
            date = news[0].text
            date = datetime.strptime(date, "%Y-%m-%d")
            last_date = date
            rel_url_path = news.xpath('.//a')[0]
            title = rel_url_path.text
            title = title.replace('"','""')
            title = title.split()
            title = ','.join(title)
            rel_url = rel_url_path.get('href')
            if last_date >= start_date and last_date <= end_date:
                dates.append(date)
                titles.append(title)
                rel_urls.append(rel_url)
        
        i = 0
        for rel_url in rel_urls:
            # TODO: 1. concatenate relative url to full url
            #       2. for each url call self.crawl_content
            #          to crawl the content
            #       3. append the date, title and content to
            #          contents
            
            full_url = self.base_url + rel_url
            contents.append(dates[i])
            contents.append(titles[i])
            contents.append(self.crawl_content(full_url))
            i += 1  
        return contents, last_date

    def crawl_content(self, url):
        """Crawl the content of given url

        For example, if the url is
        https://www.csie.ntu.edu.tw/news/news.php?Sn=15216
        then you are to crawl contents of
        ``Title : 我與DeepMind的A.I.研究之路, My A.I. Journey with DeepMind Date : 2019-12-27 2:20pm-3:30pm Location : R103, CSIE Speaker : 黃士傑博士, DeepMind Hosted by : Prof. Shou-De Lin Abstract: 我將與同學們分享，我博士班研究到加入DeepMind所參與的projects (AlphaGo, AlphaStar與AlphaZero)，以及從我個人與DeepMind的視角對未來AI發展的展望。 Biography: 黃士傑, Aja Huang 台灣人，國立臺灣師範大學資訊工程研究所博士，現為DeepMind Staff Research Scientist。``
        """
        html = requests.get(url)
        doc = lxml.html.fromstring(html.content)
        all_editor_content = doc.xpath('.//div[@class="editor content"]')
        content = ''
        for editor_content in all_editor_content:
           content += ','.join(map(str.strip, editor_content.xpath(".//text()")))
        content = content.replace('"','""')
        content = content.split()
        content = ','.join(content)
        return content
        raise NotImplementedError
