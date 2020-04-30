import time
import pandas as pd
import numpy as np


city_data = 			{'chicago': 'chicago.csv', 'new york': 'new_york.csv',
						'washington': 'washington.csv'}


months_of_the_year =    {'January': 1, 'February': 2, 'March':3,
                        'April': 4,'May': 5, 'June': 6, 'All': 'All'}

months_index =          {1: 'January', 2: 'February', 3: 'March',
				        4: 'April', 5: 'May', 6: 'June'}

days_of_the_week =      {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday':
 			            3,'Friday': 4, 'Saturday': 5, 'Sunday': 6, 'All': 'All'}

days_index =            {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3:
                        'Thursday',4: 'Friday', 5: 'Saturday', 6: 'Sunday'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - city to investigate
        (str) month - month to investigate, or "None" to apply no month filter
        (str) day - day of week to investigate, or "None" to apply no day filter
    """
    print('Hello! Let\'s explore some bikeshare data!')
    print("Please Press Ctrl + C if you DO NOT wish to continue")

    city_found, month_found, day_found = False, False, False

    filter_by =	"month"
    month = ""
    day = ""

    while True:

        # get user input for city (chicago, new york city, washington).
        if not city_found:
            city = input('Would you like to see data for Chicago, Washington, or New York?:')
            city = city.lower()
            if city not in city_data:
                print('No data is available for this city, please select from the cities listed:')
                continue
            else:
                city_found = True
                filter_by = input('would you like to filter by Month, Day, or Both?')
                filter_by = filter_by.lower()


        print('\n')

        if filter_by == "month" or filter_by == "both" :
            # to get user input for month ( January, February, ... , June, and All)
            if not month_found:
                month = input('Enter month to investigate \nJanuary, February, March, April, May, June, All?:')
                month = month.title()

                if month not in months_of_the_year:
                    print("Invalid month entered! Please enter a valid month or All")
                    continue
                elif filter_by == "both":
                     month_found = True
                else:
                    month_found = True
                    break

        print('\n')

        if filter_by == "day" or filter_by == "both":
            # to get user input for day of week (monday, tuesday, ... sunday, and None)
            day = input("Enter the day you want to investigate \nMonday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, All ?: ")
            day = day.title()

            if day not in days_of_the_week:
                print("Invalid day entered! Please enter a valid day or All")
                continue
            else:
                break

    print('-' * 40)
    print('\n')

    return city, month, day,filter_by


def load_data(city, month, day,filter_by):
    """
    To load data for the specified city and search by month and day if applicable.

    Args:
        (str) city - name of the city to investigate
        (str) month - name of the month to investigate, or "all" to select aggregate
        (str) day - name of the day of week to investigate by, or "all" to aggregate
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    start_time = time.time()
    print("Please wait for results...")

    df = pd.read_csv(city_data.get(city))

    # to get Start Month, Day, and Hour from Start Time column
    df['Start Month'] = pd.DatetimeIndex(df['Start Time']).month

    df['Start Day'] = pd.to_datetime(df['Start Time'], format='%Y-%m-%d %H:%M:%S').dt.dayofweek

    df['Start Hour'] = pd.DatetimeIndex(df['Start Time']).hour

    # using month as filter criteria, if month is specified
    if filter_by == 'month' or filter_by == 'both':
        if month != months_of_the_year.get('All'):
            df = df[df['Start Month'] == int(months_of_the_year.get(month))]

    # using day as filter criteria, if day is specified
    if filter_by == 'day' or filter_by == 'both':
        if day != days_of_the_week.get('All'):
            df = df[df['Start Day'] == int(days_of_the_week.get(day))]

    print("\nComputed in  %s seconds." % (time.time() - start_time))
    return df


def time_stats(df, month, day):
    """To displays stats on most frequent travel times"""

    print('\nComputing the most frequent times of travel...\n')
    start_time = time.time()

    # to display the most common month
    if month == months_of_the_year.get('All'):
        common_month = df['Start Month'].dropna()
        if common_month.empty:
            print("No common month found based on your selected criteria. Please check and try again")
        else:
            common_month = common_month.mode()[0]
            print('The most common month for renting is: {}'.format(months_index.get(common_month)))
    else:
        print('Sorry, no data available because the search scope is limited to {}'.format(month))

    # to display the most common day
    if day == days_of_the_week.get('All'):
        common_day = df['Start Day'].dropna()  #.mode()[0]
        if common_day.empty:
            print('No common day found for the filters chosen!! Please adjust your filter!!!')
        else:
            common_day = common_day.mode()[0]
            print('Most popular day for renting is:{}'.format(days_index.get(common_day)))
    else:
        print('Sorry, no data available because the search scope is limited to {}'.format(day.title()))

    # to display the most common start hour
    common_start_hour = df['Start Hour'].dropna()
    if common_start_hour.empty:
        print('No common start hour found based on your selected criteria. Please check and try again')
    else:
        common_start_hour = common_start_hour.mode()[0]
        print('Most common renting start hour is: {}:00 hrs'.format(common_start_hour))

    print("\nComputed in  %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """To display the most popular stations and trip stats."""

    print('\nComputing the most popular stations and trips...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station']
    if most_common_start_station.empty:
        print('No \'Start Station\' data available for the entered criteria, please check and try again')
    else:
        most_common_start_station = most_common_start_station.mode()[0]
        print('The most common start station is: {}'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station']
    if most_common_end_station.empty:
        print('No \'End Station\' data available for the entered criteria, please check and try again')
    else:
        most_common_end_station = most_common_end_station.mode()[0]
        print('The most common end station is: {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    most_common_start_and_end_station = df[['Start Station', 'End Station']].dropna()
    if most_common_start_and_end_station.empty:
        print('data available for the entered criteria, please check and try again')
    else:
        most_common_start_and_end_station = most_common_start_and_end_station.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
        trip_count = most_common_start_and_end_station.iloc[0]
        stations = most_common_start_and_end_station[most_common_start_and_end_station == trip_count].index[0]

        start_station, end_station = stations
        print('The most common start station is: {} and end station is: {}, put together were part of the trips {} times'.format(start_station, end_station, trip_count))

    print("\nComputed in  %s seconds." % (time.time() - start_time))
    print('-' * 40)


def total_travel_time(df):
    """To display bikeshare total and average trip duration stats."""

    print('\nComputing trip duration...\n')
    start_time = time.time()

    # display total travel time
    valid_time = df['Trip Duration'].dropna()
    if valid_time.empty:
        print('No data available, Please check and try again')
    else:
        total_time = valid_time.sum()
        print('Total travel time in seconds is: {}'.format(total_time))

        # display mean travel time
        mean_travel_time = valid_time.mean()

    print("\nComputed in  %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_counts(df):
    """To display bikeshare users stats"""

    print('\nComputing user stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].dropna()

    if user_type.empty:
        print('No data available for the entered criteria, please check and try again')
    else:
        user_type = user_type.value_counts()
        print('The user type details for the filter chosen is: {}'.format(user_type))

    # Display counts of gender
        if 'Gender' in df:
            user_gender = df['Gender'].dropna()
            if user_gender.empty:
                print('No data available for the entered criteria, please check and try again')
            else:
                user_gender = user_gender.value_counts()
                print('User gender count is: {}'.format(user_gender))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        birth_years = df['Birth Year'].dropna()
        if birth_years.empty:
            print('No data available for the entered criteria, please check and try again')
        else:
            user_birth_year = df['Birth Year'].dropna()
            if user_birth_year.empty:
                print('No data available for the entered criteria, please check and try again')
            else:
                oldest_user = user_birth_year.min()
                print('The oldest birth year is: {}'.format(int(oldest_user)))

                youngest_user = user_birth_year.max()
                print('The most recent birth year is: {}'.format(int(youngest_user)))

                most_common_year_of_birth = user_birth_year.mode()[0]
                print('The most common birth year is: {}'.format(int(most_common_year_of_birth)))

    print("\nComputed in  %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_raw_data(df):
    '''To print the selected data frame, 5 at a time '''
    choice = input("Would you like to see some raw data? [y/n] : ")
    choice = choice.lower()

    count = 0
    if choice == 'y':
        for row in df.iterrows():
            print(row)
            count += 1
            if count != 0 and count % 5 == 0:
                choice = input("Would you like to see some raw data? [y/n] : ")
                if choice.lower() != 'y':
                    break


def main():
    while True:
        city, month, day, filter_by = get_filters()
        print("RESULTS FOR FILTERS: City:{}, Month:{}, Day:{}".format(city, month, day))

        df = load_data(city, month, day, filter_by)

        if df.empty:
            print('No data for selected criteria, enter the right criteria and TRY AGAIN')
            continue

        time_stats(df, month, day)
        station_stats(df)
        total_travel_time(df)
        user_counts(df)

        show_raw_data(df)

        restart = input('\nWould you like to restart? [y/n].\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
    main()
