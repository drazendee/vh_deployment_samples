## 01 - Deployment with graph image responses
A simple Flask example that takes in JSON, uses matplotlib to plot it and returns an image on the html page

To run
* `python3 -m virtualenv .venv`
* `source .venv/bin/activate`
* `pip install -r requirements.txt`
* `gunicorn -b 127.0.0.1:5000 app:metadataplotter`
* Open http://127.0.0.1:5000

The project contains:

* `/fetchMetadata.py` that's used to download metadata from a Valohai execution as save it as JSON
* `/metadata.json` a sample of what does an execution metadata look like
* `/app.py` as the main application that is launched through wsgi on valohai
* `/metadataplotter/` contains the code for the app
    * In our `valohai.yaml` we define the endpoint as `wsgi: app:metadataplotter`
* `/metadataplotter/__init__.py` contains the main code
* `/metadataplotter/static/` contains static files used by the web app like css
* `/metadataplotter/static/templates` contains the base template and the `index.html` page
* `/requirements.txt` with a list of packages that need to be installed on the Valohai Docker container for the app
* `valohai.yaml` to define a single step (list files) and the endpoint