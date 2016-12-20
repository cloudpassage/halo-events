"""This class provides an iterator.  Under the covers it does multi-threaded
consumption of events, only providing information to the iterator when it's
been ordered correctly."""

import cloudpassage
from multiprocessing.dummy import Pool as ThreadPool
import time
from utility import Utility


class HaloEvents(object):
    """Initialize a CloudPassage Halo event retrieval object

    Args:
        halo_key (str): API key for CloudPassage Halo
        halo_secret (str): API key secret for CloudPassage Halo

    Keyword Args:
        api_host (str): Hostname for Halo API.  Default is api.cloudpassage.com
        api_port (str): Port for API endpoint.  Defaults to 443
        start_timestamp (str): ISO8601-formatted string.  Defalults to now.
        max_threads (int): Max number of open threads.  Defaults to 10.
        batch_size (int): Limit the depth of the query.  Defaults to 20.
        integration_name (str): Name of the tool using this library.
        search_params (dict): Params for event query


    """
    def __init__(self, halo_key, halo_secret, **kwargs):
        self.halo_key = halo_key
        self.halo_secret = halo_secret
        self.api_host = "api.cloudpassage.com"
        self.api_port = 443
        self.start_timestamp = Utility.iso8601_now()
        self.max_threads = 10
        self.batch_size = 20
        self.last_event_timestamp = None
        self.last_event_id = ""
        self.events = []
        self.halo_session = None
        self.ua = Utility.build_ua("")
        self.search_params = {}
        self.set_attrs_from_kwargs(kwargs)

    def __iter__(self):
        """Yields events one at a time. Forever."""
        while True:
            for event in self.get_next_batch():
                yield event

    def set_attrs_from_kwargs(self, kwargs):
        arg_list = ["start_timestamp", "max_threads", "batch_size",
                    "search_params", "api_host", "api_port"]
        for arg in arg_list:
            if arg in kwargs:
                setattr(self, arg, kwargs[arg])
        if "integration_name" in kwargs:
            setattr(self, "ua", Utility.build_ua(kwargs["integration_name"]))

    def get_next_batch(self):
        """Gets the next batch of events from the Halo API"""
        url_list = self.create_url_list()
        pages = self.get_pages(url_list)
        events = Utility.sorted_items_from_pages(pages, "events", "created_at")
        if events[0]["id"] == self.last_event_id:
            del events[0]
        try:
            last_event_timestamp = events[-1]['created_at']
        except IndexError:
            time.sleep(3)
            return []
        last_event_timestamp = events[-1]['created_at']
        last_event_id = events[-1]['id']
        self.last_event_timestamp = last_event_timestamp
        self.last_event_id = last_event_id
        return events

    def build_halo_session(self):
        """Instantiates the Halo session"""
        halo_session = cloudpassage.HaloSession(self.halo_key,
                                                self.halo_secret,
                                                api_host=self.api_host,
                                                api_port=self.api_port,
                                                integration_string=self.ua)
        halo_session.authenticate_client()
        return halo_session

    def create_url_list(self):
        """We initially set the 'since' var to the start_timestamp.  The next
        statement will override that value with the last event's timestamp, if
        one is set

        """

        base_url = "/v1/events"
        modifiers = self.search_params
        if self.start_timestamp is not None:
            modifiers["since"] = self.start_timestamp
        if self.last_event_timestamp is not None:
            modifiers["since"] = self.last_event_timestamp
        url_list = Utility.create_url_batch(base_url, self.batch_size,
                                            modifiers=modifiers)
        return url_list

    def get_pages(self, url_list):
        """Magic happens here... we map pages to threads in a pool, return
        results when it's all done."""
        halo_session = self.build_halo_session()
        page_helper = cloudpassage.HttpHelper(halo_session)
        pool = ThreadPool(self.max_threads)
        results = pool.map(page_helper.get, url_list)
        pool.close()
        pool.join()
        return results
