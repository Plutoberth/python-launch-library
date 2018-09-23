# python-launch-library
A simple python wrapper for the Launch Library web API.

##### Warning: The wrapper is not yet intended for general use.

Available models: Agency, AgencyType, Launch, Launch Status, Pad, Location 

The usage of the API is simple.

### Usage

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
```

### Todo
- [ ] Tidy up the repository
- [ ] Add exceptions to handle server timeout
- [x] Handle nested models (i.e. a Pad model inside a Location model inside a Launch model)
- [x] Handle times with the datetime class
- [x] Package properly and upload to PyPI
- [ ] Asynchronous operation
- [ ] Add more abstraction methods for the api calls
- [ ] Your suggestion here



Feel free to open issues and pull requests! I usually check Github daily. 
 
