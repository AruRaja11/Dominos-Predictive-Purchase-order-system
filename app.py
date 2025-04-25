import pickle
import pandas as pd
import datetime as dt
import streamlit as st
import os

# Fixed header styling
st.markdown(
    """
    <style>
    .fixed-header {
        max-height:250px;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #4CAF50; 
        color: white; 
        text-align: center;
        padding: 50px;
        padding-bottom: 20px;
        font-size: 20px;
        z-index: 9999;
        border-bottom: 2px solid #ccc;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .fixed-header img {
        height: 90px;
        width: 90px;
    }
    .main-content {
        margin-top: 120px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fixed Header Content
st.markdown(
    '''
    <div class="fixed-header">
    <img src="https://img.freepik.com/free-psd/deliciously-appealing-margherita-pizza-transparent-background_84443-26494.jpg" >
        <h1> Dominos - Predictive Purchase order System</h1>
    </div>
    ''', 
    unsafe_allow_html=True
)

# Padding space
for _ in range(4):
    st.write(" ")

# Load pizza ingredients data
data = pd.read_excel('Pizza_ingredients.xlsx')
data['Items_Qty_In_Grams'] = data['Items_Qty_In_Grams'].fillna(data['Items_Qty_In_Grams'].mean())

# Helper Functions
def get_pizza_name(dataframe):
    def sub_name(row):
        unique_names = data['pizza_name'].sort_values().unique()
        return unique_names[row]
    dataframe["pizza_name"] = dataframe["pizza_name"].apply(sub_name)
    return dataframe

def quantity_count(dataframe):
    dataframe['quantity'] = 1
    df_quantity = dataframe.groupby(["pizza_name"])['quantity'].sum().reset_index()
    return df_quantity

def get_ingredients(dataframe):
    return data[data['pizza_name'].isin(dataframe['pizza_name'].values)]

def get_required_quantity(ingredients, dataframe):
    merge_df = ingredients.merge(dataframe, on='pizza_name', how='inner')
    merge_df['required_quantity'] = merge_df['Items_Qty_In_Grams'] * merge_df['quantity']
    return merge_df


# Store current directory
original_dir = os.getcwd()

# Load and forecast from one of the models
result_df = None
forecast_final = pd.DataFrame(columns=['week', 'date', 'pizza_name', 'quantity'])

os.chdir('models')
for model_file in os.listdir():
    try:
        pizza_name = model_file.replace("_", " ").replace(".pkl", "").title()
        with open(model_file, 'rb') as file:
            model = pickle.load(file)
    
        future_steps = 7
        forecast_result = model.forecast(steps=future_steps)
        forecast_datetime = pd.date_range(start=pd.to_datetime('01-01-2016'), periods=future_steps+1, freq='D')[1:]
    
        forecast_df = pd.DataFrame({
            'week':[1, 2, 3, 4, 5, 6, 7],
            'date': forecast_datetime,
            pizza_name: forecast_result
        })
    
        forecast_df[pizza_name] = forecast_df[pizza_name].round().astype(int)
        forecast_df['pizza_name'] = pizza_name
        forecast_df['quantity'] = forecast_df[pizza_name]
        forecast_df['date'] = forecast_df['date'].dt.date
        forecast_df = forecast_df[['week', 'date', 'pizza_name', 'quantity']]
        

        forecast_final = pd.concat([forecast_final, forecast_df], ignore_index=True)
    except:
        os.chdir(original_dir)

# Return to original directory
os.chdir(original_dir)

# Display forecast results
if forecast_df is not None:
    st.markdown(f"<h4 style='background-color:violet;'>Expected Pizza & Quantity to be Sold on Next Week:</h4>", unsafe_allow_html=True)
    for i in range(1, 8):
        temp_df = forecast_final[forecast_final['week'] == i]
        st.write(f'Day - {i}')
        st.write(temp_df)

# getting ingredients dataframe
ing_data = get_ingredients(forecast_final)
result_df = get_required_quantity(ing_data, forecast_final)

    
# Display ingredient requirements
if result_df is not None:
    st.markdown(f"<h4 style='background-color:violet;'>Ingredients and Quantity required:</h4>", unsafe_allow_html=True)
    result_df.drop('pizza_name_id', axis=1, inplace=True, errors='ignore')
    result_df.rename(columns={'Items_Qty_In_Grams': 'Items_Grams', 'required_quantity': 'Required'}, inplace=True)
    result_df = result_df.groupby(['pizza_name', 'pizza_ingredients', 'Items_Grams'])[['quantity', 'Required']].sum()
    st.dataframe(result_df)

# Load and forecast profit
with open('price_model.pkl', 'rb') as file:
    price_pred = pickle.load(file)


future_steps = 7
forecast_result = price_pred.forecast(steps=future_steps)
forecast_datetime = pd.date_range(start=pd.to_datetime('01-01-2016'), periods=future_steps+1, freq='D')[1:]

result = pd.DataFrame({
    'Date': forecast_datetime,
    'profit': forecast_result
})


st.markdown(f"<h4 style='background-color:violet;'>Predicted Profits for next week:</h4>", unsafe_allow_html=True)
st.markdown(f"<h5 align='center'>Predicted Profit: {round(result['profit'].sum(), 2)}</h5>", unsafe_allow_html=True)
st.markdown('------', unsafe_allow_html=True)
