import streamlit as st

# Function to render user input elements
def render_form(catalog, num_db, num_tables):
    if (num_tables or num_db):
        st.markdown("<br>", unsafe_allow_html=True)
        st.write(
            "A total of ",
            num_tables,
            "tables and ",
            num_db,
            "databases were indexed")
        
    st.markdown("<br>", unsafe_allow_html=True)
    k = st.selectbox(
        'How many tables do you want to include in table search result?',
        (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
        index=2)
    
    st.markdown("<br>", unsafe_allow_html=True)
    query = st.text_area(
        'Prompt',
        "What is the total inventory per warehouse?")

    st.markdown("<br>", unsafe_allow_html=True)
    with st.sidebar:
        st.subheader(":violet[Data Catalog] :point_down:")
        st.write(catalog)

    return k, query