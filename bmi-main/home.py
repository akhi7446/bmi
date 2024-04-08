import streamlit as st
import mysql.connector
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
    initial_sidebar_state="collapsed"
)

# # Connect to the MySQL database
cnx = mysql.connector.connect(user='root', password='password',
                              host='localhost', database='dbname')
cursor = cnx.cursor()
create_table_query = '''CREATE TABLE IF NOT EXISTS bmi (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            name VARCHAR(255),
                            height FLOAT,
                            weight FLOAT,
                            age INT,
                            bmi_index FLOAT,
                            Bloodpressure INT
                        )'''
cursor.execute(create_table_query)
cnx.commit()

st.title('BMI Calculator')


name = st.text_input('Name')
age = st.number_input('Age', min_value=0, max_value=150, step=1)
height = st.number_input('Height (cm)', step=0.01)
weight = st.number_input('Weight (kg)', step=0.01)
bloodpressure= st.number_input('Blood Pressure',min_value=0, step=1)


if st.button('Calculate BMI'):
    bmi_index = weight / ((height/100) ** 2)
    insert_query = f"INSERT INTO bmi (name, age, height, weight, bmi_index, bloodpressure) VALUES ('{name}', {age}, {height}, {weight}, {bmi_index}, {bloodpressure})"
    cursor.execute(insert_query)
    cnx.commit()


    # Retrieve the calculated BMI value from the database
    select_query = f"SELECT bmi_index FROM bmi WHERE name = '{name}'"
    cursor.execute(select_query)
    result = cursor.fetchone()

    if result:
        bp = result
        bmi_index = result[0]
        st.success(f"Your BMI is {bmi_index:.2f}")

        if bloodpressure < 120:
            st.success("Your blood pressure is normal")
        elif bloodpressure < 140:
            st.warning("Your blood pressure is elevated")
        else:
            st.error("Your blood pressure is high")

        if bmi_index < 18.5:
            st.warning("You are underweight")
            if weight <70:
                st.success("You have to take 1200-1500 calories per day")
            elif weight >70 and weight <90:
                st.success("You have to take 1500-1800 calories per day")
            elif weight >90:
                st.success("You have to take 1800-2000 calories per day")
            st.write("You can eat a variety of foods, including:")
            st.markdown("- Whole milk, cheese, and yogurt")
            st.markdown("- Nuts and nut butter")
            st.markdown("- Whole grains and bread")
            st.markdown("- Meat, fish, and eggs")
            st.markdown("- Fruits and vegetables")
            
        elif bmi_index < 25:
            st.success("Your weight is normal")
            if weight <70:
                st.success("You have to take 1200-1500 calories per day")
            elif weight >70 and weight <90:
                st.success("You have to take 1500-1800 calories per day")
            elif weight >90:
                st.success("You have to take 1800-2000 calories per day")
            st.write("You can eat a variety of foods, including:")
            st.markdown("- Whole grains, such as brown rice and whole-wheat bread")
            st.markdown("- Lean meats, poultry, fish, and eggs")
            st.markdown("- Low-fat dairy products")
            st.markdown("- Fruits and vegetables")
            st.markdown("- Healthy fats, such as olive oil and avocado")
        elif bmi_index < 30:
            st.warning("You are overweight.")
            if weight <70:
                st.success("You have to take 1200-1500 calories per day")
            elif weight >70 and weight <90:
                st.success("You have to take 1500-1800 calories per day")
            elif weight >90:
                st.success("You have to take 1800-2000 calories per day")
            st.write("You can eat a variety of foods, including:")
            st.markdown("- Low-calorie fruits and vegetables")
            st.markdown("- Lean meats, poultry, fish, and eggs")
            st.markdown("- Low-fat dairy products")
            st.markdown("- Whole grains, such as brown rice and whole-wheat bread")
            st.markdown("- Healthy fats, such as olive oil and avocado")
            
        else:
            st.warning("You are obese.")
            if weight <70:
                st.success("You have to take 1200-1500 calories per day")
            elif weight >70 and weight <90:
                st.success("You have to take 1500-1800 calories per day")
            elif weight >90:
                st.success("You have to take 1800-2000 calories per day")
            st.write("You can eat a variety of foods, including:")
            st.markdown("- Low-calorie fruits and vegetables")
            st.markdown("- Lean meats, poultry, fish, and eggs")
            st.markdown("- Low-fat dairy products")
            st.markdown("- Whole grains, such as brown rice and whole-wheat bread")
            st.markdown("- Healthy fats, such as olive oil and avocado")
            st.markdown('''
            <style>
            [data-testid="stMarkdownContainer"] ul{
                list-style-position: inside;
            }
            </style>
            ''', unsafe_allow_html=True)

    else:
        st.error('Error: Unable to calculate BMI')
search_name = st.text_input('Search by Name')
if st.button('Search'):
    # Retrieve BMI data for the provided name
    search_query = f"SELECT name, height, weight, age, bmi_index,Bloodpressure FROM bmi WHERE name = '{search_name}'"
    cursor.execute(search_query)    
    search_result = cursor.fetchall()

    if len(search_result) > 0:
        cols = ['Name', 'Height (cm)', 'Weight (kg)', 'Age', 'BMI Index','Bloodpressure' ]
        df = pd.DataFrame(search_result, columns=cols)
        st.write("Search Results:")
        st.dataframe(df)
    else:
        st.warning('No results found for the provided name.')

if st.button('Show data entries'):
    select_query = "SELECT name, height, weight, age, bmi_index FROM bmi"
    cursor.execute(select_query)
    data = cursor.fetchall()

    st.write("BMI Data Entries")
    if len(data) > 0:
        cols = ['Name', 'Height (cm)', 'Weight (kg)', 'Age', 'BMI Index']
        df = pd.DataFrame(data, columns=cols)
        st.dataframe(df)
        
    else:
        st.warning('No data entries found.')