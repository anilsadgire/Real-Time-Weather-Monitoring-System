from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date

# Define the base for SQLAlchemy
Base = declarative_base()

# Define the Weather table to store raw weather data
class Weather(Base):
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    main = Column(String)
    temp = Column(Float)
    feels_like = Column(Float)
    timestamp = Column(DateTime)

# Define the DailySummary table to store daily rollups
class DailySummary(Base):
    __tablename__ = 'daily_summary'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    date = Column(Date)
    avg_temp = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    dominant_condition = Column(String)

# Create the SQLite database and tables
engine = create_engine('sqlite:///weather_data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

import requests

API_KEY = "f4c79cd7a0a31377ca075dbc5afb0d12"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
cities = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def get_weather_data(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 400:
        data = response.json()
        weather = {
            "city": city,
            "main": data['weather'][0]['main'],
            "temp": kelvin_to_celsius(data['main']['temp']),
            "feels_like": kelvin_to_celsius(data['main']['feels_like']),
            "dt": data['dt']
        }
        return weather
    else:
        print(f"Failed to get data for {city}")
        return None

from datetime import datetime

def store_weather_data(weather_data):
    weather_entry = Weather(
        city=weather_data['city'],
        main=weather_data['main'],
        temp=weather_data['temp'],
        feels_like=weather_data['feels_like'],
        timestamp=datetime.fromtimestamp(weather_data['dt'])
    )
    session.add(weather_entry)
    session.commit()

from sqlalchemy import func

def calculate_daily_summary(city):
    today = date.today()
    results = session.query(Weather).filter(
        Weather.city == city, 
        func.date(Weather.timestamp) == today
    ).all()

    if results:
        temps = [r.temp for r in results]
        main_conditions = [r.main for r in results]
        dominant_condition = max(set(main_conditions), key=main_conditions.count)
        
        avg_temp = sum(temps) / len(temps)
        max_temp = max(temps)
        min_temp = min(temps)

        summary = DailySummary(
            city=city, 
            date=today, 
            avg_temp=avg_temp, 
            max_temp=max_temp, 
            min_temp=min_temp,
            dominant_condition=dominant_condition
        )
        session.add(summary)
        session.commit()

ALERT_THRESHOLD = 35  # Example threshold: temperature above 35°C

def check_alerts(weather_data):
    if weather_data['temp'] > ALERT_THRESHOLD:
        print(f"Alert! {weather_data['city']} temperature exceeds {ALERT_THRESHOLD}C: {weather_data['temp']}C")
        # Email notification logic can go here using smtplib

import schedule
import time

def monitor_weather():
    for city in cities:
        weather_data = get_weather_data(city)
        if weather_data:
            store_weather_data(weather_data)
            check_alerts(weather_data)

# Schedule the monitoring function to run every 5 minutes
schedule.every(1).minutes.do(monitor_weather)

# Continuously run the scheduled jobs
while True:
    schedule.run_pending()
    time.sleep(1)

