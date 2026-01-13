# # main_app.py
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from db import cursor, conn, hash_password


# # ---------------- PAGE CONFIG ----------------

# # st.set_page_config(page_title="Smart Budget Manager", layout="wide")
# st.set_page_config(page_title="Smart Budget Manager", layout="centered")

# st.title("🎓 Smart Budget Manager for Students")
# st.caption("Track Smarter • Spend Better • Save More")

# # ---------------- SESSION STATE ----------------
# if "user" not in st.session_state:
#     st.session_state.user = None

# if "expenses" not in st.session_state:
#     st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

# # ---------------- FUNCTIONS ----------------

# # ---- REGISTER ----
# def register():
#     st.subheader(" Student Registration")
#     email = st.text_input("Email", key="register_email")
#     password = st.text_input("Password", type="password", key="register_password")

#     if st.button("Register"):
#         try:
#             cursor.execute(
#                 "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
#                 (email, hash_password(password), "student")
#             )
#             conn.commit()
#             st.success("Registered successfully! Please login.")
#         except:
#             st.error("Email already exists")

# # ---- LOGIN ----
# def login():
#     st.subheader(" Login")
#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_password")

#     if st.button("Login"):
#         cursor.execute(
#             "SELECT id, role FROM users WHERE email=%s AND password=%s",
#             (email, hash_password(password))
#         )
#         user = cursor.fetchone()
#         if user:
#             st.session_state.user = {"id": user[0], "role": user[1]}
#             st.success("Login successful")
#             st.rerun()    # <-- replace experimental_rerun with rerun


#         else:
#             st.error("Invalid credentials")

# # ---- LOGOUT ----
# def logout():
#     st.session_state.user = None
#     st.rerun()    # <-- replace experimental_rerun with rerun



# # ---- EXPENSE DASHBOARD ----
# def show_expense_dashboard():
#     st.markdown("""<h1 style='text-align:center;color:#1F4E79;'>🎓 Smart Expense Analytics System</h1>
#                  <h5 style='text-align:center;'>Track Smarter • Spend Better • Save More</h5><hr>""",
#                  unsafe_allow_html=True)

#     # Sidebar for adding expense
#     with st.sidebar:
#         st.subheader("+ Add Expense")
#         date = st.date_input("Date")
#         category_option = st.selectbox("Category", ["Food", "Transport", "Other"])
#         if category_option == "Other":
#             category = st.text_input("Enter your category", placeholder="e.g. Hostel, Books")
#         else:
#             category = category_option
#         amount = st.number_input("Amount", min_value=0.0, step=1.0)
#         description = st.text_input("Description")

#         if st.button("Add Expense"):
#             if category.strip() == "":
#                 st.warning("Please enter a category")
#             else:
#                 add_expense(date, category, amount, description)
#                 st.success("Expense added successfully!")

#         st.markdown("---")
#         st.subheader("Export Expense Report")
#         if not st.session_state.expenses.empty:
#             csv = st.session_state.expenses.to_csv(index=False).encode("utf-8")
#             st.download_button(
#                 "⬇ Download Expense Report",
#                 csv,
#                 "medicaps_expenses.csv",
#                 "text/csv"
#             )
#         else:
#             st.info("No data to download")

#     # Main Expense Table
#     st.subheader("Expense Records")
#     st.dataframe(st.session_state.expenses, use_container_width=True)

#     # Dashboard charts
#     if not st.session_state.expenses.empty:
#         st.subheader("Expense Dashboard")
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Total Expense", f"₹ {st.session_state.expenses['Amount'].sum():.2f}")
#         col2.metric("Records", len(st.session_state.expenses))
#         col3.metric("Top Category", st.session_state.expenses['Category'].mode()[0])

#         st.markdown("### Visual Insights")
#         left_col, right_col = st.columns(2)

#         # PIE CHART
#         with left_col:
#             fig1, ax1 = plt.subplots(figsize=(4,4))
#             st.session_state.expenses.groupby('Category')['Amount'].sum().plot(
#                 kind='pie', autopct='%1.1f%%', ax=ax1, startangle=90, legend=False
#             )
#             ax1.set_ylabel("")
#             ax1.set_title("Category-wise Expense (Pie)")
#             st.pyplot(fig1, clear_figure=True)

#         # BAR CHART
#         with right_col:
#             fig2, ax2 = plt.subplots(figsize=(4,4))
#             st.session_state.expenses.groupby('Category')['Amount'].sum().plot(
#                 kind='bar', color='skyblue', ax=ax2
#             )
#             ax2.set_title("Category-wise Expense (Bar)")
#             ax2.set_xlabel("Category")
#             ax2.set_ylabel("Amount")
#             ax2.tick_params(axis='x', rotation=45)
#             st.pyplot(fig2, clear_figure=True)

    #     LINE CHART
    #     df = st.session_state.expenses.copy()
    #     df['Date'] = pd.to_datetime(df['Date'])
    #     df = df.sort_values('Date')
    #     with st.expander("Expense Trend Over Time (Click here)"):
    #         fig3, ax3 = plt.subplots(figsize=(9,3))
    #         sns.lineplot(data=df, x='Date', y='Amount', marker='o', ax=ax3)
    #         ax3.set_title("Expense Trend Over Time")
    #         ax3.set_ylabel("Amount")
    #         ax3.set_xlabel("Date")
    #         st.pyplot(fig3, clear_figure=True)

    # else:
    #     st.warning("No expenses added yet")

    # # Footer
    # st.markdown("""
    # <style>
    # .footer { background-color: #0E2A47; padding: 18px; border-radius: 12px; margin-top: 30px; }
    # .footer h4 { color: #FFFFFF; text-align: center; margin-bottom: 6px; }
    # .footer p { color: #D6E4F0; text-align: center; font-size: 13px; line-height: 1.6; }
    # .footer span { color: #FFD166; font-weight: bold; }
    # </style>
    # <div class="footer">
    #     <h4>🎓 Medi-Caps University</h4>
    #     <p>
    #     © 2026 All Rights Reserved<br>
    #     Developed by <span>Labhanshu Sahu</span> | B.Tech CSE (3rd Year)<br>
    #     </p>
    # </div>
    # """, unsafe_allow_html=True)

# # ---- ADD EXPENSE FUNCTION ----
# def add_expense(date, category, amount, description):
#     new_row = pd.DataFrame([[date, category, amount, description]], columns=st.session_state.expenses.columns)
#     st.session_state.expenses = pd.concat([st.session_state.expenses, new_row], ignore_index=True)

# # ---------------- MAIN ----------------
# if st.session_state.user is None:
#     tab1, tab2 = st.tabs(["Login", "Register"])
#     with tab1:
#         login()
#     with tab2:
#         register()
# else:
#     if st.session_state.user["role"] == "student":
#         st.success("Welcome Student!")
#         show_expense_dashboard()

#     elif st.session_state.user["role"] == "admin":
#         cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
#         total = cursor.fetchone()[0]
#         st.metric("👥 Total Registered Students", total)

#     if st.button("Logout"):
#         logout()




## main_app.py
# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# from db import cursor, conn, hash_password


# # ---------------- PAGE CONFIG ----------------
# st.set_page_config(page_title="Smart Budget Manager", layout="centered")

# st.title("🎓 Smart Budget Manager for Students")
# st.caption("Track Smarter • Spend Better • Save More")

# # ---------------- SESSION STATE ----------------
# if "user" not in st.session_state:
#     st.session_state.user = None

# if "expenses" not in st.session_state:
#     st.session_state.expenses = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

# # ---------------- FUNCTIONS ----------------

# # ---- REGISTER ----
# def register():
#     st.subheader(" Student Registration")
#     email = st.text_input("Email", key="register_email")
#     password = st.text_input("Password", type="password", key="register_password")

#     if st.button("Register"):
#         try:
#             cursor.execute(
#                 "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
#                 (email, hash_password(password), "student")
#             )
#             conn.commit()
#             st.success("Registered successfully! Please login.")
#         except:
#             st.error("Email already exists")

# # ---- LOGIN ----
# def login():
#     st.subheader(" Login")
#     email = st.text_input("Email", key="login_email")
#     password = st.text_input("Password", type="password", key="login_password")

#     if st.button("Login"):
#         cursor.execute(
#             "SELECT id, role FROM users WHERE email=%s AND password=%s",
#             (email, hash_password(password))
#         )
#         user = cursor.fetchone()
#         if user:
#             st.session_state.user = {"id": user[0], "role": user[1]}
#             st.success("Login successful")
#             st.rerun()
#         else:
#             st.error("Invalid credentials")

# # ---- LOGOUT ----
# def logout():
#     st.session_state.user = None
#     st.rerun()

# # ---- ADD EXPENSE (SESSION) ----
# def add_expense(date, category, amount, description):
#     new_row = pd.DataFrame([[date, category, amount, description]],
#                            columns=st.session_state.expenses.columns)
#     st.session_state.expenses = pd.concat(
#         [st.session_state.expenses, new_row], ignore_index=True
#     )

# # ---- SAVE EXPENSES TO DATABASE (NEW) ----
# def save_expenses_to_db():
#     user_id = st.session_state.user["id"]

#     if st.session_state.expenses.empty:
#         st.warning("No expenses to save")
#         return

#     for _, row in st.session_state.expenses.iterrows():
#         cursor.execute(
#             """
#             INSERT INTO expenses (user_id, date, category, amount, description)
#             VALUES (%s, %s, %s, %s, %s)
#             """,
#             (
#                 user_id,
#                 row["Date"],
#                 row["Category"],
#                 int(row["Amount"]),
#                 row["Description"]
#             )
#         )

#     conn.commit()
#     st.success("Expenses saved permanently to database ✅")

#     # clear after save (optional but clean)
#     st.session_state.expenses = pd.DataFrame(
#         columns=['Date', 'Category', 'Amount', 'Description']
#     )

# # ---- EXPENSE DASHBOARD ----
# def show_expense_dashboard():
#     st.markdown("""
#     <h1 style='text-align:center;color:#1F4E79;'>🎓 Smart Expense Analytics System</h1>
#     <h5 style='text-align:center;'>Track Smarter • Spend Better • Save More</h5>
#     <hr>
#     """, unsafe_allow_html=True)

#     # -------- SIDEBAR --------
#     with st.sidebar:
#         st.subheader("+ Add Expense")
#         date = st.date_input("Date")
#         category_option = st.selectbox("Category", ["Food", "Transport", "Other"])
#         if category_option == "Other":
#             category = st.text_input("Enter your category", placeholder="e.g. Hostel, Books")
#         else:
#             category = category_option

#         amount = st.number_input("Amount", min_value=0, step=1)
#         description = st.text_input("Description")

#         if st.button("Add Expense"):
#             if category.strip() == "":
#                 st.warning("Please enter a category")
#             else:
#                 add_expense(date, category, amount, description)
#                 st.success("Expense added successfully!")

#         st.markdown("---")
#         st.subheader("💾 Save Expenses")
#         if st.button("Save Expenses to Database"):
#             save_expenses_to_db()

#         st.markdown("---")
#         st.subheader("Export Expense Report")
#         if not st.session_state.expenses.empty:
#             csv = st.session_state.expenses.to_csv(index=False).encode("utf-8")
#             st.download_button(
#                 "⬇ Download Expense Report",
#                 csv,
#                 "medicaps_expenses.csv",
#                 "text/csv"
#             )
#         else:
#             st.info("No data to download")

#     # -------- MAIN AREA --------
#     st.subheader("Expense Records")
#     st.dataframe(st.session_state.expenses, use_container_width=True)

#     if not st.session_state.expenses.empty:
#         st.subheader("Expense Dashboard")
#         col1, col2, col3 = st.columns(3)
#         col1.metric("Total Expense", f"₹ {st.session_state.expenses['Amount'].sum():.2f}")
#         col2.metric("Records", len(st.session_state.expenses))
#         col3.metric("Top Category", st.session_state.expenses['Category'].mode()[0])

#         left_col, right_col = st.columns(2)

#         with left_col:
#             fig1, ax1 = plt.subplots(figsize=(4,4))
#             st.session_state.expenses.groupby('Category')['Amount'].sum().plot(
#                 kind='pie', autopct='%1.1f%%', ax=ax1, startangle=90
#             )
#             ax1.set_ylabel("")
#             st.pyplot(fig1, clear_figure=True)

#         with right_col:
#             fig2, ax2 = plt.subplots(figsize=(4,4))
#             st.session_state.expenses.groupby('Category')['Amount'].sum().plot(
#                 kind='bar', ax=ax2
#             )
#             ax2.tick_params(axis='x', rotation=45)
#             st.pyplot(fig2, clear_figure=True)

#     else:
#         st.warning("No expenses added yet")

# # ---------------- MAIN ----------------
# if st.session_state.user is None:
#     tab1, tab2 = st.tabs(["Login", "Register"])
#     with tab1:
#         login()
#     with tab2:
#         register()
# else:
#     if st.session_state.user["role"] == "student":
#         st.success("Welcome Student!")
#         show_expense_dashboard()

#     elif st.session_state.user["role"] == "admin":
#         cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
#         total = cursor.fetchone()[0]
#         st.metric("👥 Total Registered Students", total)

#     if st.button("Logout"):
#         logout()




# main_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from db import cursor, conn, hash_password

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Budget Manager", layout="centered")

st.title("🎓 Smart Budget Manager for Students")
st.caption("Track Smarter • Spend Better • Save More")

# ---------------- SESSION STATE ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(
        columns=['Date', 'Category', 'Amount', 'Description']
    )

# ---------------- FUNCTIONS ----------------

# ---- LOAD USER EXPENSES FROM DB ----
def load_user_expenses(user_id):
    cursor.execute(
        "SELECT date, category, amount, description FROM expenses WHERE user_id=%s",
        (user_id,)
    )
    rows = cursor.fetchall()

    if rows:
        return pd.DataFrame(rows, columns=['Date', 'Category', 'Amount', 'Description'])
    else:
        return pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

# ---- REGISTER ----
def register():
    st.subheader(" Student Registration")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        try:
            cursor.execute(
                "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
                (email, hash_password(password), "student")
            )
            conn.commit()
            st.success("Registered successfully! Please login.")
        except:
            st.error("Email already exists")

# ---- LOGIN ----
def login():
    st.subheader(" Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        cursor.execute(
            "SELECT id, role FROM users WHERE email=%s AND password=%s",
            (email, hash_password(password))
        )
        user = cursor.fetchone()

        if user:
            st.session_state.user = {"id": user[0], "role": user[1]}
            st.session_state.expenses = load_user_expenses(user[0])
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---- LOGOUT ----
def logout():
    st.session_state.user = None
    st.session_state.expenses = pd.DataFrame(
        columns=['Date', 'Category', 'Amount', 'Description']
    )
    st.rerun()

# ---- ADD EXPENSE (DB + SESSION) ----
def add_expense(date, category, amount, description):
    user_id = st.session_state.user["id"]

    cursor.execute(
        "INSERT INTO expenses (user_id, date, category, amount, description) VALUES (%s,%s,%s,%s,%s)",
        (user_id, date, category, amount, description)
    )
    conn.commit()

    new_row = pd.DataFrame(
        [[date, category, amount, description]],
        columns=st.session_state.expenses.columns
    )
    st.session_state.expenses = pd.concat(
        [st.session_state.expenses, new_row],
        ignore_index=True
    )

# ---- EXPENSE DASHBOARD ----
def show_expense_dashboard():
    # st.markdown(
    #     """<h1 style='text-align:center;color:#1F4E79;'>🎓 Smart Expense Analytics System</h1>
    #        <h5 style='text-align:center;'>Track Smarter • Spend Better • Save More</h5><hr>""",
    #     unsafe_allow_html=True
    # )

    # Sidebar
    with st.sidebar:
        st.subheader("+ Add Expense")
        date = st.date_input("Date")
        category_option = st.selectbox("Category", ["Food", "Transport", "Other"])
        if category_option == "Other":
            category = st.text_input("Enter your category", placeholder="e.g. Hostel, Books, Gym")
        else:
            category = category_option

        amount = st.number_input("Amount ₹", min_value=0.0, step=1.0)
        description = st.text_input("Description")

        if st.button("Add Expense"):
            if category.strip() == "":
                st.warning("Please enter a category")
            else:
                add_expense(date, category, amount, description)
                st.success("Expense added successfully!")

        st.markdown("---")
        if not st.session_state.expenses.empty:
            csv = st.session_state.expenses.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇ Download Expense Report",
                csv,
                "medicaps_expenses.csv",
                "text/csv"
            )
        
        view_expenses = st.button(" View Expenses")

        if view_expenses:
            st.subheader(" Expense Records")
            st.dataframe(
            st.session_state.expenses,
            use_container_width=True
        )

    # Expense Table
    st.subheader("Expense Records")
    st.dataframe(st.session_state.expenses, use_container_width=True)

    # Dashboard
    if not st.session_state.expenses.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Expense", f"₹ {st.session_state.expenses['Amount'].sum():.2f}")
        col2.metric("Records", len(st.session_state.expenses))
        col3.metric("Top Category", st.session_state.expenses['Category'].mode()[0])

        left_col, right_col = st.columns(2)

        with left_col:
            fig1, ax1 = plt.subplots(figsize=(4,4))
            st.session_state.expenses.groupby('Category')['Amount'].sum().plot(
                kind='pie', autopct='%1.1f%%', ax=ax1
            )
            ax1.set_ylabel("")
            st.pyplot(fig1)

        with right_col:
            fig2, ax2 = plt.subplots(figsize=(4,4))
            st.session_state.expenses.groupby('Category')['Amount'].sum().plot(
                kind='bar', ax=ax2
            )
            st.pyplot(fig2)

        # LINE CHART
        df = st.session_state.expenses.copy()
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        with st.expander("Expense Trend Over Time (Click here)"):
            fig3, ax3 = plt.subplots(figsize=(9,3))
            sns.lineplot(data=df, x='Date', y='Amount', marker='o', ax=ax3)
            ax3.set_title("Expense Trend Over Time")
            ax3.set_ylabel("Amount")
            ax3.set_xlabel("Date")
            st.pyplot(fig3, clear_figure=True)

    else:
        st.warning("No expenses added yet")


# ---------------- MAIN ----------------
if st.session_state.user is None:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        login()
    with tab2:
        register()
else:
    if st.session_state.user["role"] == "student":
        show_expense_dashboard()
    # elif st.session_state.user["role"] == "admin":
    #     cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
    #     total = cursor.fetchone()[0]
    #     st.metric("👥 Total Registered Students", total)
    elif st.session_state.user["role"] == "admin":
        st.subheader(" Admin Dashboard")

        cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
        total = cursor.fetchone()[0]
        st.metric("👥 Total Registered Students", total)

        st.divider()

        st.subheader(" Registered Students Emails")
        cursor.execute("SELECT email FROM users WHERE role='student'")
        students = cursor.fetchall()

        for s in students:
            st.write("•", s[0])


    if st.button("Logout"):
        logout()

# Footer
    st.markdown("""
    <style>
    .footer { background-color: #0E2A47; padding: 18px; border-radius: 12px; margin-top: 30px; }
    .footer h4 { color: #FFFFFF; text-align: center; margin-bottom: 6px; }
    .footer p { color: #D6E4F0; text-align: center; font-size: 13px; line-height: 1.6; }
    .footer span { color: #FFD166; font-weight: bold; }
    </style>
    <div class="footer">
        <h4>🎓 Medi-Caps University</h4>
        <p>
        © 2026 All Rights Reserved<br>
        Developed by <span>Labhanshu Sahu</span> | B.Tech CSE (3rd Year)<br>
        </p>
    </div>
    """, unsafe_allow_html=True)