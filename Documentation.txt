# 📊 Dominos - Predictive Purchase Order System
# ✅ Objective:
This project aims to help Dominos optimize their inventory and supply chain by forecasting future pizza sales using historical sales data. By accurately predicting demand, the system automatically calculates the required quantity of each ingredient and generates a purchase order. This minimizes waste, prevents stockouts, and ensures efficient operations. The project uses time series forecasting models like SARIMAX or LSTM to deliver accurate weekly sales predictions and aligns ingredient orders accordingly.

# 🗂️ Project Structure:
# Pizza_Sale.xlsx
* Contains the historical pizza sales data like pizza_name, order datetime, quantity, etc.
#  Pizza_ingredients.xlsx
* Contains the data of quantity of ingredients required to make the pizza based on factors such as size of pizza
# Forecasting.ipynb
* Cleaned the raw dataset by handling missing values.
* Encoded categorical variables and normalized numerical values.
* Ensured data was suitable for Time Series models.
* Tried some models such as ARIMA, SARIMAX, Prophet, LSTM and selected the best and simple algorithm.
* Required features are selected for time series forecasting.
# EDA.ipynb
* Conducted in-depth analysis and visualizations to understand feature distributions and correlations.
* Identified key trends such as the stationarity of data and trends present in the data.
# Price Prediction.ipynb
* This is to forecast the profit expected in the upcoming week
* Tried Multiple Time Series Forecasting algorithm:
  1. ARIMA
  2. SARIMAX
  3. LSTM
* Evaluated the result using chart.
* Final model selected: ARIMA model that better suited for the price data.
## app.py
* Developed a Streamlit web application to display the results.
* The forecast for the next seven days are forecasted and displayed.
* The displays include:
  1. The Pizzas predicted to be sold for next week with the amount.
  2. The Ingredients required to make the predicted amount of data.
  3. The profit expected in the next week.
*Clean and interactive interface for demonstration.
# 📌 Technologies Used:
* Python
* Pandas, NumPy – Data handling
* Matplotlib, Seaborn – Visualization
* Time Series Forecasting Models - ARIMA, SARIMAX, PROPHET, LSTM
* Streamlit – Web application
# ✅ Requirements:
* Install Steamlit
# 🚀 How to Run:
* Execute all Three .ipynb files
* Run app.py
# ✅ Results:
* The forecasted results of sales, ingredients required and profit for the next 7 days.
*Streamlit app provides a user-friendly interface for practical use.
