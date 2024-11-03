import streamlit as st
import pyexcel as pyxl
import pandas as pd
from xlsxwriter import Workbook
from io import BytesIO
import test_del_court


output = BytesIO()


st.set_page_config(page_title="Del Data")


st.header("Del Data")
st.write("Upload your data.")


uploaded_file=st.file_uploader("Choose a file(xlsx)",type=["xlsx"])
        
submit1 = st.button("Submit")


if submit1:
    
    if uploaded_file is not None:
        st.write("File Uploaded Successfully")
    
    
    
    if uploaded_file:
        st.subheader("Processing this could take up to 20 minutes depending on file size. Please do not close or refresh this tab.")
        
        
        columns = ["Owner Last Name", "Owner First Name", "Case Number"]
    
        source_data = pd.read_excel(uploaded_file, usecols=columns)
        
        
        
        print(source_data)
        
        test_del_court.find_abnormal_size_of_case_numbers(source_data)
        test_del_court.clean_case_numbers(source_data)
        test_del_court.find_abnormal_size_of_case_numbers(source_data)
        
        web_data = test_del_court.get_new_web_case_data(source_data)
        
        
        
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        web_data.to_excel(writer, sheet_name='Sheet1')

        writer.close()
        xlsx_data = output.getvalue()

        # print(xlsx_data)
        # print(type(xlsx_data))
        
        
        st.download_button(label="Download Retrieved Data", data=xlsx_data, file_name="data.xlsx", mime="application/vnd.ms-excel")
        
    #st.dataframe(web_data1)
        
        