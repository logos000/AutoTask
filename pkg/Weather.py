import requests
from pathlib import Path
from graiax import silkcoder



def get_weather(location: str, api_key ) -> str:
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=1&aqi=no&alerts=no"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        location_name = weather_data['location']['name']
        current_temp_c = weather_data['current']['temp_c']
        condition = weather_data['current']['condition']['text']
        forecast = weather_data['forecast']['forecastday'][0]
        max_temp_c = forecast['day']['maxtemp_c']
        min_temp_c = forecast['day']['mintemp_c']
        clothing_advice = get_clothing_advice(max_temp_c, min_temp_c)
        
        weather_report = (
            f"Hi! The weather in {location_name} is currently {condition} with a temperature of {current_temp_c}°C.\n"
            f"Today's forecast:\n"
            f"Max temperature: {max_temp_c}°C\n"
            f"Min temperature: {min_temp_c}°C\n"
            f"Clothing advice: {clothing_advice}\n"
        )
        return weather_report
    except Exception as e:
        print("[Weather] Error getting weather: {}".format(e))
        return "Error getting weather data."
    
def get_clothing_advice(max_temp, min_temp) -> str:
    if max_temp > 30:
        return "It's very hot today. Wear light and breathable clothing."
    elif 20 < max_temp <= 30:
        return "The weather is warm. A t-shirt and jeans would be suitable."
    elif 10 < max_temp <= 20:
        return "It's a bit cool. Consider wearing a jacket."
    else:
        return "It's quite cold. Wear a coat and stay warm."