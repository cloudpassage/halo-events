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

What it is:
-----------

Multi-threaded API wrapper for the CloudPassage /v1/events endpoint.  Give it
API creds and talk to it like it's a generator.  See example, below.


Installing:
-----------

* Clone this repository down and enter its root dir
* pip install .


Example usage:
--------------

::


        import haloevents
        events = haloevents.HaloEvents(key, secret)
        for event in events:
            message = "%s\t%s\t%s" % (event["created_at"], event["type"], event["id"])
            print(message)


Testing:
--------

py.test --cov=haloevents
