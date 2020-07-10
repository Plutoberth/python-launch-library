Getting Started
===============

Installation
------------

The python-launch-library module only supports Python 3.6 and above. To install it, just use:

.. code::
  
  pip install python-launch-library
  

Usage
-----
  
Usage of the wrapper is simple.

.. code:: py3

  # First, import the library
  import launchlibrary as ll

  # Then, initialize an API object
  api = ll.Api()

  # And fetch whichever models you'd like.

  # Either by an explicit API call
  next_5_go_launches = api.fetch_launch(next=5, status=1)

  # Or by one of the simpler methods available for some models.
  next_5_go_launches = api.next_launches(5)

  # Now, you can utilize whatever data you'd like. Data from the API is processed recursively, so if a Launch object
  # contains a Location object, you'll have models for both.
  launch_loc = next_5_go_launches[0].location

  # Some properties, like status, are only represented by ID. You can call the appropriate methods to get a proper object from that ID
  launch_status = next_5_go_launches[0].get_status()

  # It's now possible to also use the regular API names as well as pythonic names.
  vid_urls = next_5_go_launches[0].vid_urls
  vid_urls_2 = next_5_go_launches[0].vidURLs

Asynchronous Usage
------------------

.. code:: py

  import launchlibrary as ll

  api = ll.Api()

  async def foo():
    # Use the api as usual, but with an async prefix for api functions.
    next_5_go_launches = await api.async_next_launches(5)
    status = await next_5_go_launches[0].get_status()

  


  
  