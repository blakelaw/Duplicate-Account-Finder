import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import wordpunct_tokenize
from numpy import double, int64
from multiprocessing import Pool

P1 = pd.read_feather("Dataframes/P1", use_threads=True)
P2 = pd.read_feather("Dataframes/CData2", use_threads=True)
P3 = pd.read_feather("Dataframes/RNomArchive2_", use_threads=True)

df = pd.concat([P1,P2,P3], ignore_index=True)

df_authors_normalized = pd.json_normalize(df['author'], record_prefix='author_', errors='ignore')

df2 = pd.DataFrame(columns = ['username', 'name', 'message', 'msg_length', 'time'])
df2['username'] = df_authors_normalized['username']
df2['name'] = df_authors_normalized['name']
df2['message'] = df['raw_message']
df2['msg_length'] = df2['message'].str.len()

df_times = pd.DataFrame(columns = ['username', 'name', 'message', 'msg_length', 'time'])
df_times['username'] = df_authors_normalized['username']
df_times['name'] = df_authors_normalized['name']
df_times['message'] = df['raw_message']
df_times['msg_length'] = df_times['message'].str.len()
df_times['time'] = df['createdAt']

df_times['time'] = [i[11:13] for i in df_times['time']]
df_times = df_times.astype({"time": int64})

df_times.to_feather("message_time")

df3 = pd.DataFrame(columns = ['username', 'name', 'median_length', 'avg_length', 'num_posts'])
df3['username'] = df2['username'].unique()

df3

# Step 1: Compute necessary statistics from df2 in advance
df2_stats = df2.groupby('username').agg(
    num_posts=('msg_length', 'size'),
    avg_length=('msg_length', 'mean'),
    median_length=('msg_length', 'median'),
    name=('username', lambda x: x.iat[0])  # Assuming column 1 is 'username'
).reset_index()

# Step 2: Convert df2_stats and users to dictionaries for faster access
df2_stats_dict = df2_stats.set_index('username').to_dict('index')
users = df2.groupby('username').agg(lambda x: x.iat[0, 1]).to_dict()

# Step 3: Iterate over df3 and update values using dictionaries
for i, user in enumerate(df3['username']):
    user_stats = df2_stats_dict.get(user, {'num_posts': 0, 'avg_length': 0, 'median_length': 0, 'name': None})
    df3.at[i, 'num_posts'] = user_stats['num_posts']
    df3.at[i, 'avg_length'] = user_stats['avg_length']
    df3.at[i, 'median_length'] = user_stats['median_length']
# # Merge the 'name' column from df2 to df3 based on the 'username' column
name_mapping = df2.set_index('username')['name'].to_dict()
df3['name'] = df3['username'].map(name_mapping)

df3

df4 = pd.DataFrame(columns = ['username', 'name', 'combined', 'avg_length', 'med_length', 'tot_length'])
df4['username'] = df2['username'].unique()
df4['name'] = df3['name']
df4.replace(np.nan, 0.0)

df2_grouped = df2.groupby('username')
df2_message_agg = df2_grouped['message'].apply(''.join).reset_index()
df2_stats_agg = df2_grouped['msg_length'].agg(['mean', 'median']).reset_index()

message_dict = dict(zip(df2_message_agg['username'], df2_message_agg['message']))
avg_length_dict = dict(zip(df2_stats_agg['username'], df2_stats_agg['mean']))
median_length_dict = dict(zip(df2_stats_agg['username'], df2_stats_agg['median']))

i = 0
for user in df4['username']:
    df4.at[i, 'combined'] = message_dict.get(user, "")
    df4.at[i, 'avg_length'] = avg_length_dict.get(user)
    df4.at[i, 'med_length'] = median_length_dict.get(user)
    i += 1

df4['tot_length'] = df4['combined'].str.len()

df4['combined'] = df4['combined'].str.replace(r'<[^<>]*>', '', regex=True)
df4['combined'] = df4['combined'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ')
df4['combined'] = df4['combined'].str.replace(r'\n', ' ')

df4

whole_corpus = df4['combined'].sum()

tokens = wordpunct_tokenize(whole_corpus)

for token in tokens:
    token.lower()

top100 = list(nltk.FreqDist(tokens).most_common(50))

df5 = pd.DataFrame(columns = ['username', 'name_', 'length'])
df5['username'] = df2['username'].unique()
df5['name_'] = df3['name']
df5['length'] = 0
for word, join in top100:
    df5[word] = 0.0

combined_length_dict = df4.groupby('username')['combined'].apply(lambda x: x.str.len().sum()).to_dict()
df5['length'] = df5['username'].map(combined_length_dict, na_action='ignore')

df6 = df5[df5['length'] >= 5000]
df6.reset_index(inplace=True, drop=True)

df6

# Step 1: Create mappings for 'combined' and 'length' columns
combined_dict = df4.set_index('username')['combined'].to_dict()
length_dict = df6.set_index('username')['length'].to_dict()

# Step 2: Create a dictionary for special characters with their respective regex patterns
special_chars = {
    '?': '\?', 
    '(': '\(', 
    ')': '\)', 
    '*': '\*', 
    '+': '\+', 
    ').': '\).', 
    '?"': '\?"'
}

# Step 3: Initialize the new columns in df6 with 0.0
for word, join in top100:
    df6[word] = 0.0

# Step 4: Loop through the usernames and update df6 using vectorized operations
for i, user in enumerate(df6['username']):
    df_combined = combined_dict.get(user, "")
    len = length_dict.get(user, 1)  # Avoid division by zero by using 1 as default value
    for word, join in top100:
        pattern = special_chars.get(word, word)
        df6.at[i, word] += df_combined.count(pattern) / len

df6

