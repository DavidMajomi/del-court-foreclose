import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from dateutil import parser



# Latest three entries
# Plaintiff (Mrtgage Company)
# Judge
# Attorney

# Find people with foreclosures


# 1:15 PM

# Plaintiff (Mortgage Company) Attorney Judge Below: Last 3 Docket entries, including the date, the name of the entry and the Entry


# Entry Info
# Name, Date, and entry



# https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_doct.cp_dktrpt_setup_idx New main
# https://courtconnect.courts.delaware.gov/cc/cconnect/ck_public_qry_cpty.cp_personcase_setup_idx


def conv_to_string(list_val):
    conv_str = ""
    
    count = 0
    for i in list_val:
        if count > 0:
            conv_str = conv_str + " \n" + str(i) 
        else:
            conv_str = conv_str + str(i)
        
        
    return conv_str
    
    
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
        
        
def count_num_char_for_case_no(address):
    case_no = ""
    
    if "unavailableCase" in address:
        unavailable_pos = address.find("unavailableCase:")
        clean_addr = address[unavailable_pos + len("unavailableCase:") + 2:] # +2 to address space after unavailable case
        
        space_pos = clean_addr.find(' ')
        case_no = clean_addr[:space_pos]
        
        # print(address)
        # print("Cleam: ", clean_addr)
        # print(space_pos)
        # print(case_no)
    
    else:
        
        case_pos = address.find("Case: ")
        new_addr = address[case_pos + len("Case: ") + 1:]
        # case_val = new_addr
        space_pos = new_addr.find(' ')
        
        case_no = new_addr[:space_pos]
        # print("Cleam: ", new_addr)
        # print(space_pos)
        # print(case_no)
        
    
    len_case_no = len(case_no)
    
    # print(case_no) 
    
    return len_case_no


def conv_web_space_to_normal_space(value):
    val_list = list(value)
    
    for i in range(len(val_list)):
        if val_list[i] == ' ':
            val_list[i] = ' '
            pass
        
    final_val = ""
    
    for i in val_list:
        final_val = final_val + str(i)
        
    
    return final_val


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
                    "case_status" : list_of_vals[6],
                    "Case_no" : "",
                    "Court_case" : ""
                
                }
            
                case_data["Address"] = conv_web_space_to_normal_space(case_data["Address"])
                
                len_case_no = count_num_char_for_case_no(str(case_data["Address"]))
                # print(len_case_no)
                
                case_data["Address"], case_data["Case_no"], case_data["Court_case"] = split_address(case_data["Address"], len_case_no)

                cases.append(case_data)
                # print(cases)
            
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
    
    return count
            

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


def get_names_from_file_containing_cases_without_case_no():
    
    # columns = ["Owner Last Name", "Owner First Name"]
    
    table = pd.read_excel("sample.xlsx")
    # table = pd.read_excel("PreForeclosures.xlsx", usecols=columns)
    
    
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
            cases = []
            number_of_nan = number_of_nan + 1
            
            print(f"Not a str value: {row['Case Number']} \n Number of such values: {number_of_nan}")
        
        print(f"Iteration: {i}")
        
        for case in cases:
            
            # if case["case_status"] != "CLOSED-CLOSED":
                
            all_cases.append(case)
        
    df = pd.DataFrame.from_dict(all_cases)
    print(f"Not a str value: {row['Case Number']} \n Number of such values: {number_of_nan}")
    
    
        
    return df, number_of_nan
        
    
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
        
        
def format_case_data_from_web(case_no, df_general, df_core, df_entries):
    # print(df_general)
    # print(df_core)

    list_of_relevant_entries = []
    num_rows_entries, num_cols_entries = df_entries.shape
    for index,row in df_entries.iterrows():
        if(index >= num_rows_entries - 3):
            list_of_relevant_entries.append(row[1])
            
            
    str_relevant_entries = ""

    for val in list_of_relevant_entries:
        str_relevant_entries = str_relevant_entries + "/" + str(val)
        
    # print(str_relevant_entries)
        
        
    list_of_plaintiffs = []
    list_of_plaintiff_attorney = []
    list_of_judges = []
    list_of_sheriffs = []
    list_of_program_administrators = []       
    list_of_plaintiff_attorney = []

    # print(df_core[1][2])
    # print(df_general)
    
    if len(df_general) >= 4:
        status = (df_general[2][4])
    else:
        status = "Cannot Retrieve"
        
    
    
    for index, row in df_core.iterrows():
        if index > 0:
            type_val = row[3]
            name = row[5]
            if type_val == "PLAINTIFF":
                list_of_plaintiffs.append(row[5])
                
            elif type_val == "ATTORNEY FOR PLAINTIFF":
                list_of_plaintiff_attorney.append(name)
                
            elif type_val == "JUDGE":
                list_of_judges.append(name)
                
            # elif type_val == "SHERIFF":
            #     list_of_sheriffs.append(name)
                
            # elif type_val == "PROGRAM ADMINISTRATOR":
            #     list_of_program_administrators.append(name)
                
                
                
    gathered_data = {
        "case_no" : case_no,
        "case_status" : status,
        "plaintiffs" : conv_to_string(list_of_plaintiffs),
        # "Sheriffs" : (list_of_sheriffs),
        "plaintiffs_attorney" : conv_to_string(list_of_plaintiff_attorney),
        "latest_entries" : conv_to_string(list_of_relevant_entries),
        # "program_admin" : (list_of_program_administrators)
    }         

        
    return (gathered_data)
    
    
def get_new_web_case_data(table: pd.DataFrame):
    
    all_cases = []
    num_fail = 0
    
    number_of_nan = 0
    list_of_gathered_data = []
    for i, row in table.iterrows():
        # time.sleep(0.5)
        # time.sleep(0.05)
        
        if(type(row["Case Number"]) == str):
            df_general, df_core, df_entries, fail = search_case_data_using_case_id(row["Case Number"])
            
            if fail == False:
                

                gathered_data = format_case_data_from_web(row["Case Number"], df_general, df_core, df_entries)



                list_of_gathered_data.append(gathered_data)
            else:
                num_fail = num_fail + 1



            
        else:
            number_of_nan = number_of_nan + 1
            
            print(f"Not a str value: {row['Case Number']} \n Number of such values: {number_of_nan}")
        
        print(f"Iteration: {i}")
        
        
    df = pd.DataFrame(list_of_gathered_data)    
    print(f"Not a str value: {row['Case Number']} \n Number of such values: {number_of_nan}")
    print(f"Num Fail: {num_fail}")
    
    
        
    return df, num_fail



def get_complete_web_cases_as_file():
    df = get_names_from_file_containing_cases()
    total_issues = find_abnormal_size_of_case_numbers(df)
    clean_case_numbers(df)
    total_issues = find_abnormal_size_of_case_numbers(df)

    df, num_failed_searches = get_new_web_case_data(df)
    print(df)
    store_non_closed_cases(df, "data.xlsx")


def get_first_case_no_from_search(cases):
    first_case = cases[0]

    first_case_no = first_case["Case_no"]
    
    return first_case_no


def get_first_case_with_n_or_k(cases):
    
    for case in cases:
        temp_case_no = case["Case_no"]
        temp_filling_date = parser.parse(case["filling_date"])
        
        if temp_case_no[0] == 'K' or temp_case_no[0] == 'N':
            return case
        
    return None
            

def get_filtered_case_no(cases):
    valid_case_no = None
    
    valid_case_with_most_recent_filling_date = get_first_case_with_n_or_k(cases)
    
    if valid_case_with_most_recent_filling_date is None:
        valid_case_with_most_recent_filling_date = cases[0]
    
    for case in cases:
        most_recent_filling_date = parser.parse(valid_case_with_most_recent_filling_date["filling_date"])
        
        temp_case_no = case["Case_no"]
        temp_filling_date = parser.parse(case["filling_date"])
        
        if temp_case_no[0] == 'K' or temp_case_no[0] == 'N':
            
            if temp_filling_date > most_recent_filling_date:
                valid_case_with_most_recent_filling_date = case
            
            
    valid_case_no = valid_case_with_most_recent_filling_date["Case_no"]
    
    if valid_case_no[0] == 'K' or valid_case_no[0] == 'N':
        valid_case_no = valid_case_no
    else:
        valid_case_no = "Not Valid"
        
    
    return valid_case_no


def get_case_no_for_all_data(df):
    num_not_available = 0
    case_numbers = []
    
    for i, row in df.iterrows():
        first_name = row["Owner First Name"]
        last_name = row["Owner Last Name"]
        
        # print(first_name, last_name)
        
        cases = search_case(first_name, last_name)
        
        if len(cases) == 0:
            case_numbers.append(None)
            num_not_available = num_not_available + 1
        else:
            case_numbers.append(get_first_case_no_from_search(cases))
            
        
        
        # print(cases)
        
        
    df["Case Number"] = case_numbers
    
    return df, num_not_available
        
        

# cases = search_case_matching_case_number("Linda", "Grimes", "N23L-10-013")

# display_non_closed_cases(cases)



# get_complete_web_cases_as_file()


# ##### Search using case id
# case_id = "N23L-10-013s
# df_general, df_core, df_entries = search_case_data_using_case_id(case_id)

# print(df_general


# print(table)

# new_data_from_website = get_new_data_from_website(table)

# print(table)
# print(new_data_from_website)

# store_non_closed_cases(new_data_from_website, "new_data.xlsx")



# display_all_cases(cases)



# cases = search_case("Linda", "Grimes")
# cases_two = search_case("Linda", "Grimes")

# # print(cases)
# display_all_cases(cases)
# case_no = get_first_case_no_from_search(cases)
# print(case_no)
# case_no = get_filtered_case_no(cases_two)
# print(case_no)



# df = get_names_from_file_containing_cases_without_case_no()
# print(df)
# df, num_not_available = get_case_no_for_all_data(df)
# print(df)
# print(num_not_available)

# total_issues = find_abnormal_size_of_case_numbers(df)
# clean_case_numbers(df)
# total_issues = find_abnormal_size_of_case_numbers(df)

# df, num_fails = get_new_web_case_data(df)
# print(df)






# df.to_excel("case_data_.xlsx")

