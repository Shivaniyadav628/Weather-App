# weather_step.py
# Weather App using OpenWeatherMap API

import requests
import csv
import os

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CSV_FILE = "weather_history.csv"

API_KEY = os.getenv("OPENWEATHER_API_KEY")
print("DEBUG API KEY:", API_KEY)

# ---------------- CSV INITIALIZATION ----------------

if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "City",
            "Temperature",
            "Condition",
            "Humidity",
            "Wind Speed"
        ])

# ---------------- FUNCTIONS ----------------

def save_to_csv(city, temp, condition, humidity, wind):
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([city, temp, condition, humidity, wind])


def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        data = response.json()

        if response.status_code != 200:
            print(f" Error: {data.get('message', 'Invalid city name')}\n")
            return

        temp = data["main"]["temp"]
        condition = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        print(f"\n Weather in {city}")
        print(f" Temperature : {temp}°C")
        print(f" Condition   : {condition}")
        print(f" Humidity    : {humidity}%")
        print(f" Wind Speed  : {wind} m/s\n")

        save_to_csv(city, temp, condition, humidity, wind)

    except requests.exceptions.RequestException:
        print(" Network error. Please check your internet connection.\n")
    except Exception as e:
        print(" Unexpected error:", e, "\n")


def show_history():
    if not os.path.exists(CSV_FILE):
        print("No history available.\n")
        return

    print("\n Weather History")
    print("-" * 40)

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(
                f"{row['City']} | {row['Temperature']}°C | {row['Condition']} | "
                f"Humidity: {row['Humidity']}% | Wind: {row['Wind Speed']} m/s"
            )
    print()


def analytics():
    if not os.path.exists(CSV_FILE):
        print("No data to analyze.\n")
        return

    temperatures = []
    cities = []

    with open(CSV_FILE, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            temperatures.append(float(row["Temperature"]))
            cities.append(row["City"])

    if not temperatures:
        print("No data available.\n")
        return

    avg_temp = sum(temperatures) / len(temperatures)
    max_temp = max(temperatures)
    min_temp = min(temperatures)

    hottest_city = cities[temperatures.index(max_temp)]
    coldest_city = cities[temperatures.index(min_temp)]

    print("\n Weather Analytics")
    print("-" * 30)
    print(f"Average Temperature : {avg_temp:.2f}°C")
    print(f"Hottest City        : {hottest_city} ({max_temp}°C)")
    print(f"Coldest City        : {coldest_city} ({min_temp}°C)")
    print(f"Total Queries       : {len(temperatures)}\n")

# ---------------- MAIN PROGRAM ----------------

def main():
    print("=== 🌦 Weather App (STEP Ready) ===")

    while True:
        print("1. Get Weather")
        print("2. Show History")
        print("3. Analytics")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            city = input("Enter city name: ").strip()
            if city:
                get_weather(city)
            else:
                print(" City name cannot be empty.\n")

        elif choice == "2":
            show_history()

        elif choice == "3":
            analytics()

        elif choice == "4":
            print("👋 Exiting Weather App. Goodbye!")
            break

        else:
            print(" Invalid choice! Please enter 1–4.\n")


if __name__ == "__main__":
    main()