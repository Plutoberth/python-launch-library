import launchlibrary

a = launchlibrary.Api()
agencies = launchlibrary.Agency.fetch(a, name="SpaceX")
print(agencies)
