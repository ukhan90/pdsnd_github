import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def check_input(input_str,input_type):
    """
    check the validity of user input.
    input_str: is the input of the user
    input_type: is the type of input: 1 = city, 2 = month, 3 = day
    """
    while True:
        input_read=input(input_str)
        try:
            if input_read in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif input_read in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif input_read in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Sorry, your input should be: chicago, new york city or washington")
                if input_type == 2:
                    print("Sorry, your input should be: january, february, march, april, may, june or all")
                if input_type == 3:
                    print("Sorry, your input should be: sunday, ... friday, saturday or all")
        except ValueError:
            print("Sorry, your input is wrong")
    return input_read

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello there! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = check_input("Which city data would you like to see: chicago, new york city or washington? \n Input is not case sensitive\n",1)
    # get user input for month (all, january, february, ... , june)
    month = check_input("For which Month (all, january, ... june)? \n Input is not case sensitive\n", 2)
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_input("For which day? (all, monday, tuesday, ... sunday) \n Input is not case sensitive\n", 3)
    print('-'*80)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most popular month:', popular_month)

    # display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]

    print('Most popular day of week:', popular_day_of_week)

    # display the most common start hour
    popular_common_start_hour = df['hour'].mode()[0]

    print('Most popular start hour:', popular_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Most popular end Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    group_field=df.groupby(['Start Station','End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most popular combination of Start Station and End Station trip:\n', popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('Total travel time:', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    print('Mean travel time:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type Stats:')
    print(df['User Type'].value_counts())
    if city != 'washington':
        # Display counts of gender
        print('Gender Profile:')
        print(df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print('Birth year stats:')
        most_common_year = df['Birth Year'].mode()[0]
        print('Most common birth year:',most_common_year)
        most_recent_year = df['Birth Year'].max()
        print('Most recent birth year:',most_recent_year)
        earliest_year = df['Birth Year'].min()
        print('Earliest Year:',earliest_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nIf you like to restart then enter yes or no.\n Input is not case sensitive \n"')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
