import requests
import streamlit as st

# Define the URL
url = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070?api-key=579b464db66ec23bdd0000017704f08e67e4414747189afb9ef2d662&format=json&offset=0&limit=4000'

# Fetch data from the API
response = requests.get(url)

st.header("Current Harvest Prices")

# Function to process date
def get_date(date):
    update = date
    print(update)  # You can format the date as needed

# Function to process description
def get_desc(desc):
    print(desc)

# Function to process records
def get_records(records):
    dt = []
    dt.append(["Sr", "State", "District", "Market", "Commodity", "Variety", "Min Price", "Max Price", "Modal Price"])
    for i, record in enumerate(records, start=1):
        sr = i
        state = record['state']
        districts = record['district']
        market = record['market']
        commodity = record['commodity']
        variety = record['variety']
        min_price = record['min_price']
        max_price = record['max_price']
        modal_price = record['modal_price']
        dt.append([sr, state, districts, market, commodity, variety, min_price, max_price, modal_price])

    return dt

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Call functions to process data
    get_date(data['updated_date'])
    get_desc(data['desc'])

    # Get unique states from the data
    states = set(record['state'] for record in data['records'])

    # Select a state from the dropdown
    state_sel = st.selectbox("Select State", sorted(states))

    # Filter records based on the selected state
    filtered_records = [record for record in data['records'] if record['state'] == state_sel]

    # Process and display filtered records
    df = get_records(filtered_records)
    st.table(df)
else:
    print("Failed to fetch data from the API.")
