import speech_recognition as sr
#from subprocess import call
import pyttsx


sr.Microphone(device_index=0, sample_rate=44100, chunk_size=512)
r = sr.Recognizer()
r.energy_threshold = 1000
r.dynamic_energy_threshold=True


def prompt(string,respond=False):

    engine = pyttsx.init()
    #rate = engine.getProperty('rate')
    engine.setProperty('rate', 160)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    print(string)
    engine.say(string)
    engine.runAndWait()
    #return True


def listen(datatype=None):
    while True:
        with sr.Microphone() as source:
            print('listening..')
            audio = r.record(source ,duration=2)
            print('Fetching')
            try:
                if datatype == 'num':

                    message = (r.recognize_google(audio,language='en', show_all=True))
                    print(message)
                    for subdict in message['alternative']:
                        if subdict['transcript'].isdigit():
                            message=subdict['transcript']
                            print(message)
                            return message
                if datatype == 'month':
                    message = (r.recognize_google(audio,language='en', show_all=True))
                    for subdict in message['alternative']:
                        inputlist = ["january","february","march","april","may","june","july","august","september","october","november","december"]
                        if set([subdict['transcript'].lower()]).intersection(inputlist):
                            message = subdict['transcript']
                            print(message)
                            return message
                if datatype == 'class':
                    message = (r.recognize_google(audio, language='en', show_all=True))
                    for subdict in message['alternative']:
                        if subdict['transcript'].lower() == 'economy':
                            message = subdict['transcript']
                            print(message)
                            return message
                if datatype == 'yesno':
                    message = (r.recognize_google(audio, language='en', show_all=True))
                    for subdict in message['alternative']:
                        inputlist = ['yes','no']
                        if set([subdict['transcript'].lower()]).intersection(inputlist):
                            message = subdict['transcript']
                            print(message)
                            return message
                else:
                    message = (r.recognize_google(audio,language='en', show_all=False))
                    print(message)
                    return message


            except sr.UnknownValueError:
                print("Sorry can't understand")
            except sr.RequestError as e:
                print("Could not connect; {0}".format(e))
            except:
                prompt("Please Repeat")