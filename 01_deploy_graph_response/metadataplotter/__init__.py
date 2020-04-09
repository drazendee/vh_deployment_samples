from flask import Flask, flash, redirect, render_template, request, send_file
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64

ALLOWED_EXTENSIONS = {'json'}

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='secret_for_client_session'
    )

    # Set matplot backend as 'agg' as we'll write out plots to files
    # instead of rendering them (like in Jupyter notebook)
    # https://matplotlib.org/faq/usage_faq.html#what-is-a-backend
    matplotlib.use('agg')

    # We create a route in our app to create a response for all requests on '/'
    @app.route('/', methods=('GET', 'POST'))
    def predict():
        # Check that we've receive a POST request (a form has been submitted)
        if request.method == 'POST':

            # Get the file called 'metadata' 
            # from the form on our index.html
            file = request.files['metadata']

            # Make sure the file is one of the allowed filetypes
            if not allowed_file(file.filename) :
                flash('File type not supported')
                return redirect(request.url) 
            
            # Read JSON with pandas
            df = pd.read_json(file)
            # Define our figure
            fig = plt.figure()
            x = df["step"]
            y = df["accuracy"]
            plt.xlabel('Step')
            plt.ylabel('Accuracy')
            plt.plot(x,y)

            # Save our figure to memory
            figfile = BytesIO()
            plt.savefig(figfile, format='png')
            # Rewing to te beginning of the stream
            figfile.seek(0)

            # Get the value and encode it for html
            figdata_png = figfile.getvalue()
            figdata_png = base64.b64encode(figdata_png)

            # Return index and pass it a file variable
            return render_template('index.html', image=figdata_png.decode())

            # Or download the file
            #return send_file(figfile, attachment_filename='graph.jpg', as_attachment=True)
        else :
            # There was no POST request
            # Show the empty page
            return render_template('index.html')

    return app

# Used to check that the filename has an allowed extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS