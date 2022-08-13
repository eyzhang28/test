import streamlit as st
import pandas as pd
import numpy as np
import tabula as tb
import glob, os
import pdfplumber

st.title('Test')

DATE_COLUMN = 'date/time'

notice = st.selectbox(
     'What notice is this file?',
     ('First Notice', 'Second Notice', 'Final Notice'))

st.write('Please upload the proofs in the first uploader and the State Contact Shet in the second uploader')

proofs_data = st.file_uploader("Upload Proofs PDF", type=["pdf"])
state_data = st.file_uploader("Upload the State Contact Info Sheet", type = ["csv"])
print_data = st.file_uploader("Upload Print Files", type=["csv"])


total_lines = []
def string_cleaning(s):
    try:
        s = s.replace(" ", "")
        s = s.lower()
    except:
        pass
    return s
def string_stripping(s):
    try:
        s = s.strip()
    except:
        pass
    return s
def xa_cleaning(s):
    try:
        s = s.replace('\n', ' ')
        s = s.replace('\xad', '-')
        s = s.replace('\xa0', ' ')
    except:
        pass
    return s
def compare_dict(df6, proofs_dictionary):
    if (proofs_dictionary['Form Identification'] == 'BLS 3023 - Industry Verification Form'):
        st.write('Right Form Identification')
    else:
        st.write('Wrong Identification')
    if (proofs_dictionary['OMB Clearance Information'] == 'O.M.B. No. 1220-0032'):
        st.write('Right OMB info')
    else:
        st.write('Wrong OMB info')
    if (string_cleaning(df6['State Agency Name (50 char)'].iloc[0]) == string_cleaning(proofs_dictionary['State Agency Name'])):
        st.write('Same State Agency Name')
        if (df6['Abbreviation'].iloc[0] == proofs_dictionary['Abbreviation']):
            st.write('Same Abbreviation')
        else:
            st.write('Different Abbreviation')
        if (string_cleaning(df6['Department Name (50 char)'].iloc[0]) == string_cleaning(proofs_dictionary['Department Name'])):
            st.write('Same Department Name')
        else:
            st.write('Different Department Name')
        if (string_cleaning(df6['Return Address'].iloc[0]) == string_cleaning(proofs_dictionary['Return Address'])):
            st.write('Same Return Address')
        else:
            st.write('Different Return Address')
        if (string_cleaning(df6['Return Address Line 2'].iloc[0]) == xa_cleaning(string_cleaning(proofs_dictionary['Return Address Line 2']))):
            st.write('Same Return Address 2')
        else:
            st.write('Different Return Address 2')
        if (df6['Return Address Zip Code'].iloc[0] == proofs_dictionary['Return Address Zip Code']):
            st.write('Same Return Zip Code')
        else:
            st.write('Different Return Zip Code')
        if (df6['Phone Number'].iloc[0] == proofs_dictionary['Phone Number']):
            st.write('Same Phone Number')
        else:
            st.write('Different Phone Number')
        if (df6['Print (Y/N)'].iloc[0] == proofs_dictionary['Print Email']):
            if (df6['Print (Y/N)'].iloc[0] == 'N'):
                st.write('Same Email')
            else:
                if (df6['Email Address to be printed on ARS Letters'].iloc[0] == proofs_dictionary['Email']):
                    st.write('Same Email')
                else:
                    st.write('Different Email')
    else:
        st.write('Different State Agency Name')
    if (df6['BMA_Area_Code_1'].iloc[0] == proofs_dictionary['BA_ZIP_5']):
        st.write('Same ZIP 5')
    else:
        st.write('Different ZIP 5')
    if (df6['BMA_Area_Code_2'].iloc[0] == proofs_dictionary['BA_ZIP_4']):
        st.write('Same ZIP 4')
    else:
        st.write('Different ZIP 4')
    if (df6['State Agency Name'].iloc[0] == proofs_dictionary['the State Agency Name 1']):
        st.write('Same the State Agency Name 1')
    else:
        st.write('Different the State Agency Name 1')
    if (df6['State Agency Name'].iloc[0] == proofs_dictionary['the State Agency Name 2']):
        st.write('Same the State Agency Name 2')
    else:
        st.write('Different the State Agency Name 2')
    if (string_stripping(df6['BMA_City'].iloc[0]) == proofs_dictionary['BA_City']):
        st.write('Same BMA City')
    else:
        st.write('Different BMA City')
    if (string_stripping(df6['BMA_State'].iloc[0]) == proofs_dictionary['BA_State']):
        st.write('Same BMA State')
    else:
        st.write('Different BMA State')
    if (df6['Mandatory (Y or N only)'].iloc[0] == proofs_dictionary['Is_Mandatory']):
        st.write('Same Mandatory Status')
    else:
        st.write('Different Mandatory Status')
    if (df6['Mandatory (Y or N only)'].iloc[0] == 'Y'):
        if (df6['State Law (Mandatory Only)'].iloc[0] == xa_cleaning(proofs_dictionary['State_Law'])):
            st.write('Same State Law')
        else:
            st.write('Different State Law')
    if (df6['Print Spanish Instructions link?'].iloc[0] == proofs_dictionary['spanish_link']):
        st.write('Same Spanish Link')
    else:
        st.write('Different Spanish Link')
    if (string_stripping(df6['Mail_Address_1'].iloc[0]) == proofs_dictionary['BA_Address_1']):
        st.write('Same Mail Address 1')
    else:
        st.write('Different Mail Address 1')
    if (string_stripping(df6['Mail_Address_2'].iloc[0]) == ''):
        df6['Mail_Address_2'].iloc[0] = 'Empty'
    if (string_stripping(df6['Mail_Address_2'].iloc[0]) == proofs_dictionary['BA_Address_2']):
        st.write('Same Mail Address 2')
    else:
        if (string_stripping(df6['Trade_Name'].iloc[0]) == proofs_dictionary['BA_Address_2']):
            st.write('Same Mail Address 2')
        else:
            st.write('Different Mail Address 2')
    if (string_stripping(df6['Legal_Name'].iloc[0]) == ''):
        df6['Legal_Name'].iloc[0] = 'Empty'
    if (string_stripping(df6['Legal_Name'].iloc[0]) == proofs_dictionary['Legal_Name']):
        st.write('Same Legal Name')
    else:
        if (string_stripping(df6['Trade_Name'].iloc[0]) == proofs_dictionary['Legal_Name']):
            st.write('Same Legal Name')
        else:
            st.write('Different Legal Name')
    if (string_stripping(df6['Trade_Name'].iloc[0]) == ''):
        df6['Trade_Name'].iloc[0] = 'Empty'
    if (string_stripping(df6['Trade_Name'].iloc[0]) == proofs_dictionary['Trade_Name']):
        st.write('Same Trade Name')
    else:
        if (string_stripping(df6['Trade_Name'].iloc[0]) == proofs_dictionary['Legal_Name']):
            st.write('Same Trade Name')
        else:
            if (string_stripping(df6['Mail_Address_2'].iloc[0]) == proofs_dictionary['Trade_Name']):
                st.write('Same Trade Name')
            else:
                st.write('Different Trade Name')

if st.button("Run Script"):
     st.write("test")
     df = pd.read_csv(print_data)
     st.write(df['Password'].iloc[0])
     df2 = pd.read_csv(state_data)
     df2 = df2.drop([2,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,43,44,45])
     df2_transposed = df2.T
     df3 = df2_transposed.reset_index(drop = True)
     df3.columns = df3.iloc[1]
     df3 = df3.drop([0,1])
     df3 = df3.rename(columns = {'FIPS': 'Abbreviation_list'})
     
     st.write(df3)