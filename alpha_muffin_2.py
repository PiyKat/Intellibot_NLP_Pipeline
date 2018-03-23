from nltk import SnowballStemmer,word_tokenize
from nltk.tag.stanford import StanfordPOSTagger
import speech_recognition as sr
#import pygame
import sys
from nltk.stem import WordNetLemmatizer

import stock_market_data
########################
import alpha_flight
import alpha_gi
#import alpha_iot
import alpha_simpleapis
import alpha_meaning
import meeting_2
import unit_conversion

#########################

s = SnowballStemmer('english').stem
#tagger = StanfordPOSTagger('../stanford-postagger/models/english-bidirectional-distsim.tagger','stanford-postagger/stanford-postagger.jar')

try:
    s = SnowballStemmer('english').stem
    tagger = StanfordPOSTagger(model_filename='../stanford-postagger/models/english-bidirectional-distsim.tagger',
                               path_to_jar='../stanford-postagger/stanford-postagger.jar')

    lemma = WordNetLemmatizer()

except:
    print("error::>>", sys.exc_info()[1])



sr.Microphone(device_index=0, sample_rate=44100, chunk_size=512)
r = sr.Recognizer()
r.energy_threshold = 1000
r.dynamic_energy_threshold=True
#pygame.init()
#pygame.display.set_mode([100,100])
# pygame.display.set_mode(1,1)
with sr.Microphone() as source:

                print('listening..')
                audio = r.record(source,duration=3)
                print('Fetching')

                try:
                    message = (r.recognize_google(audio,language='en', show_all=False))
                    print(message)

                    token = word_tokenize(message)
                    stem = [s(w) for w in token]
                    lem = [lemma(w) for w in token]
                    tag = tagger.tag(token)
                    count = 0
                    ret = True
                    while ret:
                        #ret = alpha_iot.trigger(ret, stem)
                        ret = alpha_flight.trigger(ret, stem, tag)
                        ret = alpha_gi.trigger(ret, stem, tag)
                        ret = alpha_simpleapis.trigger(lem)
                        ret = alpha_meaning.trigger(lem,tag)
                        ret = meeting_2.trigger(stem,tag)
                        ret = stock_market_data.trigger(tag)
                        ret = unit_conversion.trigger(stem, tag)

                        if ret == False:
                            print("Sorry can't understand")

                        else:
                            continue

                except sr.UnknownValueError:
                    print("Sorry")
                except sr.RequestError as e:
                    print("Could not connect; {0}".format(e))
                except:
                    print("Please Repeat")