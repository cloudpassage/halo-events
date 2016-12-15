import imp
import os
import sys

module_name = 'haloevents'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
haloevents = imp.load_module(module_name, fp, pathname, description)


class TestUnitHaloEvents:
    def test_utility_8601_now(self):
        assert haloevents.HaloEvents("", "")
