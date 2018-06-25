# Notes on the project
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
