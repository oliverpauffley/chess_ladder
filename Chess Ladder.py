""" Module imports """
from random import shuffle
import pickle
import time
import csv


"""
Create student class to store student results
stats can be used to print students current rank and and win percentage
"""


class Student:
    def __init__(self, firstname, lastname):
        self.f_name = firstname
        self.l_name = lastname
        self.rank = find_max_rank(names) + 1
        self.num_played = 0
        self.num_won = 0
        self.num_draw = 0
        self.num_lost = 0
        self.win_percent = 0

    def update(self):
        if self.num_played == 0:
            self.win_percent = 0
        else:
            self.win_percent = round(self.num_won/self.num_played * 100, 1)

    def stats(self):
        self.stats_str = "%s %s is rank %s, they have played %s games and have a win percentage of %s%s" % (
            self.f_name, self.l_name, self.rank, self.num_played, self.win_percent, "%")
        return self.stats_str

    def __repr__(self):
        return '{}. {} {}'.format(self.rank, self.f_name, self.l_name)


""" Unpickle file with chess ladder """
filename = 'Chessladder'
try:
    infile = open(filename, 'rb')
    names = pickle.load(infile)
    if not names:
        names = []
except:
    infile = open(filename, 'wb')
    pickle.dump("", infile)
    infile.close()
    names = []


def print_student_rank(names):  # Prints list of students with their rank
    length = 70
    print("#" * length)
    gap = length - 1 - len("# Current list of students:")
    print("# Current list of students:" + " "*gap + "#")
    print("#" + " "*(length - 2) + "#")
    for n in names:
        gap = length - 1 - len("# " + str(n.rank) + ". " + n.f_name + " " + n.l_name)
        print("# " + str(n.rank) + ". " + n.f_name + " " + n.l_name + " "*gap + "#")
    print("#" + " "*(length - 2) + "#")
    print("#" * length)


def add_students(names):  # Function to add students name, will add to bottom of the ladder.
    state = 1
    while True:
        f_name = input("Please enter student's first name, or enter 'stop' to stop entering names: ")
        if f_name == "stop":
            state=""
            break
        l_name = input("Please enter student's last name, or enter 'stop' to stop entering names: ")
        if l_name == "stop":
            state=""
            break
        names.append(Student(f_name, l_name))
        print_student_rank(sorted(names, key=sort_by_rank))


def sort_by_rank(names):  # Key function to sort by rank.
    return names.rank


def find_max_rank(names):  # Find max rank in students names.
    try:
        rank_list = []
        for n in names:
            rank_list.append(n.rank)
        maxi = max(rank_list)
    except:
        maxi = 0
    return maxi


def delete_student(names):  # Delete a student then move all students up a rank.
    names = sorted(names, key=sort_by_rank)
    print_student_rank(names)

    while True:
        rank_to_remove = user_input(
            "Please enter the rank of the student you would like to delete (enter 0 to cancel): ", 0, len(names)+1)

        if rank_to_remove == 0:
            return names

        print("Are you sure you want to delete " + str(names[rank_to_remove - 1]) + "?")

        confirm = input("Enter Y to confirm deletion, enter anything else to cancel: ")
        if confirm != "Y":
            return names

        del names[rank_to_remove - 1]
        for n in names[rank_to_remove-1:]:
            n.rank += -1
        return names


def change_rank(names, current, target):  # function to move a player to the target postion.
    move_up = False
    if current > target:
        move_up = True
    names.sort(key=sort_by_rank)

    names[current-1].rank = target

    if move_up:
        for n in names[target-1:current-1]:
            n.rank += +1

    else:
        for n in names[current:target]:
            n.rank += -1

    return names.sort(key=sort_by_rank)


def game(names):  # Pick two students to play each other and then adjust ranks.
    names.sort(key=sort_by_rank)
    print_student_rank(sorted(names, key=sort_by_rank))
    first_player = ""
    second_player = ""
    print("")

    first_player = user_input(
        "Please enter the rank of the first player (enter 0 to cancel): ", 0, len(names)+1)

    if first_player == 0:
        return names

    print("")
    print_student_rank((names[:first_player - 1:] + names[first_player:]))
    print("")

    while True:
        second_player = user_input(
            "Please enter the rank of the second_player player (enter 0 to cancel): ", 0, len(names)+1)
        if second_player == 0:
            return names
        if second_player == first_player:
            print("A player cannot play themselves!")
            continue
        break

    print("")
    print(names[first_player-1].__repr__() +
          " will play " + names[second_player-1].__repr__())
    print("")

    while True:
        try:
            winner = int(
                input("Please enter the rank of the winner (or 0 for a draw): "))
        except:
            print("Sorry, you can only enter a numerical option.")
            continue
        if winner == 0:
            names[first_player-1].num_played += 1
            names[first_player-1].num_draw += 1
            names[second_player-1].num_played += 1
            names[second_player-1].num_draw += 1
            return names

        if winner != first_player and winner != second_player:
            print("You can only enter the rank of the current players!")
            continue
        break

        # Assign winner and loser and add to number of games played

    if winner == first_player:
        loser = second_player

    else:
        loser = first_player

    names[first_player-1].num_played += 1
    names[second_player-1].num_played += 1

    if winner == first_player:  # assigns wins and loses:
        names[first_player-1].num_won += 1
        names[second_player-1].num_lost += 1
    else:
        names[second_player-1].num_won += 1
        names[first_player-1].num_lost += 1

        # Now to change ranks. Loser always drops one. Winner goes up depending on if beating worse player.
    if winner == loser + 1:
        change_rank(names, winner, winner-1)
        return names

    if loser != len(names):
        change_rank(names, loser, loser+1)

    if winner == 1:
        return names

    if winner < loser:
        change_rank(names, winner, winner-1)
        return names
    else:
        change_rank(names, winner, int((winner+loser)/2))
        return names


def randomize(names):  # Randomize the current ladder.
    ranks = []
    for n in names:
        ranks.append(n.rank)

    shuffle(ranks)

    for n in range(0, len(ranks)):
        names[n].rank = ranks[n]

    return names


def user_input(prompt, mini, maxi):  # Function to parse user input (only for numerical input)
    while True:
        try:
            value = int((input(prompt)))
        except:
            print("Sorry, you can only enter a numerical option.")
            continue

        if value not in range(mini, maxi+1):
            print("You can only enter a number from " + str(mini) + "-" + str(maxi)+" !")
            continue
        break

    return value


def save():  # Pickle to file

    outfile = open(filename, 'wb')
    pickle.dump(names, outfile)
    outfile.close()
    print("Saving and exiting")
    time.sleep(2)


# Functions all defined - Start program proper
state = 0
print("""
    _____  _                                     _    _____ _                     _               _     _
   |  __ \(_)                                   | |  / ____| |                   | |             | |   | |
   | |__) |_ _ __   __ ___      _____   ___   __| | | |    | |__   ___  ___ ___  | |     __ _  __| | __| | ___ _ __
   |  _  /| | '_ \ / _` \ \ /\ / / _ \ / _ \ / _` | | |    | '_ \ / _ \/ __/ __| | |    / _` |/ _` |/ _` |/ _ \ '__|
   | | \ \| | | | | (_| |\ V  V / (_) | (_) | (_| | | |____| | | |  __/\__ \__ \ | |___| (_| | (_| | (_| |  __/ |
   |_|  \_\_|_| |_|\__, | \_/\_/ \___/ \___/ \__,_|  \_____|_| |_|\___||___/___/ |______\__,_|\__,_|\__,_|\___|_|
                    __/ |
                   |___/

Created by: Oliver Pauffley
""")

while state != 6:
    print("")
    print("""Please select an option:
    1. View current rankings.
    2. Input new game results.
    3. Add new students.
    4. Show student statistics.
    5. Admin options.
    6. Exit and save. """)
    print("")
    state = user_input("Option: ", 1, 6)
    if state == 1:
        print_student_rank(sorted(names, key=sort_by_rank))
        continue
    if state == 2:
        if len(names) < 2:
            print("You cannot play a game with this many players!")
            continue
        names = game(names)
        state=""
        continue
    if state == 3:
        print_student_rank(sorted(names, key=sort_by_rank))
        add_students(names)
        continue
    if state == 4:

        print_student_rank(sorted(names, key=sort_by_rank))
        rank = user_input(
            "Enter the rank of the student you would like to see stats for: ", 1, len(names)+1)
        names[rank-1].update()
        print(names[rank-1].stats())
        continue
    if state == 5:
        while True:

            print("""What would you like to do?
            1. Randomize current ladder.
            2. Move a players rank.
            3. Delete player.
            4. Delete ladder.
            5. Export ladder to excel.
            6. Leave admin mode.""")

            state = user_input("Option: ", 1, 6)

            if state == 1:
                print("Now randomizing...")
                time.sleep(2)
                names = randomize(names)
                print_student_rank(sorted(names, key=sort_by_rank))
                continue

            if state == 2:
                if len(names) < 2:
                    print("You cannot adjust ranks with this many players")
                    continue
                print_student_rank(sorted(names, key=sort_by_rank))
                print("Please enter the rank of the player you would like to move.")
                print("")
                current_rank = user_input("Rank: ", 1, len(names)+1)
                print("")
                print("Please enter the rank you would like to move " +
                      names[current_rank-1].f_name + " to.")
                print("")
                new_rank = user_input("Rank: ", 1, len(names)+1)
                change_rank(names, current_rank, new_rank)
                print_student_rank(sorted(names, key=sort_by_rank))

                continue

            if state == 3:
                if len(names) < 2:
                    print("You cannot delete students when you haven't entered any students!")
                    continue
                names = delete_student(names)
                continue

            if state == 4:
                print("Are you sure you want to delete the entire ladder? (This cannot be undone!)")
                print("")
                confirm = input("Enter Y to confirm deletion, anything else to cancel: ")
                if confirm == "Y":
                    names = []
                    print("Ladder deleted")
                continue

            if state == 5:
                names.sort(key=sort_by_rank)
                with open('Ladder_excel.csv', 'w') as myfile:
                    wr = csv.writer(myfile, lineterminator='\n')
                    column_title = ["Rank", "First name", "Last name", "Games played", "Games won"]
                    wr.writerow(column_title)
                    for n in names:
                        rank = n.rank
                        f_name = n.f_name
                        l_name = n.l_name
                        games_played = n.num_played
                        games_won = n.num_won
                        row = [str(rank), f_name, l_name, str(games_played), str(games_won)]
                        wr.writerow(row)
                    print("Exporting...")
                    time.sleep(2)
                    print("")
                    print("The current ladder has been exported to excel.")
                    print("")
                    continue

            if state == 6:
                print("leaving admin mode.")
                state = ""
                break

            continue

    if state == 6:

        break


save()
