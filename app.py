import streamlit as st
import pyexcel as pyxl
import pandas as pd
from xlsxwriter import Workbook
from io import BytesIO
import test_del_court
import time
from bs4 import BeautifulSoup
import requests



output = BytesIO()

   
   
def get_case_no_for_all_data(df):
    progress_text = "Getting Case Numbers. Please wait."
    my_bar = st.progress(0, text=progress_text)
    
    num_not_available = 0
    case_numbers = []
    
    for i, row in df.iterrows():
        progress =  int((i/len(df)) * 100)
        # st.write(progress)
        my_bar.progress(progress, text=progress_text)
        first_name = row["Owner First Name"]
        last_name = row["Owner Last Name"]
        
        # print(first_name, last_name)
        
        cases = test_del_court.search_case(first_name, last_name)
        
        if len(cases) == 0:
            case_numbers.append("Not Available")
            num_not_available = num_not_available + 1
        else:
            case_numbers.append(test_del_court.get_filtered_case_no(cases))
            
        
        
        # print(cases)
        
    my_bar.progress(100, text=progress_text)
    
        
        
    df["Case Number"] = case_numbers
    
    return df, num_not_available


def search_case_data_using_case_id(case_id):
    
    get_general_info = True
    get_core_data = False
    get_entry_data = True
    
    entries_delim_list = ['Filing Date', 'Description', 'Name', 'Monetary']
    core_data_delim_list = ['Seq #', 'Assoc', 'Party End Date', 'Type', 'ID', 'Name']
    
    general_info_list = []
    core_data_list = []
    entry_data_list = []
    
    
    # https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_doct.cp_dktrpt_docket_report?backto=D&case_id=N23L-10-013&begin_date=&end_date=
    
    url = f"https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_doct.cp_dktrpt_docket_report?backto=D&case_id={case_id}&begin_date=&end_date="

    response = requests.post(url)

    if response.status_code == 200:
        print("Form submitted successfully!")
        # print("Response Content:")
        # pass
        
            
        soup=BeautifulSoup(response.content,'lxml')

        # print(response.content)
        entries = []

        count = 0
        for item in soup.select('tr'):
            if count > 1:
                # print(item, "\n\n")
                
                list_of_vals = []
                
                for val in item.children:
                    str_val = val.get_text()
                    
                    if (not (str_val == "\n")):
                        list_of_vals.append(val.get_text())
                        
                        
                if list_of_vals == core_data_delim_list:
                    get_general_info = False
                    get_entry_data = False
                    get_core_data = True
                elif list_of_vals == entries_delim_list:
                    get_general_info = False
                    get_core_data = False
                    get_entry_data = True
                        
                        
                if get_general_info == True:
                    general_info_list.append(list_of_vals)
                elif get_core_data == True:
                    core_data_list.append(list_of_vals)
                elif get_entry_data == True:
                    entry_data_list.append(list_of_vals)
                    

                if(list_of_vals[0] == "Entry:"):
                    entries.append(list_of_vals)
                else:
                    pass
                        
                # print(list_of_vals)
            
            count += 1
            
        df_general = pd.DataFrame(general_info_list)
        df_core = pd.DataFrame(core_data_list)
        df_entries = pd.DataFrame(entry_data_list)

        return df_general, df_core, df_entries, False

    else:
        print(f"Failed to submit the form. Status code: {response.status_code}")
        print(f"Case Id: {case_id}")
        
        return None, None, None, True
      
      
def conv_to_string(list_val):
    conv_str = ""
    
    count = 0
    for i in list_val:
        if count > 0:
            conv_str = conv_str + " \n" + str(i) 
        else:
            conv_str = conv_str + str(i)
        
        
    return conv_str        
            

def get_new_web_case_data(table: pd.DataFrame):
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)
    
    all_cases = []
    num_fail = 0
    
    number_of_nan = 0
    list_of_gathered_data = []
    progress = 0
    for i, row in table.iterrows():
        # time.sleep(0.5)
        # time.sleep(0.05)
        
        # if((((i/len(table) * 100) % 1) == 0)):
            
        progress =  int((i/len(table)) * 100)
        # st.write(progress)
        my_bar.progress(progress, text=progress_text)
        
        if(type(row["Case Number"]) == str):
            df_general, df_core, df_entries, fail = search_case_data_using_case_id(row["Case Number"])
            
            if fail == False:
                

                gathered_data = test_del_court.format_case_data_from_web(row["Case Number"], df_general, df_core, df_entries)



                list_of_gathered_data.append(gathered_data)
            else:
                num_fail = num_fail + 1



            
        else:
            number_of_nan = number_of_nan + 1
            
            # print(f"Not a str value: {row['Case Number']} \n Number of such values: {number_of_nan}")
        
        # print(f"Iteration: {i}")
        
    my_bar.progress(100, text=progress_text)
        
    df = pd.DataFrame(list_of_gathered_data)    
    # print(f"Not a str value: {row['Case Number']} \n Number of such values: {number_of_nan}")
    # print(f"Num Fail: {num_fail}")
    
    
        
    return df, num_fail



st.set_page_config(page_title="Del Prop Data")


st.header("Del Prop Data")
st.write("Upload your formatted excel data.")


uploaded_file=st.file_uploader("Choose a file(xlsx)",type=["xlsx"])
        
submit1 = st.button("Submit")


if submit1:
    
    if uploaded_file is not None:
        st.write("File Uploaded Successfully")
    
    
    
    if uploaded_file:
        st.subheader("Processing this could take up to 20 minutes depending on file size. Please do not close or refresh this tab.")
        
        original_data_with_no_case_data = pd.read_excel(uploaded_file)
        st.write("Your uploaded file")
        st.write(original_data_with_no_case_data)
        st.write("Getting Case Numbers")
        table_with_case_data, num_no_case_no = get_case_no_for_all_data(original_data_with_no_case_data)
        st.write(f"Table with retrieved case numbers:")
        st.write(table_with_case_data)
        st.write(f"Number of unretrieveable case number: {num_no_case_no}")
        
        columns = ["Owner Last Name", "Owner First Name", "Case Number"]
    
        # source_data = pd.read_excel(original_data_with_no_case_data, usecols=columns)
        source_data = table_with_case_data[columns]
        
        
        st.write(f"Number of rows in data: {len(source_data)}")
        st.write("Here are the relevant columns from the original data:")
        
        total_issues = test_del_court.find_abnormal_size_of_case_numbers(source_data)
        test_del_court.clean_case_numbers(source_data)
        total_issues = test_del_court.find_abnormal_size_of_case_numbers(source_data)
        
        st.write(source_data)
        st.write(f'Number of rows with case number length not = 11: {total_issues}')
        

        web_data, num_failed_searches = get_new_web_case_data(source_data)
        
        
        
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        table_with_case_data.to_excel(writer, sheet_name="Case numbers")
        web_data.to_excel(writer, sheet_name='Web Data')

        writer.close()
        xlsx_data = output.getvalue()

        
        st.write("Here is the updated data from web source:")
        st.write(f"Number of failed searches: {num_failed_searches}")
        st.write(web_data)
        st.download_button(label="Download Retrieved Data", data=xlsx_data, file_name="data.xlsx", mime="application/vnd.ms-excel")
        time.sleep(60*60)
        
        
    #st.dataframe(web_data1)
        
        