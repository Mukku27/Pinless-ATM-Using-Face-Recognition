import streamlit as st
import pandas as pd
from database import init_db, authenticate_user, get_balance, update_balance, add_transaction, get_transactions

# Initialize database
init_db()

# Main function to render the app
def main():
    st.title("ATM Interface")
    st.write("Welcome to the secure ATM interface!")

    # User authentication
    st.sidebar.title("User Authentication")
    user_name = st.sidebar.text_input("Enter your name:")
    password = st.sidebar.text_input("Enter your password:", type='password')

    if st.sidebar.button("Login"):
        user = authenticate_user(user_name, password)
        if user:
            st.sidebar.success("Authentication successful!")
            st.session_state.authenticated = True
            st.session_state.user_id = user[0]
            st.session_state.user_name = user_name
        else:
            st.sidebar.error("Authentication failed. Please try again.")
            st.session_state.authenticated = False

    if st.session_state.get('authenticated', False):
        menu = ["Balance Inquiry", "Deposit", "Withdraw", "Transaction History", "Logout"]
        choice = st.radio("Select Option", menu)

        if choice == "Balance Inquiry":
            st.subheader("Check Balance")
            balance = get_balance(st.session_state.user_id)
            st.write(f"Your current balance is: ${balance:.2f}")

        elif choice == "Deposit":
            st.subheader("Deposit Money")
            amount = st.number_input("Enter amount to deposit", min_value=0.0, step=0.01)
            if st.button("Deposit"):
                new_balance = get_balance(st.session_state.user_id) + amount
                update_balance(st.session_state.user_id, new_balance)
                add_transaction(st.session_state.user_id, "Deposit", amount)
                st.write(f"Successfully deposited ${amount:.2f}. Your new balance is ${new_balance:.2f}.")

        elif choice == "Withdraw":
            st.subheader("Withdraw Money")
            amount = st.number_input("Enter amount to withdraw", min_value=0.0, step=0.01)
            if st.button("Withdraw"):
                current_balance = get_balance(st.session_state.user_id)
                if amount > current_balance:
                    st.error("Error: Insufficient funds!")
                else:
                    new_balance = current_balance - amount
                    update_balance(st.session_state.user_id, new_balance)
                    add_transaction(st.session_state.user_id, "Withdraw", amount)
                    st.write(f"Successfully withdrew ${amount:.2f}. Your new balance is ${new_balance:.2f}.")

        elif choice == "Transaction History":
            st.subheader("Transaction History")
            transactions = get_transactions(st.session_state.user_id)
            if transactions:
                df = pd.DataFrame(transactions, columns=["Type", "Amount", "Date"])
                st.table(df)
            else:
                st.write("No transactions found.")

        elif choice == "Logout":
            st.session_state.authenticated = False
            st.sidebar.success("Logged out successfully!")
            st.experimental_rerun()

if __name__ == '__main__':
    main()
