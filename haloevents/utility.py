import datetime
import os
import re


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
