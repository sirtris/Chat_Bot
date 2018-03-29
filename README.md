# Chat_Bot
Time is limited  
In a homework, so it's hard  
To finish what you  

# About the Bot
Our idea was to create a chatbot that helps you with finding syllables in a word and writing haikus.

A haiku is a form of Japanese poetry. It is a very short poem that consist of 17 syllables that are split into three rows in a 5-7-5 pattern. Japanese syllables are somewhat shorter than English ones, so there is some debate about whether a haiku in English should only  have 10 to 14 syllables, to be more similar to the original Jaranese ones. We will, however, ignore this debate for our chatbot and just say that a haiku must be written in the characteristic 5-7-5 form.

The bot can recognize a variety of greetings and goodbyes, to which it will answer with a pre-programmed response. If the bot does not recognize the input, it will inform you that it was not able to understand the input and that with writing `info` to the bot will prompt it to tell you what it can do. \
[add image] <- hab schon ein passendes
The main functionalities of the bot are helping to write haikus and helping you finding the syllables in a word.  

## Haiku
### How to use
To make the bot help you write a haiku you can just send it a text that has approximately the length of a haiku. The bot will then check if the text is indeed in that range and send you back a similar text that matches the form of a haiku. If the text already was a haiku, the bot will send back the same text formatted as a haiku.

[add image] <- kinky haiku
### How it works
To check whether the text has the appropriate amount of syllables we must find a way to count syllables in word. For this task we use a phonetic dictionary, pythons `NLTK cmudict`. Because it is a dictionary, it does not contain all words. We use `pyphen` as a fall-back when encountering words not in `cmudict`. Unfortunately this does not work as well as the `NLTK` method (More in the Section 'Finding syllables').  
To create the haiku we check if parts of the haiku (like the first line or the last line) are
already in the right format. We then change the line(s) that is(/are) not matching.
This is done by replacing words with synonyms of the word, until the desired number of syllables is reached.
Finding the synonyms is done with the `nltk wordnet` database. We first used the word2vec model `gloVe` to find
similar words but later found that `wordnet` works better. If a word is not in the database
we fall back to the original method of using `gloVe`. 

## Finding syllables
### How to use
One way to find the syllables in a word is to clap along when saying it. Each clap corresponds to one syllable. Sometimes people still find this difficult to do. This is where our bot comes to help. Just send it the clapping hands emoji(👏) followed by the word or text you want to know the syllables of. It will then send you back a message, where the clapping hands emoji is inserted at the points where you would have to clap.
[Image]
### How it works
To achieve this task we use the hyphenator that comes with `pyphen` together with our own set of rules. Even if the hyphenator in `pyphen` would work perfectly it would not quiet get the task right.
Hyphenating a word in the English language is not exactly the same as dividing it up into phonetic syllables. The word `learning` for example would be divided into its phonetic syllables like this `lear-ning` (What we would want). In English writing (and thus in `pyphen`) one may not hyphenate it like this at the end of a line because it is left ambiguous how to pronounce the `lear-` part at the end of the line. \
If the word has as many syllables a vowels (e.g. robot) we use our own method to insert the claps otherwise we use `pyphen`.
Our method uses `cmudict` to count the phonetic syllables and checks if the number of vowel letters (aeiou) matches that.
We then put the clap emoji after that vowel. This actually works reasonably well.
#### Y, oh y!
The letter `y` can sometimes be a vowel. We just check whether it is surrounded by other vouwles to determine its status. For example: The first `y` in `Sydney` is surrounded by consonants (`S` and `d`) and is thus assumed to be a vowel, while the latter one is preceded by an `e` and thus assumed to be a consonant.

# Running the Bot
## Configurations
You need a file called `config.py` with a line `TOKEN = "YOUR_API_KEY"`
## Running
Just run `telegram.py` in `Python 3`.

# Authors
Mathis Sackers(s4463455) and Tristan Payer(sXXXXXXX)
