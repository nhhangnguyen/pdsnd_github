import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input("Enter the city (e.g., chicago, new york city, washington): ").lower()
        if city == 'chicago' or city == 'new york city' or city == 'washington':
            break
        else:
            print('Please enter chicago, new york city, or washington')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Enter the month (e.g., all, january, february, ... , june): ").lower()
        if month == 'all' or month == 'january' or month == 'february' or month == 'march' or month == 'april' or month == 'may' or month == 'june' :
            break
        else:
            print('Please enter all, january, february, ... , or june')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Enter the day (e.g., all, monday, tuesday, ... sunday): ").lower()
        if day == 'all' or day == 'monday' or day == 'tuesday'  or day == 'wednesday' or day == 'thursday'  or day == 'friday' or day == 'saturday' or day == 'sunday':
            break
        else:
            print('Please enter all, monday, tuesday, ..., or sunday')


    print('-'*40)
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    #df['month'] = df['Start Time'].dt.month_name()
    #df['day_of_week'] = df['Start Time'].dt.day_name()

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
    most_common_month = df['month'].mode()[0]
    print('\nThe most common month: ',most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('\nThe most common day of week: ',most_common_day_of_week)

    #extract hour from Start Time to create a new column
    df['start_hour'] = df['Start Time'].dt.hour
    # display the most common start hour
    most_common_start_hour = df['start_hour'].mode()[0]
    print('\nThe most common start hour: ',most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('\nThe most common start station: ',most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('\nThe most common end station: ',most_common_end_station)


    # display most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    most_frequent_trip = df['trip'].mode()[0]
    print('\nThe most frequent combination of start station and end station trip: ',most_frequent_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # convert the End Time column to datetime
    df['End Time'] = pd.to_datetime(df['End Time'])

    # display total travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    total_travel_time = df['Travel Time'].sum()
    print('\nTotal travel time: ',total_travel_time)

    # display mean travel time
    mean_travel_time = df['Travel Time'].mean()
    print('\nMean travel time: ',mean_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nValue counts for each user type:\n',user_types)

    # Display counts of gender
    if city == 'washington':
        print(f'\nCount of each gender: No gender information for {city}')
    else:
        count_genders = df['Gender'].value_counts()
        print('\nCount of each gender:\n',count_genders)


    # Display earliest, most recent, and most common year of birth
    if city == 'washington':
        print(f'\nThe earliest, most recent, and most common year of birth: No year of birth information for {city}')
    else:
        print('\nThe earliest year of birth: ',int(df['Birth Year'].min()))
        print('\nThe most recent year of birth: ',int(df['Birth Year'].max()))
        print('\nThe most common year of birth: ',int(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if len(df) == 0:
            print('No data for the input city, month, and day')
            continue
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        counter = 0
        rows_per_display = 5
        total_rows = len(df)

        while True:
            if counter == 0:
                see_5_lines = input('\nWould you like to see the first 5 lines of raw data? Enter yes or no.\n')
            else:    
                see_5_lines = input('\nWould you like to see the next 5 lines of raw data? Enter yes or no.\n')
            
            if see_5_lines.lower() != 'yes':
                print('You chose not to see more raw data. Exiting raw data display')
                break
            end = counter + rows_per_display
            if end > total_rows:
                end = total_rows
    
            print(f'\nDisplaying rows {counter + 1} to {end} of {total_rows}:\n')
            print(df[counter:end])

            counter = end

            if counter >= total_rows:
                print('\nThe last row has been reached. No more raw data to display')
                break


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Exiting the program. Thank you!')
            break


if __name__ == "__main__":
	main()
