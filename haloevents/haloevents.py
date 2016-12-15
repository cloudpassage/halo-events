"""This class provides an iterator.  Under the covers it does multi-threaded
consumption of events, only providing information to the iterator when it's
been ordered correctly."""

import cloudpassage
from multiprocessing.dummy import Pool as ThreadPool
from utility import Utility


class HaloEvents(object):

    def __init__(self, halo_key, halo_secret,
                 api_host="api.cloudpassage.com",
                 api_port=443,
                 start_timestamp=Utility.iso8601_now(),
                 max_threads=10,
                 batch_size=20,
                 integration_name=""):
        self.halo_key = halo_key
        self.halo_secret = halo_secret
        self.api_host = api_host
        self.api_port = api_port
        self.start_timestamp = start_timestamp
        self.max_threads = max_threads
        self.batch_size = batch_size
        self.last_event_timestamp = None
        self.events = []
        self.halo_session = None
        self.ua = Utility.build_ua(integration_name)

    def __iter__(self):
        while True:
            for event in self.get_next_batch():
                yield event

    def get_next_batch(self):
        url_list = self.create_url_list()
        pages = self.get_pages(url_list)
        events = Utility.sorted_items_from_pages(pages, "events", "created_at")
        last_event_timestamp = events[-1]['created_at']
        self.last_event_timestamp = last_event_timestamp
        return events

    def build_halo_session(self):
        halo_session = cloudpassage.HaloSession(self.halo_key,
                                                self.halo_secret,
                                                api_host=self.api_host,
                                                api_port=self.api_port,
                                                integration_string=self.ua)
        return halo_session

    def create_url_list(self):
        """We initially set the 'since' var to the start_timestamp.  The next
        statement will override that value with the last event's timestamp, if
        one is set

        """

        base_url = "/v1/events"
        modifiers = {}
        if self.start_timestamp is not None:
            modifiers["since"] = self.start_timestamp
        if self.last_event_timestamp is not None:
            modifiers["since"] = self.last_event_timestamp
        url_list = Utility.create_url_batch(base_url, self.batch_size,
                                            modifiers=modifiers)
        return url_list

    def get_pages(self, url_list):
        halo_session = self.build_halo_session()
        page_helper = cloudpassage.HttpHelper(halo_session)
        pool = ThreadPool(self.max_threads)
        results = pool.map(page_helper.get, url_list)
        pool.close()
        pool.join()
        return results
