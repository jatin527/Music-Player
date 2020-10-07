import os
from tkinter import *
from pygame import mixer
import tkinter.messagebox
import threading
from tkinter import filedialog
from mutagen.mp3 import MP3
import webbrowser
import time
from tkinter import ttk

mixer.init()
root = Tk()

root.title("JBR Music Player")
root.iconbitmap(r'Images/music.ico')
root.configure(background="cyan")

statusbar = Label(root,text="Please select a song to play",background='cyan',font=('Comic Sans MS',11))
statusbar.pack()
statusbar1 = Label(root,text="Total Time : --:--",background='cyan',font=('Comic Sans MS',11))
statusbar1.pack()
statusbar2 = Label(root,text="Current Time : --:--",background='cyan',font=('Comic Sans MS',11))
statusbar2.pack()

playlist=[]
ptr=FALSE

def browse_song():
    try:
        global file_location,filename,played
        played=1
        file_location = filedialog.askopenfile()
        filename=os.path.basename(file_location.name)
        add_to_playlist(filename)
    except:
        pass

def about_us():
    tkinter.messagebox.showinfo("Credits","This musicplayer is created by Rajat Sran, Jatin Singal and Bhavya Narang")

def add_to_playlist(f):
    global playlistbox
    fl=os.path.basename(f)
    playlistbox.insert(0,fl)
    playlist.insert(0,f)

def del_song():
    try:
        global play_song
        select_song = playlistbox.curselection()
        ss = int(select_song[0])
        playlistbox.delete(ss)
        playlist.pop(ss)
        if play_song in playlist:
            pass
        else:
            if len(playlist)==0:
                statusbar['text'] = "Please add a song to play"
            else:
                statusbar['text']="Please select a song from playlist to play"
            statusbar1['text']="Total Time : 00:00"
            stop_music()
    except:
        pass

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open", command=browse_song)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)





helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About...", command=about_us)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)

jai=10

def file_detail(song):  #shows details like total time , current time and which song is playing now
    global b,jai,tt
    statusbar['text'] = "Now Playing : " + song
    extension=os.path.splitext(song)
    if extension[1]==".mp3":
        audio=MP3(song)
        b=audio.info.length
    else:
        a=mixer.Sound(song)
        b=a.get_length()
    min,sec=divmod(b,60)
    tt='{:02d}:{:02d}'.format(round(min),round(sec))
    statusbar1['text']="Total Time -"+tt
    if jai==10:
        th=threading.Thread(target=current_time,args=(b,))
        th.start()
        jai=11
t=0

def current_time(b):                 # this fuction is used to calculate current time of played song
    try:
        global paused,t
        while t<=b :
            if paused==2:
                t=0
                statusbar2['text'] = "Current Time - 00:00"
            elif paused ==1:
                continue
            elif paused==0:
                paused=0
                min, sec = divmod(t, 60)
                statusbar2['text'] = "Current Time -" + '{:02d}:{:02d}'.format(round(min), round(sec))
                time.sleep(1)
                t+=1
    except:
        pass

paused=0
played=0

def play_music():
    global paused,played,play_song,ss,filename,t
    if played==0 and len(playlist)==0:
        browse_song()
    elif played==1 and (paused==0 or paused==2) :
        try:
            t=0
            if paused!=2:
                stop_music()
            sb1['text'] = "Playing Music"
            paused=0
            select_song=playlistbox.curselection()
            ss=int(select_song[0])
            play_song=playlist[ss]
            mixer.music.load(play_song)
            mixer.music.play()
            file_detail(play_song)
        except:
            tkinter.messagebox.showerror("Select song", "Select audio file from given Playlist." )
    else:
        paused=0
        mixer.music.unpause()
        sb1['text']="Music resumes"

def stop_music():
    if played==1:
        global paused
        paused=2
        mixer.music.pause()
        sb1['text']="STOP"

def pause_music():
    global paused
    if played==1:
        if paused!=2:
            paused = 1
            mixer.music.pause()
            sb1['text'] = "PAUSED"
        else:
            sb1['text'] = "Music is already Stopped"

def set_vol(val):
    global x
    x = float(val) / 100
    mixer.music.set_volume(x)

def mute_music():
    global ptr
    if ptr:
        volume.configure(file="Images/speaker.png")
        scale.set(70)
        set_vol(70)
        ptr = FALSE
        sb1['text'] = "Unmute"
    else:
        volume.configure(file="Images/mute.png")
        scale.set(0)
        mixer.music.set_volume(0)
        sb1['text'] = "Muted"
        ptr = TRUE

def searchengine():
    mtext=userinput.get()
    mtext = mtext+'official song'           # here mtext is the input to be searched in youtube
    try:
        from googlesearch import search
    except ImportError:
        print("No module named 'google' found")

    for j in search(mtext, tld="co.in", num=10, stop=1, pause=2):
        webbrowser.open(j)
        # here we called the pause function as while searching on the web the background music of the player must be paused
        pause_music()

# Images used in music player as Button
play = PhotoImage(file="Images/play1.png")
stop = PhotoImage(file="Images/stop1.png")
pause = PhotoImage(file="Images/pause1.png")
volume = PhotoImage(file="Images/speaker.png")

# left frame
left_frame = Frame(root)
left_frame.configure(background='cyan')
left_frame.pack(side=LEFT, padx=15, pady=15)

mframe = Frame(left_frame)
mframe.configure(background="cyan")
mframe.pack(pady=20,padx=20)

bframe = Frame(left_frame)
bframe.configure(background="cyan")
bframe.pack(pady=20,padx=20)

rt = Button(mframe, bg="cyan", image=play, relief=FLAT, command=play_music).grid(padx=15,row=0,column=0)
rt2 = Button(mframe, bg="cyan", image=pause, relief=FLAT, command=pause_music).grid(padx=15,row=0,column=1)
rt3 = Button(mframe, bg="cyan", image=stop, relief=FLAT, command=stop_music).grid(padx=15,row=0,column=2)
rt5 = Button(bframe, bg="cyan", image=volume, relief=FLAT, command=mute_music).grid(row=0,column=0,padx=10)


scale = ttk.Scale(bframe, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
scale.grid(row=0,column=1,pady=30,padx=20)

l2 = Label(left_frame, text="Search for web if you don't have the song", bg="cyan", font=("Comic Sans MS", 11)).pack()

sframe = Frame(left_frame)
sframe.configure(background='cyan')
sframe.pack(padx=15,pady=15)
userinput = StringVar()
entry = Entry(sframe, textvariable=userinput).grid(row=1,column=0,padx=10)
rt7 = Button(sframe,bg="DodgerBlue2", text="Search", command=searchengine,font=("Verdana",11)).grid(row=1,column=1)


sb1 = Label(root,text="Play Whatever you want",bg="cyan",font=('Comic Sans MS',11))
sb1.pack(side=BOTTOM)


# Left Frame

right_frame = Frame(root)
right_frame.configure(background='cyan')
right_frame.pack(side=RIGHT, padx=15, pady=15)


l3 = Label(right_frame, text="Playlist", bg="cyan", font=("Comic Sans MS Bold", 11)).pack()

butframe=Frame(right_frame, bg='cyan')
butframe.pack(side=BOTTOM,fill=X)

# listbox inside rightframe

playlistbox = Listbox(right_frame, height=15, width=40, font=("Helvetica", 12))
playlistbox.pack(side=LEFT)
xscroll=Scrollbar(butframe,orient='horizontal')
xscroll.config(command=playlistbox.xview)
xscroll.pack(fill=X)

yscroll=Scrollbar(right_frame, orient='vertical')
yscroll.config(command=playlistbox.yview)
yscroll.pack(side=LEFT,fill=Y)

playlistbox.config(xscrollcommand=xscroll.set,yscrollcommand=yscroll.set)

rt8 = Button(butframe, bg="DodgerBlue2", text="Add song", command=browse_song,font=("Verdana",11)).pack(side=LEFT,padx=30,pady=10)
rt9 = Button(butframe, bg="DodgerBlue2", text="Delete song", command=del_song,font=("Verdana",11)).pack(side=RIGHT,padx=30,pady=10)


def close_window():
    stop_music()
    root.destroy()
root.protocol("WM_DELETE_WINDOW",close_window)
root.mainloop()