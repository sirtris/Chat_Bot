# Chat_Bot
Time is limited  
In a homework, so it's hard  
To finish what you  

# About the Bot
Our idea was to create a chatbot that helps you with finding syllables in a word and writing haikus. \

A haiku is a form of Japanese poetry. It is a very short poem that consist of 17 syllables that are split into three rows in a 5-7-5 patter. Japanese syllables are somewhat shorter than English ones, so there is some debate about whether a haiku in English should only  have 10 to 14 syllables, to be more similar to the original ones. We will however ignore this debate for our chatbot and just say that a haiku must be written in the characteristic 5-7-5 form. \

The bot can recognize a variety of greetings and goodbyes, to which it will answer with a pre-programmed response. If the bot does not recognize the input, it will tell you that it was not able to understand that and that with writing `info` to the bot it will tell you what it can do. \
[add image] <- hab schon ein passendes
The main functionalities of the bot are helping to write haikus and helping you finding the syllables in a word.  

### Haiku
To make the bot help you writing a haiku you can just send it a text that has approximately the length of a haiku. The bot will then check if the text is indeed in that range and send you back a similar text that matches the form of a haiku. If the text already was a haiku, the bot will send back the same text formatted as a haiku.

[add image] <- kinky haiku
#### How it works
To check whether the text has the appropriate amount of syllables we must find a way to count syllables in word. For this task we use pythons `NLTK cmudict`. Because it is based on a dictionary it does not contain all words. We use `pyphen` as a fall-back for these cases. Unfortunately this does not work as well as the `NLTK` method.  

### Finding syllables
One way to find the syllables in a word is to clap along when saying it. Each clap corresponds to one syllable. Sometimes people still find this difficult to do. This is where our bot comes to help. Just send it the clapping hands emoji followed by the word or text you want to know the syllables of. It will then send you back a message, where the clapping hands emoji is inserted at the points where you would have to clap.
[Image]
#### How it works
To achieve this task we use the hyphenator that come with `pyphen` together with our own set of rules. Even if the hyphenator in `pyphen` would work perfectly it would not quiet get the task right. In English hyphenating a word is not exactly the same as dividing it up into syllables. The word `learning` for example would be divided into syllables like this `lear-ning`. One must however not hyphenate it like this at the end of a line because a reader could not know how to pronounce the `lear` part. \
If the word has a many syllables a vowels we use our own method to insert the claps otherwise we use `pyphen`


# Configurations
you need a file called `config.py` with a line `TOKEN = "YOUR_API_KEY"`

# Authors
Mathis Sackers and Tristan Payer
