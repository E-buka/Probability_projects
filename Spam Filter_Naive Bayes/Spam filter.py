# ### Classification for spam messages
# Using Naive Bayes algorithm to classify messages

import pandas as pd
import re

df = pd.read_csv('SMSSpamCollection', sep='\t', header=None, names=['Label', 'SMS'])
print(df.head())

print(df.info())

print(df.value_counts('Label', normalize=True)*100)

# Spliting the dataset into train (80%) and test (20%) dataset by randomizing and sampling. 
# About 80% of the dataset is 4458 while 1114 messages accounts for 20% roughly. 

randomized = df.sample( frac=1, random_state=1, ignore_index=False)
train_set = round(len(randomized)*0.8)

train_data = randomized[:train_set].reset_index(drop=True)
test_data = randomized[train_set:].reset_index(drop=True)

print(train_data.shape)
print(test_data.shape)


print(train_data.value_counts('Label', normalize=True)*100)
print(test_data.value_counts('Label', normalize=True)*100)


#removing punctuations from the SMS text

train_data['SMS'] = train_data['SMS'].str.replace(r'\W', ' ').str.lower()
print(train_data.head())

# Extracting all the vocabulary in the SMS text

vocabulary = []
count = 0
for sms in train_data['SMS'].str.split():
    for word in sms:
        vocabulary.append(word)

print(len(vocabulary))
vocabulary = set(vocabulary)
vocabulary = list(vocabulary)
print(len(vocabulary))


for index, word in enumerate(vocabulary):
    if word == '':
        print(index, word)


# Transforming all the words in vocabulary into dictionary and then dataframe

word_count = {word: [0] * len(train_data['SMS']) for word in vocabulary}
count = 0
for index, sms in enumerate(train_data['SMS']):
    sms = sms.split()
    for text in sms:
        word_count[text][index] += 1

word_count_per_sms = pd.DataFrame(word_count)
word_count_per_sms.head(3)


word_count_per_sms['to'].value_counts()


# concatenating both word_count_per_sms and train_set dataframes

train_set_complete = pd.concat([train_data, word_count_per_sms], axis=1)
train_set_complete.head(3)


## Calculating Constants, probability shall be represented with p, ham represents non_spam sms
## p(spam), p(ham), total words in spam sms, total words in non_spam and total vocabulary

### p(spam) and p(ham)

spam_sms = train_set_complete.loc[train_set_complete['Label'] == 'spam']
total_spam_sms = len(spam_sms)
total_non_spam_sms = len(train_set_complete) - total_spam_sms
p_spam = total_spam_sms / len(train_set_complete)
p_ham = total_non_spam_sms / len(train_set_complete)
print(p_spam)
print(p_ham)



## N_spam, N_ham, N_vocabulary, alpha is Laplace smoothing parameter for Naive Bayes

alpha = 1 
n_spam = 0
n_ham = 0

for sms in spam_sms['SMS'].str.split():
    n_spam += len(sms)

ham_sms = train_set_complete.loc[train_set_complete['Label'] == 'ham']

for sms in ham_sms['SMS'].str.split():
    n_ham += len(sms)

n_vocabulary = len(vocabulary)
      
print(n_ham, n_spam)

print(p_ham)


## Calculating parameters 
ham_parameter = {word:0 for word in vocabulary}
spam_parameter = {word : 0 for word in vocabulary}

for word in vocabulary: 
    word_given_spam = spam_sms[word].sum()
    prob_word_given_spam = (word_given_spam + alpha) / (n_spam + alpha * n_vocabulary)
    spam_parameter[word] = prob_word_given_spam
    
    word_given_ham = ham_sms[word].sum()
    prob_word_given_ham = (word_given_ham + alpha)/ (n_ham + alpha  * n_vocabulary)
    ham_parameter[word] = prob_word_given_ham


## Classifying new messages 

def classify(message):

    message = re.sub(r'\W', ' ', message)
    message = message.lower()
    message = message.split()
 
    p_spam_given_message = p_spam
    p_ham_given_message = p_ham
    for word in message:
        if word in spam_parameter: 
            p_spam_given_message *= spam_parameter[word]
        if word in ham_parameter:
            p_ham_given_message *= ham_parameter[word]
        else: 
            continue

    print('P(Spam|message):', p_spam_given_message)
    print('P(Ham|message):', p_ham_given_message)

    if p_ham_given_message > p_spam_given_message:
        print('Label: Ham')
    elif p_ham_given_message < p_spam_given_message:
        print('Label: Spam')
    else:
        print('Equal proabilities, have a human classify this!')



word1 = 'WINNER!! This is the secret code to unlock the money: C3421.'
word2 = 'Sounds good, Tom, then see u there'

classify(word1)
classify(word2)


## measuring spam filter's accuracy 
def classify_test_set(message):

    message = re.sub(r'\W', ' ', message)
    message = message.lower()
    message = message.split()
 
    p_spam_given_message = p_spam
    p_ham_given_message = p_ham
    for word in message:
        if word in spam_parameter: 
            p_spam_given_message *= spam_parameter[word]
        if word in ham_parameter:
            p_ham_given_message *= ham_parameter[word]
        else: 
            continue

    if p_ham_given_message > p_spam_given_message:
        return 'ham'
    elif p_ham_given_message < p_spam_given_message:
        return 'spam'
    else:
        return 'needs human classification'

test_data['predicted'] = train_data['SMS'].apply(classify_test_set)
print(test_data.head())


## Measuring the accuracy
correct = 0 
total = test_data.shape[0]
for row in test_data.iterrows():
    row = row[1]
    if row['Label'] == row['predicted']:
        correct += 1

accuracy = correct/total 

print(accuracy)
