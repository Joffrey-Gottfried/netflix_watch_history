import csv
import re
from collections import Counter
import matplotlib.pyplot as plt
import PySimpleGUI as sg
import tkinter as tk
from tkinter import messagebox
import webbrowser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def main():
    layout1 = [
        [sg.Titlebar("Netflixomat")],
        [sg.Text("Choose the file: "), sg.Input(), sg.FileBrowse(key="-File-")],
        [sg.Text("Otherwise download the right file here", enable_events=True, text_color="blue", key="-Link-")],
        [sg.Text("Did you choose the correct File")], [sg.Button("OK")],
    ]

    # Create the window
    window1 = sg.Window("Demo", layout1)

    character = None
    column = None
    date = None
    title = None
    series = None

    # Create an event loop
    while True:
        event1, values1 = window1.read()
        # End the program if the user closes the window
        if event1 == sg.WIN_CLOSED:
            break

        if event1 == "OK":
            window1.close()
            file = values1["-File-"]
            character = characters(file)
            column = columns(file)
            result = dates(column)
            date = result[0]
            title = result[1]
            tit = result[2]
            tit.sort()
            count = amount(tit)
            sorted_dict = dict(sorted(count.items(), key=lambda item: item[1], reverse=True))
            c_date = amount_date(date)

            series = num_series(count)
            stream = len(title)
            movies = (stream) - series

            layout2 = [
                [sg.Multiline("These are your titles sorted, with the most watched at the top:\n\n{}".format(
                    '\n'.join([f"{key}: {value}" for key, value in sorted_dict.items()])), size=(40, 10),
                    disabled=True)],
                [sg.Button("OK")]
            ]

            window2 = sg.Window("Test", layout2)

            # Create an event loop for window2
            while True:
                event2, values2 = window2.read()
                if event2 == sg.WIN_CLOSED:
                    break

                if event2 == "OK":
                    window2.close()

                    layout3 = [
                        [sg.Text(f"You watched {series} series")],
                        [sg.Text(f"You watched {movies} movies")],
                        [sg.Button("OK")],
                    ]
                    window3 = sg.Window("Test", layout3)

                    # Control variable for window3 loop
                    window3_open = True

                    while window3_open:
                        event3, values3 = window3.read()
                        if event3 == "OK" or event3 == sg.WIN_CLOSED:
                            window3.close()
                            window3_open = False  # Exit the window3 loop

                    layout4 = [
                        [sg.Titlebar("Netflixomat")],
                        [sg.Button("Generate Graph")],  # Add a button to trigger the graph generation
                        [sg.Canvas(key='-CANVAS-')],
                        [sg.Button("EXIT")],
                    ]

                    window4 = sg.Window("Netflixomat", layout4)

                    while True:
                        event4, values4 = window4.read()

                        if event4 == sg.WIN_CLOSED or event4 == "EXIT":
                            break
                        elif event4 == "Generate Graph":
                            graph(window4, c_date, sorted_dict)

                    window4.close()

        elif event1 == "-Link-":
            open_link()

        if event1 == sg.WIN_CLOSED:
            break


def open_link():
    webbrowser.open("https://www.netflix.com/settings/viewed/")

    root = tk.Tk()
    root.title("Example")

    label = tk.Label(root, text="Click here to visit the website", fg="blue", cursor="hand2")
    label.pack()

    label.bind("<Button-1>", lambda e: open_link())

    root.mainloop()

def columns(csv_file_path):
    # Initialize a list to store columns
    column = []

    # Read the CSV file and store columns in the list
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row

        # Read the rows and store each column in the list
        while True:
            try:
                row = next(csv_reader)
                column.append(row)
            except StopIteration:
                break
    return column


def characters(csv_file_path):
    # Initialize a list to store characters
    character = []

    # Read the CSV file and store characters in the list
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row

        # Read the rows and store each character in the list
        for row in csv_reader:
            for char in ''.join(row):
                character.append(char)
    return character


def dates(column):
    date = []
    titel = []
    tit = []

    for element in column:
        date.append(element[1])
        tmp = re.split("Staffel", element[0])
        tmp = re.split("Folge", tmp[0])
        tmp = re.split("Kapitel", tmp[0])
        tmp = re.split("Teil", tmp[0])
        tit.append(tmp[0])
        titel.append(element[0])
    return date, titel, tit


def num_series(dic):
    series = 0

    for char in dic:
        if dic[char] == 1:
            series += 1
    return series


def speichern(csv_directory, dates, titles):

    with open(csv_directory, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for row in dates:
            writer.writerow([row])

    count_episode = 0
    for row in titles:
        if row.find("Folge"):
            count_episode += 1


def amount_date(list):
    dic = {}

    for element in list:
        if element in dic:
            dic[element] +=1
        else:
            dic[element] = 1

    return dic


def amount(list):
    dic = {}

    for element in list:
        key = element[:10]
        if key in dic:
            dic[key] += 1
        else:
            dic[key] = 1

    return dic


def graph(window, cnt_date, cnt_title):
    # Create a figure and two subplots
    fig, axes = plt.subplots(2, 1)

    # Plot the date data in the first subplot
    axes[0].plot(list(cnt_date.keys()), list(cnt_date.values()), marker='o')
    axes[0].set_xlabel('Datum')
    axes[0].set_ylabel('Häufigkeit')
    axes[0].set_title('Line Graph')
    axes[0].grid(True)

    # Plot the title data in the second subplot
    axes[1].bar(list(cnt_title.keys()), list(cnt_title.values()))
    axes[1].set_xlabel('Title')
    axes[1].set_ylabel('Häufigkeit')
    axes[1].set_title('Bar Chart')
    axes[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

    # Create a canvas from the figure
    canvas = FigureCanvasTkAgg(fig, window['-CANVAS-'].Widget)
    canvas.get_tk_widget().pack(side='top', fill='both', expand=1)

    # Update the PySimpleGUI window
    window.refresh()



main()
