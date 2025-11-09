import psycopg2
import streamlit as st
import pandas as pd

def create_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",        
            port="5432",             
            database="cricbuzz",  
            user="postgres",       
            password="postgres" 
        )
        return conn
    except Exception as e:
        return None

def execute(query, params=None):
        try:
            conn = create_connection()
            with conn.cursor() as cur:
                cur.execute(query, params or ())
                conn.commit()
                return True
        except Exception as e:
            st.error(f"Error executing query: {e}")
            return False
        finally:
            if conn:
                conn.close()

def fetch_records(query):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        st.error(f"Error fetching records: {e}")
        return pd.DataFrame()
    finally:
        conn.close()
