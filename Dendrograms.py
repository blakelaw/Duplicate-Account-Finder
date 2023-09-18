import pandas as pd
import numpy as np
import warnings
from matplotlib import pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from scipy.cluster.hierarchy import dendrogram, linkage
warnings.filterwarnings("ignore", category=UserWarning)
scaler = MinMaxScaler()

def process_linkage(CX, LBX):
    n_data_points = len(labels)
    
    pairs_df = pd.DataFrame(cx[:, :2].astype(int), columns=['User1', 'User2'])
    pairs_df['Distance'] = cx[:, 2]
    pairs_df = pairs_df[(pairs_df['User1'] < n_data_points) & (pairs_df['User2'] < n_data_points)]
    
    pairs_df['User1'] = pairs_df['User1'].apply(lambda x: labels[x])
    pairs_df['User2'] = pairs_df['User2'].apply(lambda x: labels[x])
    pairs_df = pairs_df.sort_values(by='Distance', ascending=True)
    
    return pairs_df

df_time_words = pd.read_feather('Dataframes/df_time_words')
L1 = df_time_words.drop(df_time_words.columns[[0, 1, 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]], axis=1)
L1.fillna(0, inplace=True)
L1 = pd.DataFrame(scaler.fit_transform(L1), columns=L1.columns)
LV1 = L1.values
LB1 = list(df_time_words['name'])
C1 = linkage(LV1, method='single', metric='cityblock', optimal_ordering=True)

F1 = plt.figure(figsize=(25, 66), dpi=600)
D1 = dendrogram(C1, labels=LB1, orientation="right", color_threshold=2.75, show_leaf_counts=True)
plt.savefig('Dendrograms/dendrogram1.png', format='png', dpi=600)
plt.close(F1)

L2 = df_time_words.drop(df_time_words.columns[[0, 1, 2]], axis=1)
L2.fillna(0, inplace=True)
L2 = pd.DataFrame(scaler.fit_transform(L2), columns=L2.columns)
LV2 = L2.values
LB2 = list(df_time_words['name'])
C2 = linkage(LV2, method='single', metric='cityblock', optimal_ordering=True)

F2 = plt.figure(figsize=(25, 66), dpi=600)
D2 = dendrogram(C2, labels=LB2, orientation="right", color_threshold=4.36, show_leaf_counts=True)
plt.savefig('Dendrograms/dendrogram2.png', format='png', dpi=600)
plt.close(F2)

Top50 = pd.read_feather('Dataframes/Top50')
L3 = Top50.drop(Top50.columns[[0, 1,2,3]], axis=1)
L3 = pd.DataFrame(scaler.fit_transform(L3), columns=L3.columns)
L3.fillna(0, inplace=True)
LV3 = L3.values
LB3 = list(Top50['name_'])
C3 = linkage(LV3, method='single', metric='cityblock', optimal_ordering=True)

F3 = plt.figure(figsize=(25, 66), dpi=600)
D3 = dendrogram(C3, labels=LB3, orientation="right", color_threshold=2, show_leaf_counts=True)
plt.savefig('Dendrograms/dendrogram3.png', format='png', dpi=600)
plt.close(F3)

user_metrics = pd.read_feather('Dataframes/user_metrics')
user_metrics = user_metrics.drop(user_metrics.columns[1:3], axis=1)
user_metrics = user_metrics.drop(user_metrics.columns[8:], axis=1)
merged = pd.merge(user_metrics, df_time_words, on='username', how='inner')
L4 = merged.drop(columns=['username', 'name', 'num_posts'])
L4 = pd.DataFrame(scaler.fit_transform(L4), columns=L4.columns)
L4.fillna(0, inplace=True)
LV4 = L4.values
LB4 = list(merged['name'])
C4 = linkage(LV4, method='single', metric='cityblock', optimal_ordering=True)

L5 = L4.drop(L4.columns[7:32], axis=1)
L5 = pd.DataFrame(scaler.fit_transform(L5), columns=L5.columns)
L5.fillna(0, inplace=True)
LV5 = L5.values
LB5 = list(merged['name'])
C5 = linkage(LV5, method='single', metric='cityblock', optimal_ordering=True)

F4 = plt.figure(figsize=(25, 66), dpi=600)
D4 = dendrogram(C4, labels=LB4, orientation="right", color_threshold=5.1, show_leaf_counts=True)
plt.savefig('Dendrograms/dendrogram4.png', format='png', dpi=600)
plt.close(F4)

F5 = plt.figure(figsize=(25, 66), dpi=600)
D5 = dendrogram(C5, labels=LB5, orientation="right", color_threshold=3, show_leaf_counts=True)
plt.savefig('Dendrograms/dendrogram5.png', format='png', dpi=600)
plt.close(F5)

process_linkage(C2, LB2)

