from tkinter import Tk, N, S, E, W, END, Button
from hugchat import hugchat
from hugchat.login import Login
from tkinter import font
import tkinter as tk
from gtts import gTTS
from langdetect import detect
import pygame
import speech_recognition as sr

chat_bot_name = 'YsfGPT'
email= ''
passwd = ''
web_search_option = 'False'

sign = Login(email, passwd)
cookies = sign.login()
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
conv_id = chatbot.new_conversation()

def ask_hugchat(text):
    global cookies
    global chatbot
    chatbot.change_conversation(conv_id)
    response = chatbot.query(text)
    return str(response)

def detect_language(input_text):
    try:
        language = detect(input_text)
        return language
    except Exception as e:
        print(f"Error: {e}")
        return None

def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    
    # Wait for the sound to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def text_to_speech(txt,file_path):
    language = detect_language(txt)

    tts = gTTS(text=txt, lang=language, slow=False)

    # Stop the pygame mixer
    try:
        pygame.mixer.music.stop()
    except:
        print('hi')
    # Saving the converted audio in a file
    tts.save(file_path)
    # Playing the converted audio file
    play_audio(file_path)


def speech_to_text():
    def recognize_speech():
        while True:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

                try:
                    text = recognizer.recognize_google(audio)
                    return text
                except sr.UnknownValueError:
                    play_audio('repeat1.mp3')
                    continue
                except sr.RequestError as e:
                    print(f"Error making the request: {e}")

    recognizer = sr.Recognizer()

    # start the speech recognition in a new thread
    text = recognize_speech()
    return text
def conversation():
    text_to_speech('Hello, How are you doing today?', 'output.mp3')
    i=0
    while True:
        txt = speech_to_text()
        response = ask_hugchat(text=txt)
        text_to_speech(response,f'output{i}.mp3')
        i+=1
root = Tk()
root.title(chat_bot_name)
ask_hugchat('I want to have a conversation with you like humans from now on , so please respond like a human and with a very short response')
screen_width = 300
screen_height = 300

root_width = int(screen_width * 0.8)
root_height = int(screen_height * 0.8)
root.geometry(f"{root_width}x{root_height}")

# Set the background color of the window
root.configure(bg='#333444')
button_bg_color='#444444'
# Create a font with your preferred attributes
custom_font = font.Font(family="Segoe UI", size=12, weight="bold")

start_button = Button(root, text="Start Conversation", command=conversation, bg=button_bg_color, fg='white', font=custom_font)
start_button.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

root.configure(bg='black')

root.mainloop()
