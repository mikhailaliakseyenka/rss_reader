from dateutil import parser
from fpdf import fpdf
from bs4 import BeautifulSoup, Tag
import requests
import json
import logging
import os

system_path = os.path.dirname(os.path.abspath(__file__))
cache_file = os.path.join(system_path, 'cache.json')


def take_xml_items(link, limit):  # we accept the url and the limit and return the dict
    logging.info("Take xml items started")
    try:
        r = requests.get(link)
        soup = BeautifulSoup(r.content, features='xml')

        title = soup.find('channel').findChildren("title", recursive=False)  # out name feed
        if title:
            title = title[0].get_text()
        else:
            title = ''

        items_temp = soup.findAll("item", limit=limit)
        items = dict()
        key = 0
        for item in items_temp:
            items[key] = {'title': item.title.get_text(),
                          'pubDate': item.pubDate.get_text(),
                          'description': item.description.get_text() if item.description else 'No description',
                          'link': item.link.get_text() if item.link else 'No link', }
            key += 1
        logging.info("Take xml items finished successfully")

        return {'title': title, 'items': items}
    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Take xml items with exception")
        return False


def print_to_console(xml_items):  # output the fields to the console
    logging.info("Print to console started")
    try:
        if 'title' in xml_items:
            print(f"Feed: {xml_items['title']}")

        for item in xml_items['items'].values():
            print(f"Title: {item['title']}")
            print(f"Date: {item['pubDate']}")
            print(f"Link: {item['link']}")
            print(f"Description: {item['description']}")

        logging.info("Print to console finished successfully")
    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Print to console finished with exception")
        return False


def generate_json(xml_items):
    logging.info("Generate json started")
    try:
        for item in xml_items['items'].values():
            json_item = json.dumps(item, indent=4)
            print(json_item)

        logging.info("Generate json finished successfully")

    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Generate json finished with exception")
        return False


def read_cache_file():
    logging.info("Read cache file started")
    try:
        if os.path.exists(cache_file) and os.path.getsize(cache_file) > 0:
            with open(cache_file, 'r') as file:
                cache = json.load(file)
        else:
            logging.info("Read cache file: cache file is not exist")
            return dict()

        logging.info("Read cache file finished successfully")
        return cache
    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Read cache file finished with exception")
        return False


def write_cache_file(cache):
    logging.info("Write cache file started")
    try:
        with open(cache_file, 'w+') as file:
            json.dump(cache, file, indent=4)

        logging.info("Write cache file finished successfully")
    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Write cache file finished with exception")
        return False


def re_generate_cache(cache_object, source, items):
    logging.info("Re-generate cache started")
    try:
        for item in items.values():
            date = parser.parse(item['pubDate']).strftime('%Y%m%d')

            if date not in cache_object:
                cache_object[date] = dict()

            if source not in cache_object[date]:
                cache_object[date][source] = dict()

            cache_object[date][source][item['title']] = item
        logging.info("Re-generate cache finished successfully")
        return cache_object
    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Re-generate cache finished with exception")
        return False


def set_cache_news(source, items):
    logging.info("Set cache news started")
    try:
        cache = read_cache_file()
        if not cache:
            cache = dict()

        cache = re_generate_cache(cache, source, items)

        write_cache_file(cache)
        logging.info("Set cache news finished successfully")
        return cache

    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Set cache news finished with exception")
        return False


def get_cache_news(date, source=False):
    logging.info("Get cache news started")
    try:
        cache = read_cache_file()
        date = str(date)

        if date in cache:
            if source != False and source in cache[date]:
                items = dict()
                key = 0
                for item in cache[date][source].values():
                    items[key] = item
                    key += 1
                logging.info("Get cache news by date and source finished successfully")
                return {'items': items}
            elif source != False:
                print(f'News by date and source not found in cache')
                logging.info("News by date and source not found in cache")
                return False
            else:
                items = dict()
                key = 0
                for key_source in cache[date]:
                    for item in cache[date][key_source].values():
                        items[key] = item
                        key += 1
                logging.info("Get cache news by date finished successfully")
                return {'items': items}
        else:
            print(f'News by date not found in cache')
            logging.info("News by date not found in cache")
            return False

    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Get cache news finished with exception")
        return False


def generate_html(xml_items):
    logging.info("Generate html started")
    soup = BeautifulSoup()
    html = Tag(soup, name="html")
    body = Tag(soup, name="body")
    soup.append(html)
    html.append(body)

    try:
        for item in xml_items['items'].values():
            div = Tag(soup, name="div")

            h1 = Tag(soup, name="h1")
            h1.string = item['title']
            pPubDate = Tag(soup, name="p")
            pPubDate.string = item['pubDate']
            pdescription = Tag(soup, name="p")
            pdescription.string = item['description']
            alink = Tag(soup, name="a")
            alink.string = item['link']

            div.append(h1)
            div.append(pPubDate)
            div.append(pdescription)
            div.append(alink)

            body.append(div)

        return soup.prettify()

    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Generate html finished with exception")
        return False


def save_html(path, html_str):
    logging.info("Save html started")
    try:
        with open(os.path.join(path, "HTML_file.html"), 'w', encoding='utf-8') as file:
            file.write(html_str)
        logging.info("Save html finished successfully")

    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Save html finished with exception")
        return False


def generate_pdf(path, xml_items):
    logging.info("Generate pdf started")

    try:
        pdf = fpdf.FPDF()
        pdf.add_font("Sans", style="", fname="Noto_Sans/NotoSans-Regular.ttf", uni=True)
        pdf.set_font("Sans", size=16)

        pdf.add_page()

        feed = xml_items['title']
        pdf.cell(200, 10, feed, ln=1, align='C')

        for item in xml_items['items'].values():
            pdf.cell(200, 10, 'NEWS', ln=1, align='C')
            pdf.multi_cell(200, 10, item['title'])
            pdf.multi_cell(200, 10, item['pubDate'])
            pdf.multi_cell(200, 10, item['description'])
            pdf.multi_cell(200, 10, f"Link: {item['link']}")

        pdf.output(os.path.join(path, "PDF_file.pdf"))
        logging.info("Generate pdf finished successfully")

    except Exception as e:
        print(f'This extraction job failed. See exceptions: {e}')
        logging.info("Generate pdf finished with exception")
        return False