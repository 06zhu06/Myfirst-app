# import packages
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
df=pd.read_csv('train.csv')
df1=df[['Pclass','Fare']]
st.title("Box Plot of Ticket Prices by Passenger Class")
fig,ax = plt.subplots(1, 3, figsize=(15, 5))
st.write(df1)
for i in range(3):       
    cls = i + 1
    data = df1[df1['Pclass'] == cls]['Fare']
    ax[i].boxplot(data)
    ax[i].set_title('Class'+str(cls))
    ax[i].set_xlabel('Pclass')
    ax[i].set_ylabel('Ticket Price')
st.pyplot(fig)


# show the title

# create a figure with three subplots, size should be (15, 5)
# show the box plot for ticket price with different classes
# you need to set the x labels and y labels
# a sample diagram is shown below

