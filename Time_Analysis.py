import numpy as np
import pandas as pd
import nltk
from nltk.tokenize import wordpunct_tokenize
from numpy import double, int64

#Import database of all comments
P1 = pd.read_feather("Dataframes/P1", use_threads=True)
P2 = pd.read_feather("Dataframes/P2", use_threads=True)
P3 = pd.read_feather("Dataframes/P3", use_threads=True)
P4 = pd.read_feather("Dataframes/P4", use_threads=True)

#combined into one database
df = pd.concat([P1,P2,P3,P4], ignore_index=True)

#normalize author column to extract username
df_authors_normalized = pd.json_normalize(df['author'], record_prefix='author_')

#create new database with username, name, message, message length, and time
df_clean = pd.DataFrame(columns = ['username', 'name', 'message', 'msg_length', 'time'])
df_clean['username'] = df_authors_normalized['username']
df_clean['name'] = df_authors_normalized['name']
df_clean['message'] = df['raw_message']
df_clean['msg_length'] = df_clean['message'].str.len()
df_clean['time'] = [i[11:13] for i in df['createdAt']]
df_clean = df_clean.astype({"time": int64})

#create database of proportions of posts by hour
df_times = pd.DataFrame(columns = ['username', 'name', 'num_posts', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'])

#fill in username column from df_clean
df_times['username'] = df_clean['username'].unique()
df_times.replace(np.nan, 0.0)

df_clean

# Fill in names column
unique_users = df_clean.drop_duplicates(subset='username')
df_times['name'] = df_times['username'].map(unique_users.set_index('username')['name'])

# Fill in num_posts column
num_posts_series = df_clean.groupby('username').size()
df_times['num_posts'] = df_times['username'].map(num_posts_series)


df_times

# Prepare a mapping of time to string format to align with your column names
df_clean['time_str'] = df_clean['time'].astype(str)

# Get the count of posts at each time for each user
pivot_table = df_clean.pivot_table(index='username', columns='time_str', values='message', aggfunc='count', fill_value=0)

# Calculate num_posts and the proportion of posts at each time
df_times.set_index('username', inplace=True)
df_times['num_posts'] = pivot_table.sum(axis=1)
for col in pivot_table.columns:
    df_times[col] = pivot_table[col] / df_times['num_posts']

# Reset the index
df_times.reset_index(inplace=True)

#make smaller database for people with 240 posts or more
df_times_smaller = df_times[df_times['num_posts'] >= 240]
df_times_smaller.reset_index(inplace=True, drop=True)

#save to feather file
df_times_smaller.to_feather("time_data")

#create database with username, name, and corpus
df_corpus = pd.DataFrame(columns = ['username', 'name', 'combined'])
df_corpus['username'] = df_times_smaller['username'].unique()
df_corpus['name'] = df_times['name']

# Create a series with concatenated messages for each user
combined_messages = df_clean.groupby('username')['message'].agg(lambda x: ' '.join(x.astype(str)))

# Map the combined messages to the corresponding users in df_corpus
df_corpus['combined'] = df_corpus['username'].map(combined_messages)

#clean up combined column: remove HTML tags, links, and line breaks
df_corpus['combined'] = df_corpus['combined'].str.replace(r'<[^<>]*>', '', regex=True)
df_corpus['combined'] = df_corpus['combined'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ')
df_corpus['combined'] = df_corpus['combined'].str.replace(r'\n', ' ')

# sum up all combined into one string
whole_corpus = df_corpus['combined'].sum()

# put words into tokens, then put them in lowercase
tokens = wordpunct_tokenize(whole_corpus)
for token in tokens:
    token.lower()

# find the 50 most common words
top50 = list(nltk.FreqDist(tokens).most_common(50))

#create a new dataframe with username, name, and each of the top 50 words
df_words = pd.DataFrame(columns = ['username', 'name'])
df_words['username'] = df_corpus['username']
df_words['name'] = df_corpus['name']
for word, join in top50:
    df_words[word] = 0.0

df_times_smaller

# Create a dictionary to escape special characters in words
escape_dict = { '?': '\?', '(': '\(', ')': '\)', '*': '\*', '+': '\+', ').': '\).', '?"': '\?"'}

# Create a function to apply the count operations
def word_count(row):
    user = row['username']
    df_combined = df_corpus.loc[df_corpus['username'] == user, 'combined'].iloc[0]
    len_combined = len(df_combined)

    if len_combined == 0:
        return row

    for word, join in top50:
        escaped_word = escape_dict.get(word, word)
        row[word] = df_combined.count(escaped_word) / len_combined
    return row

# Apply the function on each row of df_words
df_words = df_words.apply(word_count, axis=1)

df_words_for_concat = df_words.drop(['username', 'name', '.'], axis =1)

df_time_words = pd.concat([df_times_smaller, df_words_for_concat], axis=1)

df_time_words.to_feather("df_time_words_expanded")

