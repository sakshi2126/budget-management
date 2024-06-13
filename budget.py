import streamlit as st
import pandas as pd

# Title and data structure initialization
st.title("Simple Budget Tracker")
transactions = pd.DataFrame(columns=["Date", "Category", "Amount", "Description"])

def update_data(new_data):
  global transactions
  transactions = pd.concat([transactions, new_data.iloc[[0]]])
  st.session_state.update({"transactions": transactions.to_dict()})

def display_data():
  if not transactions.empty:
    st.write("## Transaction History")
    st.dataframe(transactions)
  else:
    st.write("No transactions recorded yet.")

# Transaction input section
st.header("Add a Transaction")
date = st.date_input("Date:")
category = st.selectbox("Category:", ["Income", "Expense"])
amount = st.number_input("Amount:")
description = st.text_area("Description (Optional):")

if st.button("Add Transaction"):
  # Validate input (optional)
  if amount == 0:
    st.error("Amount cannot be zero.")
  else:
    new_transaction = pd.DataFrame({
        "Date": [date],
        "Category": [category],
        "Amount": [amount * (-1 if category == "Expense" else 1)],  # Negate for expense
        "Description": [description]
    })
    update_data(new_transaction)
    st.success("Transaction added!")

# Display transaction history
display_data()

# Calculate and display total balance
if not transactions.empty:
  total_balance = transactions["Amount"].sum()
  st.write(f"## Total Balance: {total_balance:.2f}")
