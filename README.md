# Turkish song analysis
***Natural language processing of over 15,000 Turkish-language pop songs***

## Overview
This project builds supervised and unsupervised learning models for text data from 15,000+ Turkish songs scraped from alternatifim.com with additional information gathered from Spotify's API. This project is intended to demonstrate the following skills:
### Scraping
Lyrics are scraped using BeautifulSoup. Other data is gathered through API queries.
### Data cleaning
The data coming from alternatifim.com is messy, containing missing values and bad characters. Modeling required extensive cleaning.
### Natural Language Processing
I chose this project to draw on my background as an ethnomusicologist as well as to do an NLP project with the training wheels off, so to speak&mdash;Turkish language libraries are not as developed as English libraries, so I had to write and understand feature extraction, selection, and engineering in deeper ways than an English-language project would allow.
### Unsupervised learning - topic modeling
This corpus is an opportunity to explore how Turkish song lyrics are organized&mdash;in other words, what categories or genres are present in the data. I used hierarchical modeling and discovered a major division in the data that correlates directly with musical genres.
### Supervised learning - classification
With the year a song was published available, I built a classifier capable of sorting songs into time-based categories based on text data alone.  

***Word cloud***
![alt text](https://github.com/jonwithers/turkish-song-nlp/blob/master/assets/visualizations/wordcloud1.png "Logo Title Text 1")

## Goals and results
- Produce a large, clean corpus of Turkish-language song lyrics with data labels.
  - Achieved by scraping from a large lyrics site, matching these songs to Spotify queries for release date, and grooming to reduce the number of non-Turkish songs.
- Build a model for clustering these songs.
  - Achieved using agglomerative hierarchical clustering. The most important division in the data is between songs that use more archaic vocables (e.g. folk songs) and songs that use a vocabulary similar to modern spoken Turkish (e.g. hip hop).
- Build a model to classify these songs based on year.
  - Achieved with  a surprising degree of accuracy using a Support Vector Classification model (areaUnderROC socre of 63%). This result is higher than expected because there is a lot of noise in this data.
  - Built a Logistic Regression model that beats the baseline (areaUnderROC score of 55%). This model allows for better interpretation--for example, the engineered features of vocable length are among the most significant according to a Chi-square test.

***Clusters in the corpus***  
<img src="https://github.com/jonwithers/turkish-song-nlp/blob/master/assets/visualizations/ward_cluster.png" height="600">


## Limitations
The biggest limitation of this project is that the date column is difficult to validate. Because songs were scraped from one site and merged to a list gathered from another source, the matching between song and date may not be accurate. To limit this, I accepted only exact matches with both artist and song title. However, it's possible that even if the song is exactly the same, the release date might not represent the time period in which the song was produced.  

## Further work
At this point, I have accomplished what I set out to do. There are more areas to explore with this data and models:
- While a good classifier, the model I selected is a black box. To interpret it, I could build a LIME model. However, the Spark implementation of LIME is unclear.
- I could try other clustering methods to be able to further uncover patterns in the data. The division between archaic and modern language that I've found is interesting but there is likely more to the data.
- I can convert my functional approach to an object-oriented library that can be used for other Turkish-language tasks.

## Data pipeline
Since this project uses multiple notebooks, it may be useful to explain the data flow precisely.

| File | Source | Role |
|------|--------|------|
|list_of_artists.csv   |get_all_artists.py   |A list of all artists    |
|all_lyrics_scraped_20180625-155423.csv  | lyrics_scraper.py  | Lots of data gathered from alternatifim using the list of artists   |
|lyrics_with_spotify.csv   |spotify_scraper.py   |contains date data   |
|master_data_20180626.csv   |Notebook 01   |Songs, artists, albums, and date   |
|assembled_20180711.csv   | Notebooks 02-04   |Cleaned and groomed and ready for modelling  |

## Table of contents
- assets
  - data
    - Contains csv files of data at different stages of cleaning (final data is full_frame_20180711.csv)
  - literature
    - Contains pdfs of relevant articles
  - lyrics
    - Contains raw data scraped from the web
  - visualizations
    - Contains data visualizations produced by notebooks and scripts.
- notebooks
  - Notebooks 01-04 are ipynb files that illustrate different stages of the data cleaning, exploration, and feature engineering process.
  - Notebook 05a contains the unsupervised learning models for the data
  - Notebook 05b contains the final supervised model for the data.
  - Older notebooks that represent intermediate stages are in the subdirectories `depreciated` for ipynb files and `other-Spark-notebooks` for html files.
- scripts
  - `spacy_stop_words.py` and `turkish_spacy_lemmatizer.py` are slightly edited files from the spaCy repos on Turkish. spaCy has no current implementation for Turkish that compares to its implementation for English or other languages, but these resources (a list and a dictionary) are essential resources.
  - scrapers:
    - `get_all_artists.py` gets a list of all artists on alternatifim.com. Output is `assets/lyrics/list_of_artists.csv`.
    - `lyrics_scraper.py` uses this list to get all lyrics. Running this script takes a long time. Output is `assets/lyrics/all_lyrics_scraped_20180625-155423.csv`.
    - `spotify_scraper.py` makes queries to Spotify's API to attempt to get year data for every song in the lyrics dataframe. Output is `assets/lyrics/lyrics_with_spotify.csv`.
    - `discogs_scraper.py` makes queries to Discogs' API to attempt to get year data for every song in the lyrics dataframe. Output is `discog_year.csv`. Since this didn't add anything to the project it is not currently implemented.
  - `post_scraping_text_processing.py` is a proto-module of functions for text processing. Because other NLP libraries are unsuited for Turkish lyrics data, these functions are written specifically for this data.
  - `assemble_all_data.py` creates the final data using inputs from notebooks.

## Sources  
[spaCy Turkish tools](https://github.com/explosion/spaCy/tree/master/spacy/lang/tr)  
[alternatifim.com](https://sarki.alternatifim.com/)  
[Spotify](https://developer.spotify.com/documentation/web-api/)  
[discogs](https://www.discogs.com/developers/)  
[SpotiPy (Spotify Client)](https://github.com/plamere/spotipy)  
[Discogs Client](https://github.com/discogs/discogs_client)  
