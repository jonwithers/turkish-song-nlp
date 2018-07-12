Notes on the project

====================
## July 11, 2018
- Thanks to Spark, I have a decent classifier now. I can report more than 60% areaUnderROC for distinguishing between the two classes.
- Hierarchical clustering in Python produces a good dendrogram that can be used to figure out how many clusters I need. I have a pretty good idea of what the big separation in the data might be.
- I need to clarify the data pipeline:
  - Scraping:
    - Start with lyrics_scraper.py to get the lyrics
    - Get year data from spotify_scraper.py
    - Produces files all_lyrics_scraped_20180625-155423.csv and lyrics_with_spotify.csv
    - Combine these in Notebook 01 to produce master_data_20180626.csv
  - Cleaning:
    - Cleaning functions gathered in post_scraping_text_processing.py
    - Functions developed and implemented in Notebook 02
    - train_test_split.py produces a new train and test set with target column
  - EDA:
    - Notebook 03 produces charts and graphs
    - Feature engineering in Notebook 04 uses the output of train_test_split.py
  - Modeling:
    - Supervised learning models in Scala html files
    - Unsupervised learning in Notebook 05.

## July 9, 2018
- Multinomial Naive Bayes models for barely processed data isn't very performant, essentially returning the baseline.
- Ward clustering on barely processed data is also not very performant, with difficult to interpret clusters.
- Before returning to these two problems, I will definitely need to do more careful feature engineering.
- Additionally, these models are very slow to build on my computer. I will figure out how to implement them using Spark. I'll do data preparation on my local computer and use a pipeline in a Databricks notebook to push the data through a model on Spark. Models to make and tune using Spark:
  - Clustering models (k-means and hierarchical clustering)
  - Classification models (NaiveBayes and Logistic Regression)

## July 1, 2018
- spacy doesn't have full support for Turkish, but they have some tools that have been useful. An enormous lemmatizer dictionary can look up every word (except stopwords, included in another file) and replace it with the root form.
- The relationships between words is still not clear. Some cliched phrases are probably good features to include. I started exploring the ngrams to figure out what sorts of phrases to look for.

## June 26, 2018
Progress on data collection:
- Junks 1 & 2 have been dealt with.
  - To get rid of English, I used my pretty naive English score function. If ANY of a few important keywords appear, a song's English score increases. The most naive version, currently in use, only accepts songs with an English score of 0.
  - To get release data, I used Spotify's API to search for songs and artists, and pull the release date and name of the top hit. Potential issues:
    - The top hit might not be the song, even though the name is the same.
    - The Spotify version might be the most recent release, not the original release. This is probably only an issue for the more famous artists.
- EDA
  - The year data is very heavily skewed toward the most recent two decades (not too surprising), so a pre-1980 target is unfeasible (although the challenge of minority class resampling is worth exploring)
  - Each step resulted in a loss of data. Filtering out non-Turkish lyrics reduced my song list by a huge amount; filtering out songs I couldn't find on Spotify reduced my song list by about 50%; and filtering out songs that didn't match exactly reduced by song list to about 85% of that. Still this is more than 14,000 songs, so it's definitely a good scale for a data science approach.

## June 25, 2018
Project outline so far:
- Problems
  - Unsupervised learning&mdash;topic modeling on Turkish lyrics
  - Supervised learning&mdash;make a model using NLP and as much advanced stuff as I can to build some classifiers (given lyrics, model the period in which a song was released)
- Data
  - All lyrics (including junk) have been scraped. Now the junk needs to be winnowed away.
  - Junk #1: anything that isn't Turkish-language
    - I have some scripts ready to do naive language testing for English and French, my two main concerns
    - I may also use Google or some other existing service
  - Junk #2: anything I can't get date data for
    - This is going to be harder. I will scrape from discogs.com and from the Spotify API to get as much album release data I can, and then merge them.
    - The problems I hope to avoid are that my decent amount of data will become nothing if I can't merge enough.
- EDA
  - Still haven't really done this, but there are some trends I've noticed. Most music is pretty short, and some genres have many many more words than others.

## June 22, 2018
Project outline so far:
- Problems
  - Unsupervised learning&mdash;topic modeling on Turkish lyrics
  - Supervised learning&mdash;make a model using NLP and as much advanced stuff as I can to build some classifiers (given lyrics, model the period in which a song was released)
- Data
  - Built a scraping script to pull from alternatifim, which is a user-updated lyrics site of questionable quality. The poor quality introduces lots of interesting hurdles that make the project more interesting
  - Built some cleaning functions that clean the text of ads, awkward formatting issues, and some scripts that remove non-Turkish songs (although these are still rough)
  - Some early EDA. I likely need to gather lots more data. I think I'm going to need outside sources as well, particularly for the dates for each album.
- EDA
  - Still haven't really done this, but there are some trends I've noticed. Most music is prett short, and some genres have many many more words than others.
  - Lyrics contain songs in English and French which is not useful for my project.
