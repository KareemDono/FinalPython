import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import colorama

# Initialize colorama
colorama.init()

# User data table
df = pd.DataFrame(columns=['Id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'birth_date', 'city'],
                  data=[
                      [1, 'Avraham', 'Cohen', 'avrahamk', 'avraham.cohen@gmail.com', '+972523456789', '1966-03-15', 'Tel Aviv'],
                      [2, 'Sarah', 'Levi', 'sarahlevi', 'sarah.levi@outlook.com', '+972533456789', '1945-05-20', 'Jerusalem'],
                      [3, 'Moshe', 'Goldstein', 'mosheg', 'moshe.goldstein@gmail.com', '+972543456789', '1977-07-10', 'Tel Aviv'],
                      [4, 'Rebecca', 'Barak', 'ravitb', 'ravit.barak@outlook.com', '+972553456789', '1988-09-25', 'Raanana'],
                      [5, 'Daniel', 'Cohen', 'danielk', 'daniel.cohen@gmail.com', '+972523456790', '1950-11-05', 'Tel Aviv'],
                      [6, 'Rachel', 'Schwartz', 'rachels', 'rachel.schwartz@gmail.com', '+972533456790', '1998-04-01', 'Tel Aviv'],
                      [7, 'Jacob', 'Green', 'yaakovg', 'yaakov.green@outlook.com', '+972543456790', '1981-08-12', 'Jerusalem'],
                      [8, 'Miriam', 'Cohen', 'miriamk', 'miriam.cohen@gmail.com', '+972553456790', '1967-02-18', 'Netanya'],
                      [9, 'Aaron', 'Levi', 'aharonl', 'aharon.levi@outlook.com', '+972523456791', '1972-06-29', 'Raanana'],
                      [10, 'Hannah', 'Friedman', 'hanaf', 'hannah.friedman@gmail.com', '+972533456791', '1948-12-24', 'Kfar Monash'],
                      [11, 'David', 'Cohen', 'davidk', 'david.cohen@gmail.com', '+972543456791', '1942-07-07', 'Tel Aviv'],
                      [12, 'Sarah', 'Adelman', 'sarahe', 'sarah.adelman@outlook.com', '+972553456791', '1991-09-11', 'Jerusalem'],
                      [13, 'Jacob', 'Zilberstein', 'yaakovz', 'yaakov.zilberstein@gmail.com', '+972523456792', '1987-11-16', 'Netanya'],
                      [14, 'Esther', 'Cohen', 'estherk', 'esther.cohen@gmail.com', '+972533456792', '1993-02-28', 'Jerusalem'],
                      [15, 'Israel', 'Solomon', 'israels', 'israel.solomon@outlook.com', '+972543456792', '1969-06-03', 'Netanya'],
                      [16, 'Deborah', 'Cohen', 'devorak', 'deborah.cohen@gmail.com', '+972553456792', '1962-08-08', 'Tel Aviv'],
                      [17, 'Joshua', 'Cohen', 'yehoshuak', 'joshua.cohen@gmail.com', '+972523456793', '1972-10-13', 'Jerusalem'],
                      [18, 'Rebecca', 'Levi', 'ravitl', 'rebecca.levi@outlook.com', '+972533456793', '1982-01-26', 'Netanya'],
                      [19, 'Aaron', 'Friedman', 'aharonf', 'aaron.friedman@gmail.com', '+972543456793', '1958-04-09', 'Raanana'],
                      [20, 'Sarah', 'Green', 'sarahg', 'sarah.green@outlook.com', '+972553456793', '1960-06-22', 'Kfar Monash'],
                  ])


# Color codes for menu
MENU_COLOR = '\033[38;2;255;165;0m'
OPTION_COLOR = '\033[38;2;0;191;255m'
OUTPUT_COLOR = '\033[38;2;50;205;50m'
PROMPT_COLOR = '\033[38;2;255;255;0m'
RESET_COLOR = '\033[0m'

def display_table(dataframe):
    table = tabulate(dataframe, headers=dataframe.columns, tablefmt='fancy_grid')
    print(f"{OUTPUT_COLOR}{table}")

def display_graph(dataframe, x, y, graph_type='bar'):
    dataframe.plot(x=x, y=y, kind=graph_type)
    plt.show()

def average_age(dataframe):
    current_year = pd.to_datetime('today').year
    dataframe['birth_date'] = pd.to_datetime(dataframe['birth_date'])
    dataframe['age'] = current_year - dataframe['birth_date'].dt.year
    avg_age = dataframe['age'].mean()
    print(f"{OUTPUT_COLOR}The average age of individuals is: {avg_age:.2f} years")

def most_common_first_names(dataframe):
    common_names = dataframe['first_name'].value_counts().reset_index()
    common_names.columns = ['First Name', 'Count']
    print(f"{OUTPUT_COLOR}Most common first names:")
    display_table(common_names)

    # Pie chart of top 5 most common first names
    common_names[:5].plot(kind='pie', y='Count', labels=common_names['First Name'][:5], autopct='%1.1f%%')
    plt.title("Top 5 Most Common First Names")
    plt.ylabel('')
    plt.show()

def percentage_by_city(dataframe):
    city_percentage = (dataframe['city'].value_counts() / len(dataframe)) * 100
    print(f"{OUTPUT_COLOR}Percentage of individuals from each city:")
    print(city_percentage)

    # Bar chart of percentage by city
    city_percentage.plot(kind='bar')
    plt.title("Percentage of Individuals from Each City")
    plt.ylabel('Percentage')
    plt.show()

def earliest_birth_date(dataframe):
    earliest_date = dataframe['birth_date'].min()
    person = dataframe[dataframe['birth_date'] == earliest_date]
    print(f"{OUTPUT_COLOR}Person with the earliest birth date:")
    display_table(person)

def count_gmail_users(dataframe):
    gmail_users = dataframe[dataframe['email'].str.contains('gmail.com')]
    count = len(gmail_users)
    print(f"{OUTPUT_COLOR}Number of individuals with Gmail email address: {count}")

def sort_by_last_name(dataframe):
    sorted_data = dataframe.sort_values('last_name')
    print(f"{OUTPUT_COLOR}Sorted data by last name in alphabetical order:")
    display_table(sorted_data)

def count_last_name_occurrences(dataframe):
    last_name_counts = dataframe['last_name'].value_counts().reset_index()
    last_name_counts.columns = ['Last Name', 'Occurrences']
    print(f"{OUTPUT_COLOR}Occurrences of individuals with the same last name:")
    display_table(last_name_counts)

    # Bar chart of last name occurrences
    last_name_counts.plot(kind='bar', x='Last Name', y='Occurrences')
    plt.title("Occurrences of Individuals with the Same Last Name")
    plt.xlabel('Last Name')
    plt.ylabel('Occurrences')
    plt.show()

def average_email_length(dataframe):
    dataframe['email_length'] = dataframe['email'].apply(len)
    avg_length = dataframe['email_length'].mean()
    print(f"{OUTPUT_COLOR}The average length of email addresses is: {avg_length:.2f} characters")

def individuals_by_decade(dataframe):
    dataframe['birth_date'] = pd.to_datetime(dataframe['birth_date'])
    dataframe['decade'] = (dataframe['birth_date'].dt.year // 10) * 10
    individuals_per_decade = dataframe['decade'].value_counts().sort_index().reset_index()
    individuals_per_decade.columns = ['Decade', 'Count']
    print(f"{OUTPUT_COLOR}Number of individuals born in each decade:")
    display_table(individuals_per_decade)

    # Line graph of individuals by decade
    individuals_per_decade.plot(kind='line', x='Decade', y='Count', marker='o')
    plt.title("Number of Individuals Born in Each Decade")
    plt.xlabel('Decade')
    plt.ylabel('Count')
    plt.show()

def filter_older_than_50(dataframe):
    current_year = pd.to_datetime('today').year
    dataframe['birth_date'] = pd.to_datetime(dataframe['birth_date'])
    dataframe['age'] = current_year - dataframe['birth_date'].dt.year

    filtered_data = dataframe[dataframe['age'] > 50]
    print(f"{OUTPUT_COLOR}Filtered data including only individuals older than 50 years:")
    display_table(filtered_data)

def youngest_oldest_individuals_by_city(dataframe):
    dataframe['birth_date'] = pd.to_datetime(dataframe['birth_date'])
    dataframe['age'] = pd.to_datetime('today').year - dataframe['birth_date'].dt.year
    grouped_data = dataframe.groupby('city')

    youngest = dataframe.loc[grouped_data['age'].idxmin()]
    oldest = dataframe.loc[grouped_data['age'].idxmax()]

    print(f"{OUTPUT_COLOR}Youngest individuals by city:")
    display_table(youngest)
    print(f"{OUTPUT_COLOR}Oldest individuals by city:")
    display_table(oldest)

    # Bar chart of youngest and oldest individuals by city
    youngest_oldest_data = pd.concat([youngest, oldest])
    display_graph(youngest_oldest_data, 'city', 'age', 'bar')


# Menu options
menu_options = {
    '1': (average_age, "Calculate the average age of individuals"),
    '2': (most_common_first_names, "Identify the most common first names in the dataset"),
    '3': (percentage_by_city, "Determine the percentage of individuals from each city"),
    '4': (earliest_birth_date, "Find the person with the earliest birth date"),
    '5': (count_gmail_users, "Count the number of individuals with a Gmail email address"),
    '6': (sort_by_last_name, "Sort the data by last name in alphabetical order"),
    '7': (count_last_name_occurrences, "Identify individuals with the same last name and count their occurrences"),
    '8': (average_email_length, "Calculate the average length of email addresses"),
    '9': (individuals_by_decade, "Calculate the number of individuals born in each decade"),
    '10': (filter_older_than_50, "Filter the data to include only individuals older than 50 years"),
    '11': (youngest_oldest_individuals_by_city, "Determine the youngest and oldest individuals from each city"),
}

# Display menu
def display_menu():
    print(MENU_COLOR + "Statistical Reports Menu:")
    for option, description in menu_options.items():
        print(OPTION_COLOR + f"{option}. {description[1]}")

# User input for menu selection
def get_user_choice():
    selected_option = input(PROMPT_COLOR + "Select an option (1-11): ")
    print(RESET_COLOR)  # Reset colorama style
    return selected_option

# Validate and execute selected option
def execute_option(option):
    if option in menu_options:
        selected_function, _ = menu_options[option]
        selected_function(df)
    else:
        print(OPTION_COLOR + "Invalid option selected.")

# Main program
while True:
    display_menu()
    choice = get_user_choice()
    execute_option(choice)
    print()
    continue_choice = input(PROMPT_COLOR + "Do you want to choose another option? (y/n): ")
    print()
    if continue_choice.lower() != 'y':
        break

# Reset colorama style
colorama.deinit()
