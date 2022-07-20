Thank you for choosing our program.
1. After downloading the program from the RSS_reader directory, 
enter the commands in console:
    python3 setup.py sdist
    pip install dist/rss_reader-1.4.tar.gz
2. please install all the libraries listed in requirements.txt file.
3. RSS reader  a command-line utility which receives RSS URL and outputs the results in a human-readable format
You can enter to console: 
example: rss_reader https://vse.sale/news/rss 
or from directory crc
example: python3 rss_reader.py https://vse.sale/news/rss
4. If you need limited number of articles then enter after the link  --limit
example: rss_reader https://vse.sale/news/rss --limit 3 
5. If you want to know the version of the application enter after --version
example: rss_reader https://vse.sale/news/rss --version
or example: rss_reader --version
6. If you want out in console news in format json then enter after the link --json
example: rss_reader https://vse.sale/news/rss --json
7. If you want write the information from the article to a file in the format pdf or html, 
you need then enter after the link --pdf or --html after Required - path to save.
if your sistem Linux: 
example: rss_reader https://vse.sale/news/rss --pdf /home/m/PycharmProjects/Homework_new/RSS_reader
or if your sistem Windows: 
example: rss_reader https://vse.sale/news/rss --html C:\\Program Files\\RSS_reader\\
8. If you want get information from the cache, you need enter --date and 
the date you need in the format '%Y%m%d' example: 20220627 (2022 is year, 06 is month, 27 is day)
exemple: rss_reader https://vse.sale/news/rss --date 20220627
or exemple: rss_reader --date 20220627
The cache is stored in a file with the json format. Example structure:
{
  '20220628': {
    'https://vse.sale/news/rss': {
      'The problem of blocked streets': {
        'title': 'The problem of blocked streets',
        'pubDate': 'Tue, 28 Jun 2022 19:52:00 +0300',
        'description': 'The celebration of the City Day was held at a high level.',
        'link': 'https://vse.sale/news/view/37519'
      }
      'Of blocked streets': {
        'title': 'Of blocked streets',
        'pubDate': 'Tue, 28 Jun 2022 19:52:00 +0300',
        'description': 'The celebration of the City Day was held at a high level.',
        'link': 'https://vse.sale/news/view/375171892'
      }
    }
  }
}


