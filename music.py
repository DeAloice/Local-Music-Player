import tkinter as tk
import customtkinter as ctk
import os
import pygame
import random

home_dir = os.path.expanduser("~")
music_folder = os.path.join(home_dir, "Downloads/Music1")

is_playing = False
playlist = []
curr_index = 0

pygame.mixer.init()

if os.path.exists(music_folder):
    playlist = [f for f in os.listdir(music_folder) if f.endswith(".mp3") ]
    random.shuffle(playlist)
else:
    print(f"Error: The folder '{music_folder}' does not exist!")

def autoplay():
    global is_playing

    if is_playing and not pygame.mixer.music.get_busy():
        go_forward(event=None)

    root.after(1000, autoplay)

def handle_tap(event=None):
    if event.widget == play_button:
        toggle_play_pause(event)
    elif event.widget == for_button:
        go_forward(event)
    elif event.widget == back_button:
        go_back(event)

def load():
    global is_playing

    song_path = os.path.join(music_folder, playlist[curr_index])
    print(f"Now playing: {playlist[curr_index]}")

    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()

    play_button.config(image=pause_img)
    song_label.config(text=playlist[curr_index])
    is_playing = True

def toggle_play_pause(event=None):
    global is_playing

    if is_playing:
        pygame.mixer.music.pause()
        play_button.config(image=play_img)
        is_playing = False
        print("Paused song")
    else:
        if pygame.mixer.music.get_pos() == -1:
            load()
        else:
            pygame.mixer.music.unpause()
            play_button.config(image=pause_img)
            is_playing = True
        
def go_back(event=None):
    global curr_index

    curr_index = (curr_index - 1) % len(playlist)
    load()

def go_forward(event=None):
    global curr_index

    curr_index = (curr_index + 1) % len(playlist)
    load()


# Creates root: main window
root = tk.Tk()
root.title("Local Music Player")
root.config(bg="#2D2D2D")
root.resizable(False, False)
root.geometry("400x250")

# Creates the frame the widget, able to arrange things inside
frame = ctk.CTkFrame(master=root, fg_color="#2B6286", width=400, height=120, corner_radius=20)
frame.pack(padx=20, pady=(20, 5), side=tk.TOP)
frame.pack_propagate(False) 

song_label = tk.Label(
    frame,
    text="No Song Playing",
    fg="white",
    bg="#2B6286",
    font=("Inclusive Sans", 20, "bold"),
    anchor="w",
    justify="left"
)
song_label.pack(side=tk.BOTTOM, padx=20, pady=20)

button_frame = tk.Frame(root, bg="#2D2D2D")
button_frame.pack(pady=10)

back_img = tk.PhotoImage(file="images/Back.png")
forward_img = tk.PhotoImage(file="images/Forward.png")
play_img = tk.PhotoImage(file="images/Play.png")
pause_img = tk.PhotoImage(file="images/Pause.png")
frame_bg = button_frame.cget("bg")

# Backward UI element
back_button = tk.Label(
    button_frame, 
    image=back_img,
    bg=frame_bg,
    cursor="hand2"
)
back_button.grid(row=0, column=0, padx=20)

# Play/Pause UI element
play_button = tk.Label(
    button_frame, 
    image=play_img,
    bg=frame_bg,
    cursor="hand2"
)
play_button.grid(row=0, column=1, padx=20)

# Forward UI element
for_button = tk.Label(
    button_frame, 
    image=forward_img,
    bg=frame_bg,
    cursor="hand2"
)
for_button.grid(row=0, column=2, padx=20)

root.bind_all("<Button-1>", handle_tap)
root.bind("<space>", toggle_play_pause)
root.bind("<Left>", go_back)
root.bind("<Right>", go_forward)


autoplay()
root.mainloop()
