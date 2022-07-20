import argparse
import logging
from src import work_xml


def main():
    arg_parser = argparse.ArgumentParser(description="Pure Python command-line src reader.")
    arg_parser.add_argument("source", nargs='?', default='', type=str, help="src reader URL")
    arg_parser.add_argument("--version", action="store_true", help="Print version info")
    arg_parser.add_argument("--json", action="store_true", help=" Print result as JSON in stdout")
    arg_parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    arg_parser.add_argument("--limit", type=int, help="Limit news topics if this parameter provided")
    arg_parser.add_argument("--date", type=int, help="Outputs news from cash by date. Required format: 20220525")
    arg_parser.add_argument("--html", type=str, help=" Print result as HTML format in file. Required - path to save.")
    arg_parser.add_argument("--pdf", type=str, help=" Print result as PDF format in file. Required - path to save.")

    args = arg_parser.parse_args()

    xml_items = False

    if args.verbose:
        logging.basicConfig(level=logging.INFO)

    try:
        if args.version:
            print(get_version())
        elif args.source == '':
            if args.date:
                xml_items = work_xml.get_cache_news(args.date)
            else:
                print("URL is are required")
                return False
        elif args.date:
            xml_items = work_xml.get_cache_news(args.date, args.source)
        else:
            xml_items = work_xml.take_xml_items(args.source, args.limit)
            work_xml.set_cache_news(args.source, xml_items["items"])

        if xml_items == False:
            return False

        if args.json:
            work_xml.generate_json(xml_items)
        elif args.html:
            work_xml.save_html(args.html, work_xml.generate_html(xml_items))
        elif args.pdf:
            work_xml.generate_pdf(args.pdf, xml_items)
        else:
            work_xml.print_to_console(xml_items)
    except AttributeError:
        print("Error, failed to get an attribute. Check correctness URL")


def get_version():
    return "Version 1.4"


if __name__ == "__main__":
    main()
