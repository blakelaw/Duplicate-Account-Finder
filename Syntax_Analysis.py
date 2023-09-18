import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
import plotly.express as px

import nltk

from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage

df = pd.read_feather('Dataframes/unfiltered_corpus')

df['combined'] = df['combined'].str.replace(r'<[^<>]*>', '', regex=True)

df['combined'] = df['combined'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ')

df['combined'] = df['combined'].str.replace(r'\n', ' ')

df.to_feather('Dataframes/corpus')

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
import plotly.express as px

import nltk
nltk.download('punkt')

from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage

df = pd.read_feather('Dataframes/corpus')

df['sen_length'] = pd.Series(dtype='int')
df['long_words'] = pd.Series(dtype='int')
df['per_capital'] = pd.Series(dtype='int')
df.replace(np.nan, 0.0)

def calculate_features(row):
    wtokens = nltk.word_tokenize(row['combined'])
    wfreq = nltk.FreqDist(wtokens)
    sentcount = wfreq['.'] + wfreq['?'] + wfreq['!']
    total_tokens = len(wtokens)
    
    if sentcount == 0 or total_tokens == 0:
        row['sen_length'] = 0
        row['long_words'] = 0
        row['per_capital'] = 0
        return row
    
    row['sen_length'] = total_tokens / sentcount
    long_words_count = len([w for w in wfreq if len(w) >= 8])
    row['long_words'] = long_words_count / total_tokens
    
    cap_words_count = sum(1 for x in wtokens if x[0].istitle())
    row['per_capital'] = cap_words_count / total_tokens
    
    return row

df = df.apply(calculate_features, axis=1)

df["per_capital_norm"] = df["per_capital"] / df["per_capital"].max()
df["long_word_norm"] = df["long_words"] / df["long_words"].max()
df["sen_length_norm"] = df["sen_length"] / df["sen_length"].max()
df["med_length_norm"] = df["med_length"] / df["med_length"].max()

df.to_feather("Dataframes/user_metrics")

