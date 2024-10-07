import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

# https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_doct.cp_dktrpt_setup_idx New main
# https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_cpty.cp_personcase_setup_idx





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
    else:
        print(f"Failed to submit the form. Status code: {response.status_code}")
        
        
    soup=BeautifulSoup(response.content,'lxml')
    
    # print(response.content)
    cases = []
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
                    
                    
            # if get_general_info == True:
                
            if(list_of_vals[0] == "Entry:"):
                entries.append(list_of_vals)
            else:
                pass
                    
            print(list_of_vals)
        
        count += 1
        
    print(entries)
        
        
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
        

def find_abnormal_size_of_case_numbers(table):
    size = 11
    
    count = 0
    for i, row in table.iterrows():
        case_number = row["Case Number"]
        
            
            
        if (type(case_number) == str):
            
            if (len(case_number) != size):
                
                print(f"Len: {len(case_number)}, Value: {case_number}")
                count += 1
                
            
        else:
            print(case_number)
            
            count += 1
            
        
        
    print(f"Total issues: {count}")
            

def clean_case_numbers(table):
    size = 11
    
    for i, row in table.iterrows():
        case_number = row["Case Number"]

        if (type(case_number) == str):
            
            if (len(case_number) != size):
                row["Case Number"] = (row["Case Number"]).replace(' ', '')
                row["Case Number"] = (row["Case Number"]).replace('\n', '')
            
            
def store_non_closed_cases(table: pd.DataFrame, file_name: str):
    
    table.to_excel(file_name)

    
def get_names_from_file_containing_cases():
    
    columns = ["Owner Last Name", "Owner First Name", "Case Number"]
    
    table = pd.read_excel("Pre-Foreclosures.xlsx", usecols=columns)
    
    return table


def get_new_data_from_website(table: pd.DataFrame):
    
    all_cases = []
    
    number_of_nan = 0
    for i, row in table.iterrows():
        first_name = row["Owner First Name"]
        last_name = row["Owner Last Name"]
        
        # time.sleep(0.05)
        
        if(type(row["Case Number"]) == str):
            
            
            cases = search_case_matching_case_number(first_name, last_name, row["Case Number"])
            
            
        else:
            number_of_nan = number_of_nan + 1
            
            print(f"Not a str value: {row['Case Number']} \n Number of such values: {number_of_nan}")
        
        print(f"Iteration: {i}")
        
        for case in cases:
            
            # if case["case_status"] != "CLOSED-CLOSED":
                
            all_cases.append(case)
        
    df = pd.DataFrame.from_dict(all_cases)
    print(f"Not a str value: {row['Case Number']} \n Number of such values: {number_of_nan}")
    
    
        
    return df
        
    

def search_case_matching_case_number(first_name, last_name, case_number):
    # Define the URL to post the data to
    
    # https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_cpty.cp_personcase_srch_details?backto=P&soundex_ind=&partial_ind=&last_name=Grimes&last_name=Grimes&first_name=Linda&middle_name=&begin_date=&end_date=&case_type=ALL&id_code=&PageNo=1
    
    url = f"https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_cpty.cp_personcase_srch_details?backto=P&soundex_ind=&partial_ind=&last_name={last_name}&last_name={last_name}&first_name={first_name}&middle_name=&begin_date=&end_date=&case_type=ALL&id_code=&PageNo=1"

    # Perform the POST request
    response = requests.post(url)

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
                    "case_status" : list_of_vals[6],
                    "Case_no" : "",
                    "Court_case" : ""
                
                }
            
            
                case_data["Address"], case_data["Case_no"], case_data["Court_case"] = split_address(case_data["Address"], len(case_number))
                

            
                # print(case_data)
                
                if (case_number == case_data["Case_no"]):
                    print(f"Retrieved case No: {case_data['Case_no']}")
                    print(f"Initial Case No: {case_number} \n \n")
                    cases.append(case_data)
                    
                else:
                    pass
                    # print("Not matched with case no from file")
            
                # print("\n")
                
                
                case_data = {}
        
        count += 1
        
        
    return cases
     
            
def split_address(value, size_of_case_number):
    # 11
    # unavailableCase:  K22L-02-007  PENNYMAC LOAN SERVICES, LLC, PLAINTIFF, V. KERI CU
    
    # 211 CORNWELL DRIVE BEAR DE 19701 Case:  JP13-10-007833  WILMINGTON TRUST COMPANY VS ROBERT ANTHONY HUNTER

    if "unavailable" in value:
        address = "Not Available"
        case_no = value[18: 18 + size_of_case_number]
        case = value[18 + 2 + size_of_case_number:]
    else:
        case_pos = value.find("Case")
        
        address = value[:case_pos]
        case_no = value[case_pos + 8: case_pos + 8 + size_of_case_number]
        case = value[case_pos + 8 + 2 + size_of_case_number:]
        
        
    return address, case_no, case
    
    
def display_case_details(case):
    
    print(f'Case ID: {case["case_id"]}')
    print(f'Name: {case["name"]}')
    print(f'Address: {case["Address"]}')
    print(f'Case No: {case["Case_no"]}')
    print(f'Case: {case["Court_case"]}')
    print(f'Party Type: {case["party_type"]}')
    print(f'Party End Date: {case["party_end_date"]}')
    print(f'Filling Date: {case["filling_date"]}')
    print(f'Case Status: {case["case_status"]}')
    
    print("\n")    

    
def display_non_closed_cases(cases):
        
    for case in cases:
        if case["case_status"] != "CLOSED-CLOSED":
            
            display_case_details(case)
            
            
def display_all_cases(cases):
    
    for case in cases:
        display_case_details(case)
        
        
        
# cases = search_case_matching_case_number("Linda", "Grimes", "N23L-10-013")

# display_non_closed_cases(cases)


# df = get_names_from_file_containing_cases()
# find_abnormal_size_of_case_numbers(df)
# clean_case_numbers(df)
# find_abnormal_size_of_case_numbers(df)

##### Search using case id
search_case_data_using_case_id("N23L-10-013")



# table = get_names_from_file_containing_cases()
# clean_case_numbers(table)

# print(table)

# new_data_from_website = get_new_data_from_website(table)

# print(table)
# print(new_data_from_website)

# store_non_closed_cases(new_data_from_website, "new_data.xlsx")






# display_all_cases(cases)


