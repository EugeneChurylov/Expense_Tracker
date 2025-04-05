import streamlit as st
import pandas as pd
import os

st.title("My Expense Tracker")
st.header("Add a new expense")
st.subheader("Summary")

with st.form("form_name"):
    # your input elements go here
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Rent", "Transport", "Other"])
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)
    submitted = st.form_submit_button("Add Expense")
    if submitted:
        new_entry = {
            "Date": date,
            "Category": category,
            "Description": description,
            "Amount": amount
        }

        filename = "expenses.csv"

        if os.path.exists(filename):
            df = pd.read_csv(filename)
        else:
            df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)

        df.to_csv(filename, index=False)
        st.success("✅ Expense added successfully!")

        print(df)
