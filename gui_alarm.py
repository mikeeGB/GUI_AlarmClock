import tkinter as tk
from datetime import datetime
from pygame import mixer


def clock():
    """
    Updates current time in root window
    """
    current_time = datetime.now().strftime("%H:%M:%S")
    myTimeLabel.config(text=current_time, font='Banschrift 30')
    root.after(1000, clock)  # run itself again after 1000 ms


def play_music():
    """
    Plays music
    """
    mixer.init()
    mixer.music.load("music/basic.wav")
    mixer.music.play()


def start_alarm():
    """
    Launch alarm if no time left
    """
    try:
        hours_inp = int(hours_item.get())  # get info from spinbox
        assert hours_inp in range(0, 24)
        minutes_inp = int(minutes_item.get())
        assert minutes_inp in range(0, 60)
    except ValueError as e:
        print(f"Error occured: {e}")
    except AssertionError:
        print("Range is not correct!")
    else:
        time_left_check(hours_inp, minutes_inp)


def time_left_check(hours_inp, minutes_inp):
    """
    Outputs alarm time left
    """
    curr_hour = datetime.now().hour
    curr_min = datetime.now().minute

    curr_time_in_min = curr_hour * 60 + curr_min

    if hours_inp == 0:  # if 24:00 now
        minutes_left = (24 * 60 + minutes_inp) - curr_time_in_min
    else:
        minutes_left = (hours_inp * 60 + minutes_inp) - curr_time_in_min

    timerLabel = tk.Label(root)
    timerLabel.config(text=f"Wait: {minutes_left//60}h:{minutes_left % 60}min",
                      font='Banschrift 12', width=15)

    timerLabel.grid(row=3, column=1, columnspan=2)

    if minutes_left == 0:
        play_music()
    elif minutes_left < 0:
        timerLabel.config(text="This time has passed",
                          font='Banschrift 11', width=15)
    else:
        root.after(1000, start_alarm)


# root window
root = tk.Tk()
root.title("AlarmClock")

# label with current time
myTimeLabel = tk.Label(root)
myTimeLabel.grid(row=0, column=0)
clock()

# Text - 'Enter time'
myTextLabel = tk.Label(root, text="Enter time to alarm", font='Banschrift 12')
myTextLabel.grid(row=1, column=0)


# spin boxes
hours_item = tk.Spinbox(root, from_=0, to=23, width=5, font='Times 15')
minutes_item = tk.Spinbox(root, from_=0, to=59, width=5, font='Times 15')

hours_item.grid(row=1, column=1)
minutes_item.grid(row=1, column=2)


# Enter time button
enterButton = tk.Button(root, text='Enter', font='Banschrift 10', padx=50,
                        command=start_alarm)
enterButton.grid(row=2, column=1, columnspan=2)


root.mainloop()
