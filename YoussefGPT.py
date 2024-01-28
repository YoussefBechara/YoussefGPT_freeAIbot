import threading
import queue
from tkinter import Tk, Entry, Text, N, S, E, W, END, Button
from hugchat import hugchat
from hugchat.login import Login

response_queue = queue.Queue()
global last_response
last_response = ""

def ask_hugchat(text):
    global last_response
    email= ''
    passwd = ''
    sign = Login(email, passwd)
    cookies = sign.login()
    cookie_path_dir = "./cookies_snapshot"
    sign.saveCookiesToDir(cookie_path_dir)
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    response = chatbot.query(text)
    last_response += response
    response_queue.put(response)

def copy_to_clipboard():  # Get the last response from the chat log
    global last_response
    root.clipboard_clear()  # Clear the clipboard contents
    root.clipboard_append(last_response)  # Append the response to the clipboard
    last_response = ""
    
def send_message(event=None):
    message = input_box.get()
    input_box.delete(0, END)
    chat_log.config(state='normal')
    chat_log.insert(END, 'You: ' + message + '\n')
    chat_log.insert(END, 'ChatBot: Generating...\n')
    chat_log.config(state='disabled')
    threading.Thread(target=ask_hugchat, args=(message,)).start()
    root.after(100, update_chat_log)


def update_chat_log():
    if not response_queue.empty():
        response = response_queue.get()
        chat_log.config(state='normal')
        chat_log.delete('end-2l', 'end-1c')  # Delete the 'Generating...' message
        chat_log.insert(END, 'ChatBot: ' + response + '\n\n\n')  # Add three newlines after the response
        chat_log.see(END)
        chat_log.config(state='disabled')
    root.after(100, update_chat_log)

from tkinter import filedialog

def open_file():
    filename = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if filename:
        with open(filename, 'r') as file:
            content = file.read()
        # Now 'content' contains the text file content as a string
        # You can send 'content' to the chatbot
        prompt = input_box.get()
        message = f"{prompt} {content}"
        # ask_hugchat(message)
        input_box.delete(0, END)
        chat_log.config(state='normal')
        chat_log.insert(END, 'You: ' + message + '\n')
        chat_log.insert(END, 'ChatBot: Generating...\n')
        chat_log.config(state='disabled')
        threading.Thread(target=ask_hugchat, args=(message,)).start()
        root.after(100, update_chat_log)
root = Tk()
root.title('YoussefGPT')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

root_width = int(screen_width * 0.8)
root_height = int(screen_height * 0.8)
root.geometry(f"{root_width}x{root_height}")

# Set the background color of the window
root.configure(bg='#D9D8D7')

chat_log = Text(root, state='disabled', bg='#4A7A8C', fg='white')
chat_log.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=N + S + E + W)

input_box = Entry(root, width=root_width-root_width//2, borderwidth=5, bg='#4A7A8C', fg='white')
input_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky=N + S + E + W)

send_button = Button(root, text="Send", command=send_message, bg='#4A7A8C', fg='white')
send_button.grid(row=1, column=1, padx=10, pady=10, sticky=N + S + E + W)

copy_button = Button(root, text="Copy", command=copy_to_clipboard, bg='#4A7A8C', fg='white')
copy_button.grid(row=1, column=2, padx=10, pady=10, sticky=N + S + E + W)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)

root.bind('<Return>', send_message)

upload_button = Button(root, text="Upload", command=open_file, bg='#4A7A8C', fg='white')
upload_button.grid(row=1, column=3, padx=10, pady=10, sticky=N + S + E + W)

update_chat_log()
root.configure(bg='purple')

chat_log.config(state='normal')
chat_log.insert(END, "Welcome! I'm YoussefGPT, Your personal AI assistant.\n\n")
chat_log.config(state='disabled')

root.mainloop()
