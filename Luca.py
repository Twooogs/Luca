import os
import openai
import pyttsx3
import speech_recognition as sr

# Creating the root window


# Set up the speech recognition object
r = sr.Recognizer()

# Set up the tts
tts = pyttsx3.init()
voice = tts.getProperty('voices') #get the available voices

# eng.setProperty('voice', voice[0].id) #set the voice to index 0 for male voice
tts.setProperty('voices', voice[0].id)

# Set up the microphone
mic = sr.Microphone()



# Makes speaking quicker to do
def speak(word):
    tts.say(word)
    tts.runAndWait()


# Constantly listens to default mic
def recogniser(understand):

    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)


    # Try to recognize the command
    try:
        print("Recognising...")
        command = r.recognize_google(audio)
        if understand:
            commandCon = r.recognize_google(audio, show_all=True)
            commandConFl = float((commandCon['alternative'][0]['confidence']))

            if commandConFl < 0.7:
                speak("Did not understand that")
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        print("Error making request; {0}".format(e))
        return ""


# Start listening for luca then asks what the user wants
def listener():
    while True:
        print("Start of loop\n")
        # Listen for the command to turn on
        signal = recogniser(False)
        #If the command is "turn on," turn on the system
        if "luca" in signal or "luka" in signal:
            speak("What do you want?")
            prompt = recogniser(True)

            return prompt


# Defines where the open ai key is
openai.api_key_path = 'openai_key'
openai.api_key = os.getenv("OPENAI_API_KEY")

#params for ai
model = "text-davinci-003"
stop = "text"

# Open Ai does all the hard stuff here
def AI(prompt):

    response = openai.Completion.create(model=model,
      prompt=prompt,temperature=temp,max_tokens=maxToken,top_p=topP,frequency_penalty=frequencyP,presence_penalty=presenceP,stop=stop)

    if response is None:
        speak("Unfortunately I can not understand you, please try again")
    else:
        speak(response["choices"][0]["text"])
        print(response["choices"][0]["text"])




temp = 0
maxToken = 300
topP = 1
frequencyP = 0
presenceP = 0

while True:

    aiPrompt = listener()

    if aiPrompt == "":
         pass
    else:
        AI(aiPrompt)



