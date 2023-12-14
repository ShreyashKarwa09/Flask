import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer

from tensorflow.python.keras.models import load_model

lematizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())

words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lematizer.lemmatize(word) for word in sentence_words]
    return sentence_words


def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list


def get_response(intents_list, intents_json):
    result = 0
    if(len(intents_list)!=0):
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
    elif(result==0):
        result = "Didn't understand what you said!!"
    return result


print("ChatBot is Running Correctly, Enter Your Queries! \n Enter Exit or Quit to Exit from the ChatBot \n")


def bot_message(message):
    rep=0
    if message == "Exit" or message == "Quit" or message == "quit" or message == 'exit':
        rep = "Exiting from the chatbot, Thank You for Using It!"
    else:
        ints = predict_class(message)
        rep = get_response(ints, intents)
    return rep
#while(True):
 #   user = input("You : ")
  #  print("Bot :",bot_message(user))
