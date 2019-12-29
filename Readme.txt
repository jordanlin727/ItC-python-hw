Team member:
B08902115 鄭諾駿
B05902131 林子翔

How to implement:
(get_args)
1.We get the start date, end date and output file name for the command.
(Crawler)
2.In order to get all the news from the CSIE page, we get the html from the website by 'requests'.
(crawler.crawl)
3.We get the date, title and link of the content from the table with id 'RSS_Table_page_news_1'in the html.
4.We check whether the date is in range, if it is, we go in the the link and get its html also by 'requests', and we form a string of all the words in div with id 'editor content' with is content.
5.We put all the data within time range to the contents list.
6.We flip to the next page by the link from the last href  of the table if the last date doesn't pass the start date.
7.After the last date passes the start date we break the loop and put return the contents list to main.py.
(main)
8.We put all the date, title and content from the contents list into a csv file with the given name.

Environment:
CSIE Workstsaion
Python 3.6.2
lxml == 4.4.2
tqdm == 4.28.1

Collaboration contribution:
B08902115 鄭諾駿: Python programming (args.py, crawler.py, main.py) & test, readme.txt.
B05902131 林子翔: Github part, code review & modification, readme.txt.