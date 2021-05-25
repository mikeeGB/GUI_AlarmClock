import tkinter as tk
from datetime import datetime
from pygame import mixer
from random import randint


# Функции будильника
def clock():
    """
    обновляет текущее время в окне tkinter
    """
    current_time = datetime.now().strftime("%H:%M:%S")
    myTimeLabel.config(text=current_time, font='Banschrift 30')
    root.after(1000, clock)  # run itself again after 1000 ms


def play_music():
    """
    Включает музыку
    """
    mixer.music.load("music/basic.wav")
    mixer.music.play()


def start_alarm():
    """
    Запускает будильник, если оставшееся время равно 0
    """
    try:
        hours_inp = int(hours_item.get())  # получаем информацию из spin box
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
    Updates current time in root window
    """
    curr_hour = datetime.now().hour
    curr_min = datetime.now().minute

    curr_time_in_min = curr_hour * 60 + curr_min

    if hours_inp == 0:  # если нулевой час (24:00)
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


# Timer functions
def generate_time_in_sec():
    """Time generation in seconds"""
    rand_h = randint(0, 23)
    rand_m = randint(0, 59)

    var_1 = tk.StringVar(root)
    var_1.set(f"{rand_h}")

    var_2 = tk.StringVar(root)
    var_2.set(f"{rand_m}")

    hours_timer.config(textvariable=var_1)
    minutes_timer.config(textvariable=var_2)


def start_timer():
    """Launchs timer"""
    hours_timer_inp, minutes_timer_inp = hours_timer.get(), minutes_timer.get()
    if hours_timer_inp.isdigit() and minutes_timer_inp.isdigit():
        time_left = int(hours_timer_inp) * 3600 + int(minutes_timer_inp) * 60
        countdown(time_left)


def countdown(time_left):
    """Counts time left in seconds"""
    if time_left:
        timerStartButton['state'] = tk.DISABLED
        timer_text_label['text'] = f"{time_left} sec"
        root.after(1000, countdown, time_left - 1)
    else:
        timer_text_label['text'] = f"Time is up"
        mixer.music.load("music/short_sound.wav")
        mixer.music.play()
        timerStartButton['state'] = tk.NORMAL


# root window
root = tk.Tk()
root.title("AlarmClock")

# music initialization
mixer.init()


# label with current time
myTimeLabel = tk.Label(root)
myTimeLabel.grid(row=0, column=0)
clock()

# text label - 'enter time'
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


# Text Timer
timerGameLabel = tk.Label(root, text="Timer", font='Banschrift 14')
timerGameLabel.grid(row=4, column=0, columnspan=3)

# Generating random time button
timeGenerateButton = tk.Button(root, text="Generate time(H:M)", font="Time 13",
                               padx=10, command=generate_time_in_sec)
timeGenerateButton.grid(row=5, column=0, columnspan=1)

# start timet button
timerStartButton = tk.Button(root, text="START timer", font="Time 13",
                             padx=35, command=start_timer)
timerStartButton.grid(row=6, column=0, columnspan=1)

# Spinboxes for timer
hours_timer = tk.Spinbox(root, from_=0, to=23, width=5, font='Times 15')
minutes_timer = tk.Spinbox(root, from_=0, to=59, width=5, font='Times 15')
hours_timer.grid(row=5, column=1)
minutes_timer.grid(row=5, column=2)

# Text label - output time left
timer_text_label = tk.Label(root, font='Banschrift 12')
timer_text_label.grid(row=6, column=1, columnspan=2)

root.mainloop()
