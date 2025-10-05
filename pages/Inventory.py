import streamlit as st
import shelve
import pandas as pd
import supplementary as sup
from streamlit_javascript import st_javascript
import time

database = "inventory_database"

st.set_page_config(layout="wide")
Width = st_javascript("window.innerWidth", key="inventory_width")
sup.render_nav("Inventory Data", Width)
time.sleep(0.5)

tab1, tab2, tab3 = st.tabs(["View", "Add", "Update"])



# if "ad" not in st.session_state:
#     st.session_state.ad = False



# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------

st.markdown("""<style> button { height: 56px !important; padding-bottom:5px !important; } </style>""", unsafe_allow_html=True)
with tab1:
    if "bigv" not in st.session_state:
        st.session_state.bigv = False
    # Toggle for custom made table of built in st.framework()
    bcol1, bcol2 = st.columns(2)

    with st.container(border=True):
        with bcol2: 
            if st.button("Reload", width="stretch", icon=":material/autorenew:"): st.rerun()
            
        with bcol1:
            if st.button("Big Screen", width="stretch", icon=":material/fullscreen:"):
                st.session_state.bigv = not st.session_state.bigv
        st.button("Add Data", width="stretch", icon=":material/add:", on_click=sup.add_data, args=(database,))

    if st.session_state.bigv:
        info1, info2 = st.columns(2)
        col1, col2, col3, col4, col5, col6= st.columns(6)

        with shelve.open(database) as db:
            with col1: st.info("ID")
            with col2: st.info("Label")
            with col3: st.info("Quantity [Units\Litre\]")
            with col4: st.info("Date")
            with col5: st.button("", icon=":material/edit:", type="secondary", width='stretch')
            with col6: st.button("",icon=":material/warning:",type="primary", width="stretch")

            st.divider()

            for key in db:  # Loop over the db keys and display results
                inventory = db[key]
                with st.container():
                    with col1: st.success(inventory.id)
                    with col2: st.success(inventory.label)
                    with col3: st.success(inventory.quantity)
                    with col4: st.success(inventory.date)
                    with col5: st.button("", icon=":material/edit:", type="secondary", key=f"edit{key}",help="Edit Data", on_click=sup.edit, args=(database, key), width="stretch")
                    with col6: st.button("", icon=":material/delete:", type="primary",key=f"del{key}", help="Delete Data Permanently", on_click=sup.delete, args=(database, key), width="stretch")



    else:  # DataFrame for small table id toggle not toggled
        with shelve.open(database) as db:
            data = {key: vars(inventory) for key, inventory in db.items()}
            # st.write("Loaded keys:", list(db.keys()))
            data = pd.DataFrame.from_dict(data, orient="index")
            if "id" in data.columns:
                data = data.drop(columns=["id"])
            data.index.name = "ID"
            data = data.rename(columns={
                "id": "ID",
                "label": "Label",
                "quantity": "Quantity [Units\Litre\]",
                "date": "Date"
            })
            st.dataframe(data, width="stretch")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:  # Clear DataBase

        if "confirmv" not in st.session_state:
            st.session_state.confirmv = False

        if st.button("Clear", width="stretch", icon=":material/warning:"):
            st.session_state.confirmv = True

        if st.session_state.confirmv:

            st.error("WARNING", width="stretch", icon=":material/warning:")
            st.error("YOU ARE ABOUT TO CLEAR ALL YOUR DATABASE!!!", width="stretch", icon=":material/clear:")
            dcol1, dcol2 = st.columns(2)

            with dcol1:
                if st.button("DELETE", type="primary", use_container_width=True, icon=":material/clear:"):

                    with shelve.open(database) as db:
                        db.clear()
                    with col2:
                        st.success("Database cleared", icon=":material/clear:")
                        st.session_state.confirmv = False

            with dcol2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.confirmv = False



    
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
# def toggle():   # Advanced Obtion Toggle
#     st.session_state.adv = not st.session_state.ad
with tab2:
    left, middle, right = st.columns([1, 2, 1])
    with middle:
        with st.container():
            st.title("Add Crop")
            # st.toggle("Advanced", on_change=toggle, value=st.session_state.ad)
            with st.form(key="inv info"):
                # Collect Crop Informatioln
                id = str(st.text_input("ID: ", placeholder="3 digit ID recommended"))
                label = st.selectbox(label="Type", options=[key for key in sup.inventory_dict])
                quantity = st.number_input(label="Quantity [Units\Litre\]", min_value=1)
                date = st.date_input("Planted Date")
                submit = st.form_submit_button(width="stretch")
                
                if submit:  # Check if ID is taken or not
                    if all([id, label,submit]) == False:  # check if every parameter is filled
                        st.warning("Please Fill every box")
                    else:
                        with shelve.open(database) as db:
                            if id not in db:
                                inventory = sup.inventory(id=id, label=label, date=date, quantity=quantity)
                                db[id] = inventory
                                st.success(f"Saved Successfully {inventory.id}: {inventory.label}", width="stretch")
                            else:
                                st.warning("Crop ID is Taken")
# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
with tab3:
    if "editv" not in st.session_state: st.session_state.editv = False
    if "deletev" not in st.session_state: st.session_state.deletev = False
    if "searchv" not in st.session_state: st.session_state.searchv = False

    search_col1, search_col2, search_col3 = st.columns([1, 2, 1])
    with search_col2:  # Search Bar
        with st.container(border=True):
            with shelve.open(database) as db:
                search_id = str(st.selectbox(options=[keys for keys in db.keys()], label="Crop ID"))
            search = st.button("Search", width="stretch", icon=":material/search:")
            edit = st.button("Edit", width="stretch",icon=":material/edit:")
            delete = st.button("Delete", width="stretch", icon=":material/clear:", type="primary")
        def check_id(search_id):
            with shelve.open(database) as db:
                if search_id in db:
                    return True
                else:
                    with search_col2:
                        st.warning("ID not Found")
                    return False

        if delete: 
            st.session_state.deletev = check_id(search_id)
            st.session_state.editv = False
            st.session_state.searchv = False
        if edit: 
            st.session_state.editv = check_id(search_id)
            st.session_state.deletev = False
            st.session_state.searchv = False

        if search: 
            st.session_state.searchv = check_id(search_id)
            st.session_state.editv = False
            st.session_state.deletev = False
            
        if st.session_state.deletev:
            st.error("WARNING, Are You Sure You WANT To DELETE THE SELECTED DATA PERMENENTLY!!", width="stretch", icon=":material/warning:")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("DELETE", type="primary", use_container_width=True):
                    with shelve.open(database) as db: del db[search_id]
                    with search_col2: st.success("Data Deleted", icon=":material/clear:")
                    st.session_state.deletev = False
                    # st.rerun()
            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.deletev = False
                    # st.rerun()

    
    if st.session_state.searchv:  # Search Alg
        col1, col2, col3, col4 = st.columns(4)
        st.session_state.editv = False
        with shelve.open(database) as db:
            if search_id not in db:
                with search_col2:
                    st.warning("ID not found")
            else:
                with col1:
                    st.info("ID")
                    st.success(db[search_id].id)
                with col2:
                    st.info("Type")
                    st.success(db[search_id].label)
                with col3:
                    st.info("Planted Date")
                    st.success(db[search_id].quantity)
                with col4:
                    st.info("Harvest")
                    st.success(db[search_id].date)
    with search_col2:
        if st.session_state.editv:
            with st.container():
                st.title("Edit Inventory")
                with st.form(key="inv delete"):
                    with shelve.open(database) as db:
                    # Collect Crop Informatioln
                        new_id = str(st.text_input("ID", placeholder="3 digit ID recommended", value=db[search_id].id))
                        new_label = st.selectbox(label="Type", options=[key for key in sup.inventory_dict], index=[key for key in sup.inventory_dict].index(db[search_id].label))
                        new_quantity = st.number_input(label="Quantity", value=db[search_id].quantity)
                        new_date = st.date_input("Planted Date", value=db[search_id].date)
                        submit_edit = st.form_submit_button(width="stretch")
                        
                        
                        if submit_edit:
                            if not all([new_id, new_label, new_date, submit_edit]):  # check if every parameter is filled
                                st.warning("Please Fill every box")
                            if not (new_id in db and new_id!= search_id):
                                if new_id != search_id:
                                    del db[search_id]
                                new_inventory = sup.inventory(label=new_label, date=new_date, id=new_id, quantity=new_quantity)
                                db[new_id] = new_inventory
                                st.success(f"Saved Successfully {new_inventory.id}: {new_inventory.label}", width="stretch")
                                st.session_state.editv = False
                            else:
                                st.warning("ID Already Taken")

                    

                        
 