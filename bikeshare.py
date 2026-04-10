import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all','january','february','march','april','may','june']
DAYS = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Enter city (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please try again.")

    while True:
        month = input("Enter month (all, january, february, march, april, may, june): ").lower()
        if month in MONTHS:
            break
        else:
            print("Invalid month. Please try again.")

    while True:
        day = input("Enter day of week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday): ").lower()
        if day in DAYS:
            break
        else:
            print("Invalid day. Please try again.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """

    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_index = MONTHS.index(month)
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print("Most common month:", common_month)

    common_day = df['day_of_week'].mode()[0]
    print("Most common day of week:", common_day)

    common_hour = df['hour'].mode()[0]
    print("Most common start hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    start_station = df['Start Station'].mode()[0]
    print("Most common start station:", start_station)

    end_station = df['End Station'].mode()[0]
    print("Most common end station:", end_station)

    df['trip'] = df['Start Station'] + " -> " + df['End Station']
    common_trip = df['trip'].mode()[0]
    print("Most common trip:", common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    print("Total travel time:", total_time)

    mean_time = df['Trip Duration'].mean()
    print("Mean travel time:", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print("User Types:")
    print(df['User Type'].value_counts())

    if 'Gender' in df.columns:
        print("\nGender Counts:")
        print(df['Gender'].value_counts())

    if 'Birth Year' in df.columns:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])

        print("\nEarliest Birth Year:", earliest)
        print("Most Recent Birth Year:", recent)
        print("Most Common Birth Year:", common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()