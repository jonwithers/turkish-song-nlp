# Notes on the project
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
