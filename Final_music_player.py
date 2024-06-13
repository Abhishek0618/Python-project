from tkinter import *
from tkinter import Scale
import tkinter.messagebox
import os
from tkinter import filedialog  # open window from where we select music
from pygame import mixer  # Import mixer module for music playing 
from mutagen.mp3 import MP3  # for song length
import time

mixer.init()

class MusicPlayer:
    def __init__(self, window):
        self.window = window
        self.window.title("Music Player")
        self.window.geometry('700x500')
        self.window.configure(bg='black')

        # Initialize the paused variable
        self.paused = False

        # Openfile function:
        def Openfile():
            global filename
            filename = filedialog.askopenfilename()
            songinf()

        # Menu:
        self.menubar = Menu(self.window)
        self.window.configure(menu=self.menubar)

        self.submenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='File', menu=self.submenu)
        self.submenu.add_command(label='Open', command=Openfile)
        self.submenu.add_command(label='Exit', command=self.window.destroy)

        def About():
            tkinter.messagebox.showinfo('About Us', 'Music player Created by Abhishek')

        self.submenu2 = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label='Help', menu=self.submenu2)
        self.submenu2.add_command(label='About', command=About)

        # Adding Label:
        self.filelabel = Label(window, text='Select And Play', bg='white', font=('Arial', 20, 'bold italic'))
        self.filelabel.place(x=10, y=10)

        def songinf():
            if 'filename' in globals():
                self.filelabel['text'] = 'Current Music :-' + os.path.basename(filename)

        # Adding leftside image:
        self.photo2 = PhotoImage(file='image22.png')
        self.photo = Label(self.window, image=self.photo2, bg='black')
        self.photo.place(x=200, y=80, width=800, height=200)

        # Adding image:
        self.photo1 = PhotoImage(file='main11.png')
        self.photo_label = Label(self.window, image=self.photo1, bg='black', fg='teal')
        self.photo_label.place(x=0, y=50)

        # Label:
        self.label1 = Label(self.window, text='Let\'s make it', bg='white', font=('Arial', 20, 'bold'))
        self.label1.pack(side=BOTTOM, fill=X)

        # Function to play music:
        def play_music():
            try:
                if self.paused:
                    mixer.music.unpause()
                    self.label1['text'] = 'Music Unpaused'
                else:
                    mixer.music.load(filename)
                    mixer.music.play()
                    self.label1['text'] = 'Music Playing...'
                    songinf()
                    length_bar()
                    self.im1 = PhotoImage(file='ani11.png')
                    self.im2 = PhotoImage(file='ani22.png')
                    self.im3 = PhotoImage(file='ani33.png')
                    self.im4 = PhotoImage(file='ani44.png')

                    self.imglabel = Label(self.window, text='', bg='black')
                    self.imglabel.place(x=430, y=50)
                    animation()
                self.paused = False
            except Exception as e:
                tkinter.messagebox.showerror('Error', f'File Could Not Be Found, Please Try Again. \n{str(e)}')

        # for song length:
        def length_bar():
            if 'filename' in globals():
                # starting from zero
                current_time = mixer.music.get_pos() / 1000

                # convert current time in min.. and sec...
                convert_current_time = time.strftime('%M:%S', time.gmtime(current_time))

                # select mp3 songs
                song_mut = MP3(filename)
                # get length of songs
                song_mut_length = song_mut.info.length
                # convert into min. and sec
                convert_song_mut_length = time.strftime('%M:%S', time.gmtime(song_mut_length))
                # blit on screen
                self.lengthbar.config(text=f'Total Length: {convert_current_time} / {convert_song_mut_length}')
                self.lengthbar.after(1000, length_bar)

        # label for length bar
        self.lengthbar = Label(self.window, text='Total Length: 00:00 / 00:00', font=('Arial', 15))
        self.lengthbar.place(x=10, y=325)

        # Creating play button:
        self.play_button = PhotoImage(file='play1.png')
        self.play_button1 = Button(self.window, image=self.play_button, bd=0, bg='black', borderwidth=0, command=play_music)
        self.play_button1.place(x=20, y=360, width=60, height=60)

        # Function for pause button:
        def pause_button():
            self.paused = True
            mixer.music.pause()
            self.label1['text'] = 'Music Paused'

        # Creating pause button:
        self.pause_button = PhotoImage(file='pause1.png')
        self.pause_button2 = Button(self.window, image=self.pause_button, bd=0, bg='black', borderwidth=0, command=pause_button)
        self.pause_button2.place(x=90, y=360, width=60, height=60)

        # Function for stop button:
        def stop_music():
            mixer.music.stop()
            self.label1['text'] = 'Music Stopped'

        # Creating stop button:
        self.stop_button = PhotoImage(file='stop1.png')
        self.stop_button2 = Button(self.window, image=self.stop_button, bd=0, bg='black', borderwidth=0, command=stop_music)
        self.stop_button2.place(x=160, y=360, width=60, height=60)

        # Animation:
        def animation():
            self.im1, self.im2, self.im3, self.im4 = self.im2, self.im3, self.im4, self.im1
            self.imglabel.config(image=self.im1)
            self.imglabel.after(1000, animation)

        # Function for mute button:
        def mute():
            mixer.music.set_volume(0)
            self.mute_button.config(command=unmute, image=self.mute_image)
            self.label1['text'] = 'Music Muted'

        # Function for unmute button:
        def unmute():
            mixer.music.set_volume(self.scale.get() / 100)
            self.mute_button.config(command=mute, image=self.volume_label)
            self.label1['text'] = 'Music Unmuted'

        # Function for volume control:
        def volume(vol):
            volume_level = int(vol) / 100
            mixer.music.set_volume(volume_level)

        # Creating volume button:
        self.volume_label = PhotoImage(file='volume.png')
        self.mute_image = PhotoImage(file='mute.png')
        self.mute_button = Button(self.window, image=self.volume_label, bd=0, bg='black', borderwidth=0, command=mute)
        self.mute_button.place(x=310, y=370, width=40, height=40)

        # Creating volume bar:
        self.scale = Scale(self.window, from_=0, to=100, orient=HORIZONTAL, bg='skyblue', length=150, command=volume)
        self.scale.set(25)
        self.scale.place(x=360, y=370)

# Run the application
window = Tk()
obj = MusicPlayer(window)
window.mainloop()