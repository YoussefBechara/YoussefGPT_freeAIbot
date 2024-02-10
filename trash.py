import threading
import queue
from tkinter import Tk, Entry, Text, N, S, E, W, END, Button
from tkinter import filedialog
from hugchat import hugchat
from hugchat.login import Login
from bing_image_downloader import downloader
import os
from PIL import Image, ImageTk
from tkinter import Label


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
    response = chatbot.query(text, web_search=True)
    last_response += response
    response_queue.put(response)
    for source in response.web_search_sources:
        response_queue.put(source.link)


def get_image(query,path='images',size='',color='',type='',layout=''):
    downloader.download(query, limit=1, output_dir=path, adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
    



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

def detail(event=None):
    message = f"Please make this text more detailed: {last_response}"
    input_box.delete(0, END)
    chat_log.config(state='normal')
    chat_log.insert(END, 'You: Detail please' + '\n')
    chat_log.insert(END, 'ChatBot: Detailing...\n')
    chat_log.config(state='disabled')
    threading.Thread(target=ask_hugchat, args=(message,)).start()
    root.after(100, update_chat_log)

def native(event=None):
    message = f"Please make this text sound native speakers: {last_response}"
    input_box.delete(0, END)
    chat_log.config(state='normal')
    chat_log.insert(END, 'You: make it more native please' + '\n')
    chat_log.insert(END, 'ChatBot: Making it sound native...\n')
    chat_log.config(state='disabled')
    threading.Thread(target=ask_hugchat, args=(message,)).start()
    root.after(100, update_chat_log)

def translate(event=None):
    lang = input_box.get()
    message = f"Please translate this text to {lang} language: {last_response}"
    input_box.delete(0, END)
    chat_log.config(state='normal')
    chat_log.insert(END, 'You: Translate please' + '\n')
    chat_log.insert(END, 'ChatBot: Translating...\n')
    chat_log.config(state='disabled')
    threading.Thread(target=ask_hugchat, args=(message,)).start()
    root.after(100, update_chat_log)

def summarize(event=None):
    message = f"Please summarize this text : {last_response}"
    input_box.delete(0, END)
    chat_log.config(state='normal')
    chat_log.insert(END, 'You: Summarize please' + '\n')
    chat_log.insert(END, 'ChatBot: Summarizing...\n')
    chat_log.config(state='disabled')
    threading.Thread(target=ask_hugchat, args=(message,)).start()
    root.after(100, update_chat_log)
def generate_image():
    query = input_box.get()
    input_box.delete(0, END)
    get_image(query=query)

    # Assuming the image is saved with a standard name like 'Image_1.jpg' inside the dynamically named folder
    folder_name = f'images\\{query}'  # Update this to match the actual naming convention
    image_path = os.path.join(folder_name, 'Image_1.jpg')

    try:
        # Load and display the image using Pillow
        image = Image.open(image_path)
        image.thumbnail((300, 300))  # Adjust the size as needed
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo
    except FileNotFoundError:
        print(f"Image not found: {image_path}")

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
from tkinter import messagebox
# from docx import Document

import fitz  # PyMuPDF

def open_file():
    filename = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt'), ('PDF Files', '*.pdf'), ('Word Files', '*.docx')])
    
    if filename:
        content = ""

        if filename.lower().endswith(".txt"):
            with open(filename, 'r') as file:
                content = file.read()
        elif filename.lower().endswith(".pdf"):
            content = read_text_from_pdf(filename)
        elif filename.lower().endswith(".docx"):
            #content = read_text_from_docx(filename)
            pass
        else:
            messagebox.showinfo("Unsupported File", "Unsupported file type. Please select a .txt, .pdf, or .docx file.")
            return

        prompt = input_box.get()
        message = f"{prompt} {content}"

        input_box.delete(0, END)
        chat_log.config(state='normal')
        chat_log.insert(END, 'You: ' + message + '\n')
        chat_log.insert(END, 'ChatBot: Generating...\n')
        chat_log.config(state='disabled')

        threading.Thread(target=ask_hugchat, args=(message,)).start()
        root.after(100, update_chat_log)

def read_text_from_pdf(pdf_path):
    text = ""
    try:
        with fitz.open(pdf_path) as pdf_document:
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                text += page.get_text()
    except Exception as e:
        messagebox.showerror("Error", f"Error reading PDF: {str(e)}")
    return text

# def read_text_from_docx(docx_path):
#     text = ""
#     try:
#         doc = Document(docx_path)
#         for paragraph in doc.paragraphs:
#             text += paragraph.text + '\n'
#     except Exception as e:
#         messagebox.showerror("Error", f"Error reading Word document: {str(e)}")
#     return text

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
input_box.grid(row=1, column=0, columnspan=1, padx=10, pady=10, sticky=N + S + E + W)

send_button = Button(root, text="Send", command=send_message, bg='#4A7A8C', fg='white')
send_button.grid(row=1, column=1, padx=10, pady=10, sticky=N + S + E + W)

copy_button = Button(root, text="Copy", command=copy_to_clipboard, bg='#4A7A8C', fg='white')
copy_button.grid(row=0, column=4, padx=10, pady=10, sticky=N + S + E + W)

native_button = Button(root, text="Native", command=native, bg='#4A7A8C', fg='white')
native_button.grid(row=1, column=4, padx=10, pady=10, sticky=N + S + E + W)

translate_button = Button(root, text="Translate", command=translate, bg='#4A7A8C', fg='white')
translate_button.grid(row=2, column=0, padx=10, pady=10, sticky=N + S + E + W)

detail_button = Button(root, text="Detail", command=detail, bg='#4A7A8C', fg='white')
detail_button.grid(row=2, column=1, padx=10, pady=10, sticky=N + S + E + W)

upload_button = Button(root, text="Upload", command=open_file, bg='#4A7A8C', fg='white')
upload_button.grid(row=1, column=2, padx=10, pady=10, sticky=N + S + E + W)

summarize_button = Button(root, text="Summarize", command=summarize, bg='#4A7A8C', fg='white')
summarize_button.grid(row=2, column=4, padx=10, pady=10, sticky=N + S + E + W)

generate_image_button = Button(root, text="Generate Image", command=generate_image, bg='#4A7A8C', fg='white')
generate_image_button.grid(row=3, column=0, padx=10, pady=10, sticky=N + S + E + W)

image_label = Label(root)
image_label.grid(row=3, column=1, padx=10, pady=10, sticky=N + S + E + W)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=3)


root.bind('<Return>', send_message)

update_chat_log()
root.configure(bg='purple')

chat_log.config(state='normal')
chat_log.insert(END, "Welcome! I'm YoussefGPT, Your personal AI assistant.\n\n")
chat_log.config(state='disabled')

root.mainloop()
