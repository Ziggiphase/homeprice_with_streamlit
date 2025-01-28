import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import zscore

def load_data():
    #load the dataset excel file to a dataframe
    house_prices = pd.read_csv('House_price.csv')
    years = house_prices['Age']
    house_prices['Age'] = 2024 - house_prices['Age'] #Calculate the age of the house in the year 2024
    return house_prices, years

house_prices, years = load_data()
          
def outliers():
    #Z-score method
    outliers_col = []
    z_thresh = 3
    obj_cols = house_prices.select_dtypes(include = ['number']).columns
    for obj_col in obj_cols:
        b = zscore(house_prices[obj_col])
        outliers = np.where(np.abs(b) > z_thresh)
        if len(outliers) > 0:
                outliers_col.append(outliers)  # Store columns with outliers
                
                # Handle outliers by capping them to the mean ± z_thresh * std
                mean = house_prices[obj_col].mean()
                std = house_prices[obj_col].std()
                lower_bound = mean - (z_thresh * std)
                upper_bound = mean + (z_thresh * std)

                # Capping and flooring outliers to upper and lower bounds respectively
                house_prices[obj_col] = house_prices[obj_col].apply(lambda x: lower_bound if x < lower_bound else upper_bound if x > upper_bound else x)
                return house_prices
                #print(outliers_col, house_prices)

#@st.cache

house_prices = outliers()
            
def show_explore_page():
    st.title("Explore House Prices in Minna")
    
    #st.line_chart(data=house_prices,x="SalePrice", y="Age", x_label="SalePrice", y_label="Age")
    data = house_prices['Location'].value_counts()
    
    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")
    st.write("### Houses Area Division")
    st.pyplot(fig1)
    st.write(
        """ Check out the houses in Minna
        """
    )
    plt.figure(figsize=(25, 15))
    plt.scatter(years, house_prices['SalePrice'], c='blue', alpha=0.7)
    plt.title('House Ages in Minna')
    plt.xlabel('Years')
    plt.ylabel('Price')
    st.pyplot(plt)
    
    #st.area_chart(house_prices['SalePrice'])
 #= house_prices['Age'].value_counts()