import time
import pandas as pd
import numpy as np


""" Defining colors for better text reading """
class color:
   PURPLE = '\033[95m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   BU = BOLD + UNDERLINE
   BLUE_BOLD = BLUE + BOLD
   GREEN_BOLD = GREEN + BOLD
   END = '\033[0m'

""" The data sets as csv files stored in a dictionary """
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

""" Two global lists with months and days needed to be sccessed by the functions """
months_l = ['January', 'February', 'March', 'April', 'May', 'June']
days_l = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    For month you can choose a certain month, no filtering or displaying statistics of each month
    For day you can choose a certain day of the week, no filtering or displaying statistics of each day of the week

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, "all" to apply no month filter "each_month" for statistics of each month
        (str) day - name of the day of week to filter by, "all" to apply no day filter or "each_day" for statistics of each day of the week
    """

    # different lists for filtering. "Short forms" of the lists take starting strings of each element in the lists. Short forms allow faster user inputself.
    # "Short form" input as well as "long form" input of names/data are allowed
    cities_l = ['Chicago', 'New York City', 'Washington']
    cities_s = [item[0].lower() for item in cities_l]
    months_s = [item[0:3].lower() for item in months_l]
    days_s = [item[0:2].lower() for item in days_l]
    type_of_filter_l = ['month', 'day', 'not at all']
    type_of_filter_s = [item[0].lower() for item in type_of_filter_l]

    month = 'all'
    day = 'all'

    print('\n{}Hello! Let\'s explore some US bikeshare data!{}\n'.format(color.GREEN_BOLD, color.END))


    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago ({0}c{1}), New York City ({0}n{1}) or Washington ({0}w{1})? '.format(color.BU, color.END))

        if city.title() in cities_l:
            print('Thank you for your input! You have chosen: {}'.format(color.BLUE_BOLD + city.title() + color.END), '\n')
            break
        elif city.lower() in cities_s:
            city = cities_l[cities_s.index(city.lower())]
            print('Thank you for your input! You have chosen: {}'.format(color.BLUE_BOLD + city + color.END), '\n')
            break
        else:
            print('That\'s not a valid city!')

    # setting the filter type: monthly, dayly, or not at all?
    while True:
        type_of_time_filter = input('Would you like to filter the data by month ({0}m{1}), day ({0}d{1}), or not at all ({0}n){1}? '.format(color.BU, color.END))
        if type_of_time_filter.lower() in type_of_filter_s or type_of_time_filter.lower() in type_of_filter_l:
            break
        else:
            print('That\'s not a valid input!')

    # if filter type was set to "monthly" get user input for month (each month or january, february, ... , june). Allow short and long form input.
    if type_of_time_filter.lower() == 'm' or type_of_time_filter.lower() == 'month':
        while True:
            month = input('Which month - January ({0}jan{1}), February ({0}feb{1}), March ({0}mar{1}), April ({0}apr{1}), May ({0}may{1}), or June ({0}jun{1}) or each month ({0}em{1})? '.format(color.BU, color.END))
            if month.title() in months_l:
                print('Thank you for your input! You have chosen: {}'.format(color.BLUE_BOLD + month.title() + color.END), '\n')
                break
            elif month.lower() in months_s:
                month = months_l[months_s.index(month.lower())]
                print('Thank you for your input! You have chosen: {}'.format(color.BLUE_BOLD + month + color.END), '\n')
                break
            elif month.lower() == 'em' or month.lower() == 'each month':
                print('Thank you for your input! You have chosen: {}'.format(color.BLUE_BOLD + 'each month' + color.END), '\n')
                month = 'each_month'
                break
            else:
                print('That\'s not a valid name of a month!')

    # if filter type was set to "daily" get user input for day of the week (each day or monday, tuesday, ... sunday). Allow short and long form input.
    if type_of_time_filter.lower() == 'd' or type_of_time_filter.lower() == 'day':
        while True:
            day = input('Which day - Monday ({0}mo{1}), Tuesday ({0}tu{1}), Wednesday ({0}we{1}), Thursday ({0}th{1}), Friday ({0}fr{1}), Saturday ({0}sa{1}), or Sunday ({0}su{1}) or each day ({0}ed{1})? '.format(color.BU, color.END))
            if day.title() in days_l:
                print('Thank you for your input! You have chosen: {}'.format(color.BLUE_BOLD +  day.title()), '\n' + color.END)
                break
            elif day.lower() in days_s:
                day = days_l[days_s.index(day.lower())]
                print('Thank you for your input! You have chosen: {}'.format(color.BLUE_BOLD + day + color.END), '\n')
                break
            elif day.lower() == 'ed' or day.lower() == 'each day':
                print('Thank you for your input! You have chosen: {}'.format(color.BLUE_BOLD + 'each day' + color.END), '\n')
                day = 'each_day'
                break
            else:
                print('That\'s not a valid name of a day!')

    # handle input 'not at all'
    if type_of_time_filter.lower() == 'n' or type_of_time_filter.lower() == 'not at all':
        print('Thank you for your input! You have chosen: ' + color.BLUE_BOLD + 'no filtering' + color.END)


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # df = df.head(14)
    # print(df)
    return df

def set_dataframe(df, month, day):
    """
    Filters by month and day if applicable.
    Args:
        (DataFrame) df_copy - a copy is needed for cycling through all months/days, when each_month or each_day was chosen
        (str) month_copy - name of the month to filter by, or "all" to apply no month filter
        (str) day_copy - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # filter by month if applicable
    df_copy = df.copy()
    month_copy = month
    day_copy = day
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month_copy = months_l.index(month_copy.title()) + 1
        print('Month: {0}{2}{1}'.format(color.PURPLE, color.END, months_l[month_copy - 1]))

        # filter by month to create the new dataframe
        df_copy = df_copy[df_copy['month'] == month_copy]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        print('Day of week: {0}{2}{1}'.format(color.PURPLE, color.END, day_copy.title()))
        df_copy = df_copy[df_copy['day_of_week'] == day_copy.title()]

    # print(df_copy)
    return df_copy, month_copy, day_copy


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""
    # display the most common month
    if month == 'all':
        popular_month = months_l[df['month'].mode()[0] - 1]
        rents_in_total_month = df['month'].value_counts().max()
        print('The most common month is: {0}{2}{1} with {0}{3}{1} rents in total'.format(color.BLUE_BOLD, color.END, popular_month, rents_in_total_month))


    # display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        rents_in_total_day = df['day_of_week'].value_counts().max()
        print('The most common day of the week is: {0}{2}{1} with {0}{3}{1} rents in total'.format(color.BLUE_BOLD, color.END, popular_day, rents_in_total_day))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    # find the rent count for the most popular hour
    rents_in_total_popular_hour = df['hour'].value_counts().max()
    # display the most common start hour
    print('Most Popular Start Hour: {0}{2}{1} with {0}{3}{1} rents in total'.format(color.BLUE_BOLD, color.END, popular_hour, rents_in_total_popular_hour))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    # find the most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    # find the rent count for the most commonly used start station
    rents_in_total_start_station = df['Start Station'].value_counts().max()
    # display most commonly used start station
    print('Most popular Start Station: {0}{2}{1} with {0}{3}{1} rents in total'.format(color.BLUE_BOLD, color.END, popular_start_station, rents_in_total_start_station))

    # find the most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    # find the rent count for the most commonly used end station
    rents_in_total_end_station = df['End Station'].value_counts().max()
    # display most commonly used end station
    print('Most popular End Station: {0}{2}{1} with {0}{3}{1} rents in total'.format(color.BLUE_BOLD, color.END, popular_end_station, rents_in_total_end_station))

    # arithmetic operation (sum) of columns "Start Station" and "End Station"
    df['start_end_combination'] = df['Start Station'] + ' -- ' + df['End Station']
    # find most frequent combination of start station and end station trip
    popular_start_end_combination = df['start_end_combination'].mode()[0]
    # find the rent count for the most frequent combination of start station and end station trip
    rents_in_total_start_end_combination = df['start_end_combination'].value_counts().max()
    # display most frequent combination of start station and end station trip
    print('Most popular combination of Start and End station Trip: {0}{2}{1} with {0}{3}{1} rents in total'.format(color.BLUE_BOLD, color.END, popular_start_end_combination, rents_in_total_start_end_combination))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    print('Total travel time of all trips for the chosen time set in years: ', color.BLUE_BOLD + str(total_trip_duration / 31536000) + color.END)

    # display mean travel time
    mean_trip_duration = df['Trip Duration'].mean()
    print('Mean travel time of all trips for the chosen time set in minutes: ', color.BLUE_BOLD + str(mean_trip_duration / 60) + color.END)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    # Display counts of user types
    user_types = df['User Type'].value_counts(dropna=False)
    print('Counts of user types: ')
    for user_type in range(len(user_types.index)):
        print(user_types.index[user_type], '--', color.BLUE_BOLD + str(user_types[user_type]) + color.END)
    print('dtype of raw data in column \'User Type\': ', user_types.dtype)


    # Display counts of gender
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts(dropna=False)
        print('\nCounts of gender: ')
        for gender_type in range(len(gender.index)):
            print(gender.index[gender_type], '--', color.BLUE_BOLD + str(gender[gender_type]) + color.END)
        print('dtype of raw data in column \'Gender\': ', df['Gender'].dtype)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nThe earlist year of birth: ', color.BLUE_BOLD +  str(int(earliest_birth_year))+ color.END)
        print('The most recent year of birth: ', color.BLUE_BOLD +  str(int(most_recent_birth_year))+ color.END)
        print('The most common year of birth: ', color.BLUE_BOLD +  str(int(most_common_birth_year))+ color.END)
        print('dtype of raw data in column \'Birth Year\': ', df['Birth Year'].dtype)


def timer_start():
    """ Start timer for calculation duration """

    start_time = time.time()
    return start_time

def timer_end(start_time):
    """ End timer fo rcalculation duration """

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main_routine(df, month, day, set_list):
    """ This function calls the function set_dataframe to reload the dataframe based on the specific day or month.
        The actual dataframe is stored in df_set. This data_frame will be passed to the statistics function (time_stats(...), station_stats(...), etc. )for further calculations.
        For each statistics section the timer functions timer_start() and timer_end(start_time) will be called tto measure the calculation duration.
    """
    print('\n{}Calculating The Most Frequent Times of Travel...{}\n'.format(color.BOLD, color.END))
    for x in set_list:
        if set_list == months_l:
            month = x
        if set_list == days_l:
            day = x
        df_set, month_set, day_set = set_dataframe(df, month, day)
        start_time = timer_start()
        time_stats(df_set, month_set, day_set)
        timer_end(start_time)

    print('\n{}Calculating The Most Popular Stations and Trip...{}\n'.format(color.BOLD, color.END))
    for x in set_list:
        if set_list == months_l:
            month = x
        if set_list == days_l:
            day = x
        df_set, month_set, day_set = set_dataframe(df, month, day)
        start_time = timer_start()
        station_stats(df_set)
        timer_end(start_time)

    print('\n{}Calculating Trip Duration...{}\n'.format(color.BOLD, color.END))
    for x in set_list:
        if set_list == months_l:
            month = x
        if set_list == days_l:
            day = x
        df_set, month_set, day_set = set_dataframe(df, month, day)
        start_time = timer_start()
        trip_duration_stats(df_set)
        timer_end(start_time)

    print('\n{}Calculating User Stats...{}\n'.format(color.BOLD, color.END))
    for x in set_list:
        if set_list == months_l:
            month = x
        if set_list == days_l:
            day = x
        df_set, month_set, day_set = set_dataframe(df, month, day)
        start_time = timer_start()
        user_stats(df_set)
        timer_end(start_time)

    display_data(df)

def display_data(df):
    row_counter = 0
    inc = 5
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:

        if row_counter == len(df.index):
            print('End of dataset')
            break

        raw_data_request = input('Would you like to view individual trip data? Type yes ({0}y{1}) or no ({0}n{1}) '.format(color.BU, color.END))

        if raw_data_request.lower() == 'yes' or raw_data_request.lower() == 'y' and row_counter < len(df.index):
            print(df.iloc[row_counter : row_counter + inc])
            row_counter += inc

            if row_counter  >= len(df.index):
                row_counter = row_counter - inc
                inc = len(df.index) - row_counter
                print(df.iloc[row_counter : row_counter + inc])
                row_counter += inc

        elif raw_data_request.lower() == 'no' or raw_data_request.lower() == 'n':
            break
        else:
            print('That\'s not a valid input!')

def main():
    """ Main function. As long as user restarts the program the while loop is True, the program continues. """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if month != 'each_month' and day != 'each_day':
            set_list = ['']

        elif month == 'each_month':
            set_list = months_l

        elif day == 'each_day':
            set_list = days_l

        # jump to main routine. Further program progrssion is determined by the filter mode.
        # "each_month" for month = 'each_month' --> set_list = months_l
        # "each_day" for day = 'each day' --> set_list = days_l
        # certain day --> set_list = ['']
        # "all" --> set_list = ['']
        main_routine(df, month, day, set_list)



        """ ******************************************************************** """

        restart = input('\nWould you like to restart? Enter yes (y) or no (\'any key\').\n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
