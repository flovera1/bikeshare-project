import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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

    try:
        df = pd.read_csv(CITY_DATA[city])
    except FileNotFoundError:
        print(f"Error: File for {city} not found.")
        return pd.DataFrame()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_index = MONTHS.index(month)
        df = df[df['month'] == month_index]
        if df.empty:
            print("No data available for the selected filters.")

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

    df['hour'].value_counts().sort_index().plot(kind='bar')
    plt.title("Trips by Hour")
    plt.xlabel("Hour")
    plt.ylabel("Count")
    plt.show()

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

def display_raw_data(df):
    """Displays raw data in chunks of 5 rows upon user request."""
    i = 0
    pd.set_option('display.max_columns', None)

    while True:
        # Input validation loop
        while True:
            raw = input('Would you like to see 5 lines of raw data? Enter yes or no: ').lower()
            if raw in ['yes', 'no']:
                break
            print("Invalid input. Please enter yes or no.")

        if raw == 'no':
            break

        print(df.iloc[i:i+5])
        i += 5

        if i >= len(df):
            print("No more data to display.")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
            print("No data loaded. Restarting...")
            continue

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data(df) 

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()