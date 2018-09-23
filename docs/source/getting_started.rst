Getting Started
===============

Installation
------------

The python-launch-library module only supports Python 3.6 and above. If your installation passes these requirements, just use:

.. code::
  
  pip install python-launch-library
  

Usage of the API is simple.

.. code:: py

  # First, import the library
  import launchlibrary as ll
  
  # Then, initialize an API object
  api = ll.Api(retries=10)  # Although `retries` is optional, I included it for the sake of the example.
  
  # And fetch whichever models you'd like.
  
  # Either by an explicit API call
  next_5_go_launches = ll.Launch.fetch(api, next=5, status=1)
  
  # Or by one of the simpler methods available for some models.
  next_5_go_launches = ll.Launch.next(api, 5)
  
  # Now, you can utilize whatever data you'd like. Data from the API is processed recursively, so if a Launch object
  # contains a Location object, you'll have models for both.
  launch_loc = next_5_go_launches[0].location
  
  # Some properties, like agency, mandate the use of special methods, as their availability is not guaranteed or represented as an id only.
  launch_agency = next_5_go_launches[0].get_agency()
  
  