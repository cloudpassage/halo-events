"""This class provides an iterator.  Under the covers it does multi-threaded
consumption of events, only providing information to the iterator when it's
been ordered correctly."""

import cloudpassage
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
        self.ua = Utility.build_ua("")
        self.set_attrs_from_kwargs(kwargs)

    def __iter__(self):
        """Yields events one at a time. Forever."""
        session = cloudpassage.HaloSession(self.halo_key, self.halo_secret,
                                           api_host=self.api_host,
                                           api_port=self.api_port,
                                           integration_string=self.ua)
        streamer = cloudpassage.TimeSeries(session, self.start_timestamp,
                                           "/v1/events", "events")
        while True:
            for event in streamer:
                yield event

    def set_attrs_from_kwargs(self, kwargs):
        arg_list = ["start_timestamp", "max_threads", "batch_size",
                    "search_params", "api_host", "api_port"]
        for arg in arg_list:
            if arg in kwargs:
                setattr(self, arg, kwargs[arg])
        if "integration_name" in kwargs:
            setattr(self, "ua", Utility.build_ua(kwargs["integration_name"]))
