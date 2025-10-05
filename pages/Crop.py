import streamlit as st
import shelve
import pandas as pd
import supplementary as sup
import time
from streamlit_javascript import st_javascript
st.set_page_config(layout="wide")
database = "crop_database"
width = st_javascript("window.innerWidth", key="crop_width")
with st.spinner("Loading..."):
    sup.render_nav("Crop Data", width)

time.sleep(0.5)



width = st_javascript("window.innerWidth")

# tab1, tab2, tab3 = st.tabs(["View", "Add", "Update"])

if "ad" not in st.session_state:
    st.session_state.ad = False

# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------

st.markdown("""<style> button { height: 56px !important; padding-bottom:5px !important; } </style>""", unsafe_allow_html=True)



if "big" not in st.session_state:
    st.session_state.big = False
# Toggle for custom made table of built in st.framework()
bcol1, bcol2 = st.columns(2)

with st.container(border=True):
    with bcol2: 
        if st.button("Reload", width="stretch", icon=":material/autorenew:"): 
            st.rerun()
    with bcol1:
        if st.button("Big Screen", width="stretch", icon=":material/fullscreen:"):
            st.session_state.big = not st.session_state.big
    st.button("Add Data", width="stretch", icon=":material/add:", on_click=sup.add_data, args=(database,)) 

        
    
if st.session_state.big:
    info1, info2 = st.columns([0.84,1])
    
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([2,3,3,3,3,3,2.5,2.5,1,1])

    with info1:
        st.info("Progress")
    with info2:
        st.info("Economics [Birr]")
    


    with shelve.open(database) as db:
        with col1: st.info("ID")
        with col2: st.info("Type")
        with col3: st.info("Planted Date")
        with col4: st.info("Harvest Date")
        with col5: st.info("Import Cost")
        with col6: st.info("Export Cost")
        with col7: st.info("Prod. Cost")
        with col8: st.info("Profit")
        with col9: st.button("", icon=":material/edit:", type="secondary")
        with col10: st.button("",icon=":material/warning:",type="primary")
        st.divider()

        for key in db:  # Loop over the db keys and display results
            crop = db[key]
            with st.container():
                with col1: st.success(crop.id)
                with col2: st.success(crop.type)
                with col3: st.success(crop.date)
                with col4: st.success(str(crop.estimated) + " " + crop.user)
                with col5: st.success(sup.format_number(crop.import_cost))
                with col6: st.success(sup.format_number(crop.export_cost))
                with col7: st.success(sup.format_number(crop.production_cost))
                with col8: st.success(sup.format_number(crop.profit))
                with col9: st.button(icon=":material/edit:", label="", key=f"edit{key}", on_click=sup.edit, args=(database, key), type="secondary")
                with col10: st.button(icon=":material/delete:",label="", key=f"del{key}", on_click=sup.delete, args=(database, key), type="primary")


else:  # DataFrame for small table id toggle not toggled
    with shelve.open(database) as db:
        data = {key: vars(crop) for key, crop in db.items()}
        # st.write("Loaded keys:", list(db.keys()))
        data = pd.DataFrame.from_dict(data, orient="index")
        if "id" in data.columns:
            data = data.drop(columns=["id"])
        data.index.name = "ID"
        data = data.rename(columns={
            "id": "Crop ID",
            "type": "Crop Type",
            "date": "Planted Date",
            "estimated": "Harvest Estimation",
            "import_cost": "Import Cost",
            "export_cost": "Export Cost",
            "production_cost" : "Prod.Cost",
            "profit" : "Profit"
        })
        st.dataframe(data, width="stretch")


    





# ---------------------------------------------------------------------------------------------------
# ==================================================================================================
# ---------------------------------------------------------------------------------------------------
