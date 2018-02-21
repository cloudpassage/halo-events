import imp
import os
import sys

module_name = 'haloevents'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
haloevents = imp.load_module(module_name, fp, pathname, description)


class TestUnitUtility:
    def test_utility_8601_now(self):
        assert isinstance(haloevents.Utility.iso8601_now(), str)

    def test_unit_utility_build_ua(self):
        assert isinstance(haloevents.Utility.build_ua(), str)

    def test_unit_utility_build_ua_2(self):
        canary = "canary"
        assert canary in haloevents.Utility.build_ua(integration_name=canary)
