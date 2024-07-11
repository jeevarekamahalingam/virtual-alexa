from flask import Flask, render_template, request, jsonify
import datetime
import pyjokes
import pyttsx3
import pywhatkit
import requests
import speech_recognition as sr
import wikipedia
import geocoder
from geopy.geocoders import Nominatim
import webbrowser
import re
from bardapi import Bard
import subprocess
enable_talkback=False #possible values True or False
app = Flask(__name__,static_url_path='/static', static_folder='static')
print('Flask setup complete')

#listener = sr.Recognizer()
#engine = pyttsx3.init()
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)

def talk(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    print('Talk Started...')
    engine.say(text)
    engine.runAndWait()
    print('Talk Complete...')


def weather(city):
    api_key = "c80f376d169fb61a0c229aaafb86514f"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if "main" in x:
        y = x["main"]
        current_temperature = int(y["temp"]-273.15)
        return str(current_temperature)
    else:
        return "Sorry, I couldn't fetch the weather data for that city."

def open_website(website_name):
    websites = {
        "youtube": "https://www.youtube.com",
        "instagram": "https://www.instagram.com",
        "whatsapp": "https://web.whatsapp.com",
        "chrome": "https://www.google.com/chrome/",
        "google": "https://www.google.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "linkedin": "https://www.linkedin.com",
        "gmail"    : "https://mail.google.com",
        "cricinfo":"https://www.espncricinfo.com",
        "spotify":"https://open.spotify.com/",
        "byju's": "https://byjus.com/",
        "vedantu":"https://www.vedantu.com/",
        "daily hunt":"https://m.dailyhunt.in/news/india/english/for+you?launch=true&mode=pwa",
        "brainly":"Brainly.in https://brainly.in/",
        "quora":"https://www.quora.com/"
    }

    if website_name in websites:
        url = websites[website_name]
        webbrowser.open(url)
        return (f"Opening {website_name} in your web browser.")
    else:
        return ("I don't know how to open that website.")

def calculate(expression):
    try:
        expression = re.sub(r'[^\d+\-*/().]', '', expression)
        result = eval(expression)
        return result
    except Exception as e:
     return str(e)

'''def take_command():
    try:
        with sr.Microphone() as source:
            listener = sr.Recognizer()
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please repeat.")
        command = take_command()
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        command = None
    return command'''

def get_current_location():
    g = geocoder.ip('me')
    lat, lon = g.latlng
    geolocator = Nominatim(user_agent="location_app")
    location = geolocator.reverse((10.9601,78.0766))
    return location.address

def wikipedia_summary(to_search):
    try:
        info = wikipedia.summary(to_search, 1)
        return info
    except Exception as e:
        print(f"Error: {e}")
        return 'Sorry, I got zero or multiple match'

def search_pinterest_images(query, api_key):
    endpoint = "cwiz7lm5ogS3BqHRQkZJMM8umjK5-lVJVs_urPTj9nrytiZX32oUeKJmX0qHO6g-R5SM_w."  # Replace with the actual Pinterest API endpoint
    headers = {
        "Authorization": f"Bearer {api_key}"
    }
    params = {
        "q": query
    }

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        data = response.json()
        # Process the data and extract image URLs as needed
        image_urls = [item["image_url"] for item in data.get("items", [])]
        return image_urls
    except Exception as e:
        return f"Error searching Pinterest for images: {str(e)}"
    


def run_alexa(command=None,computer=None, name=None, No=None):
    print("entering run alexa")
    print(command)
    '''if command==None:
        command = take_command()
    '''
    print(f'you spoke: {command}')
    if command:
        if 'alexa' in command:
            bard = Bard(token='cggZCfD3s7LYD9GA_sb3NcN-sFBkDNY2XdQJIRBMklnf7kUSrsfByWGOe41T4Q3P9ON_ZA.')
            print("lara called")
            hint='in less than two sentence'
            input_text = command.replace('alexa', '')+" "+hint 
            answer = bard.get_answer(input_text)
            m=answer['content'].replace("\r\n","").replace("*"," ").replace("**"," ").replace(hint," ")
            print(m)
            if(enable_talkback==True):
             talk(m)
            return m

        elif 'play' in command:
            song = command.replace('play', '')
            if(enable_talkback==True):
             talk('Playing ' + song)
            pywhatkit.playonyt(song)
            return "Playing"+song


        elif 'play' in command:
            movie = command.replace('play', '')
            if(enable_talkback==True):
             talk('Playing ' + movie)
            pywhatkit.playonyt(movie)
            return "Playing"+movie
        
        elif 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            if(enable_talkback==True):
             talk('Current time is ' + time)
            return 'Current time is ' + time

#        elif 'who is' in command:
#            person = command.replace('who is', '')
#            info = wikipedia.summary(person, 1)
#            print(info)
#            talk(info)

        elif 'who is' in command:
            to_search = command.replace('who is', '')
            info = wikipedia_summary(to_search)
            print(info)
            if(enable_talkback==True):
             talk(info)
            return info
        elif 'what is' in command:
            to_search = command.replace('what is', '')
            info = wikipedia_summary(to_search)
            print(info)
            if(enable_talkback==True):
             talk(info)
            return info
        elif 'where is' in command:
            to_search = command.replace('where is', '')
            info = wikipedia_summary(to_search)
            print(info)
            if(enable_talkback==True):
             talk(info)
            return info

        elif 'date' in command:
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            if(enable_talkback==True):
             talk('Current date is ' + date)
            return 'Current date is ' + date

        elif 'day' in command:
            current_datetime = datetime.datetime.now()
            day = current_datetime.strftime('%A')
            if(enable_talkback==True):
             talk('Current day is ' + day)
            return 'Current day is ' + day

        elif 'who are you' in command:
            if(enable_talkback==True):
             talk('I am Alexa')
            return 'I am Alexa'

        elif 'how are you' in command:
            if(enable_talkback==True):
             talk('I am fine what about you')
            return 'I am fine what about you'
        elif 'fine or good' in command:
            if(enable_talkback==True):
             talk('ok thank you')
            return 'ok thank you'
        
        elif 'hello' in command:
            if(enable_talkback==True):
             talk('hello welcome say something..')
            return 'hello welcome say something..'

        elif 'tell me about vsb engineering college' in command:
            if(enable_talkback==True):
             talk('Our Institution, a temple of learning and a hallmark of discipline, treads towards the zenith of glory by preferring the education of global standards in the best quality and variety, and substantiates to be a benchmark among all the colleges in India.')
            return 'Our Institution, a temple of learning and a hallmark of discipline, treads towards the zenith of glory by preferring the education of global standards in the best quality and variety, and substantiates to be a benchmark among all the colleges in India.'

        elif 'what is computer' in command:
            if(enable_talkback==True):
             talk('A computer is an electronic device that processes data and performs various tasks by executing instructions provided by a user or a program')
            return 'A computer is an electronic device that processes data and performs various tasks by executing instructions provided by a user or a program'
        elif 'what is' in command:
            information = command.replace('what is', '')
            info = wikipedia.summary(information, 1)
            print(info)
            if(enable_talkback==True):
             talk(info)
            return info
        
        elif 'joke' in command:
            joke = pyjokes.get_joke()
            print(joke)
            if(enable_talkback==True):
             talk(joke)
            return(joke)
        
        elif 'weather in ' in command:
            to_search = command.replace('weather in ', '')
            weather_api = weather(to_search)
            if(enable_talkback==True):
             talk(f'The weather in {} is {weather_api} degrees celsius')
            return f'The weather in {} is {weather_api} degrees celsius'
        
        elif 'location' in command:
            current_location = get_current_location()
            print("Current Location:", current_location)
            if(enable_talkback==True):
             talk('Your current location is ' + current_location)
            return 'Your current location is ' + current_location

        elif 'open ' in command and ' in web browser' in command:
            to_search = command.replace('open ', '').replace(' in web browser', '')
            return_val=open_website(to_search)
            if(enable_talkback==True):
             talk(return_val)
            return return_val

        elif 'calculate' in command:
            expression = re.search(r'calculate (.+)', command).group(1)
            result = calculate(expression)
            if result is not None:
                if(enable_talkback==True):
                 talk(f'The result is {result}')
                return f'The result is {result}'
            else:
                if(enable_talkback==True):
                 talk('Sorry, I couldn\'t calculate that.')
                return 'Sorry, I couldn\'t calculate that.'
            

        elif 'open camera' in command:
            try:
                subprocess.Popen("start microsoft.windows.camera:", shell=True)
                return "Opening the camera app..."
            except Exception as e:
                return f"Error opening the camera app: {str(e)}"

        
        elif 'open powerpoint' in command:
            try:
                subprocess.Popen("start powerpnt", shell=True)
                if enable_talkback:
                    talk("Opening Microsoft PowerPoint")
                return "Opening Microsoft PowerPoint"
            except Exception as e:
                if enable_talkback:
                    talk("Error opening Microsoft PowerPoint")
                return "Error opening Microsoft PowerPoint"

        elif 'open word' in command:
            try:
                subprocess.Popen("start winword", shell=True)
                if enable_talkback:
                    talk("Opening Microsoft Word")
                return "Opening Microsoft Word"
            except Exception as e:
                if enable_talkback:
                    talk("Error opening Microsoft Word")
                return "Error opening Microsoft Word"

        elif 'open excel' in command:
            try:
                subprocess.Popen("start excel", shell=True)
                if enable_talkback:
                    talk("Opening Microsoft Excel")
                return "Opening Microsoft Excel"
            except Exception as e:
                if enable_talkback:
                    talk("Error opening Microsoft Excel")
                return "Error opening Microsoft Excel"
            
        elif 'open music folder' in command:
            folder_path = r"C:\Users\Jeeva Reka\OneDrive\Documents\music"  # Replace with the actual path to your folder

            try:
                subprocess.Popen(['explorer', folder_path], shell=True)
                if enable_talkback:
                    talk(f"Opening the music folder")
                return f"Opening the music folder"
            except Exception as e:
                if enable_talkback:
                    talk(f"Error Opening the music folder")
                return f"Error Opening the music folder"

        elif 'open paper folder' in command:
            folder_path = r"C:\Users\Jeeva Reka\OneDrive\Documents\presentation"  # Replace with the actual path to your folder

            try:
                subprocess.Popen(['explorer', folder_path], shell=True)
                if enable_talkback:
                    talk(f"Opening the paper folder")
                return f"Opening the paper folder"
            except Exception as e:
                if enable_talkback:
                    talk(f"Error Opening the paper folder")
                return f"Error Opening the paper folder"
        
        elif 'open movie folder' in command:
            folder_path = r"C:\Users\Jeeva Reka\Videos\movies"  # Replace with the actual path to your folder

            try:
                subprocess.Popen(['explorer', folder_path], shell=True)
                if enable_talkback:
                    talk(f"Opening the movie folder")
                return f"Opening the movie folder"
            except Exception as e:
                if enable_talkback:
                    talk(f"Error Opening the movie folder")
                return f"Error Opening the movie folder"
          
        elif 'open screenshot folder' in command:
            folder_path = r"C:\Users\Jeeva Reka\OneDrive\Pictures\Screenshots"  # Replace with the actual path to your folder

            try:
                subprocess.Popen(['explorer', folder_path], shell=True)
                if enable_talkback:
                    talk(f"Opening the screenshot folder")
                return f"Opening the screenshot folder"
            except Exception as e:
                if enable_talkback:
                    talk(f"Error Opening the screenshot folder")
                return f"Error Opening the screenshot folder"  

        elif 'open image of' in command:
            search_query = command.replace('open image of', '').strip()
            pinterest_url = f"https://www.pinterest.com/search/pins/?q={search_query}"
            try:
                webbrowser.open(pinterest_url)
                if enable_talkback:
                    talk(f"Opening the images of {search_query}")
                return f"Opening Pinterest and searching for images of {search_query}"
            except Exception as e:
                if enable_talkback:
                    talk(f"Error opening Pinterest for image search: {str(e)}")
                return f"Error opening Pinterest for image search: {str(e)}"  


        elif 'stop' in command:
            #talk('Stopping Alexa')
            #talk('Thank You')
            if(enable_talkback==True):
             talk("Stopping Alexa Thank you")
            return "Stopping Alexa Thank you"
            exit()

        else:
            if(enable_talkback==True):
             talk('Please say the command again.')
            return'Please say the command again.'


#def user_commands():
#    pass

#while True:
#    engine.setProperty('rate', 130)
#    run_alexa()

#if _name_ == "_main_":
#    command = "location"

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/process', methods=['POST'])
def process():
    print('Alexa called')
    
    '''print("value under request.form")
    print(request.form)
    is_text=request.form[is_text]
    print("under is_text")
    print(is_text)
    '''
    command = request.form['command'].lower()
    print("printing command")
    print(command)
    '''if command=="":
        command=take_command()
    '''
    result= run_alexa(command)
    return jsonify({'response': result})
@app.route('/destination.html')
def destination():
    return app.send_static_file('destination.html')


if __name__ == '__main__':
    app.run(debug=True, port=80)
