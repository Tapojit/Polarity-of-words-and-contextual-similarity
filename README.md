# Determining Polarity of words and Contextual Similarity amongst words

This includes an implementation of Turney method to determine polarity of a given word based on its proximity to negative and
positive seed words. Also includes implementation of Cosine Similarity to determine contextual similarity of two given words.

## Polarity

The script **polarity.py** contains a function called **polarity_calc** which parses all space deliminated linguistic objects (eg: words) from tweets in the file *tweets.txt* and calculates a their polarity scores. Higher frequency of linguistic objects appearing near other negative objects mean they have lower polarity and vice versa for positive objects. Objects with negative polarity are mostly associated with negative objects and objects with positive polarity are mostly associated with positive objects.

Below are two lists of positive and negative seed words used in this script to calculate polarity of words *near* to them:
```
Positive seed list: ["good", "nice", "love", "excellent", "fortunate", "correct", "superior"]

Negative seed list: ["bad", "nasty", "poor", "hate", "unfortunate", "wrong", "inferior"]

```
**Pointwise Mutual Information** (PMI) is used to measure the log probability of each object *x* appearing near each individual positive and negative seed word *y*.

![Image](https://raw.githubusercontent.com/Tapojit/Polarity-of-words-and-contextual-similarity/master/PMI.png)

Using the **Turney method**, polarity for each object is calculated by subtracting sum of PMI of object with all negative words from sum of PMI of object with all positive words.

![Image](https://raw.githubusercontent.com/Tapojit/Polarity-of-words-and-contextual-similarity/master/polarity.png)

### Top 50 Positive and Negative linguistic objects(tokens):

Below is a demonstration of obtaining top positive and negative tokens from **tweets.txt** using *polarity_calc* function. 

Once you download this repository, *cd* into its directory using *bash*, open the python console and run the lines below:

```
>>> import operator
>>> from collections import defaultdict
>>> from polarity import polarity_calc
>>> polarity=polarity_calc()

# Top 50 positive tokens
>>> max_50=dict(sorted(polarity.iteritems(), key=operator.itemgetter(1), reverse=True)[:50]).keys()

# Top 50 negative tokens
>>> min_50=dict(sorted(polarity.iteritems(), key=operator.itemgetter(1), reverse=True)[-50:]).keys()

```
*print*ing out top 50 positive tokens will give this output:

```
['friend\xf0\x9f\xa4\x9e\xf0\x9f\x8f\xbd', 'https://t.co/unteosecly', 'cassievers\xe2\x98\xba', 'https://t.co/rcgdsyymir',
'eighteet', 'you\\n-i', '-*', 'througho\xe2\x80\xa6', 'one\\ngood', 'gf\xf0\x9f\x92\x8d', 'ex\xf0\x9f\x97\x91', 'amiracan', 
'lovvveeeee', 'https://t.co/filzv6f2ze', 'dulce\xf0\x9f\x98\xa9', 'https://t.co/lvrki7uwhd', 'you\xc2\xa1\xc2\xa1\\', 
'chazelle', 'n-i', 'dirty\xf0\x9f\xa4\xa2', 'aside\\', 'it\xf0\x9f\xa4\x91', 'https://t.co/p1fyayehnz', '-tb\\', 
'https://t.co/xketcvmmno', 'https://t.co/4vy3fv70rk', 'https://t.co/38zyfmjco8', '\xcb\x97\xcb\x8f\xcb\x8b', 
'https://t.co/pyvhn56pje', 'https://t.co/ve99xlwp0g', 'https://t.co/bnk2hia1mk', 'nori\xe2\x80\xa6', 'forever\\n-i', 'todos', 
'much\\n-i', 'noriega', 'bidadari', 'https://t.co/o1ii42byhl', 'bodoamatlah', '\xcb\x8e\xcb\x8a\xcb\x97', 
'girl\xf0\x9f\x98\xad\xf0\x9f\x98\xad\xf0\x9f\x98\xadits', 'luck\xf0\x9f\x92\x9e\xf0\x9f\x92\x9c', 
'\xe2\x9d\xa4\xf0\x9f\x92\x99\xf0\x9f\x92\x9b\xf0\x9f\x92\x9c', '2017.02', 'https://t.co/hsyskqcnn6', 'octavia', 
'\xe2\x9b\x88\xe2\x9a\xa1\xef\xb8\x8f\xf0\x9f\x98\x8d', '\\n\\nfaveeeee', 'looooooovveeee', 'https://t.co/jm\xe2\x80\xa6'] 

```
*print*ing out top 50 negative tokens will give this output:

```
['us-they', 'sudmalis', 'bitchness', 'deomocrats', 'https://t.co/tx\xe2\x80\xa6', 'https://t.co/fxveuydvfx', 
'hurt/disregarded', 'https://t.co/uchmaxafrk', 'looser', 'https://t.co/cmz27nmopl', "day's.", 
'https://t.co/rjmh9eh\xe2\x80\xa6', 'all-i', 'usa-they', 'https://t.co/rnqhff13az', 'https://t.co/mtehygjxtl', 
'democracy\\nleftists', 'look\xf0\x9f\x98\x85', 'wowowowowowowowow', 'winnn', 'ill-they', 'anti-patriotism', 'bumbling', 
'https://t.co/qio17l0iqz', 'proclivity', 'chavs', 'congressperson-to-congressperson', 'https://t.co/2tiza9n7\xe2\x80\xa6', 
'nap/bad', '\xf0\x9f\x93\x8csaying', 'https://t.co/wwfvgyfolm', 'racist\\', '4cm', 'my-', 'home\xf0\x9f\x98\xad', 
'l\xc3\xb8v\xc3\xab', 'https://t.co/lqwhh2qora', 'torbjorn', 'hinduism\\nyet', 'nazi\\', 'india\\nleftists', 
'cough*cincy*cough', 'https://t.co/wzz4ndbn7n', '||i', 'https://t.co/qfpq8hcd3l', 'https://t.co/tkzqcrnry8', 'cialis', 
'condiment', 'https://t.co/yjikxov0q9', 'https://t.co/itqwxo\xe2\x80\xa6']

```

## Contextual Similarity

Two or more words are said to be *contextually similar* when they appear beside a large number of mutual words. For instance, *"cat"* & *"dog"* are contextually similar as they are both animals, hence they share a large number of words they can appear beside.

**Cosine Similarity** function (Cossim) is used to calcualte a score representing how contextually similar a pair of tokens are. It is between 0 and 1; the higher the score, stronger the similarity. For each word, it requires two vectors, *x* & *y*. Each vector contains counts of appearances beside each mutual words **(context counts)**. Hence, the vectors are of length equivalent to the number of individual mutual words they appear beside. 

![Image](https://raw.githubusercontent.com/Tapojit/Polarity-of-words-and-contextual-similarity/master/COSSIM.png)

The script **distsim.py** contains a function called **cos_sim** for calculating Cosine Similarity, which takes as arguments:
1. Dictionary containing Bag of Words(BOW) representaion of context counts for each of the pair of words.
2. First word.
3. Second word.

### Calculating Context Count

**nytcounts.university_cat_dog.txt** contains context count BOWs for three words: "cat", "dog" & "university". Here are the instructions to calculate cosine similarities amongst these three words.

Open the python console in *bash* while in the downloaded repository directory. Run the lines below:

```
>>> import distsim
>>> word_to_ccdict = distsim.load_contexts("nytcounts.university_cat_dog")
>>> cat_dog_sim=distsim.cos_sim(word_to_ccdict,'cat','dog')
>>> cat_uni_sim=distsim.cos_sim(word_to_ccdict,'cat','university')
>>> dog_uni_sim=distsim.cos_sim(word_to_ccdict,'university','dog')
>>> print "\ncosine similarity between cat and dog: ", cat_dog_sim, "\n"
>>> print "cosine similarity between cat and university: ", cat_uni_sim, "\n"
>>> print "cosine similarity between university and dog: ", dog_uni_sim

```
Below are the printed outputs:

```
file nytcounts.university_cat_dog has contexts for 3 words

cosine similarity between cat and dog:  0.966891672715 

cosine similarity between cat and university:  0.660442421144 

cosine similarity between university and dog:  0.659230248969

```
## Notes
