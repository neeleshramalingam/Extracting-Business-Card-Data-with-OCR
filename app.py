import streamlit as st
import easyocr
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import re
import sqlite3

# Set up the page title and description
st.set_page_config(page_title='Business Card Extractor', page_icon=':credit_card:', layout='wide')
st.title('Business Card Extractor')
st.write('Upload an image of a business card to extract its information')

# Create a file uploader widget
uploaded_file = st.file_uploader(label='Upload a business card image', type=['jpg', 'jpeg', 'png'])




# Define a function to extract the business card information
def extract_info(image):
    # Load the image using OpenCV
    image = cv2.imdecode(np.frombuffer(image.read(), np.uint8), cv2.IMREAD_COLOR)

    # Use EasyOCR to extract text from the image
    read = easyocr.Reader(['en'])
    l = read.readtext(image, detail=0, paragraph=False)

    k = {'Company_name': "",'Name': "", 'Designation': "", 'Number': "", 'Email': "", 'Website': "", 'Area': "", 'Pincode': ""}

    # Parse the text to extract the relevant information

    k['Name'] = l[0]
    k['Designation'] = l[1]
    for i in range(len(l)):
        if re.findall("[a-zA-Z0-9]+ [a-zA-Z0-9]+ [ St]+", l[i]):
            k['Area'] = (l[i])
        if re.search('[^- +a-zA-z]{6}', l[i]):
            res = l[i]
            result = [int(l[i]) for l[i] in res.split() if l[i].isdigit()]
            k['Pincode'] = result[0]
        if re.findall("[^A-Z0-9.-_+~!@#$ %&*()]+@+[a-zA-Z0-9]+.[a-z]+", l[i]):
            k['Email'] = l[i]
        if re.findall("[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]", l[i]):
            k['Number'] = l[i]
        if re.findall('[^ ,0-9!@#$%&*()_+]+[A-Za-z]+.com', l[i]):
            k["Website"] = l[i]

    cn = ""  # adding company name
    for i in l:
        if i not in k.values():
            if i.isalpha():
                print(i)
                cn = cn + ' ' + i
    k['Company_name'] = cn

    return k


table_name = 'Bdata'
# Create a button to extract the business card information
if uploaded_file is not None:
    st.image(uploaded_file, caption='Uploaded business card', use_column_width=True)
    k = extract_info(uploaded_file)
    k['Website'] = k['Website'].replace(" ", ".")
    k['Area'] = k['Area'].replace(";", ".")
    k['Area'] = k['Area'].replace(" ", "")
    k['Area'] = k['Area'].replace(",,", ",")
    if st.button('Extract information'):
        st.write('Extracted information:')
        st.write(k)


    if st.button("save data to database!"):
        conn = sqlite3.connect('Business.db')
        query = f'''Create table if not Exists {table_name} (Company_name text,Name text,Designation text,Number text, Email text, Website text,Area text,
                pincode integer)'''
        conn.execute(query)
        conn.commit()

        columns = ', '.join(k.keys())
        placeholders = ':' + ', :'.join(k.keys())
        query1 = f'INSERT INTO {table_name} (%s) VALUES (%s)' % (columns, placeholders)
        conn.execute(query1, k)
        st.write("Data saved successfully")
        conn.commit()
        conn.close()


if st.button("view data"):
    conn = sqlite3.connect('Business.db')
    query = f'''select * from {table_name} '''
    r_df = pd.read_sql(query, conn)
    st.table(r_df)
    conn.commit()
    conn.close()


email = st.text_input(key="placeholder", label="enter Email on your card to delete the data")
if st.button("Delete data "):
    conn = sqlite3.connect('Business.db')
    query = f'''delete from {table_name} where Email=email'''
    conn.execute(query)
    conn.commit()
    conn.close()
    st.write("Information deleted")



