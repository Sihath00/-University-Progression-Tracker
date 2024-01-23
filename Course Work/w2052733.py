# Import Graphic Module
from graphics import *

def welcome_screen():
    # Function to display a welcome screen
    win = GraphWin("Welcome to Progression Tracker", 600, 400)
    win.setBackground("#FFE6E8")

    # Title
    title = Text(Point(300, 50), "Progression Tracker")
    title.setSize(20)
    title.setStyle("bold")
    title.setTextColor("blue")
    title.draw(win)

    # Description
    description = Text(Point(300, 120), "This program helps you track your progression outcomes.")
    description.setSize(12)
    description.setTextColor("black")
    description.draw(win)

    # Instructions
    instructions = Text(Point(300, 180), "Enter the credits for pass, defer, and fail when prompted.")
    instructions.setSize(12)
    instructions.setTextColor("black")
    instructions.draw(win)

    start_button = Rectangle(Point(250, 250), Point(350, 300))
    start_button.setFill("green")
    start_button_text = Text(Point(300, 275), "Start")
    start_button.draw(win)
    start_button_text.draw(win)

    win.getMouse()
    win.close()

# Histogram Variables
progress_count = 0
trailer_count = 0
exclude_count = 0
retriever_count = 0
total_count = 0

def is_valid_input(credits):
    return credits in [0, 20, 40, 60, 80, 100, 120]


def draw_bar(win, x, count, max_height, color, label):
    bar_width = 100  # Set the width for the bars
    gap = 20  # Set the gap between bars
    base_line = 450  # Y-coordinate for the baseline

    bar_height = (count / max_height) * 300  # Scale the bar height
    bar = Rectangle(Point(x, base_line - bar_height), Point(x + bar_width, base_line))
    bar.setFill(color)
    bar.draw(win)

    # Label for the bars
    label_text = Text(Point(x + bar_width / 2, base_line + 20), label)
    label_text.draw(win)

    # Count above the bars
    count_text = Text(Point(x + bar_width / 2, base_line - bar_height - 10), str(count))
    count_text.draw(win)


def histogram():
    win = GraphWin("Histogram Results", 600, 550)
    win.setBackground("#FFE6E8")

    # Title for the histogram
    title = Text(Point(300, 30), "Histogram Results")
    title.setSize(18)
    title.setStyle("bold")
    title.draw(win)

    bar_line = Line(Point(25, 450), Point(750, 450))
    bar_line.draw(win)

    # Max height calculation
    max_height = max(progress_count, trailer_count, retriever_count, exclude_count)
    if max_height == 0:
        max_height = 1

    # Draw bars
    draw_bar(win, 50, progress_count, max_height, "green", "Progress")
    draw_bar(win, 170, trailer_count, max_height, "blue", "Trailer")
    draw_bar(win, 290, retriever_count, max_height, "orange", "Retriever")
    draw_bar(win, 410, exclude_count, max_height, "red", "Excluded")

    # Total outcomes text
    total_outcomes_text = Text(Point(300, 500), f"{total_count} outcomes in total.")
    total_outcomes_text.draw(win)

    win.getMouse()
    win.close()


def get_user_input():

    try:
        pass_credits = int(input("Please enter your credits at pass: "))
        defer_credits = int(input("Please enter your credit at defer: "))
        fail_credits = int(input("Please enter your credit at fail: "))
        return pass_credits, defer_credits, fail_credits
    except ValueError:
        print("Integer required")
        return None


def save_to_file(data, filename):
    with open(filename, 'a') as file:
        for item in data:
            file.write(','.join(map(str, item)) + '\n')


def load_from_file(filename):
    loaded_data = []
    with open(filename, 'r') as file:
        for line in file:
            # Skip lines that start with 'Total incorrect' and lines that don't contain valid data
            if line.startswith('Total incorrect') or ' - ' not in line:
                continue

            outcome, credits_data = line.strip().split(' - ')
            pass_credits, defer_credits, fail_credits = map(int, credits_data.split(','))
            loaded_data.append((outcome, pass_credits, defer_credits, fail_credits))

    return loaded_data


# List to store progression data
progression_data = []

# Main program
welcome_screen()
while True:
    user_input = get_user_input()

    if user_input != 0:
        pass_credits, defer_credits, fail_credits = user_input
        total_credits = pass_credits + defer_credits + fail_credits

        if not all(map(is_valid_input, [pass_credits, defer_credits, fail_credits])):
            print("Out of Range")


        if pass_credits == 120:
            outcome = "Progress"
            progress_count = progress_count + 1

        elif pass_credits == 100:
            outcome = "Progress (module trailer)"
            trailer_count = trailer_count + 1

        elif fail_credits >= 80:
            outcome = "exclude"
            exclude_count = exclude_count + 1
        else:
            outcome = "module retriver"
            retriever_count = retriever_count + 1

        total_count = total_count + 1
        print("Progression Outcome:", outcome)

        # Append input data to the list
        progression_data.append((outcome, pass_credits, defer_credits, fail_credits))
        example = [progress_count, trailer_count, exclude_count, retriever_count, total_count]

        # Ask the user if they want to enter another set of data
        another_set = input("Do you want to enter another set of data? (yes/no): ").lower()
        if another_set != 'yes':
            save_to_file(progression_data, 'progression_data.txt')
            histogram()
            break
    else:
        break

 

print("\nPart 2:")
for data in progression_data:
    outcome, pass_credits, defer_credits, fail_credits = data
    print(f"{outcome} - {pass_credits}, {defer_credits}, {fail_credits}")

# Part 3: Load and print data from the text file
loaded_data = load_from_file('progression_data.txt')
print("\nPart 3: Text File")
for data in loaded_data:
    outcome, pass_credits, defer_credits, fail_credits = data
    print(f"{outcome} -  {pass_credits}, {defer_credits}, {fail_credits}")