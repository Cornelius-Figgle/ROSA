filename = 'C:/Users/Max.Harrison/source/py/ROSA/myles anthem (1).wav'
    
def getShortAudio(filename):
    import speech_recognition as sr

    # initialize the recognizer
    r = sr.Recognizer()

    with sr.AudioFile(filename) as source:
        # listen for the data (load audio to memory)
        audio_data = r.record(source)
        # recognize (convert from speech to text)
        text = r.recognize_google(audio_data)
        return text

def getLargeAudioTranscription(path): # a function that splits the audio file into chunks and applies speech recognition
    from pydub import AudioSegment
    from pydub.silence import split_on_silence
    import speech_recognition as sr

    # create a speech recognition object
    r = sr.Recognizer()

    #Splitting the large audio file into chunks and apply speech recognition on each of these chunks
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name): os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try: text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e: print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    return whole_text

def getMicrophoneAudio():
    import speech_recognition as sr

    # initialize the recognizer
    r = sr.Recognizer()

    with sr.Microphone() as source:
        # read the audio data from the default microphone
        print("\n\tTalk to me...")
        audio_data = r.record(source, duration=5) #dur in sec
        print("\n\tRecognizing...\n")
        # convert speech to text
        try: text = r.recognize_google(audio_data) ; return text
        except: return "\n\tError in recording"

#print(getMicrophoneAudio())
getwch()

from playsound import playsound
try: playsound('C:/Users/Max.Harrison/source/py/ROSA/blankinterlude.mp3')
except: 
    pathT = input("\n\tpaste file url as it don't work")
    playsound(pathT)