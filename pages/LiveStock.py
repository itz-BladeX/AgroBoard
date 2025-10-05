import streamlit as st
import shelve
import pandas as pd
import supplementary as sup
from streamlit_javascript import st_javascript
import time

database = "livestock_database"
st.set_page_config(layout="wide")


Width = st_javascript("window.innerWidth", key="livestock_width")
sup.render_nav("Livestock Data", Width)
time.sleep(0.5)


if "adl" not in st.session_state:
    st.session_state.adl = False




st.markdown("""<style> button { height: 56px !important; padding-bottom:5px !important; } </style>""", unsafe_allow_html=True)


if "bigl" not in st.session_state:
    st.session_state.bigl = False
# Toggle for custom made table of built in st.framework()
bcol1, bcol2 = st.columns(2)
c1, c2, c3 = st.columns(3)

with st.container(border=True):
    with bcol2: 
        if st.button("Reload", width="stretch", icon=":material/autorenew:"):
            st.rerun()
        
    with bcol1:
        if st.button("Big Screen", width="stretch", icon=":material/fullscreen:"):
            st.session_state.bigl = not st.session_state.bigl
    st.button("Add Data", width="stretch", icon=":material/add:", on_click=sup.add_data, args=(database,))
        

if st.session_state.bigl:
    info1, info2 = st.columns([0.84,1])
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns([2,3,3,3,3,3,2.5,2.5,1,1])
    
    with info1:
        st.info("Progress")
    with info2:
        st.info("Economics [Birr]")

    with shelve.open(database) as db:
        with st.container(key="big_table", border=True):
            with col1: st.info("ID")
            with col2: st.info("Type")
            with col3: st.info("Imported Date")
            with col4: st.info("Estimated Date")
            with col5: st.info("Import Cost")
            with col6: st.info("Export Cost")
            with col7: st.info("Prod. Cost")
            with col8: st.info("Profit")
            with col9: st.button("", icon=":material/edit:", type="secondary")
            with col10:st.button("",icon=":material/delete:", type="secondary")

        
            for key in db:  # Loop over the db keys and display results
                livestock = db[key]
                with col1: st.success(livestock.id)
                with col2: st.success(livestock.type)
                with col3: st.success(livestock.date)
                with col4: st.success(livestock.estimated)
                with col5: st.success(sup.format_number(livestock.import_cost))
                with col6: st.success(sup.format_number(livestock.export_cost))
                with col7: st.success(sup.format_number(livestock.production_cost))
                with col8: st.success(sup.format_number(livestock.profit))
                with col9: st.button(icon=":material/edit:", label="", key=f"edit{key}", on_click=sup.edit, args=(database, key), type="secondary", help="Edit Data")
                with col10: st.button(icon=":material/delete:",label="", key=f"del{key}", on_click=sup.delete, args=(database, key), type="primary", help="Delete Data Permanently")


else:  # DataFrame for small table id toggle not toggled
    with shelve.open(database) as db:
        data = {key: vars(livestock) for key, livestock in db.items()}
        # st.write("Loaded keys:", list(db.keys()))
        data = pd.DataFrame.from_dict(data, orient="index")
        if "id" in data.columns:
            data = data.drop(columns=["id"])
        data.index.name = "ID"
        data = data.rename(columns={
            "id": "LiveStock ID",
            "type": "LiveStock Type",
            "date": "Imported Date",
            "estimated": "Estimated",
            "amount": "Amount",
            "import_cost": "Import Cost",
            "export_cost": "Export Cost",
            "production_cost" : "Prod.Cost",
            "profit" : "Profit"
        })
        st.dataframe(data, width="stretch")



