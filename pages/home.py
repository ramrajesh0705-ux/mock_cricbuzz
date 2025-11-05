import streamlit as st
st.title("Cricbuzz Application - Project Description")

st.subheader("Description")
st.write("It is a mock application of Cricbuzz.")
st.write("It includes feature as follows")
import streamlit as st

st.markdown("""
    <div class="custom-list">
        <ol>
            <li>Live Match Scores</li>
            <li>Player Career Info</li>
            <li>SQL Analysis of Player & Teams</li>
            <li>CRUD Application</li>
        </ol>
    </div>
""", unsafe_allow_html=True)

st.subheader("Tool Used")
st.markdown("""
    <div class="custom-list">
        <ol>
            <li>Python</li>
            <li>requests library</li>
            <li>python-postgresql connector</li>
            <li>Streamlit</li>
            <li>JSON</li>
        </ol>
    </div>
""", unsafe_allow_html=True)
