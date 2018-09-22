# python-launch-library
A simple python wrapper for the Launch Library web API.

##### Warning: The wrapper is not yet intended for general use.

For now, usage is constricted to the "Launch" and "Agency" endpoints. Other models and richer support for existing ones will be added soon.

The usage of the API is simple.

### Usage

```python
# Import the launchlibrary lib
import launchlibrary

# Create an instance of the API
api = launchlibrary.Api()  # You can also specify data mode, api url, api version...

# And request the next 5 launches, for example.
launches = launchlibrary.Launch.fetch(api, next=5) # Any argument after "api" is not constrained (w/ kwargs).
# ^ Returns a list of launch objects.

# You can fetch the pythonic property names by using launch.param_names
properties = launches[0].param_names
```

### Todo
[ ] Tidy up the repository

[ ] Add exceptions to handle server timeout

[ ] Handle nested models (i.e. a Rocket model inside a Launch model)

[ ] Handle times with the datetime class

[ ] More?

Feel free to open issues and pull requests! I usually check Github daily. 
 
