import unittest
from src.work_xml import generate_html, set_cache_news, read_cache_file, re_generate_cache, take_xml_items
from src.rss_reader import get_version



class TestStringMethods(unittest.TestCase):

    def test_generate_html(self):
        items = dict()
        items[0] = {'title': 'Проблема перегороженных улиц',
                    'pubDate': 'Tue, 28 Jun 2022 19:52:00 +0300',
                    'description': 'Празднование Дня города прошло на высоком уровне - была '
                                   'составлена насыщенная программа, соблюдались меры '
                                   'безопасности и контроля, оперативно убран мусор. ',
                    'link': 'https://vse.sale/news/view/37519', }
        generate = generate_html({'title': str(), 'items': items})
        HTML_file = open("tests/HTML_file.html", "r")
        html = HTML_file.read()
        HTML_file.close()
        self.assertEqual(generate, html)

    def test_re_generate_cache(self):
        source = 'https://vse.sale/news/rss'
        items = dict()
        items[0] = {
                "title": "Проблема перегороженных улиц",
                "pubDate": "Tue, 28 Jun 2022 19:52:00 +0300",
                "description": "Празднование Дня города прошло на высоком уровне.",
                "link": "https://vse.sale/news/view/37519",
            }
        generate = re_generate_cache(dict(), source, items)
        cache_file = open("tests/cache.json", "r")
        cache = cache_file.read()
        cache_file.close()
        self.assertEqual(str(generate), cache)

    def test_version(self):
        version = "Version 1.4"
        self.assertEqual(version, get_version())

    def test_take_xml_items(self):
        xml_items = take_xml_items('https://vse.sale/news/rss', 10)
        self.assertTrue('items' in xml_items.keys() and bool(xml_items['items']))

    def test_write_read_cache(self):
        source = 'https://vse.sale/news/rss'
        xml_items = take_xml_items(source, 10)
        set_cache_news(source, xml_items['items'])
        self.assertTrue(bool(read_cache_file()))

if __name__ == 'main':
    unittest.main()

# python3 -m unittest tests/unit_rss.py
