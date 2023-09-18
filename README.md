# NLP-Driven Identification of Similar Accounts 



## Description

This project investigates several methods of detecting users operating multiple accounts online. This project is written in Python, and uses pandas, NLTK, NumPy, scikit-plearn, SciPy, and matplotlib throughout.

## Features
  
- **Methods**
  - Word Frequency: Created a corpus (collection of all words in over 400,000 comments), found the top 50 most frequently used words, and found the user frequency for each word
  - Syntax Analysis: Created syntax based metrics, including average sentence length, frequency of long words, percent of sentences capitalized
  - Temporal Analysis: Extracted the hour (0-23) of each post and created a dataframe of post frequency by hour

- **Visualization**: Created dendrograms for each hierarchical clustering method. Check the `Dendrograms` folder for each. (Note: It may be difficult to see eacha image on a brwoser, as the files are very large. I recommend using GIMP or some other photo-editing software)




## Usage

`API_Requests.py` - Script to extract Disqus comments to a feather file format

`Stylometry.py` - Initial data preprocessing and analysis: finding 50 most frequent  words and their distributions

`Syntax_Analysis.py` - Builds on previous output to include new metrics, including capitalization frequency, sentence length, and use of long words

`Time_Analysis.py` - Extracts statistics about post frequency for each user 

`Dendrograms.py` - Hierarchical cluster analysis of the data to identify duplicate accounts

`Dataframes` - Contains all dataframes created or used in the above files (Note: this does not include raw data which was too expensive to upload. I'm happy to share it with anyone who requests it).
- `message_time` - raw data for time of each message
- `time_data` - Posting frequency for every hour for each user
- `unfiltered_corpus` - contains raw corpus for each user along with three statistics
- `corpus` - contains cleaned up (i.e., HTML tags and links removed) corpus for each user along with three style-based statistics
- `Top50` - Top 50 word frequency for each user
- `df_time_words` - contains time and word frequencies for 266 active users
- `df_time_words_expanded` - contains time and word frequencies for 521 users
- `metrics_top25` - style-based statistics and word frequency for each user



`Dendrograms` - Contains .png files of each dendrogram created in `Dendrograms.py`. I recommend viewing them in GIMP or other photo editing software, as the file is quite large and might slow your browser if viewed directly.


## Results 

<table>
  <tr>
    <th>Method</th>
    <th>Accuracy<sup>1</sup></th>
  </tr>
  <tr>
    <td>Word Frequency (All Users)</td>
    <td rowspan="2" style="vertical-align:middle; text-align:center">93%</td>
  </tr>
  <tr>
    <td>Word Frequency (Active Users)</td>
  </tr>
  <tr>
    <td>Word Frequency + Temporal Analysis</td>
    <td style="text-align:center">73%</td>
  </tr>
  <tr>
    <td>Word Frequency + Syntax Analysis</td>
    <td style="text-align:center">73%</td>
  </tr>
  <tr>
    <td>Word Frequency + Syntax Analysis + Temporal Analysis</td>
    <td style="text-align:center">67%</td>
  </tr>
</table>


<sup>1</sup> - lower bound of the true positive identification rate, taken by obtaining the top 15 closest points in each clustering, and identifying the proportion of the matches that are known duplicate accounts. The accuracy could be even higher if it was later revealed a match was the same person.

**Sample Calculation**: Running `process_linkage(C1, LB1).head(15)` in `Dendrogram.py` yields the following table. It has been annotated to denote known alternate accounts:

<p align="center">
  <img src="https://i.imgur.com/cVQpAMN.png" width="50%">
</p>



In this chart, blue represents a match, while orange represents no evidence of a match. Note that when it matches users with the same exact name (e.g. BlueDot and BlueDot), these are not the same account. This occurred because the user made a new account and had similar word frequencies to their previous. Thus, the lower bound for accuracy in this method is $\frac{14}{15} = 93\%$. However, it is possible that Xzplorer is indeed Heebs13, and the accuracy is even higher than we expected.


**Sample Visualizations**
<br>


<figure style="text-align:center;">
  <img src="https://i.imgur.com/HEn7zlG.png" width="60%" alt="dendrogram1.png zoomed in. Colored components indicate matches">
  <figcaption><code>dendrogram1.png</code> zoomed in. Colored components indicate matches</figcaption>
</figure>

<br>
<figure style="text-align:center;">
  <img src="https://i.imgur.com/InUeNxk.png" width="60%" alt="Word cloud of the top 50 words in the PredictIt.org community">
  <figcaption>Word cloud of the words in the PredictIt.org community, from <code>corpus</code></figcaption>
</figure>




