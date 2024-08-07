"""
Little program I've made to help me on my quest to visit every Metro station in Melbourne. This program will select a random station name from an imported .json file and
give me the option to select it (which removes it from the selection next time) or roll for another one. I might add more features too, but I thought this would be a fun
project now I've finished up with my tic tac toe program :3

Plan:
- Simple terminal interface (maybe using colours?)
- Import and modify a .json file for data storage
- Options to reroll if I don't like the choice
- Show what line the station is on and it's distance from the CBD/Southern Cross
- Counter for how many stations visited/how many remaining, in total and by line (maybe a small hooray msg if a line is completed)
- Maybe a "queue" that doesn't clear a station until I confirm I visited it?
- Maybe a GUI eventually!
- Option to manually mark a station as visited
- Log date a station was visited (can take user input for this)
- Look up info on stations (PT connections, nearby stations + other stuff already included in datastore)
- More?
"""

import json
import os
import random

# Library to do fancy text formatting and stuff, including colours. I could just implement colours with ASCII escape characters buuut this is better.
from rich.console import Console


# Enhanced print() functionality provided by Rich
console = Console(highlight=False)


# Runs OS-specific shell command to clear console
def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# Load saved, visited and unvisited stations from datastore.json, which should be in the same directory. Not bothering with error handling.
def read():
    # I kind of understand how this works? Basically with is shorthand for a try/except/finally statement and I think there are some benefits beyond that too? I dunno. Either way I'm opening a file!
    with open('datastore.json', 'r') as file:
        return json.load(file)


# Write modified .json to datastore.json
def write(data):
    with open('datastore.json', 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


# Check whether a station name has been written to to_visit dict. If yes, prompt the user whether they want to mark it as visited & continue or return/exit
def check_to_visit(data):
    clear()

    if len(data['to_visit']) > 0:
        print("Warning! There's a station queued up for you to visit already!\n")
        print('1) Mark as visited and continue')
        print('2) Return to main menu')
        print('3) Exit')

        while True:
            choice = input('> ')
            if choice == '1':
                # Insert the dict associated with the randomly chosen station into visited after grabbing it from unvisited with get()
                data['visited'].update(
                    {data['to_visit']: data['unvisited'].get(data['to_visit'])}
                )
                # Now that we've copied over the station dict into visited, we can remove it from unvisited with pop()
                data['unvisited'].pop(data['to_visit'])
                # Reset to_visit to be an empty string again
                data['to_visit'] = ''
                # Write changes to datastore.json so the program remembers them when reopened
                write(data)

                roll_station(data)
                break
            elif choice == '2':
                break
            elif choice == '3':
                exit()
            else:
                print(
                    '\nInvalid choice. Please select one of the listed options above by typing the number next to the option.\n'
                )
    else:
        roll_station(data)


# Selects a random station from the data['unvisited'] dictionary/object by doing (sparkles) magic (sparkles)
def roll_station(data):
    # Check whether there are any stations left to visit (the function we call here is just a screen that congratulates the user and gives options to return to main menu or exit)
    if len(data['unvisited']) == 0:
        no_unvisited()
        return

    # Get the name's of all stations by converting the dictionary keys (the names) into a list
    stations = list(data['unvisited'].keys())
    # I stored times as an int like this in datastore.json to save myself retyping stuff. This dict just contains what each number correlates to.
    time_conversion = {
        0: 'under 10',
        1: '11 to 20',
        2: '21 to 30',
        3: '31 to 40',
        4: '41 to 50',
        5: '51 to 60',
        6: '61 to 70',
        7: '71 to 80',
        8: '81 to 90',
        9: '91 to 100',
        10: '101 to 110',
    }

    line_colours = {
        'Alamein': 'white on #094c8d',
        'Belgrave': 'white on #094c8d',
        'Glen Waverley': 'white on #094c8d',
        'Lilydale': 'white on #094c8d',
        'Cranbourne': 'black on #16b4e8',
        'Pakenham': 'black on #16b4e8',
        'Hurstbridge': 'white on #b1211b',
        'Mernda': 'white on #b1211b',
        'Craigieburn': 'black on #ffb531',
        'Sunbury': 'black on #ffb531',
        'Upfield': 'black on #ffb531',
        'Flemington Racecourse': 'white on #909295',
        'Frankston': 'black on #159943',
        'Stony Point': 'black on #159943',
        'Werribee': 'black on #159943',
        'Williamstown': 'black on #159943',
        'Sandringham': 'black on #fc7fbb',
    }

    while True:
        clear()
        # Pick a random station name from our list made above
        station = random.choice(stations)
        # Now that we have a station name/key, grab info on the station from data['unvisited'] including line, distance, travel time...
        station_info = data['unvisited'][station]
        lines = ''
        for line in station_info['line']:
            colour = line_colours[line]
            lines += f'[{colour}] {line} [/{colour}]'

            if line != station_info['line'][-1]:
                lines += ', '

        console.print(f"Looks like you're heading to... [bold]{station}!\n")
        console.print(
            f'- [bold]{station}[/bold] is served by the {lines} line/s.'
        )
        console.print(
            f'- [bold]{station}[/bold] is {station_info['distance']}km from the CBD.'
        )
        console.print(
            f'- Journeys to [bold]{station}[/bold] take {time_conversion[station_info['time']]} minutes on average.\n'
        )
        print('1) Reroll')
        print('2) Accept\n')

        while True:
            choice = input('> ')
            if choice == '1':
                roll_station(data)
                break
            elif choice == '2':
                # Writes the key/station name to to_visit, a string value in datastore.json. This is so we can retrieve info on this station later. For now, we can leave it in unvisited.
                data['to_visit'] = station
                write(data)
                break
            else:
                print(
                    '\nInvalid choice. Please select one of the listed options above by typing the number next to the option.\n'
                )

        break


# We call this when data['unvisited'] has a length of 0 (meaning it contains nothing)
def no_unvisited():
    clear()

    print(
        "There aren't any more stations to visit - you've been to them all! Congratulations!\n"
    )
    print('1) Main menu')
    print('2) Exit\n')

    while True:
        choice = input('> ')

        if choice == '1':
            break
        elif choice == '2':
            exit()


def stats(data):
    clear()

    print('\n -+ Statistics +-\n')
    console.print(
        f'- You have visited {len(data['visited'])} out of {len(data['visited']) + len(data['unvisited'])} stations.\n'
    )
    print('1) Main menu')
    print('2) Exit\n')

    while True:
        choice = input('> ')

        if choice == '1':
            break
        elif choice == '2':
            exit()


# Main program
def main(data):
    unmodified_title = ' | |E|v|e|r|y| |M|e|t|r|o| |S|t|a|t|i|o|n| |'
    modified_title = (
        '[bright_black] +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+[bright_black]\n'
    )
    for i in range(44):
        if unmodified_title[i] == '|':
            modified_title += '[bright_black]|[/bright_black]'
        elif i > 14 and i < 25:
            modified_title += '[dodger_blue1]' + unmodified_title[i] + '[/dodger_blue1]'
        else:
            modified_title += '[default]' + unmodified_title[i] + '[/default]'
    modified_title += (
        '\n[bright_black] +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+[/bright_black]'
    )

    clear()

    console.print(modified_title)
    console.print('\n1) Get next station')
    console.print('2) Mark station as visited')
    console.print('3) Statistics')
    console.print('4) Exit\n')

    choice = input('> ')

    if choice == '1':
        check_to_visit(data)
    elif choice == '2':
        pass
    elif choice == '3':
        stats(data)
    elif choice == '4':
        exit()
    else:
        print(
            '\nInvalid choice. Please select one of the listed options above by typing the number next to the option.\n'
        )

    main(data)


main(read())
