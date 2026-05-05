import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Weather Intelligence Platform | Suyash Magdum",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Font Awesome only (no emojis)
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #1e3c72;
            --secondary: #2a5298;
            --accent: #00a8ff;
            --dark: #2c3e50;
            --light: #f8f9fa;
        }
        
        .main {
            background-color: var(--light);
        }
        
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            border-left: 4px solid var(--primary);
            transition: transform 0.2s;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
        }
        
        .metric-title {
            font-size: 14px;
            color: #6c757d;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: var(--dark);
        }
        
        .metric-delta {
            font-size: 12px;
            margin-top: 8px;
        }
        
        .section-header {
            border-left: 4px solid var(--accent);
            padding-left: 15px;
            margin: 20px 0 15px 0;
        }
        
        .developer-credit {
            text-align: center;
            padding: 10px;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            border-radius: 8px;
            margin-top: 20px;
        }
        
        .info-box {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        
        .impact-box {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            border-radius: 12px;
            padding: 20px;
            color: white;
        }
        
        .footer {
            text-align: center;
            padding: 20px;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown(f"""
    <div style="text-align: center; margin-bottom: 30px;">
        <i class="fas fa-cloud-sun" style="font-size: 48px; color: #2a5298;"></i>
        <h1 style="margin: 10px 0 5px 0;">Weather Intelligence Platform</h1>
        <p style="color: #6c757d;">Real-Time Business Weather Analytics | Enterprise Dashboard</p>
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: inline-block; padding: 5px 20px; border-radius: 20px; margin-top: 10px;">
            <i class="fas fa-user-circle"></i> Developed by: Suyash Magdum | Data Analyst
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 20px;">
            <i class="fas fa-chart-line" style="font-size: 32px; color: #00a8ff;"></i>
            <h3 style="margin-top: 10px;">Dashboard Controls</h3>
            <hr>
            <p style="font-size: 12px; color: #6c757d;">
                <i class="fas fa-user"></i> Suyash Magdum<br>
                <i class="fas fa-chart-bar"></i> Data Analyst Portfolio
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<i class="fas fa-key"></i> API Configuration', unsafe_allow_html=True)
    api_key = st.text_input("OpenWeatherMap API Key", type="password", label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown('<i class="fas fa-map-marker-alt"></i> Location', unsafe_allow_html=True)
    city = st.text_input("City Name", "Pune", label_visibility="collapsed")
    
    popular_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"]
    selected_city = st.selectbox("Quick Select", ["-- Choose --"] + popular_cities)
    if selected_city != "-- Choose --":
        city = selected_city
    
    st.markdown("---")
    
    st.markdown('<i class="fas fa-sliders-h"></i> Settings', unsafe_allow_html=True)
    auto_refresh = st.checkbox("Auto Refresh (30s)", value=True)
    units = st.radio("Temperature Unit", ["Celsius (C)", "Fahrenheit (F)"], horizontal=True)
    
    st.markdown("---")
    
    with st.expander("About Developer"):
        st.markdown("""
        **Suyash Magdum**  
        Data Analyst
        
        Business Intelligence Specialist  
        Real-time Data Analytics  
        Python | SQL | Streamlit  
        Predictive Modeling
        """)

# Unit conversion
unit_symbol = "metric" if "Celsius" in units else "imperial"
temp_unit = "C" if "Celsius" in units else "F"

@st.cache_data(ttl=30)
def fetch_current_weather(api_key, city, units):
    if not api_key:
        return None
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units={units}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

@st.cache_data(ttl=30)
def fetch_forecast(api_key, city, units):
    if not api_key:
        return None
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units={units}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

# Fetch data
current_data = fetch_current_weather(api_key, city, unit_symbol)
forecast_data = fetch_forecast(api_key, city, unit_symbol)

if current_data:
    # Extract data
    temp = current_data['main']['temp']
    feels_like = current_data['main']['feels_like']
    humidity = current_data['main']['humidity']
    wind_speed = current_data['wind']['speed']
    pressure = current_data['main']['pressure']
    weather_desc = current_data['weather'][0]['description'].title()
    
    # KPI Row
    st.markdown('<div class="section-header"><i class="fas fa-chart-simple"></i> Key Performance Indicators</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title"><i class="fas fa-thermometer-half"></i> Temperature</div>
                <div class="metric-value">{temp:.1f}°{temp_unit}</div>
                <div class="metric-delta">Feels like {feels_like:.1f}°{temp_unit}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title"><i class="fas fa-tint"></i> Humidity</div>
                <div class="metric-value">{humidity}%</div>
                <div class="metric-delta">{'Normal' if humidity < 70 else 'Elevated'}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title"><i class="fas fa-wind"></i> Wind Speed</div>
                <div class="metric-value">{wind_speed:.1f} m/s</div>
                <div class="metric-delta">{'Calm' if wind_speed < 5 else 'Windy'}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title"><i class="fas fa-cloud-sun"></i> Conditions</div>
                <div class="metric-value">{weather_desc}</div>
                <div class="metric-delta">Pressure: {pressure} hPa</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Location Details
    st.markdown('<div class="section-header"><i class="fas fa-location-dot"></i> Location Intelligence</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class="info-box">
                <i class="fas fa-city" style="font-size: 20px; color: #2a5298;"></i>
                <h4 style="display: inline; margin-left: 10px;">Geographic Information</h4>
                <hr>
                <p><i class="fas fa-map-pin"></i> City: {current_data['name']}, {current_data['sys'].get('country', '')}</p>
                <p><i class="fas fa-globe"></i> Coordinates: {current_data['coord']['lat']}, {current_data['coord']['lon']}</p>
                <p><i class="fas fa-sun"></i> Sunrise: {datetime.fromtimestamp(current_data['sys']['sunrise']).strftime('%H:%M:%S')}</p>
                <p><i class="fas fa-moon"></i> Sunset: {datetime.fromtimestamp(current_data['sys']['sunset']).strftime('%H:%M:%S')}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="info-box">
                <i class="fas fa-chart-line" style="font-size: 20px; color: #2a5298;"></i>
                <h4 style="display: inline; margin-left: 10px;">Detailed Metrics</h4>
                <hr>
                <p><i class="fas fa-arrow-up"></i> Max Temperature: {current_data['main']['temp_max']:.1f}°{temp_unit}</p>
                <p><i class="fas fa-arrow-down"></i> Min Temperature: {current_data['main']['temp_min']:.1f}°{temp_unit}</p>
                <p><i class="fas fa-eye"></i> Visibility: {current_data.get('visibility', 10000)/1000:.1f} km</p>
                <p><i class="fas fa-cloud"></i> Cloud Cover: {current_data['clouds']['all']}%</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Forecast Section
    if forecast_data:
        st.markdown('<div class="section-header"><i class="fas fa-calendar-week"></i> Forecast Analytics (5-Day)</div>', unsafe_allow_html=True)
        
        forecast_list = []
        for item in forecast_data['list'][:24]:
            forecast_list.append({
                'datetime': datetime.fromtimestamp(item['dt']),
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'weather': item['weather'][0]['description'].title()
            })
        
        df_forecast = pd.DataFrame(forecast_list)
        
        # Temperature Chart
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=df_forecast['datetime'],
            y=df_forecast['temperature'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='#e74c3c', width=3),
            marker=dict(size=8, symbol='circle'),
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.1)'
        ))
        fig_temp.update_layout(
            title='Temperature Forecast Trend',
            xaxis_title='Date and Time',
            yaxis_title=f'Temperature ({temp_unit})',
            height=400,
            hovermode='x unified',
            template='plotly_white'
        )
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Multi-metric charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_humidity = go.Figure()
            fig_humidity.add_trace(go.Bar(
                x=df_forecast['datetime'],
                y=df_forecast['humidity'],
                name='Humidity',
                marker_color='#3498db'
            ))
            fig_humidity.update_layout(
                title='Humidity Forecast',
                xaxis_title='Date and Time',
                yaxis_title='Humidity (%)',
                height=350,
                template='plotly_white'
            )
            st.plotly_chart(fig_humidity, use_container_width=True)
        
        with col2:
            fig_wind = go.Figure()
            fig_wind.add_trace(go.Scatter(
                x=df_forecast['datetime'],
                y=df_forecast['wind_speed'],
                mode='lines+markers',
                name='Wind Speed',
                line=dict(color='#27ae60', width=3),
                fill='tozeroy',
                fillcolor='rgba(39, 174, 96, 0.1)'
            ))
            fig_wind.update_layout(
                title='Wind Speed Forecast',
                xaxis_title='Date and Time',
                yaxis_title='Wind Speed (m/s)',
                height=350,
                template='plotly_white'
            )
            st.plotly_chart(fig_wind, use_container_width=True)
        
        # Forecast Table
        with st.expander("View Detailed Forecast Data"):
            df_display = df_forecast.copy()
            df_display['datetime'] = df_display['datetime'].dt.strftime('%Y-%m-%d %H:%M')
            df_display.columns = ['Date/Time', 'Temperature', 'Humidity (%)', 'Wind (m/s)', 'Weather']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
    
    # Business Intelligence Section
    st.markdown('<div class="section-header"><i class="fas fa-chart-pie"></i> Business Intelligence and Insights</div>', unsafe_allow_html=True)
    
    # Business impact analysis
    impact_score = 0
    if temp > 35:
        impact_score += 30
        temp_impact = "High Impact: Cooling products demand surge"
    elif temp > 30:
        impact_score += 15
        temp_impact = "Moderate Impact: Beverages demand increasing"
    else:
        temp_impact = "Low Impact: Normal operations"
    
    if humidity > 80:
        impact_score += 25
        humidity_impact = "Logistics disruptions likely"
    elif humidity > 65:
        impact_score += 10
        humidity_impact = "Supply chain monitoring recommended"
    else:
        humidity_impact = "Normal logistics"
    
    if wind_speed > 10:
        impact_score += 20
        wind_impact = "Delivery delays expected"
    elif wind_speed > 6:
        impact_score += 8
        wind_impact = "Delivery monitoring advised"
    else:
        wind_impact = "On-time deliveries"
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class="impact-box">
                <i class="fas fa-chart-line" style="font-size: 24px;"></i>
                <h4 style="margin-top: 10px;">Weather Impact Score</h4>
                <h1 style="font-size: 48px;">{impact_score}%</h1>
                <p>Overall business risk level</p>
                <hr>
                <p><i class="fas fa-thermometer-half"></i> {temp_impact}</p>
                <p><i class="fas fa-tint"></i> {humidity_impact}</p>
                <p><i class="fas fa-wind"></i> {wind_impact}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="info-box">
                <i class="fas fa-lightbulb" style="font-size: 20px; color: #f39c12;"></i>
                <h4 style="display: inline; margin-left: 10px;">Actionable Recommendations</h4>
                <hr>
                <ul style="margin-left: 20px;">
                    <li><i class="fas fa-box"></i> Inventory: {'Increase stock of cooling products' if temp > 30 else 'Standard inventory levels'}</li>
                    <li><i class="fas fa-truck"></i> Logistics: {'Implement contingency plans' if wind_speed > 8 else 'Normal routing'}</li>
                    <li><i class="fas fa-chart-bar"></i> Marketing: {'Launch weather-based campaigns' if temp > 32 else 'Regular promotions'}</li>
                </ul>
                <div class="metric-delta" style="margin-top: 15px; text-align: center;">
                    <i class="fas fa-clock"></i> Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # SQL Analytics Section
    with st.expander("Advanced Analytics and SQL Queries"):
        st.markdown("""
            <div style="background: #1e1e1e; border-radius: 8px; padding: 15px;">
                <i class="fas fa-database" style="color: #00a8ff;"></i>
                <strong style="color: white;"> Weather-Business Correlation Analysis | Suyash Magdum</strong>
            </div>
        """, unsafe_allow_html=True)
        
        st.code(f"""
        Real-time Weather Impact Analysis Query
        Developed by: Suyash Magdum | Data Analyst
        
        WITH weather_metrics AS (
            SELECT 
                city = '{city}',
                current_temperature = {temp:.1f},
                current_humidity = {humidity},
                wind_speed = {wind_speed:.1f},
                impact_score = {impact_score},
                CASE 
                    WHEN {temp} > 35 THEN 'High Alert'
                    WHEN {temp} > 30 THEN 'Moderate Alert'
                    ELSE 'Normal'
                END as alert_level
        )
        SELECT 
            wm.*,
            o.total_orders,
            o.total_revenue,
            (o.total_revenue * (wm.impact_score / 100.0)) as estimated_impact
        FROM weather_metrics wm
        LEFT JOIN orders o ON DATE(o.order_date) = CURRENT_DATE
        WHERE o.city = wm.city;
        """, language="sql")

else:
    st.markdown("""
        <div style="text-align: center; background: #f8f9fa; border-radius: 12px; padding: 60px 20px;">
            <i class="fas fa-cloud-sun" style="font-size: 64px; color: #dee2e6;"></i>
            <h3 style="margin-top: 20px;">Welcome to Weather Intelligence Platform</h3>
            <p style="color: #6c757d;">Enter your OpenWeatherMap API Key in the sidebar to begin.</p>
            <hr style="width: 50%; margin: 20px auto;">
            <p style="font-size: 14px;">
                <i class="fas fa-key"></i> Get your free API key from openweathermap.org
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown(f"""
    <div class="footer">
        <i class="fas fa-chart-line"></i> Real-Time Weather Intelligence | 
        Powered by OpenWeatherMap API | 
        <i class="fas fa-chart-bar"></i> Enterprise Dashboard
        <br><br>
        <div class="developer-credit">
            <i class="fas fa-code"></i> Developed by Suyash Magdum | Data Analyst
            <br>
            <i class="fas fa-envelope"></i> suyash.magdum@example.com | 
            <i class="fab fa-github"></i> github.com/suyashmagdum |
            <i class="fab fa-linkedin"></i> linkedin.com/in/suyash-magdum
        </div>
    </div>
""", unsafe_allow_html=True)

# Auto-refresh
if auto_refresh and api_key:
    time.sleep(30)
    st.rerun()