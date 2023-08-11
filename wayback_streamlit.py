import datetime
import re
import time

import requests
import streamlit as st

st.set_page_config(page_title="Wayback Machine with Efficiency", page_icon=None, layout="centered", initial_sidebar_state="expanded", menu_items={"About": "## Wayback Machine with Efficiency \n Made by Atsuya Nakata"})

st.sidebar.title("Wayback Machine with Efficiency")
wayback_url = "http://archive.org/wayback/available"

# Check the datetime format
def is_valid_date(date_str):
    pattern = re.compile(r'^(\d{8}|\d{4})$')
    if pattern.match(date_str):
        return True
    else:
        return False

# Check the domain format
def is_valid_domain(domain_str):
    pattern = re.compile(r'^(?!http://|https://)[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)+$')
    if pattern.match(domain_str):
        return True
    else:
        return False

target_domains = []
timestamps = []

# Required Input as the 1st target domain URL
target_domain_1st = st.sidebar.text_input(label="Enter the target domain URL. NOT include http:// or https:// .", value="google.com", type="default")

# Input the timestamp: by number or by calendar
check_1 = st.sidebar.checkbox(label="Specify Date by Calendar", value=False, key="check_1")
if check_1 == False:
    timestamp_1st = st.sidebar.number_input(label="Enter the year or year-and-date you want to get the snapshot, like: '2020' or '20200401'.", min_value=None, max_value=None, value=2021, key="num_1")
    timestamp_str_1st = str(timestamp_1st)
elif check_1:
    timestamp_1st = st.sidebar.date_input(label="Pick the date from calendar.", value=(datetime.datetime.now() - datetime.timedelta(days=365)), key="cal_1")
    timestamp_str_1st = timestamp_1st.strftime("%Y%m%d")


# Optional: Input more target domain URLs
with st.sidebar.expander(label="More target domain URLs", expanded=False):
    target_domain_2nd = st.text_input(label="2nd URL", value="", type="default")
    check_2 = st.checkbox(label="Specify Date by Calendar", value=False, key="check_2")
    if check_2 == False:
        timestamp_2nd = st.number_input(label="Enter the year or year-and-date for the 2nd.", min_value=None, max_value=None, value=2022, key="num_2")
        timestamp_str_2nd = str(timestamp_2nd)
    elif check_2:
        timestamp_2nd = st.date_input(label="Pick the date from calendar.", value=(datetime.datetime.now() - datetime.timedelta(days=365)), key="cal_2")
        timestamp_str_2nd = timestamp_2nd.strftime("%Y%m%d")
    st.divider()

    target_domain_3rd = st.text_input(label="3rd URL", value="", type="default")
    check_3 = st.checkbox(label="Specify Date by Calendar", value=False, key="check_3")
    if check_3 == False:
        timestamp_3rd = st.number_input(label="Enter the year or year-and-date for the 3rd.", min_value=None, max_value=None, value=2022, key="num_3")
        timestamp_str_3rd = str(timestamp_3rd)
    elif check_3:
        timestamp_3rd = st.date_input(label="Pick the date from calendar.", value=(datetime.datetime.now() - datetime.timedelta(days=365)), key="cal_3")
        timestamp_str_3rd = timestamp_3rd.strftime("%Y%m%d")
    st.divider()

    target_domain_4th = st.text_input(label="4th URL", value="", type="default")
    check_4 = st.checkbox(label="Specify Date by Calendar", value=False, key="check_4")
    if check_4 == False:
        timestamp_4th = st.number_input(label="Enter the year or year-and-date for the 4th.", min_value=None, max_value=None, value=2022, key="num_4")
        timestamp_str_4th = str(timestamp_4th)
    elif check_4:
        timestamp_4th = st.date_input(label="Pick the date from calendar.", value=(datetime.datetime.now() - datetime.timedelta(days=365)), key="cal_4")
        timestamp_str_4th = timestamp_4th.strftime("%Y%m%d")
    st.divider()

    target_domain_5th = st.text_input(label="5th URL", value="", type="default")
    check_5 = st.checkbox(label="Specify Date by Calendar", value=False, key="check_5")
    if check_5 == False:
        timestamp_5th = st.number_input(label="Enter the year or year-and-date for the 5th.", min_value=None, max_value=None, value=2022, key="num_5")
        timestamp_str_5th = str(timestamp_5th)
    elif check_5:
        timestamp_5th = st.date_input(label="Pick the date from calendar.", value=(datetime.datetime.now() - datetime.timedelta(days=365)), key="cal_5")
        timestamp_str_5th = timestamp_5th.strftime("%Y%m%d")
    st.divider()

st.sidebar.write("")
submit_flag = False
submit_flag = st.sidebar.button("Get Archived Snapshot")
if submit_flag:
    # Store the target domain URLs and timestamps
    target_domains.append(target_domain_1st)
    timestamps.append(timestamp_str_1st)

    if target_domain_2nd:
        target_domains.append(target_domain_2nd)
        timestamps.append(timestamp_str_2nd)
    if target_domain_3rd:
        target_domains.append(target_domain_3rd)
        timestamps.append(timestamp_str_3rd)
    if target_domain_4th:
        target_domains.append(target_domain_4th)
        timestamps.append(timestamp_str_4th)
    if target_domain_5th:
        target_domains.append(target_domain_5th)
        timestamps.append(timestamp_str_5th)

    # Check the domain format
    for target_domain in target_domains:
        if not is_valid_domain(target_domain):
            st.error("Invalid domain format: %s" % target_domain)
            st.stop()

    # Check the datetime format
    for timestamp in timestamps:
        if not is_valid_date(timestamp):
            st.error("Invalid date format: %s" % timestamp)
            st.stop()        

    st.header("Results")
    # Make a request to Wayback Machine API
    for i, target_domain in enumerate(target_domains):
        st.subheader(f"{i+1}: {target_domain}")
        with st.spinner('Wait for it...'):
            params = {
                "url": target_domain,
                "timestamp": timestamps[i]
            }
            response = requests.get(wayback_url, params=params)

            if response.status_code == 200:
                json_response = response.json()
                if json_response["archived_snapshots"]:
                    st.write(f"Archived snapshot available at {json_response['archived_snapshots']['closest']['url']}")
                    archived_date = json_response['archived_snapshots']['closest']['timestamp']
                    # Convert the date format: YYYYMMDDhhmmss to YYYY/MM/DD
                    archived_date = datetime.datetime.strptime(archived_date, "%Y%m%d%H%M%S").strftime("%Y/%m/%d")
                    st.write(f"Archived snapshot captured on {archived_date}")
                else:
                    st.write("No archived snapshot for the target URL")
            else:
                st.write("Error: %d" % response.status_code)
            st.divider()
            time.sleep(2)


elif submit_flag == False:
    st.write("Input the target domain URL and the date from the sidebar.")
    