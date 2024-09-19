import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


# https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_cpty.cp_personcase_setup_idx



def store_non_closed_cases(table: pd.DataFrame, file_name: str):
    
    table.to_excel(file_name)


    
    
    
def get_names_from_file_containing_cases():
    
    columns = ["Owner Last Name", "Owner First Name"]
    
    table = pd.read_excel("Pre-Foreclosures.xlsx", usecols=columns)
    
    return table


def get_new_data_from_website(table: pd.DataFrame):
    
    all_cases = []
    
    for i, row in table.iterrows():
        first_name = row["Owner First Name"]
        last_name = row["Owner Last Name"]
        
        # time.sleep(0.05)
        
        cases = search_case(first_name, last_name)
        
        print(f"Iteration: {i}")
        
        for case in cases:
            
            if case["case_status"] != "CLOSED-CLOSED":
                
                all_cases.append(case)
        
    df = pd.DataFrame.from_dict(all_cases)
        
        
    return df
        
    

def search_case(first_name, last_name):
    # Define the URL to post the data to
    
    # https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_cpty.cp_personcase_srch_details?backto=P&soundex_ind=&partial_ind=&last_name=Grimes&last_name=Grimes&first_name=Linda&middle_name=&begin_date=&end_date=&case_type=ALL&id_code=&PageNo=1
    
    url = f"https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_cpty.cp_personcase_srch_details?backto=P&soundex_ind=&partial_ind=&last_name={last_name}&last_name={last_name}&first_name={first_name}&middle_name=&begin_date=&end_date=&case_type=ALL&id_code=&PageNo=1"

    # Perform the POST request
    response = requests.post(url)
    # response = requests.post(url, headers=headers, cookies=cookies, data=data)

    # Check if the request was successful
    if response.status_code == 200:
        # print("Form submitted successfully!")
        # print("Response Content:")
        pass
    else:
        print(f"Failed to submit the form. Status code: {response.status_code}")
        
        
        
    soup=BeautifulSoup(response.content,'lxml')
    
    
    cases = []
    
    count = 0
    for item in soup.select('tr'):
        
        if count > 1:
            
            list_of_vals = []
            
            
            for val in item.children:
                str_val = val.get_text()
                
                if (not (str_val == "\n")):
                    list_of_vals.append(val.get_text())
                    
            
            
            if len(list_of_vals) == 7:    
                # print(list_of_vals)
            
            
                case_data = {
                    "case_id" : list_of_vals[0],
                    "name" : list_of_vals[1],
                    "Address" : list_of_vals[2],
                    "party_type" : list_of_vals[3],
                    "party_end_date" : list_of_vals[4],
                    "filling_date" : list_of_vals[5],
                    "case_status" : list_of_vals[6]
                
                }
            
                # print(case_data)

                cases.append(case_data)
            
                # print("\n")
        
        count += 1
        
        
    return cases
     
            
            
def split_address(value):
    
    if "unavailable" in value:
        address = "Not Available"
        case = value[18:]
    else:
        case_pos = value.find("Case")
        
        address = value[:case_pos]
        case = value[case_pos + 8:]
        
        
    return address, case
    
    
def display_non_closed_cases(cases):
        
    for case in cases:
        if case["case_status"] != "CLOSED-CLOSED":
            address, court_case = split_address(case["Address"])
            
            print(f'Case ID: {case["case_id"]}')
            print(f'Name: {case["name"]}')
            print(f'Address: {address}')
            print(f"Case: {court_case}")
            print(f'Party Type: {case["party_type"]}')
            print(f'Party End Date: {case["party_end_date"]}')
            print(f'Filling Date: {case["filling_date"]}')
            print(f'Case Status: {case["case_status"]}')
            
            print("\n")    
            
            
def display_all_cases(cases)                :
    
    for case in cases:
        
        address, court_case = split_address(case["Address"])
        
        print(f'Case ID: {case["case_id"]}')
        print(f'Name: {case["name"]}')
        print(f'Address: {address}')
        print(f"Case: {court_case}")
        print(f'Party Type: {case["party_type"]}')
        print(f'Party End Date: {case["party_end_date"]}')
        print(f'Filling Date: {case["filling_date"]}')
        print(f'Case Status: {case["case_status"]}')
        
        print("\n")    
        
        
        
# cases = search_case("Linda", "Grimes")


# display_non_closed_cases(cases)


table = get_names_from_file_containing_cases()

# print(table)

new_data_from_website = get_new_data_from_website(table)

store_non_closed_cases(new_data_from_website, "new_data.xlsx")

# display_all_cases(cases)/


