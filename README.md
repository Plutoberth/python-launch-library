# python-launch-library
A simple python wrapper for the Launch Library web API. Can also be used asynchronously too.

[![PyPI Version](https://img.shields.io/pypi/v/python-launch-library.svg)](https://pypi.org/project/python-launch-library/) [![Documentation Status](https://readthedocs.org/projects/python-launch-library/badge/?version=latest)](https://python-launch-library.readthedocs.io/en/latest/?badge=latest)

Available models: `Agency, AgencyType, Launch, Launch Status, Pad, Location, Rocket, RocketFamily`

The usage of the API is simple.

### Usage

##### Proper documentation is available in [Read The Docs](https://python-launch-library.readthedocs.io/en/latest/).

To install, simply use pip: ```pip install python-launch-library```

```python
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
```

### Changelog

Since version `1.0.1`, the library is versioned according to semantic versioning rules.

* 1.0.3, 1.0.4, 1.0.5, 1.0.6 - Fixed some bugs in the async variant

* 1.0.2 - Added an exception hierarchy. All exceptions now inherit from LlException

* 1.0.1 - Improved caching. 

* 1.0 - Changed all fetch calls to be through the Api object. This is a breaking change.
  

  
  ```python
  # Porting guide

  import launchlibrary as ll
  api = ll.Api()
  
  # Before
  next_launch = ll.Launch.next(api, 1)
  
  # After
  next_launch = api.next_launches(1)
  ```


### Todo
- [x] Tidy up the repository
- [x] Add exceptions to handle server timeout
- [x] Handle nested models (i.e. a Pad model inside a Location model inside a Launch model)
- [x] Handle times with the datetime class
- [x] Package properly and upload to PyPI
- [x] Add more abstraction methods for the api calls (open to suggestions)
- [x] Add magic method comparisons (open to suggestions)
- [x] Asynchronous operation
- [x] Add aliases for actual API names with getattr
- [ ] Add tests
- [ ] Your suggestion here




Feel free to open issues and pull requests! I usually check Github daily. 
 
