Module Documentation
====================

Api
---

The Api class exposes the main interface for this library. A fetch method is provided for all models.

The fetch method will get the data, turn it into python objects recursively, and do a few other nice things like adding python date-time objects.

.. autoclass:: launchlibrary.Api
   :members:
   
   .. automethod:: __init__

Models
------

As this library is based on the **launchlibrary** API, you can find a lot of info on `their website <https://launchlibrary.net/docs/1.4/api.html>`_ .
Note that the wrapper only uses the `detailed` mode.

Additionally, the parameters of every model can be accessed post-creation by using `model.param_names`.

.. automodule:: launchlibrary.models
   :members:
   :undoc-members:
   :show-inheritance:

Asynchronous Models
-------------------

The library also supports asynchronous operation. To receive proper coroutines, just prepend Async to the name of the class.

.. automodule:: launchlibrary.async_models
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
----------

The library attempts not to leak any exceptions except the regular Python ones, like ValueError and KeyError.

.. automodule:: launchlibrary.exceptions
   :members:
   :undoc-members:
   :show-inheritance:
