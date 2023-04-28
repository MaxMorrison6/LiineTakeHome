import re
from datetime import datetime
import pandas as pd
from fastapi import FastAPI

app = FastAPI()
restaurants = {}
hours_file = pd.read_csv('hours.csv')


def parse_restaurants():
    """
    Parses restaurant hours from a CSV file and stores them in a dictionary.
    """
    for _, row in hours_file.iterrows():
        name = row['Restaurant Name']
        hours_str = row['Hours']
        hours_dict = parse_hours(hours_str)
        if name not in restaurants:
            restaurants[name] = {}
        restaurants[name].update(hours_dict)


def parse_hours(hours_str):
    """
    Parses a string containing a restaurant's opening hours and returns a dictionary with each day of the week and its
    corresponding opening hours.
    """
    days_of_week = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hours_dict = {day: "" for day in days_of_week}
    for day_range, times in re.findall(r"([a-zA-Z]{3}-?[a-zA-Z]{0,3})\s+([0-9: apm-]+)", hours_str):
        days = day_range.split("-")
        start_time, end_time = map(str.strip, times.split("-"))
        hours_range = f"{start_time} - {end_time}"
        if len(days) == 1:
            hours_dict[days[0]] = hours_range
        else:
            start_day_idx = days_of_week.index(days[0])
            end_day_idx = days_of_week.index(days[-1])
            for i in range(start_day_idx, end_day_idx + 1):
                hours_dict[days_of_week[i]] = hours_range
    return hours_dict


parse_restaurants()


def get_open_restaurants(dt):
    """
    Returns a list of restaurants that are open at a given date and time.
    """
    day_of_week = dt.strftime("%a")  # get day of week abbreviation
    if day_of_week == "Tue":
        day_of_week = "Tues"
        # built in datetime doesn't like Tues
    meal_time = dt.strftime("%I:%M %p").lstrip('0')  # get time in 12-hour format

    open_restaurants = []

    for restaurant, hours in restaurants.items():
        if hours[day_of_week] != "":  # if the restaurant is open on this day
            open_hours = hours[day_of_week].split(" - ")  # split the opening and closing times
            if open_hours[0] <= meal_time < open_hours[1]:  # if the current time is between opening and closing times
                open_restaurants.append(restaurant)

    if not open_restaurants:
        return "Nothing open!"

    return open_restaurants


@app.get("/get_food")
def get_food(meal_time: datetime):
    """
    API endpoint that returns a list of restaurants that are open at a given date and time.
    """
    return get_open_restaurants(meal_time)
