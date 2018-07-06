from post_scraping_text_processing import clean_bad_language
import re
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

df = pd.read_csv("../assets/lyrics/master_data_20180626.csv", index_col = 0)
df = clean_bad_language(df)
corpus = df['text']
cvec = CountVectorizer()
cvec.fit(corpus)
transformed_corpus = cvec.transform(corpus)
word_table = pd.DataFrame(transformed_corpus.toarray(), columns=cvec.get_feature_names())
word_series = word_table.sum()
word_series = word_series.sort_values(ascending = False)
zipfs_test_df = pd.DataFrame({
    'word': word_series.index,
    'count': word_series.values
})

plt.figure(figsize=(15,12))
plt.yscale('log')
plt.xscale('log')
plt.scatter(zipfs_test_df.index, zipfs_test_df['count'], s = 100, marker = 'o', alpha = 0.2, c = "teal")
plt.xlim((10**-.4,10**5.4))
plt.xlabel("Term rank (log scale)", fontsize = 18)
plt.ylabel("Term count (log scale)", fontsize = 18)
plt.title("Zipf's law for total Turkish song corpus\n", fontsize = 28)

plt.savefig("../assets/visualizations/zipf.png")
