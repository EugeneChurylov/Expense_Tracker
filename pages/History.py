import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.title("My Expense History")

# Radio button to toggle between desktop and mobile view
layout_mode = st.radio("View mode", ["🖥️ Desktop", "📱 Mobile"], horizontal=True)

filename = "expenses.csv"

if os.path.exists(filename):
    df = pd.read_csv(filename)

    if df.empty:
        st.info("No expenses found yet.")
        st.stop()

    categories = df["Category"].unique()
    selected_category = st.selectbox("Filter by Category", options=["All"] + list(categories))
    if selected_category != "All":
        df = df[df["Category"] == selected_category]

    # 1. Make sure Date column is in datetime format
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 2. Date range filter UI
    start_date = st.date_input("Start date", value=df["Date"].min().date())
    end_date = st.date_input("End date", value=df["Date"].max().date())

    # 3. Filter the DataFrame
    df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

    # 4. Format Date column as string for display
    df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

    st.subheader("📋 All Expenses")

    # # Table headers
    # header1, header2, header3, header4, header5 = st.columns([2, 2, 3, 2, 1])
    # header1.markdown("**Date**")
    # header2.markdown("**Category**")
    # header3.markdown("**Description**")
    # header4.markdown("**Amount**")
    # header5.markdown(" ")  # blank for delete column

    for index, row in df.iterrows():
        if layout_mode == "Desktop":
            col1, col2, col3, col4, col5 = st.columns([2, 2, 3, 2, 1])
            col1.write(row["Date"])
            col2.write(row["Category"])
            col3.write(row["Description"])
            col4.write(f"€{row['Amount']:.2f}")
            if col5.button("🗑️", key=f"delete_{index}"):
                df = df.drop(index)
                df.reset_index(drop=True, inplace=True)
                df.to_csv("expenses.csv", index=False)
                st.success("Deleted!")
                st.rerun()

        else:  # Mobile layout
            with st.container():
                st.markdown("---")
                st.markdown(f"**📅 Date:** {row['Date']}")
                st.markdown(f"**🏷️ Category:** {row['Category']}")
                st.markdown(f"**📝 Description:** {row['Description']}")
                st.markdown(f"**💶 Amount:** €{row['Amount']:.2f}")
                if st.button("🗑️ Delete", key=f"delete_{index}"):
                    df = df.drop(index)
                    df.reset_index(drop=True, inplace=True)
                    df.to_csv("expenses.csv", index=False)
                    st.success("Deleted!")
                    st.rerun()

    total_spent = df["Amount"].sum()
    st.markdown(
        f"""
        <div style='text-align:center; line-height:1;'>
            <h2 style='margin-bottom:0; padding-bottom:0;'>💶 Total Spent</h2>
            <h1 style='margin-top:0; padding-top:0;'>€{total_spent:.2f}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Group expenses by category
    category_summary = df.groupby("Category")["Amount"].sum().reset_index()

    # Create pie chart
    fig = px.pie(
        category_summary,
        names="Category",
        values="Amount",
        title="Spending Breakdown by Category",
        hole=0.3  # Optional: makes it a donut chart
    )

    # Show it in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    df["Date_dt"] = pd.to_datetime(df["Date"], errors="coerce")
    monthly_summary = df.groupby(df["Date_dt"].dt.to_period("M"))["Amount"].sum().reset_index()
    monthly_summary["Date"] = monthly_summary["Date_dt"].astype(str)
    st.subheader("📈 Monthly Spending Trend")
    st.line_chart(monthly_summary.set_index("Date")["Amount"])

else:
    st.info("No expenses found yet.")


