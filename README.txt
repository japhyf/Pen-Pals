Installation guide Pen Pals


* Installation of the Flask Libraries which can be found at 
            http://flask.pocoo.org/docs/1.0/
* Clone the Pen Pals github at https://github.com/abteen/Pen-Pals using:
            git clone git@github.com:abteen/Pen-Pals.git
* Create and run a Python virtual environment for this project:
          - Make sure the correct version of Python (3.6) is installed in your computer. 
          - Run : python3 -m venv 
          - Activate the virtual environment by running   :     source venv/bin/activate
          - Install correct dependencies using pip and provided requirements.txt, found in the root directly of the master branch
          - Initialize the flask server, and start it by running:
                  - export FLASK_ENV = development
                  - export FLASK_APP = flaskr
                  - init-db
                  - flask run
          - Navigate to the required server at the address provided by the flask console
          
