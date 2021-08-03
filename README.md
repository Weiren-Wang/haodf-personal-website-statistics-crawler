# haodf-personal-website-statistics-crawler
好大夫医生主页个人网站数据统计爬虫

说明：
本代码用于爬取好大夫医生主页上的个人网站数据统计数据，如下图红方块部分所示
![image](https://github.com/Weiren-Wang/haodf-personal-website-statistics-crawler/blob/main/example.png)

Requirements：
1.Firefox浏览器
2.Geckodriver驱动
3.文件中import的packages
4.包含要爬取的医生主页url的excel，例如下图
![image](https://github.com/Weiren-Wang/haodf-personal-website-statistics-crawler/blob/main/requirement1.png)

使用：
1.下载haodf-statistics-crawler.py
1.将excel文件与py文件放置在一个目录下，将py文件中第23行的"durl_y.xls"替换为包含需要爬取的医生主页url的xls文件
2.终端中cd到py文件目录下输入python haodf-statistics-crawler.py即可
