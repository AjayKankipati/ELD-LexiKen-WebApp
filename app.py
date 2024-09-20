from tkinter import *
from PIL import ImageTk, Image
import os
from generateImage import UrlGen, getImage
from generateVocab import VocabGenerator
from translate import LangTranslator
from io import BytesIO
import requests 
import webbrowser
from supported_langs import LANGUAGES,d
import time
from tkinter import ttk
import random
from gtts import gTTS
import pygame
import sys
# from progress import ProgressModule

# pmd = ProgressModule()

pygame.mixer.init()
#UNCOMMENT BOTTOM TWO LINES FOR WEB DEPLOYMENT
#import win32com.client
#VirtualUI = win32com.client.Dispatch("Thinfinity.VirtualUI")



initial_x = 0
initial_y = 0
window = Tk()
w = Canvas(window, width=1920, height=1080)
w.pack()
window.title('ELD App')


known_lang = "spanish"
native_lang = LANGUAGES[known_lang]


#Initialize module tools
urlGen = UrlGen()
translator = LangTranslator()
#vocabGen = VocabGenerator("EL1", pmd)
vocabGen = VocabGenerator("EL1")


oframe = Frame(window, bg= "orange")
oframe.pack(side=LEFT)
oframe.pack_propagate(False)
oframe.configure(width=200,height=1080)
oframe.place(x=0,y=0)
    
    
def on_button_press(event):
    # Remember the starting position of the button
    button = event.widget
    button.drag_data = {'x': event.x, 'y': event.y}
    

correct_guesses = 0
wrong_guesses = 0
num_overlaps = 0
def on_button_motion(event):
    
    # Calculate the distance moved
    button = event.widget
    dx = event.x - button.drag_data['x']
    dy = event.y - button.drag_data['y']
    
    if is_matched[button_names.index(button._name)]:
        img = matched_images[button_names.index(button._name)]
        x = img.winfo_x() + (img.winfo_width() / 2) - (button.winfo_width() / 2)
        y = img.winfo_y() + (img.winfo_height() / 2) - (button.winfo_height() / 2)
        button.place(x=x,y=y)
    else:
        button.place(x=button.winfo_x() + dx, y=button.winfo_y() + dy)
    
def convertUrlToButtonImage(url, x, y):
    
    #return to oringal spot after an incomplete move
    
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    
    photo = ImageTk.PhotoImage(img)
    button = Button(practice_frame)
    button.configure(image = photo)
    button.image = photo
    image_names.append(button._name)
    button.place(x = x, y = y)
    buttons.append(button)
    curr_game_elements.append(button)
    

    # Bind the button motion event to move the button
    #button.bind('<B1-Motion>', on_button_motion)
    #^DONT DELETE MIGHT NEED LATER
    button.config(highlightbackground="purple", highlightthickness=3)

    translate_buttons.append(None)
    is_destroyed.append(True)

   
def check_button_overlap(button1, button2):
    # Get the position and size of button1
    x1 = button1.winfo_x()
    y1 = button1.winfo_y()
    width1 = button1.winfo_width()
    height1 = button1.winfo_height()

    # Get the position and size of button2
    x2 = button2.winfo_x()
    y2 = button2.winfo_y()
    width2 = button2.winfo_width()
    height2 = button2.winfo_height()

    # Calculate the overlapping rectangle
    x_overlap = max(0, min(x1 + width1, x2 + width2) - max(x1, x2))
    y_overlap = max(0, min(y1 + height1, y2 + height2) - max(y1, y2))

    # Calculate the area of button1
    area1 = width1 * height1

    # Calculate the overlapping area
    overlap_area = x_overlap * y_overlap

    # Check if the overlapping area is greater than 50% of button1's area
    if overlap_area > 0.2 * area1:
        return True
    else:
        return False

#words = ['cat', 'tree', 'stairs', 'computer', 'apple']
# check to see if button is clicked(prints out the word corresponding to that button)
def button_Clicked():
    d = 0



practice_frame = Frame(window,highlightbackground='black',highlightthickness=3)
practice_frame.pack(side = LEFT)
practice_frame.pack_propagate(False)
practice_frame.configure(width=1720, height=1080)


    

def on_button_release(event):
    
    button = event.widget
    isImage = False
    try:
        z = button.image
        isImage = True
        if is_matched[image_names.index(button._name)]:
            return
    except:
        isImage = False
        if is_matched[button_names.index(button._name)]:
            return

     # Check for overlap with other buttons
    for other_button in buttons:
        other_isImage = False
        try:
            z = other_button.image
            other_isImage =True
        except:
            other_isImage = False
        if isImage and other_isImage:
            continue
        global wrong_guesses
        global correct_guesses
        if other_button != button and (check_button_overlap(button, other_button) or check_button_overlap(other_button, button)):

                if isImage and not other_isImage:
                    if(button_names.index(other_button._name)!=image_names.index(button._name)):
                        #other_button.config(highlightbackground="#FF0000", highlightthickness=3)
                        wrong_guesses = wrong_guesses + 1
                        #pmd.set_accuracy(words[button_names.index(other_button._name)], 5, 0 , 1)
                        continue
                else:
                    if(button_names.index(button._name)!=image_names.index(other_button._name)):
                        #other_button.config(highlightbackground="#FF0000", highlightthickness=3)
                        wrong_guesses = wrong_guesses + 1
                        #pmd.set_accuracy(words[button_names.index(button._name)], 5,  0, 1)
                        continue
                
                # Create a Text widget
                #text_widget = Text(window, height=40, width=50)
                # Add text to the Text widget
                
                #text_widget.insert(END, "OVERLAPPED")
                # Disable editing in the Text widget
                #text_widget.configure(state='disabled') 
                #text_widget.place(x = 500, y = 500)
                
                #put text on top of image
                
                if other_isImage:
                    is_matched[button_names.index(button._name)] = True
                    matched_images[button_names.index(button._name)] = other_button
                    other_button.config(highlightbackground="#00FF00", highlightthickness=3)
                    button.config(highlightbackground="#00FF00", highlightthickness=3)
                    correct_guesses += 1
                    #pmd.set_accuracy(words[button_names.index(button._name)], 5, 1 , 0)
                    

                else:
                    is_matched[button_names.index(other_button._name)] = True
                    matched_images[button_names.index(other_button._name)] = button
                    button.config(highlightbackground="#00FF00", highlightthickness=3)
                    other_button.config(highlightbackground="#00FF00", highlightthickness=3)
                    correct_guesses += 1
                    #pmd.set_accuracy(words[button_names.index(other_button._name)], 5, 1, 0)
                    
                #text_widget1 = Text(window, height = 1, width = x_width)
                #text_widget1.insert(END, "cat")
                #text_widget1.configure(state='disabled')
                     
                #print(x_image)
                #print(y_image)
                #y_image = y_image - 20
                
                #text_widget1.place(x = x_image, y = y_image)
                #global num_overlaps
                #num_overlaps = num_overlaps + 1
                #print("overlap " + str(num_overlaps))
                #other_button.pack_forget()
                #button.pack_forget()
                
        if correct_guesses==5:
            print(correct_guesses)
            print(wrong_guesses)
            correct_guesses=0
            wrong_guesses=0

        x,y = button_original_positions[button_names.index(button._name)]

    if not is_matched[button_names.index(button._name)]:
        button.place(x=x,y=y)
    else:
        img = matched_images[button_names.index(button._name)]
        x = img.winfo_x() + (img.winfo_width() / 2) - (button.winfo_width() / 2)
        y = img.winfo_y() + (img.winfo_height() / 2) - (button.winfo_height() / 2)
        button.place(x=x,y=y)


def add_button(x,y, word):
    global translated_words
    translated_words.append(translator.translate_to_native(word,native_lang))
    vocab_word = Button(practice_frame, text=word, command=button_Clicked(), font=('Prophet 15'), highlightbackground="purple", highlightthickness=1)
    button_names.append(vocab_word._name)
    word_buttons.append(vocab_word)
    is_matched.append(False)
    vocab_word.place(x = x, y = y)
    curr_game_elements.append(vocab_word)
    button_original_positions.append((x,y))
    matched_images.append(None)
    # Bind the vocab_word button press event to start dragging
    vocab_word.bind('<ButtonPress-1>', on_button_press)
    vocab_word.bind("<ButtonRelease-1>", on_button_release)
    # Bind the vocab_word button motion event to move the button
    vocab_word.bind('<B1-Motion>', on_button_motion)

def add_button_lock(x,y, word):
    #adds buttons that can't move
    global translated_words
    translated_words.append(translator.translate_to_native(word,native_lang))
    vocab_word = Button(practice_frame, text=word, command=button_Clicked(), font=('Prophet 15'), highlightbackground="purple", highlightthickness=1)
    button_names.append(vocab_word._name)
    word_buttons.append(vocab_word)
    is_matched.append(False)
    vocab_word.place(x = x, y = y)
    curr_game_elements.append(vocab_word)
    button_original_positions.append((x,y))
    matched_images.append(None)
    # Bind the vocab_word button press event to start dragging
    #vocab_word.bind('<ButtonPress-1>', on_button_press)
    #vocab_word.bind("<ButtonRelease-1>", on_button_release)
    # Bind the vocab_word button motion event to move the button
    #vocab_word.bind('<B1-Motion>', on_button_motion)






search_frame = Frame(window,highlightbackground='black',highlightthickness=3)
search_frame.pack(side = LEFT)
search_frame.pack_propagate(False)
search_frame.configure(width=1720, height=1080)
label1 = Label(search_frame, text = "Enter word here",font=('Arial 10'),bg='blue')
label1.place(x=115, y= 20)
enter_box = Entry(search_frame,width = 25)
enter_box.place(x=220,y=20)

sets_frame = Frame(window,highlightbackground='black',highlightthickness=3)
sets_frame.pack(side = LEFT)
sets_frame.pack_propagate(False)
sets_frame.configure(width=1720, height=1080)
label2 = Label(sets_frame, text = "SETS PAGE",font=('Arial 20'))
label2.place(x=250, y= 20)

progress_frame = Frame(window,highlightbackground='black',highlightthickness=3)
progress_frame.pack(side = LEFT)
progress_frame.pack_propagate(False)
progress_frame.configure(width=1720, height=1080)
label3 = Label(progress_frame, text = "Progress PAGE",font=('Arial 20'))
label3.place(x=115, y= 20)



def search():
    search_word = enter_box.get()
    global word_to_speak
    word_to_speak = search_word
    play_word()
    if search_word == '':
        return
    native_trans =  translator.translate_to_english(search_word, native_lang)
    url = getImage([native_trans])[0]
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    
    photo = ImageTk.PhotoImage(img)
    trans_image = Button(search_frame)
    trans_image.configure(image = photo)
    trans_image.image = photo
    trans_word = ttk.Button(search_frame, text=native_trans)
    trans_image.place(x=500, y=400)
    trans_word.place(x=600, y=400)

search_button = Button(search_frame, text = "Search", command= search, background="#00FF00", foreground = "#4B0082", font=('Arial 10'))
search_button.place(x=450, y= 20)

home_frame = Frame(window,highlightbackground='black',highlightthickness=3)
home_frame.pack(side = LEFT)
home_frame.pack_propagate(False)
label = ttk.Label(home_frame, text="LexiKen", font=('Prophet 30'),foreground = "#4B0082")
label.place(x=200, y= 50)
home_frame.configure(width=1720, height=1080)
label = ttk.Label(home_frame, text="LexiKen is an innovative learning platform dedicated to supporting\nEnglish Language Learners on their path to success!\nLanguage learning should be a fun and empowering\nexperience which is why our user-friendly platform\n provides a simple and welcoming environment. Regardless\nof where you are in your learning journey, join our\nsupportive community and embark on a transformative\njourney for your English proficiency. Together, let’s make\n(our tagline)", font=('Prophet 15'),foreground = "#4B0082")
label.place(x=200, y= 100)


def on_selection_change(selection):
    selected_language = clicked.get()
    print(selected_language)
    global native_lang
    native_lang = LANGUAGES[selected_language]
    
    
clicked = StringVar()
clicked.set("Select Native Language")
language_selector = OptionMenu(home_frame,clicked,*LANGUAGES, command=on_selection_change)
language_selector.place(x=800, y= 100)



def search_page():
    search_frame.tkraise()
    search_frame.place(x=200,y=0)
    
def exercises_page():
    #practice_frame.tkraise()
    #practice_frame.place(x=200,y=0)
    practice_frame.tkraise()
    practice_frame.place(x=200,y=0)

def home_page():
    home_frame.tkraise()
    home_frame.place(x=200,y=0)

def sets_page():
    sets_frame.tkraise()
    sets_frame.place(x=200,y=0)

def progress_page():
    sets_frame.tkraise()
    sets_frame.place(x=200,y=0)


home_label = Button(oframe,text="Home",font=('Arial 20'), command=home_page)
home_label.place(x=50,y=200)
# search_label = Button(oframe,text="Search",font=('Arial 20'), command=search_page)
# search_label.place(x=50,y=300)
# sets_label = Button(oframe,text="Sets",font=('Arial 20'), command=sets_page )
# sets_label.place(x=50,y=400)
# exercises_label = Button(oframe,text="Exercises",font=('Arial 20'), command=exercises_page)
# exercises_label.place(x=50,y=500)
# progress_label = Button(oframe,text="Progress",font=('Arial 20'), command=progress_page)
# progress_label.place(x=50,y=600)
exercises_label = Button(oframe,text="Exercises",font=('Arial 20'), command=exercises_page)
exercises_label.place(x=50,y=300)

button_names = []
translate_buttons = []
button_original_positions = []
is_matched = []
matched_images = []
is_destroyed = []
buttons = []
word_buttons = []
translated_words = []
image_names = []


"""
def next_game():
    t1 = time.time()
    global button_names
    global translate_buttons
    global button_original_positions
    global is_matched
    global matched_images
    global is_destroyed
    global buttons
    global word_buttons
    global image_names
    global translated_words

    for button in buttons:
        button.destroy()
    for button in word_buttons:
        button.destroy()
        
    button_names = []
    translate_buttons = []
    button_original_positions = []
    is_matched = []
    matched_images = []
    is_destroyed = []
    buttons = []
    image_names = []
    word_buttons = []
    translated_words = []

    words = vocabGen.generateWords(5)
    t2 = time.time()
    print("Time Interval 1: " + str(t2-t1))
    urls = urlGen.getImage(words)

    
    x=0
    for url in urls:
        x = x + 200
        convertUrlToButtonImage(url, x, 200)

    t3 = time.time()
    print("Time Interval 2: " + str(t3-t2))

    #loop through the list of generated words and places each as a button
    z = [225,425,625,825,1025]

    for word in words:
        random_index = random.randint(0, len(z) - 1)
        # Access the value at the random index
        selected_value = z[random_index]
        # Remove the selected value from the array
        del z[random_index]
        add_button(selected_value,125, word)
    t4 = time.time()
    print("Time Interval 3: " + str(t4-t3))

    def on_button_flipped(event):
        button = event.widget
        if is_destroyed[image_names.index(button._name)]:
            txt = translated_words[image_names.index(button._name)]
            translate_button = Button(practice_frame, text=txt, font=('Arial 15'),highlightbackground='purple',highlightthickness=1)
            x = button.winfo_x()
            y = button.winfo_y()
            translate_button.place(x=x, y=y)
            translate_button.after(800, translate_button.destroy)
            
            translate_buttons[image_names.index(button._name)] = translate_button
            is_destroyed[image_names.index(button._name)] = False
    for button in buttons:
        button.bind('<ButtonPress-1>', on_button_flipped)
"""

word_to_speak = ""
p = 0
def play_word():
    global p
    tts = gTTS(word_to_speak)
    base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, 'tmp' + str(p) + '.mp3')
    tts.save(audio_path)
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(loops=0)
    p = p + 1
    if p > 1:
        p = 0



selected_image1_game5 = 0 
def play_word_game5():
    global p
    tts = gTTS(words[correct_word_index1])
    base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    audio_path = os.path.join(base_dir, 'tmp' + str(p) + '.mp3')
    tts.save(audio_path)
    pygame.mixer.music.load(audio_path)
    pygame.mixer.music.play(loops=0)
    p = p + 1
    if p > 1:
        p = 0

correct_button_game5 = ""
def convertUrlToButtonImage_game5(url, x, y, flag):
    
    
    #return to oringal spot after an incomplete move
    
    response = requests.get(url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    
    photo = ImageTk.PhotoImage(img)
    button = Button(practice_frame)
    button.configure(image = photo)
    button.image = photo
    image_names.append(button._name)

    button.place(x = x, y = y)
    buttons.append(button)
    curr_game_elements.append(button)

    # Bind the button motion event to move the button
    #button.bind('<B1-Motion>', on_button_motion)
    #^DONT DELETE MIGHT NEED LATER
    button.config(highlightbackground="purple", highlightthickness=3)

    translate_buttons.append(None)
    is_destroyed.append(True)

    # Bind the button motion event to move the button
    #button.bind('<B1-Motion>', on_button_motion)
    #^DONT DELETE MIGHT NEED LATER
    button.config(highlightbackground="purple", highlightthickness=3)
    
    button.bind('<ButtonPress-1>', on_button_press)
    button.bind('<ButtonRelease-1>', on_button_release_game5)
    
    translate_buttons.append(None)
    is_destroyed.append(True)
    button.bind("")
    
    if flag: 
        global correct_button_game5
        correct_button_game5 = button._name
        print("Flagged: " + correct_button_game5)
    
    
#need this to work
#def remove_button_border():
    #button.configure(highlightbackground="purple", highlightthickness=3)

def change_button_color(button):
    button.configure(highlightbackground="purple", highlightthickness=3)


def on_button_release_game5(event):
    
    button = event.widget
    print(button._name)
    print("hi")
    print(correct_button_game5)
    if button._name == correct_button_game5:
        #pmd.set_accuracy(words[correct_word_index1], 5,  1, 0)
        button.config(highlightbackground="#00FF00", highlightthickness=3)
        label = Label(practice_frame, text = "Well done!",font=('Arial 50'), borderwidth=2, relief="solid")
        label.place(x=750, y= 600)
        label.after(2500, label.destroy)
    else:
        #pmd.set_accuracy(words[correct_word_index1], 5,  0, 1)
        #print("hello 1")
        button.config(highlightbackground="green")
        
    print(button._name)   
    #words[selected_image1_game5] """
    


def enter1():
    if enter_box1.get()==words[correct_word_index]:
        #pmd.set_accuracy(words[correct_word_index], 5,  1, 0)        
        next_game1()
    else:
        #pmd.set_accuracy(words[correct_word_index], 5,  0, 1)
        v = 0
        
def next_game1():
    global word_to_speak
    enter_box1.delete(0, END)
    label = Label(practice_frame, text = "Well done!",font=('Arial 50'), borderwidth=2, relief="solid")
    label.place(x=750, y= 600)
    label.after(2500, label.destroy)
    #word = vocabGen.generateWords(1)
    answer = words[correct_word_index]
    next_exercise_tracker = 3

def enter2():
    if enter_box2.get()==words[random_word2]:
        #pmd.set_accuracy(words[random_word2], 5,  1, 0)        
        next_game2()
    else:
        #pmd.set_accuracy(words[random_word2], 5,  0, 1)
        v=0
        
def next_game2():
    global word_to_speak
    enter_box2.delete(0, END)
    label = Label(practice_frame, text = "Well done!",font=('Arial 50'), borderwidth=2, relief="solid")
    label.place(x=750, y= 600)
    label.after(2500, label.destroy)
    #word = vocabGen.generateWords(1)
    answer = words[random_word2]


progress_value = 0
progress = ttk.Progressbar(practice_frame, orient="horizontal", length=200, mode="determinate")
progress.place(x = 800, y = 500)
progress_label = Label(practice_frame, text="Progress Bar: " + str(progress_value) + "%")
progress_label.place(x = 800, y = 520)

def update_progress():
    global progress_value
    # global progress
    progress_value += 20
    if progress_value > 100:
        progress_value = 100
    progress['value'] = progress_value
    progress_label.config(text="Progress Bar: " + str(progress_value) + "%")
    

def reset_progress():
    global progress_value
    progress['value'] = 0
    progress_value = 0
    progress_label.config(text="Progress Bar: " + str(progress_value) + "%")
    
next_exercise_tracker = 0
curr_game_elements = []

words = []
urls = []
def next_exercise():
    global urls
    global words
    
    global curr_game_elements
    #matching game exercise
    global next_exercise_tracker
    # Create a progress bar
    if next_exercise_tracker == 0:
        reset_progress()
        words = vocabGen.generateWords(5)
        urls = urlGen.getImage(words)
        for element in curr_game_elements:
            element.destroy()
        curr_game_elements = []
        global audio_enter_box
        audio_enter_box = Entry(practice_frame,width = 25, highlightbackground = "purple",highlightthickness=3)
        audio_enter_box.place(x=350,y=300)
        audio_enter_box.focus_set()
        global hear_word_button
        hear_word_button = Button(practice_frame, text="Hear Word", command=play_word)
        global word_to_speak
        word_to_speak = words[random.randint(0, 4)]
        def enter():
            if audio_enter_box.get() == word_to_speak:
                #pmd.set_accuracy(word_to_speak, 5,  1, 0)
                def next_game():
                    global word_to_speak
                    audio_enter_box.delete(0, END)
                    #word = vocabGen.generateWords(1)
                    word_to_speak = words[random.randint(0, 4)]
                
                label = Label(practice_frame, text = "Well done!",font=('Arial 50'), borderwidth=2, relief="solid")
                label.place(x=750, y= 600)
                label.after(2500, label.destroy)
                
            else:
                #pmd.set_accuracy(word_to_speak, 5,  0, 1)
                v = 0
        hear_word_button.place(x=220,y=300)
        global submit_button
        submit_button = Button(practice_frame, text = "Check", command= enter, background="#00FF00", foreground = "#4B0082", font=('Arial 10'))
        submit_button.place(x=600, y= 300)
        curr_game_elements.append(audio_enter_box)
        curr_game_elements.append(hear_word_button)
        curr_game_elements.append(submit_button)

    elif next_exercise_tracker == 1:
        update_progress()
        print('lol')
        for element in curr_game_elements:
            element.destroy()
        curr_game_elements = []
        label1 = Label(practice_frame, text="Match The Word To It's Correct Image!", font=('Prophet 30'),foreground = "#4B0082")
        label1.place(x=450, y= 50)
        curr_game_elements.append(label1)
        t1 = time.time()
        global button_names
        global translate_buttons
        global button_original_positions
        global is_matched
        global matched_images
        global is_destroyed
        global buttons
        global word_buttons
        global image_names
        global translated_words

        button_names = []
        translate_buttons = []
        button_original_positions = []
        is_matched = []
        matched_images = []
        is_destroyed = []
        buttons = []
        image_names = []
        word_buttons = []
        translated_words = []

        t2 = time.time()
        print("Time Interval 1: " + str(t2-t1))
        
        x=0
        for url in urls:
            x = x + 200
            convertUrlToButtonImage(url, x, 200)

        t3 = time.time()
        print("Time Interval 2: " + str(t3-t2))


        #loop through the list of generated words and places each as a button
        global z
        z = [225,425,625,825,1025]

        for word in words:
            random_index = random.randint(0, len(z) - 1)
            # Access the value at the random index
            selected_value = z[random_index]
            # Remove the selected value from the array
            del z[random_index]
            add_button(selected_value,125, word)
        t4 = time.time()
        print("Time Interval 3: " + str(t4-t3))

        def on_button_flipped(event):
            button = event.widget
            if is_destroyed[image_names.index(button._name)]:
                txt = translated_words[image_names.index(button._name)]
                translate_button = Button(practice_frame, text=txt, font=('Arial 15'),highlightbackground='purple',highlightthickness=1)
                x = button.winfo_x()
                y = button.winfo_y()
                translate_button.place(x=x, y=y)
                translate_button.after(800, translate_button.destroy)
                
                translate_buttons[image_names.index(button._name)] = translate_button
                is_destroyed[image_names.index(button._name)] = False
        for button in buttons:
            button.bind('<ButtonPress-1>', on_button_flipped)
        
    #getting rid of the matching game and creating new game (writing correct english word based on picture)
    if next_exercise_tracker == 2:
        update_progress()
        for element in curr_game_elements:
            element.destroy()
        curr_game_elements = []

        global arr 
        arr = [0,1,2,3,4]

        global correct_word_index

        global b
        
        b = 400
        random_valueee = random.randint(0,2)
        print(random_valueee)
        global countt
        countt = 0
        print(countt)
        for i in range(3):
            j = random.choice(arr)
            if countt ==random_valueee:
                correct_word_index = j
            add_button_lock(b, 200, words[j])
            
            del arr[arr.index(j)]
            b = b+100
            countt = countt+1
            print(countt)
        convertUrlToButtonImage(urls[correct_word_index], 200, 200)
        
        global enter_box1
        enter_box1 = Entry(practice_frame,width = 25, highlightbackground = "purple",highlightthickness=3)
        enter_box1.focus_set()  # Set the focus to the button
        enter_box1.place(x=400,y=275)
        curr_game_elements.append(enter_box1)
        instruction_label = Label(practice_frame, text="Type the correct word that corresponds to the image")
        instruction_label.place(x=250,y=150)
        curr_game_elements.append(instruction_label)
        global submit_button1
        submit_button1 = Button(practice_frame, text = "Check", command= enter1, background="#00FF00", foreground = "#4B0082", font=('Arial 10'))
        submit_button1.place(x=650,y=275)
        curr_game_elements.append(submit_button1)

    elif next_exercise_tracker == 3:
        update_progress()
        #translating native word to english excersize
        #delete enter_box1, submit_button1, and word choices, and image
        for element in curr_game_elements:
            element.destroy()
        curr_game_elements = []
        global random_word2
        random_word2 = random.randint(0, 4)
        native_trans1 = translator.translate_to_native("How do you say '" + words[random_word2] + "' in english?", native_lang)
        print(native_trans1)
        native_to_english_label = Label(practice_frame, text = native_trans1,font=('Arial 25'), borderwidth=1, relief="groove")
        native_to_english_label.place(x=200, y= 200)
        curr_game_elements.append(native_to_english_label)

        global enter_box2
        enter_box2 = Entry(practice_frame,width = 25, highlightbackground = "purple",highlightthickness=3)
        enter_box2.focus_set()
        enter_box2.place(x=775,y=200)
        curr_game_elements.append(enter_box2)
        global submit_button2
        submit_button2 = Button(practice_frame, text = "Check", command= enter2, background="#00FF00", foreground = "#4B0082", font=('Arial 10'))
        submit_button2.place(x=1050,y=200)
        curr_game_elements.append(submit_button2)
        global a
        a = [250,400,550,700,850]
        for word in words:
            random_index = random.randint(0, len(a) - 1)
            # Access the value at the random index
            selected_value = a[random_index]
            # Remove the selected value from the array
            del a[random_index]
            add_button_lock(selected_value,275, word)

    
    elif next_exercise_tracker == 4:
        update_progress()
        #audio to image matching game: says audio of word and user has to choose 1 image of 3
        #selected_image1_game5 is the correct answer
        for element in curr_game_elements:
            element.destroy()
        curr_game_elements = []


        global count1
        count1 = 0

        global randval
        randval = random.randint(0,2)
        global arr1 
        arr1 = [0,1,2,3,4]

        global correct_word_index1
        correct_word_index1  = randval
        global b1
        global c
        b1 = 250

        for i in range(3):
            if i == randval:
                convertUrlToButtonImage_game5(urls[i], b1, 300, True)
            else: 
                convertUrlToButtonImage_game5(urls[i], b1, 300, False)
            b1 = b1+200


        hear_word_button_game5 = Button(practice_frame, text="Hear Word", font=('Arial 15'),command=play_word_game5)
        hear_word_button_game5.place(x=850,y= 400)
        curr_game_elements.append(hear_word_button_game5)
        
    
    elif next_exercise_tracker == 5:
        update_progress()
        for element in curr_game_elements:
            element.destroy()
        curr_game_elements = []
        
        complete_label = Label(practice_frame, text="Set is Complete", font=('Arial 50'), borderwidth=2, relief="solid")
        complete_label.place(x = 350, y = 400)
        curr_game_elements.append(complete_label)
    
    next_exercise_tracker = next_exercise_tracker + 1
    if next_exercise_tracker > 5:
        next_exercise_tracker = 0
    
    print(words)
        
home_page()
new_exercise_button = Button(practice_frame, text="New exercise", command = next_exercise, font=('Arial 15'),highlightbackground="gold", highlightthickness=3)
new_exercise_button.place(x=120,y=600)
next_exercise()



#UNCOMMENT BOTTOM LINE FOR WEB DEPLOYMENT
#VirtualUI.Start (60)



window.mainloop()

#end

