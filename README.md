# Football-Project
Getting data and building a predictive model for football games (Total Corners and Total Goals)

links.py -- Used to get all the links from the page where we get the data from.
players.py -- Scraper to get player level data.
games.py -- Used to get game level data.
execute.py -- Executes the scripts above.
Model.ipynb -- Notebook where we build the predictive model in to parts:

* First we cluster the teams by the attributes of their player useing K - Means.
* Once we have the teams classified, we use that as one of the features of our model together with, country, and attendace in order to predict the total number of Corners and games.

