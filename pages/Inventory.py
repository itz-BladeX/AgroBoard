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



# if "ad" not in st.session_state:
#     st.session_state.ad = False



# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------

st.markdown("""<style> button { height: 56px !important; padding-bottom:5px !important; } </style>""", unsafe_allow_html=True)

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