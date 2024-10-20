# Real-Time Weather Monitoring System

This project is a real-time data processing system that fetches weather data from the OpenWeatherMap API, processes it, and generates daily weather summaries. The system can trigger alerts based on user-configurable thresholds for temperatures or weather conditions.

## Features

- Real-time weather data retrieval using OpenWeatherMap API
- Daily rollups and summaries (average, max, min temperature, dominant weather)
- User-configurable alert thresholds
- Temperature conversion (Kelvin to Celsius/Fahrenheit)
- Visualizations for weather trends and alerts
- Dockerized deployment for easy setup

## Design Choices

- **Python**: Chosen for its wide range of libraries (SQLAlchemy, requests, schedule, matplotlib) and ease of use for API interaction and data processing.
- **SQLAlchemy ORM**: For database interaction and easy query execution.
- **Docker & Docker Compose**: To ensure the application can run in isolated environments without worrying about local setups.
- **SQLite/PostgreSQL**: SQLite for local development, PostgreSQL for production, using Docker for easy management.

## Dependencies

- Python 3.8 or higher
- Docker and Docker Compose
- OpenWeatherMap API key (you can sign up [here](https://home.openweathermap.org/users/sign_up))

### Python Libraries:
These can be installed using `pip`:

```bash
pip install -r requirements.txt
