# python-launch-library
A simple python wrapper for the Launch Library web API. Can also be used asynchronously too.

[![PyPI Version](https://img.shields.io/pypi/v/python-launch-library.svg)](https://pypi.org/project/python-launch-library/) [![Documentation Status](https://readthedocs.org/projects/python-launch-library/badge/?version=latest)](https://python-launch-library.readthedocs.io/en/latest/?badge=latest)

Available models: `Agency, AgencyType, Launch, Launch Status, Pad, Location, Rocket, RocketFamily`

The usage of the API is simple.

### Usage

##### Proper documentation is available in [Read The Docs](https://python-launch-library.readthedocs.io/en/latest/).

To install, simply use pip: ```pip install python-launch-library```

```python
# Import the launchlibrary lib
import launchlibrary as ll

# Create an instance of the API
api = ll.Api()  # You can also specify api url, api version...

# And request the next 5 launches, for example.
launches = ll.Launch.fetch(api, next=5) # Any argument after "api" is not constrained (w/ kwargs).
# ^ Returns a list of launch objects.

# You can fetch the pythonic property names by using launch.param_names
properties = launches[0].param_names

# It's now possible to also use the regular API names as well as pythonic names.
vid_urls = launches[0].vid_urls
vid_urls_2 = launches[0].vidURLs
```

### Changelog

Since version `1.0.1`, the library is versioned according to Semver.

* 1.0.3 - Bugfix

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
 
