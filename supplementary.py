import requests
import geocoder
import datetime as dt
import streamlit as st
import altair as alt
import shelve
import pandas as pd
from datetime import datetime
import streamlit_option_menu as om
import time
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def format_number(number):
    if number == None:
        return None
    return "{:,}".format(number)
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------\
# Crop Class used under Crop.py / tab2
@st.dialog("Delete Data Permenantly🚨")
def delete(database=None, id=None):
    with shelve.open(database) as db:
        if database == "inventory_database":
            st.write(f"Are you sure you want to delete data {id} of label {db[id].label} ? ?")
        else: st.write(f"Are you sure you want to delete data {id} of type {db[id].type} ?")
        st.error("This action is irreversible! ⚠️", width="stretch")
        confirm = st.button("Confirm Delete", type="primary", width="stretch", icon=":material/delete:", help="This action is irreversible")
        if confirm:
            del db[id]
            st.success("Deleted Successfully", width="stretch")
            time.sleep(1)
            st.rerun()

class class_crop:  # Class for crops called by Crops.py file to save new crops to db
    def __init__(self, type=None, date=None, id=None, estimated=None, import_cost=None,profit=None, production_cost=None, export_cost=None):
        self.type = type
        self.date = date
        if estimated != None:
            self.estimated = estimated
            self.user = "[User]"
        else:
            self.estimated = estimated_date(date, crop_dict[type])
            self.user  = "[Auto]"
        self.id = id
        self.import_cost = import_cost
        self.export_cost = export_cost
        self.production_cost = production_cost
        if import_cost != None and export_cost != None:
            self.profit = cal_profit(import_cost, export_cost, production_cost)
        else:
            self.profit = profit
   
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------


class class_livestock:
    def __init__(self, id, type, date, amount, estimated=None, import_cost=None, export_cost=None,production_cost=None, profit=None):
        self.id = id
        self.type = type
        self.date = date
        self.estimated = estimated
        self.amount = amount
        self.import_cost = import_cost
        self.export_cost = export_cost
        self.production_cost = production_cost
        if import_cost != None and export_cost != None:
            self.profit = cal_profit(import_cost, export_cost, production_cost)
        else:
            self.profit = profit
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
class class_inventory:
    def __init__(self, id, label, quantity, date):
        self.id = id
        self.label = label
        self.quantity = quantity
        self.date = date

# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------

inventory_dict={
    "Shovel",
    "Fertilizer",
    "Tractors",
    "Seed",
    "Pesticides",
    "Hoes",
    "Watering Cans",
    "Plough",
    "Sprayers",
    "Wheelbarrows",
}
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
livestock_dict = {
    "Goat": 1,
    "Sheep": 1,
    "Cattle": 1,
    "Cow": 1,
    "Chicken": 1,
    "Pig": 1,
    "Beehive": 1,
    "Fish": 1,
}
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
crop_dict = {  # Some pre-defined crops used to show the obtions and contains their average harvest peroid in days
    "Teff": 75,
    "Maize": 90,
    "Inset": 730,
    "Wheat": 91,
    "Sorghum": 110,
    "Corn": 80,
    "Barley": 130,
    "Rice": 150,
}
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------

# Get Weather -----------------------------------------------------------------------------------------------
@st.cache_data()  # Store to catch
def get_weather(arg):
    try:
        g = geocoder.ip('me')
        city = g.city
        state = g.state
        country = g.country
        lat, lon = g.latlng
        # url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=precipitation"
        print("Your approximate location (latitude, longitude):", g.latlng)

        response = requests.get(url)
        data = response.json()
        weather = data["current_weather"]
        rainfall = sum(data["hourly"]["precipitation"][:12])

        if arg == "temp":
            return f"☀️ {round(weather["temperature"], 2)} °C"
        elif arg == "wind":
            return f"💨 {round(weather["windspeed"],2)} km/h"
        elif arg == "rainfall":
            return f"🌧️ {round(rainfall,2)} mm"
        elif arg == "station":
            return f"🏠 {city}"

        print("Open-Meteo Current Weather:")
        print(data["current_weather"])
        print(response)
        print(response)
        print(f"""
            City: {city}
            State: {state}
            Country: {country}
            Time: {weather['time']}
            Temp: {weather["temperature"]} °C
            Wind Speed: {weather["windspeed"]} km/h
            Rainfall: {rainfall} mm
        """)
        # lit.st.metric("Weather", weather["temperature"], -3)

    except Exception as e:
        print(
            "Error while Searching for weather, Try again when enternet is available !", e)
        return "—"
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
# Caculate Estimated Harvest Day, Called by class Crop


def estimated_date(current_date, add_days):

    def is_leap_year(year):  # Check for leap year, if found make feb 28 days else feb is 29 days
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    days_in_month = {  # Days for each month
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
    }

    day = current_date.day
    month = current_date.month
    year = current_date.year
    while add_days > 0:  # Calculate the day, month and year
        if month == 2 and is_leap_year(year):
            days_in_month[month] += 1
        if day < days_in_month[month]:
            day += 1
        else:
            day = 1
            month += 1
            if month > 12:
                month = 1
                year += 1
        add_days -= 1
    # return the estimated date as datetime object
    return dt.date(year, month, day)
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def cal_profit(import_cost, export_cost, production_cost=None):  #Profil Calculation
    if production_cost != None: 
        return export_cost - (import_cost + production_cost)
    return export_cost - import_cost
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def alter_graph(id, database, height): #
    with shelve.open(database) as db:
        df = pd.DataFrame({
            "Metric" : ["Import", "Export","Prod", "Profit"],
            "Value" : [db[id].import_cost, db[id].export_cost, db[id].production_cost, db[id].profit],
            "colors" :["#e74c3c","#3498db","#e74c3c","#2ecc71"]    
    })
    chart = alt.Chart(df).mark_bar().encode(
        x = "Metric",
        y = "Value",
        # tooltip=None,
        color = alt.Color("colors:N", scale=None)
    ).properties(
        width=600,
        height=height,
    )
    return chart
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def percent_complete(id, database):
    with shelve.open(database) as db:
        try:
            start_date = db[id].date
            end_date = db[id].estimated
            print(type(start_date), start_date, end_date, id)
            total_days = (end_date - start_date).days
            current_date = datetime.now().date()
            days_passed = (current_date - start_date).days

            print(total_days, days_passed, current_date, start_date)
            if total_days == 0:
                day = 100
            else:
                day = min((days_passed / total_days) *100,100)

            return int(day)
        except:
            return None
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
def render_nav(current_page, width):
    pages = {
    "main": "main.py",
    "Crop Data": "pages/Crop.py",
    "Livestock Data": "pages/LiveStock.py",
    "Inventory Data": "pages/Inventory.py",
    "About": "pages/About.py",
    }
    page_list = list(pages.keys())
    if width < 1300:
        with st.sidebar:
            selected = om.option_menu(
                menu_title=None,
                options=page_list ,
                icons=["house", "bar-chart"],
                default_index=page_list.index(current_page)
            )
    else:
         selected = om.option_menu(
                menu_title=None,
                options=page_list, 
                icons=["house", "bar-chart"],
                default_index=page_list.index(current_page),
                orientation="horizontal",
                styles={"nav-link": {"text-align": "center", "margin": "0em", "--hover-color": "#676767"},
                
            }
         )
            
    if selected != current_page:
        st.switch_page(pages[selected])
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
@st.dialog("Add Data")
def add_data(database):
    if database == "crop_database":
        with st.form(key="crop info"):
            st.success("Mandatory Fields 📌")
            id = str(st.text_input("ID: ", placeholder="3 digit ID recommended", help="Unique ID for each crop"))
            type = st.selectbox(label="Type", options=[key for key in crop_dict],help="Type of crop")
            date = st.date_input("Planted Date: ", help="Date when the crop was planted")
            st.info("Non Mandatory Fields ℹ️")
            estimated = st.date_input(label="Expected Harvest: ",value=None,help="date of harvest. If left empty, it will be calculated automatically")
            import_cost = st.number_input(label="Import Price", value=None, min_value=0.0, help="Cost of importing or buying the crop")
            export_cost = st.number_input(label="Export Price", value=None, min_value=0.0, help="Expected selling price of the crop")
            production_cost = st.number_input(label="Production Cost", value=None, min_value=0.0, help="Cost of producing the crop, e.g. fertilizer, water, etc.")
            submit = st.form_submit_button("Submit", type="primary", width='stretch')
            
            if submit:  # Check if ID is taken or not
                if all([id, type, date, submit]) == False:  # check if every parameter is filled
                    st.warning("Please Fill every box")
                else:
                    with shelve.open(database) as db:
                        if id not in db:
                            crop = class_crop(
                                type=type, 
                                date=date, 
                                id=id, import_cost=import_cost,
                                estimated=estimated,
                                export_cost=export_cost, 
                                production_cost=production_cost)
                            db[id] = crop
                            st.success(f"Saved Successfully {crop.id}: {crop.type}", width="stretch")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("Crop ID is Taken")


    elif database == "livestock_database":
        with st.form(key="livestock info"):
            st.success("Mandatory Fields 📌")
            id = str(st.text_input("ID: ", placeholder="3 digit ID recommended", help="Unique ID for each livestock"))
            type = st.selectbox(label="Type", options=[key for key in livestock_dict], help="Type of livestock")
            date = st.date_input("Date: ",help="Date when the livestock was imported or bought")
            amount = st.number_input(label="Amount", value=1, min_value=1, help="Number of livestock imported or bought")
            st.info("Non Mandatory Fields ℹ️")
            estimated = st.date_input(label="Estimated: ",value=None,help="estimated export date, if left empty, it will be filled automatically")
            import_cost = st.number_input(label="Import Price", value=None, min_value=0.0, help="Cost of importing or buying the livestock")
            export_cost = st.number_input(label="Export Price", value=None, min_value=0.0, help="Expected selling price of the crop")
            production_cost = st.number_input(label="Production Cost", value=None, min_value=0.0, help="Cost of producing the crop, e.g. fertilizer, water, etc.")
            submit = st.form_submit_button("Submit", type="primary", width='stretch')           
            if submit:  # Check if ID is taken or not
                if all([id, type, date, amount, submit]) == False:  # check if every parameter is filled
                    st.warning("Please Fill every box")
                else:
                    with shelve.open(database) as db:
                        if id not in db:
                            livestock = class_livestock(
                                id=id,
                                type=type,
                                date=date,
                                amount=amount,
                                import_cost=import_cost,
                                export_cost=export_cost,
                                production_cost=production_cost,
                                estimated=estimated
                                )
                            db[id] = livestock
                            st.success(f"Saved Successfully {livestock.id}: {livestock.type}", width="stretch")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("Livestock ID is Taken")
    elif database == "inventory_database":
        with st.form(key="inventory info"):
            st.success("Mandatory Fields 📌")
            id = str(st.text_input("ID: ", placeholder="3 digit ID recommended", help="Unique ID for each inventory item"))
            label = st.selectbox(label="Label", options=[key for key in inventory_dict], help="Type of inventory item")
            date = st.date_input("Date: ", help="Date when the inventory item was added")
            quantity = st.number_input(label="Quantity", value=1, min_value=1, help="Quantity of the inventory item")
            submit = st.form_submit_button("Submit", type="primary", width='stretch')           
            if submit:  # Check if ID is taken or not
                if all([id, label, date, quantity, submit]) == False:  # check if every parameter is filled
                    st.warning("Please Fill every box")
                else:
                    with shelve.open(database) as db:
                        if id not in db:
                            inventory = class_inventory(
                                id=id,
                                label=label,
                                date=date,
                                quantity=quantity
                                )
                            db[id] = inventory
                            st.success(f"Saved Successfully {inventory.id}: {inventory.label}", width="stretch")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("Inventory ID is Taken")

  # ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------  
# ---------------------------------------------------------------------------------------------------
@st.dialog("Update / Edit Data")
def edit(database, edit_id):
    if database == "crop_database":
        with st.form(key="crop edit"):
                with shelve.open(database) as db:
                # Collect Crop Informatioln
                    new_id = str(st.text_input("ID", placeholder="3 digit ID recommended", value=db[edit_id].id))
                    new_type = st.selectbox(label="Type", options=[key for key in crop_dict], index=[key for key in crop_dict].index(db[edit_id].type))
                    new_date = st.date_input("Planted Date", value=db[edit_id].date)
                    new_estimated = st.date_input(label="Expected Harvest", value=db[edit_id].estimated)
                    new_import_price = st.number_input(label="Import Price [Birr]", value=db[edit_id].import_cost)
                    new_exported_price = st.number_input(label="Exported Price [Birr]", value=db[edit_id].export_cost)
                    new_production_cost = st.number_input(label = "Production Cost [Birr]", value=db[edit_id].production_cost)
                    submit_edit = st.form_submit_button(width="stretch")
                    if submit_edit:
                                if not all([new_id, new_type, new_date, submit_edit]):  # check if every parameter is filled
                                    st.warning("Please Fill every box")
                                if not (new_id in db and new_id!= edit_id):
                                    if new_id != edit_id:
                                        del db[edit_id]
                                    new_crop = class_crop(type=new_type, date=new_date, id=new_id, import_cost=new_import_price, estimated=new_estimated, export_cost=new_exported_price, production_cost=new_production_cost)
                                    db[new_id] = new_crop
                                    st.success(f"Saved Successfully {new_crop.id}: {new_crop.type}", width="stretch")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.warning("ID Already Taken")


    elif database == "livestock_database":
        with st.form(key="Livestock edit"):
                with shelve.open(database) as db:
                # Collect Crop Informatioln
                    new_id = str(st.text_input("ID", placeholder="3 digit ID recommended", value=db[edit_id].id))
                    new_type = st.selectbox(label="Type", options=[key for key in livestock_dict], index=[key for key in livestock_dict].index(db[edit_id].type))
                    new_date = st.date_input("Imported Date", value=db[edit_id].date)
                    new_amount = st.number_input("Amount Imported", min_value=1, value=db[edit_id].amount)
                    new_estimated = st.date_input(label="Estimated", value=db[edit_id].estimated)
                    new_import_price = st.number_input(label="Import Price [Birr]", value=db[edit_id].import_cost)
                    new_exported_price = st.number_input(label="Exported Price [Birr]", value=db[edit_id].export_cost)
                    new_production_cost = st.number_input(label = "Production Cost [Birr]", value=db[edit_id].production_cost)
                    submit_edit = st.form_submit_button(width="stretch")
                    if submit_edit:
                        if not all([new_id, new_type, new_date, submit_edit]):  # check if every parameter is filled
                            st.warning("Please Fill every box")
                        if not (new_id in db and new_id!= edit_id):
                            if new_id != edit_id:
                                del db[edit_id]
                            new_livestock = class_livestock(
                                type=new_type,
                                date=new_date,
                                id=new_id,
                                amount=new_amount,
                                import_cost=new_import_price,
                                estimated=new_estimated,
                                export_cost=new_exported_price,
                                production_cost=new_production_cost)
                            db[new_id] = new_livestock
                            st.success(f"Saved Successfully {new_livestock.id}: {new_livestock.type}", width="stretch")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("ID Already Taken")
    elif database == "inventory_database":
        with st.form(key="Inventory edit"):
                with shelve.open(database) as db:
                # Collect Crop Informatioln
                    new_id = str(st.text_input("ID", placeholder="3 digit ID recommended", value=db[edit_id].id))
                    new_label = st.selectbox(label="Label", options=[key for key in inventory_dict], index=[key for key in inventory_dict].index(db[edit_id].label))
                    new_date = st.date_input("Date", value=db[edit_id].date)
                    new_quantity = st.number_input("Quantity", min_value=1, value=db[edit_id].quantity)
                    submit_edit = st.form_submit_button(width="stretch")
                    if submit_edit:
                        if not all([new_id, new_label, new_date, new_quantity, submit_edit]):  # check if every parameter is filled
                            st.warning("Please Fill every box")
                        if not (new_id in db and new_id!= edit_id):
                            if new_id != edit_id:
                                del db[edit_id]
                            new_inventory = class_inventory(
                                id=new_id,
                                label=new_label,
                                date=new_date,
                                quantity=new_quantity)
                            db[new_id] = new_inventory
                            st.success(f"Saved Successfully {new_inventory.id}: {new_inventory.label}", width="stretch")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.warning("ID Already Taken")
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================

# ---------------------------------------------------------------------------------------------------
