import datetime
import operator
import os
import re
import urllib


class Utility(object):
    @classmethod
    def date_to_iso8601(cls, date_obj):
        """Returns an ISO8601-formatted string for datetime arg"""
        retval = date_obj.isoformat()
        return retval

    @classmethod
    def iso8601_now(cls):
        return Utility.date_to_iso8601(datetime.datetime.utcnow())

    @classmethod
    def read(cls, fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

    @classmethod
    def get_version(cls):
        raw_init_file = Utility.read("__init__.py")
        rx_compiled = re.compile(r"\s*__version__\s*=\s*\"(\S+)\"")
        ver = rx_compiled.search(raw_init_file).group(1)
        return ver

    @classmethod
    def build_ua(cls, integration_name=""):
        product = "HaloEvents"
        version = Utility.get_version()
        if integration_name == "":
            ua_string = "%s/%s" % (product, version)
        else:
            ua_string = "%s %s/%s" % (integration_name, product, version)
        return ua_string

    @classmethod
    def order_items(cls, items, sort_key):
        sorted_list = sorted(items, key=operator.itemgetter(sort_key))
        return sorted_list

    @classmethod
    def sorted_items_from_pages(cls, pages, pagination_key, sort_key):
        items = []
        for page in pages:
            for item in page[pagination_key]:
                items.append(item)
        result = Utility.order_items(items, sort_key)
        return result

    @classmethod
    def build_url(cls, base_url, modifiers):
        params = urllib.urlencode(modifiers)
        url = "%s?%s" % (base_url, params)
        return url

    @classmethod
    def create_url_batch(cls, base_url, batch_size, modifiers={}):
        """We initially set the 'since' var to the start_timestamp.  The next
        statement will override that value with the last event's timestamp, if
        one is set

        """
        url_list = []
        for page in range(1, batch_size + 1):
            url = None
            modifiers["page"] = page
            url = Utility.build_url(base_url, modifiers)
            url_list.append(url)
        return url_list

    @classmethod
    def get_number_of_empty_pages(cls, pages):
        empty_pages = 0
        for page in pages:
            if page["events"] == []:
                empty_pages += 1
        return empty_pages

    @classmethod
    def get_number_of_full_pages(cls, pages, page_size):
        full_pages = 0
        for page in pages:
            if len(page["events"]) == page_size:
                full_pages += 1
        return full_pages
