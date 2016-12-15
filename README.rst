Python module: haloevents
=========================

Installing:
-----------

* Clone this repository down and enter it's root dir
* pip install .


Example usage:
--------------

::

        import haloevents
        events = haloevents.HaloEvents(halo_key, halo_secret)
        for event in events:
            print event["created_at"]


Testing:
--------

py.test --cov=haloevents
