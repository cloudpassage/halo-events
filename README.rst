Python module: haloevents
=========================

.. image:: https://travis-ci.org/cloudpassage/halo-events.svg?branch=master
    :target: https://travis-ci.org/cloudpassage/halo-events

.. image:: https://codeclimate.com/github/cloudpassage/halo-events/badges/gpa.svg
   :target: https://codeclimate.com/github/cloudpassage/halo-events
   :alt: Code Climate

.. image:: https://codeclimate.com/github/cloudpassage/halo-events/badges/coverage.svg
  :target: https://codeclimate.com/github/cloudpassage/halo-events/coverage
  :alt: Test Coverage

.. image:: https://codeclimate.com/github/cloudpassage/halo-events/badges/issue_count.svg
   :target: https://codeclimate.com/github/cloudpassage/halo-events
   :alt: Issue Count


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
