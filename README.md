# MovieBall

The application is composed of a main file, application.py and a folder for other dependenceis, called applicatio
There is also a templates folder that contains all the html and javascript needed to run the site.

Besides these, there are multiple files CIS550projectDict.dict, CIS550projectModel, CIS550projectModel.state, and CIS550projectModelTfidf that contain the data needed for the LDA model we use for movie predictions

To install, run 

`pip install -r requirements.txt`

Then run

`python application.py`

Which should host the app at 0.0.0.0:5000 or localhost:5000

The application.py file contains two main route functions, movie() and select(). The select function loads the initial page with all the movies listed and the movie function loads the customizable page for each movie. In terms of database queries, all queries are done in the movie function since it is specific to one movie. The select funtion uses the xml file (posters_xml.xml) to load the images and file movie descriptions for all the movies.

The site is presently hosted at http://54.173.17.142/

CIS550project MovieBall. 2015.
