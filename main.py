from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
from time import ctime
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

engine = pyttsx3.init('sapi5')  #windows provied voice api for male and female voice
voices = engine.getProperty("voices") #voices la list mai 2 voice store hai -male and female
#print(voices[1].id)
engine.setProperty('voices',voices[0].id)

def authenticate_google():
    
    creds = None
   
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(n,service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=n, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary']) 

def speak(audio):
    engine.say(audio)
    engine.runAndWait()



def wishme():
    hour = int(datetime.datetime.now().hour)

    if hour>=0 and hour<=12:
        speak("GOOD MORNING SIR.")
    elif hour>12 and hour<=18:
        speak("GOOD AFTERNOON")
    else:
        speak("GOOD EVENING")
    speak("THIS IS NEMO SIR. HOW MAY I HELP YOU.")

def takeCommand():
    # it takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
            print("Recognizing...")
            text = r.recognize_google(audio,language='en-in')
            print("YOU SAID : {}".format(text))
    except:
        speak("Sorry could not Recognize your voice...please say it again...")
        return "None"
    return text   #what we said we have return

#def sendEmail(to, content):
#    server = smtplib.SMTP('smtp.gmail.com', 587)
#    server.ehlo()
#    server.starttls()
#    server.login('arjun.pillai17@siesgst.ac.in, )
#    server.sendmail('arjun.pillai17@siesgst.ac.in', to, content)
#    server.close()
if __name__ == "__main__":
    wishme()
    while True:
        text = takeCommand().lower()
        if 'wikipedia' in text:
            speak("Searchiing Wikipedia")
            text = text.replace('wikipedia','')
            results = wikipedia.summary(text,sentences=2)
            speak("According to wikipedia")
            speak(results)
        elif 'youtube' in  text:
            webbrowser.open("youtube.com")
        elif 'google' in  text:
            webbrowser.open("google.com")
        elif 'google maps' in  text:
            webbrowser.open("https://www.google.com/maps")
        elif 'coronavirus' in  text:
            webbrowser.open("https://www.mohfw.gov.in/")
        elif 'images' in text:
            img_dir="C:\\Users\\karan\\Downloads\\original\\Bootstrap4_Code\\13_Museum_Of_Candy\\Starter\\imgs"
            images = os.listdir(img_dir)
            print(images)
        elif 'time' in text:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strtime}")
        elif "pycharm" in text:
            path = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2019.2.1\\bin\\pycharm64.exe"
            os.startfile(path)
        elif "visual studio code" in text:
            path = "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\Common7\IDE\devenv.exe"
            os.startfile(path)
        elif "google classroom" in text:
            webbrowser.open("https://classroom.google.com/u/1/h")
        elif "email to arjun" in text:
            try:
                speak("What would you like to say sir..")
                content = takecommand()
                to = "arjun.pillai17@siesgst.ac.in"
                sendEmail(to,content)
                speak("Email has been sent..")
            except:
                speak("Sorry sir, The email has not been send due to some error.")
        elif "shutdown" in text:
            shutdown = input("Do you wish to shutdown your computer ? (yes / no): ") 
            if shutdown == 'no': 
                exit() 
            else: 
                os.system("shutdown /s /t 1") 
        elif "introduction" in text:
            speak("My name is Nemooo,I 'am a voice assistant robot working for Karan Pillai")
        elif "age" in text:
            speak("Its very bad to ask sommeone's age.By the way i am just been created...")
        elif "calendar" in text:
            service = authenticate_google()
            get_events(2,service)
        #elif "search" in text:
        #    search = record_audio("Wht do you want to search for??")
        #    url = "https://www.google.com/search?q=" + search
        #    webbrowser.open(url)
        elif "time" in text:
            print(ctime())


        elif "quit" in text:
                 break
speak("Thank you, your program has been ended")
exit()


  