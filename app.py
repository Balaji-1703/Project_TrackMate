import streamlit as st
import pandas as pd
import os
import supabase
from datetime import datetime, date
from supabase import create_client, Client
import time
from PIL import Image

def set_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg, #D8125B 35%, #2C2E39 100%);
            background-image: 
                linear-gradient(135deg, #0f0c29 0%, #24243e 90%),
                url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='rgba(255,255,255,0.075)' fill-rule='evenodd'/%3E%3C/svg%3E");
            background-size: cover;
            background-repeat: repeat;
            background-blend-mode: soft-light;
        }
        
        [data-testid="stSidebar"] h1 {
            color: #ffffff !important;
            font-weight: bold !important;
        }

        [data-testid="stSidebar"] .stMarkdown {
            color: #ffffff !important;
        }

        [data-testid="stSidebar"] button:hover {
            background-color: #6d954b !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
        }

        /* Tab hover effect */
        .stTabs [data-baseweb="tab"]:hover {
            background-color: rgba(76, 175, 80, 0.6);
            padding: 1rem;
            border-radius: 5px;
            color: white !important;
        }
        
        /* Make Active Viewers text white */
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] .stSubheader,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] div {
            color: white !important;
        }

        /* Make the total viewers and currently viewing text white */
        [data-testid="stSidebar"] .stMarkdown div {
            color: white !important;
        }

        /* Make the bullet points and usernames white */
        [data-testid="stSidebar"] .element-container div {
            color: white !important;
        }

        /* Make text and elements more visible */
        .main .block-container {
            background: rgba(255, 255, 255, 0.9);
            color: #1E1E1E;
            padding: 2rem;
            border-radius: 10px;
        }
        
        /* Dancing emojis with better visibility */
        .emoji-decor {
            position: fixed;
            font-size: 30px;
            opacity: 0.4;
            z-index: 0;
        }
        
        /* Improved animations */
        @keyframes dance1 {
            0% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(10deg); }
            100% { transform: translateY(0) rotate(0deg); }
        }
        
        @keyframes dance2 {
            0% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-15px) rotate(-10deg); }
            100% { transform: translateY(0) rotate(0deg); }
        }
        
        .emoji-1 { left: 5%; top: 10%; animation: dance1 3s infinite; }
        .emoji-2 { right: 5%; top: 10%; animation: dance2 3s infinite; }
        .emoji-3 { left: 50%; top: 35%; animation: dance1 4s infinite; }
        .emoji-4 { right: 15%; top: 30%; animation: dance2 4s infinite; }
        .emoji-5 { left: 10%; bottom: 15%; animation: dance1 3.5s infinite; }
        .emoji-6 { right: 30%; bottom: 10%; animation: dance2 3.5s infinite; }
        .emoji-7 { right: 50%; bottom: 20%; animation: dance1 3.5s infinite; }
        .emoji-8 { right: 10%; bottom: 20%; animation: dance2 3.5s infinite; }
        .emoji-9 { right: 70%; bottom: 5%; animation: dance1 3.5s infinite; }
        
        /* Ensure text visibility */


        h1, h2, h3, .stMarkdown, .stText {
            color: #ebd8d0 !important;
            position: relative;
            z-index: 1;
        }

        /* Make buttons and inputs more visible */
        .stButton button, .stSelectbox select, .stTextInput input {
            background-color: #1E1E1E !important;
            position: relative;
            z-index: 1;
        }

        
        /* Stats Card styling */
        .stats-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #4CAF50;
            transition: transform 0.2s ease-in-out;
        }

        .stats-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }

        .stats-card h4 {
            color: #1E1E1E;
            margin-bottom: 1rem;
            font-size: 1.2rem;
            font-weight: 600;
        }

        .stats-card .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #4CAF50;
        }

        .stats-card .metric-label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 0.5rem;
        }

        /* Different colors for different stat types */
        .regular-card {
            border-left-color: #2196F3;
        }
        .regular-card .metric-value {
            color: #2196F3;
        }

        .special-card {
            border-left-color: #9C27B0;
        }
        .special-card .metric-value {
            color: #9C27B0;
        }

        .combined-card {
            border-left-color: #FF9800;
        }
        .combined-card .metric-value {
            color: #FF9800;
        }

        </style>
        
        <div id="emoji-container">
            <div class="emoji-decor emoji-1">💃</div>
            <div class="emoji-decor emoji-7">💃</div>
            <div class="emoji-decor emoji-2">🕺</div>
            <div class="emoji-decor emoji-3">🎵</div>
            <div class="emoji-decor emoji-8">🎵</div>
            <div class="emoji-decor emoji-4">🎶</div>
            <div class="emoji-decor emoji-5">✨</div>
            <div class="emoji-decor emoji-6">💫</div>
            <div class="emoji-decor emoji-9">💫</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Call this function at the start of your app
set_background()

# Add this function after your existing functions
def get_attendance_emoji(percentage):
    if percentage >= 90:
        return f"<div class='good-attendance'>🌟 Excellent! ({percentage:.1f}%)</div>"
    elif percentage >= 75:
        return f"<div class='good-attendance'>😊 Good! ({percentage:.1f}%)</div>"
    elif percentage >= 60:
        return f"<div class='good-attendance'>🙂 Fair ({percentage:.1f}%)</div>"
    elif percentage >= 40:
        return f"<div class='bad-attendance'>😕 Needs Improvement ({percentage:.1f}%)</div>"
    else:
        return f"<div class='bad-attendance'>😢 Poor ({percentage:.1f}%)</div>"

# Initialize session state
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'last_cleanup' not in st.session_state:
    st.session_state.last_cleanup = time.time()

# Initialize Supabase client
supabase: Client = create_client(st.secrets["SUPABASE_CREDENTIALS"]["SUPABASE_URL"], st.secrets["SUPABASE_CREDENTIALS"]["SUPABASE_KEY"])

# Replace file loading with Supabase queries
def load_attendance_data():
    response = supabase.table('attendance').select('*').execute()
    if response.data:
        df = pd.DataFrame(response.data)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.date
        return df
    return pd.DataFrame(columns=['name', 'date', 'status', 'class_type', 'event'])

def load_student_info():
    response = supabase.table('student_info').select('*').execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame(columns=['name', 'bio', 'join_date', 'contact'])

# Replace the file loading code with Supabase queries
# Use it when loading data
# with st.spinner():
#     show_loading_animation()
#     df = load_attendance_data()
#     student_info_df = load_student_info()

def check_existing_attendance(name, date):
    """Check if attendance already exists for given name and date"""
    response = supabase.table('attendance')\
        .select('*')\
        .eq('name', name)\
        .eq('date', str(date))\
        .execute()
    return len(response.data) > 0

def save_attendance(df, is_edit_mode=False):
    try:
        if not df.empty:
            # Create a copy and convert data types
            df_to_save = df.copy()
            
            # Convert date to string
            if 'date' in df_to_save.columns:
                df_to_save['date'] = df_to_save['date'].astype(str)
            
            # Remove id column if it exists to let Supabase auto-generate it
            if 'id' in df_to_save.columns:
                df_to_save = df_to_save.drop('id', axis=1)
            
            # Convert numeric columns to appropriate types
            numeric_columns = df_to_save.select_dtypes(include=['float64', 'int64']).columns
            for col in numeric_columns:
                df_to_save[col] = df_to_save[col].fillna(0).astype(int)
            
            # Convert DataFrame to records
            records = df_to_save.to_dict('records')
            
            # Process in batches
            batch_size = 100
            for i in range(0, len(records), batch_size):
                batch = records[i:i + batch_size]
                if is_edit_mode:
                    # Update existing records
                    for record in batch:
                        supabase.table('attendance')\
                            .update({
                                'status': record['status'],
                                'class_type': record['class_type'],
                                'event': record['event']
                            })\
                            .eq('name', record['name'])\
                            .eq('date', record['date'])\
                            .execute()
                else:
                    # For new records, check existence and insert
                    filtered_batch = []
                    for record in batch:
                        exists = check_existing_attendance(record['name'], record['date'])
                        if not exists:
                            filtered_batch.append(record)
                        else:
                            st.warning(f"Attendance already marked for {record['name']} on {record['date']}")
                    
                    if filtered_batch:
                        supabase.table('attendance').insert(filtered_batch).execute()

            return True
    except Exception as e:
        st.error(f"Error saving attendance data: {str(e)}")
        st.error("Data types:", df_to_save.dtypes)  # Debug info
        return False

# def save_student_info(df):
#     supabase.table('student_info').delete().neq('id', 0).execute()
#     if not df.empty:
#         records = df.to_dict('records')
#         supabase.table('student_info').insert(records).execute()

def save_student_info(df):
    try:
        # Create a copy of the DataFrame
        df_to_save = df.copy()
        
        # Handle any numeric columns - convert to finite values
        numeric_cols = df_to_save.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            df_to_save[col] = df_to_save[col].fillna(0).astype(int)
            # Replace inf/-inf with None
            #df_to_save[col] = df_to_save[col].replace([float('inf'), float('-inf')], None)
            # Replace NaN with None
            #df_to_save[col] = df_to_save[col].where(df_to_save[col].notna(), None)
        
        # Convert date columns to string format
        if 'join_date' in df_to_save.columns:
            df_to_save['join_date'] = pd.to_datetime(df_to_save['join_date']).dt.strftime('%Y-%m-%d')

        # Get the student name we're updating
        student_name = df_to_save['name'].iloc[0]

         # First delete the existing record for this student
        supabase.table('student_info').delete().eq('name', student_name).execute()
        
        # Convert DataFrame to record
        record = df_to_save.to_dict('records')[0]
        if 'id' in record:
            del record['id']  # Remove id if present

        supabase.table('student_info').insert(record).execute()

        return True
    except Exception as e:
        st.error(f"Error saving student info: {str(e)}")
        return False

def load_active_users():
    response = supabase.table('active_users').select('username').execute()
    if response.data:
        return [user['username'] for user in response.data]
    return []

# Modify the active users functions
def add_active_user(username, is_admin=False):
    timestamp = datetime.now().isoformat()
    supabase.table('active_users').insert({
        'username': username,
        'is_admin': is_admin,
        'last_active': timestamp
    }).execute()

def remove_active_user(username):
    supabase.table('active_users').delete().eq('username', username).execute()

def update_user_activity(username):
    timestamp = datetime.now().isoformat()
    supabase.table('active_users').update({
        'last_active': timestamp
    }).eq('username', username).execute()

def cleanup_inactive_users():
    threshold = (datetime.now() - pd.Timedelta(minutes=5)).isoformat()
    supabase.table('active_users').delete().lt('last_active', threshold).execute()

# Modify event functions
def load_events():
    response = supabase.table('events').select('*').execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame(columns=['event_name', 'start_date', 'end_date', 'description'])

def add_event(name, start, end, desc):
    supabase.table('events').insert({
        'event_name': name,
        'start_date': start.isoformat(),
        'end_date': end.isoformat(),
        'description': desc
    }).execute()
    return load_events()

# Add after loading other DataFrames
#events_df = load_events()

def verify_member(username, password):
    try:
        response = supabase.table('member_credentials')\
            .select('*')\
            .eq('username', username)\
            .eq('password', password)\
            .execute()

        if len(response.data) == 0:
            st.error("Invalid member credentials")
            return False
        
        member = response.data[0]
        if not member['is_active']:
            st.error("Your account is inactive. Please contact the admin.")
            return False
        else:
            return True

    except Exception as e:
        st.error(f"Error verifying member: {str(e)}")
        return False

# Modify the login function
def login():
    st.title("Zoho Dance Crew's Attendance Register - Login")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        is_admin_attempt = st.checkbox("Login as Admin")
        
        if is_admin_attempt:
            admin_name = st.text_input("Admin Username")
            admin_password = st.text_input("Password", type="password")
            
            if st.button("Login as Admin"):
                if admin_name == st.secrets["ADMIN_CREDENTIALS"]["username"] and st.secrets["ADMIN_CREDENTIALS"]["password"] == admin_password:
                    st.session_state.is_admin = True
                    st.session_state.current_user = f"admin:{admin_name}"
                    add_active_user(admin_name, is_admin=True)
                    st.balloons()  # Celebration with balloons
                    st.success(f"Logged in as Admin: {admin_name}")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("Invalid admin credentials")
        else:
            member_name = st.text_input("Member Username")
            member_password = st.text_input("Member Password", type="password")

            if st.button("Login as Member"):
                if verify_member(member_name, member_password):
                    st.session_state.current_user = f"viewer:{member_name}"
                    add_active_user(member_name)
                    st.balloons()  # Celebration with balloons
                    st.success(f"Welcome, {member_name}")
                    time.sleep(2)
                    st.rerun()

# Add this helper function at the top
def get_date_range(period):
    today = date.today()
    if period == "This Month":
        start_date = today.replace(day=1)
        end_date = today
    elif period == "Last Month":
        if today.month == 1:
            start_date = date(today.year - 1, 12, 1)
            end_date = date(today.year - 1, 12, 31)
        else:
            start_date = today.replace(month=today.month - 1, day=1)
            end_date = (today.replace(day=1) - pd.Timedelta(days=1))
    elif period == "Last 3 Months":
        start_date = (today - pd.Timedelta(days=90)).replace(day=1)
        end_date = today
    elif period == "Last 6 Months":
        start_date = (today - pd.Timedelta(days=180)).replace(day=1)
        end_date = today
    elif period == "Last Year":
        start_date = today.replace(year=today.year - 1)
        end_date = today
    else:
        return None, None
    return start_date, end_date


# Replace the viewer display section
def display_active_users():
    # Cleanup inactive users every 5 seconds
    current_time = time.time()
    if current_time - st.session_state.last_cleanup > 5:
        cleanup_inactive_users()
        st.session_state.last_cleanup = current_time

    # Update current user's activity timestamp
    if st.session_state.current_user:
        username = st.session_state.current_user.split(':')[1]
        update_user_activity(username)

    # Display active users
    active_users = load_active_users()
    st.sidebar.subheader("Active Viewers")
    st.sidebar.write(f"Total viewers: {len(active_users)}")
    st.sidebar.write("Currently viewing:")
    for user in active_users:
        st.sidebar.write(f"- {user}")

# Move the title inside the main content section
if not st.session_state.current_user:
    login()
    st.stop()
else:
    # Show title and logout in sidebar only after login
    st.sidebar.title("Menu")

    # Display current user
    username = st.session_state.current_user.split(':')[1]
    is_admin = st.session_state.current_user.startswith('admin:')
    st.sidebar.markdown(f"**Current User:** {username}")
    st.sidebar.markdown(f"**Role:** {'Admin' if is_admin else 'Viewer'}")
    st.sidebar.divider()

     # Add refresh button
    if st.sidebar.button("🔄 Refresh"):
        st.rerun()

    # Display active users
    display_active_users()

    if st.sidebar.button("Logout"):
        if st.session_state.current_user:
            username = st.session_state.current_user.split(':')[1]
            remove_active_user(username)
        st.session_state.current_user = None
        st.session_state.is_admin = False
        st.rerun()
    
    # Show main title
    st.title("Zoho Dance Crew Attendance Register")

    # Load data with loading animation
    with st.spinner():
        df = load_attendance_data()
        student_info_df = load_student_info()
        events_df = load_events()  # Move this here as well

# Rest of your existing code remains the same...

def add_member_credentials(username, password):
    try:
        supabase.table('member_credentials').insert({
            'username': username,
            'password': password
        }).execute()
        return True
    except Exception as e:
        st.error(f"Error adding member credentials: {str(e)}")
        return False

def update_member_status(username, is_active):
    try:
        supabase.table('member_credentials')\
            .update({'is_active': is_active})\
            .eq('username', username)\
            .execute()
        return True
    except Exception as e:
        st.error(f"Error updating member status: {str(e)}")
        return False

# Create tabs based on user role
if st.session_state.is_admin:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Mark Attendance", "Mark/Edit Past Attendance", "View Records", "Statistics", "Events", "Manage Members"])
else:
    tab3, tab4, tab5 = st.tabs(["View Records", "Statistics", "Events"])

# Get today's date
today = date.today()

# Only show attendance marking tabs for admin
if st.session_state.is_admin:
    with tab1:
        # Get list of members from member_credentials
        response = supabase.table('member_credentials')\
            .select('username')\
            .eq('is_active', True)\
            .execute()
        
        existing_names = []
        if response.data:
            existing_names = sorted([member['username'] for member in response.data])

        if not existing_names:
            st.info("No active members found. Please add members in the Manage Members tab.")
        else:
            # Bulk Attendance Section
            st.subheader("Bulk Attendance Marking")

            if existing_names:
                 # Date and class type selection
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    bulk_date = st.date_input("Select Date for Bulk Attendance", today, key="bulk_date")
                with col2:
                    class_type = st.selectbox(
                        "Class Type",
                        ["Regular", "Special", "Event/Competition"],
                        help="Select the type of class",
                        key="bulk_class_type"  # Add unique key
                    )

                # Show event selection if class type is Event/Competition
                if class_type == "Event/Competition":
                    st.divider()
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        # Option to select existing event or create new
                        existing_events = events_df['event_name'].unique().tolist() if not events_df.empty else []
                        event_option = st.radio("Event", ["Select Existing", "Create New"], horizontal=True)

                        if event_option == "Select Existing":
                            if existing_events:
                                selected_event = st.selectbox("Select Event", existing_events)
                            else:
                                st.warning("No events found. Create a new event.")
                                event_option = "Create New"

                        if event_option == "Create New":
                            with st.expander("Add New Event"):
                                new_event_name = st.text_input("Event Name")
                                event_start = st.date_input("Start Date")
                                event_end = st.date_input("End Date")
                                event_desc = st.text_area("Description")

                                if st.button("Add Event"):
                                    if new_event_name and event_start and event_end:
                                        events_df = add_event(new_event_name, event_start, event_end, event_desc)
                                        st.balloons()  # Celebration with balloons
                                        st.success("Event added successfully!")
                                        selected_event = new_event_name
                                    else:
                                        st.error("Please fill all required fields")

                # Create two columns for Present/Absent selection
                col1, col2 = st.columns(2)

                with col1:
                    st.write("Select Present Students")
                    present_students = st.multiselect(
                        "Present",
                        options=existing_names,
                        default=[],
                        key="present_multiselect"
                    )

                with col2:
                    st.write("Select Absent Students")
                    # Show only students not marked as present
                    absent_options = [name for name in existing_names if name not in present_students]
                    absent_students = st.multiselect(
                        "Absent",
                        options=absent_options,
                        default=[],
                        key="absent_multiselect"
                    )

                # Bulk mark attendance button
                if st.button("Mark Bulk Attendance"):
                    if present_students or absent_students:
                        # Check if any students already have attendance for selected date
                        existing_records = df[df['date'] == bulk_date]['name'].tolist()
                        new_records = []
                        skipped_students = []

                        # Add present students
                        for student in present_students:
                            if student not in existing_records:
                                new_records.append({
                                    'name': student,
                                    'date': bulk_date,
                                    'status': 'Present',
                                    'class_type': class_type,
                                    'event': selected_event if class_type == "Event/Competition" else None
                                })
                            else:
                                skipped_students.append(student)

                        # Add absent students
                        for student in absent_students:
                            if student not in existing_records:
                                new_records.append({
                                    'name': student,
                                    'date': bulk_date,
                                    'status': 'Absent',
                                    'class_type': class_type,
                                    'event': selected_event if class_type == "Event/Competition" else None
                                })
                            else:
                                skipped_students.append(student)

                        if new_records:
                            #df = pd.concat([df, pd.DataFrame(new_records)], ignore_index=True)
                            save_attendance(pd.DataFrame(new_records), is_edit_mode=False)
                            st.balloons()  # Celebration with balloons
                            st.success(f"Bulk attendance marked for {len(new_records)} students on {bulk_date}")

                            # Show summary
                            st.write("Summary:")
                            st.write(f"Date: {bulk_date}")
                            st.write(f"Present: {len([r for r in new_records if r['status'] == 'Present'])} students")
                            st.write(f"Absent: {len([r for r in new_records if r['status'] == 'Absent'])} students")

                            # Show detailed lists
                            col3, col4 = st.columns(2)
                            with col3:
                                if present_students:
                                    st.write("Present Students:", ", ".join([s for s in present_students if s not in skipped_students]))
                            with col4:
                                if absent_students:
                                    st.write("Absent Students:", ", ".join([s for s in absent_students if s not in skipped_students]))

                            # Show skipped students if any
                            if skipped_students:
                                st.warning(f"Skipped {len(skipped_students)} students (attendance already marked):")
                                st.write(", ".join(skipped_students))
                        else:
                            st.warning("Attendance already marked for all selected students on this date")
                    else:
                        st.warning("Please select at least one student")
            else:
                st.info("No students available. Please add students first.")

    with tab2:
        st.subheader("Mark/Edit Past Attendance")
    
        # Select date
        selected_date = st.date_input("Select date for attendance", today)
    
        # Get list of unique names
        existing_names = sorted(df['name'].unique()) if not df.empty else []

        # Select student
        student_name = st.selectbox("Select student (Past Attendance)", 
                              existing_names if existing_names else ['No students yet'])
        
        # Class type selection
        class_type = st.selectbox(
            "Class Type",
            ["Regular", "Special", "Event/Competition"],
            help="Select the type of class",
            key="edit_class_type"  # Add unique key
        )

        # Event selection for Event/Competition
        selected_event = None
        if class_type == "Event/Competition":
            st.divider()
            # Option to select existing event or create new
            existing_events = events_df['event_name'].unique().tolist() if not events_df.empty else []
            event_option = st.radio("Event", ["Select Existing", "Create New"], horizontal=True)
            
            if event_option == "Select Existing":
                if existing_events:
                    selected_event = st.selectbox("Select Event", existing_events)
                else:
                    st.warning("No events found. Create a new event.")
                    event_option = "Create New"
            
            if event_option == "Create New":
                with st.expander("Add New Event"):
                    new_event_name = st.text_input("Event Name")
                    event_start = st.date_input("Start Date")
                    event_end = st.date_input("End Date")
                    event_desc = st.text_area("Description")
                    
                    if st.button("Add Event"):
                        if new_event_name and event_start and event_end:
                            events_df = add_event(new_event_name, event_start, event_end, event_desc)
                            st.balloons()  # Celebration with balloons
                            st.success("Event added successfully!")
                            selected_event = new_event_name
                        else:
                            st.error("Please fill all required fields")

        # Mark attendance
        status = st.radio("Attendance Status (Past)", ['Present', 'Absent'])
    
        if st.button("Mark/Update Attendance"):
            if student_name != 'No students yet':
                new_data = {
                    'name': student_name,
                    'date': selected_date,
                    'status': status,
                    'class_type': class_type,
                    'event': selected_event if class_type == "Event/Competition" else None
                }

                # Create a single-row DataFrame for the new/updated record
                new_df = pd.DataFrame([new_data])

                # Always use is_edit_mode=True since this is in the edit tab
                if save_attendance(new_df, is_edit_mode=True):
                    st.balloons()  # Celebration with balloons
                    st.success(f"Attendance {'updated' if check_existing_attendance(student_name, selected_date) else 'marked'} for {student_name} on {selected_date}")
                else:
                    st.error("Failed to save attendance")

        # Show existing attendance for selected date
        st.divider()
        st.subheader(f"Attendance Records for {selected_date}")
        date_records = df[df['date'] == selected_date]
        if not date_records.empty:
            st.dataframe(date_records)
            
            # Show summary for the selected date
            st.subheader("Summary")
            total_present = len(date_records[date_records['status'] == 'Present'])
            total_absent = len(date_records[date_records['status'] == 'Absent'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Present", total_present)
            with col2:
                st.metric("Absent", total_absent)
        else:
            st.info("No records found for selected date")
        pass

    #In tab6:
    with tab6:
        st.subheader("Manage Members")
        
        # Add new member
        with st.expander("Add New Member"):
            new_username = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
            if st.button("Add Member"):
                if new_username and new_password:
                    if add_member_credentials(new_username, new_password):
                        st.balloons()  # Celebration with balloons
                        st.success(f"Added member: {new_username}")
                else:
                    st.error("Please provide both username and password")
        
        # View/manage existing members
        response = supabase.table('member_credentials').select('*').execute()
        if response.data:
            members_df = pd.DataFrame(response.data)

            # Create a styled dataframe
            styled_df = members_df[['username', 'is_active', 'created_at']].copy()
            # Convert is_active to colored text
            styled_df['is_active'] = styled_df['is_active'].apply(
                lambda x: f"🟢 Active" if x else f"🔴 Inactive"
            )
        
            # Rename columns for better display
            styled_df.columns = ['Username', 'Status', 'Created At']

            # Display the styled dataframe
            st.dataframe(
                styled_df,
                column_config={
                    "Status": st.column_config.TextColumn(
                        "Status",
                        help="Member account status",
                        width="medium"
                    )
                }
            )
            
            # Manage member status
            member_to_update = st.selectbox("Select member to update", members_df['username'])
            current_status = members_df[members_df['username'] == member_to_update]['is_active'].iloc[0]
            new_status = st.checkbox("Is Active", value=current_status)
            if st.button("Update Status"):
                if update_member_status(member_to_update, new_status):
                    st.balloons()  # Celebration with balloons
                    st.success(f"Updated status for {member_to_update}")
                    time.sleep(2)
                    st.rerun()

# View Records tab (available to all)
with tab3:
    st.subheader("Attendance Records")
    
    # Add period selection
    period_options = ["Custom", "This Month", "Last Month", "Last 3 Months", 
                     "Last 6 Months", "Last Year"]
    selected_period = st.selectbox("Select Period", period_options)
    
    # Date range selection
    if selected_period == "Custom":
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", 
                                     today.replace(day=1))
        with col2:
            end_date = st.date_input("End Date", today)
    else:
        start_date, end_date = get_date_range(selected_period)
    
    names = sorted(df['name'].unique()) if not df.empty else []
    search_options = ['View All'] + names  # Add 'View All' as first option

    # Create dropdown for name selection
    search_name = st.selectbox("Select name (or View All)", search_options)
    
    # Filter data
    if not df.empty:
        filtered_df = df.copy()
        
        # Apply date filter
        if start_date and end_date:
            filtered_df = filtered_df[
                (filtered_df['date'] >= start_date) & 
                (filtered_df['date'] <= end_date)
            ]
        
        # Apply name filter if provided
        if search_name != 'View All':
            filtered_df = filtered_df[
                filtered_df['name'] == search_name
            ]
        
        if not filtered_df.empty:
            # Calculate statistics
            total_days = len(filtered_df['date'].unique())
            
            if search_name:

                # Single student statistics
                student_stats = filtered_df[
                    filtered_df['name'].str.lower() == search_name.lower()
                ]

                if not student_stats.empty:
                    student_name = student_stats['name'].iloc[0]
                    st.subheader(f"Statistics for {student_name}")
                    
                    # Get student bio
                    student_bio = student_info_df[student_info_df['name'] == student_name] if not student_info_df.empty else pd.DataFrame()
                    # Display student info in columns
                    info_col1, info_col2 = st.columns([2, 1])

                    with info_col1:

                        current_user = st.session_state.current_user.split(':')[1]
    
                        # Check if viewing own profile
                        is_own_profile = current_user.lower() == student_name.lower()

                        if is_own_profile or st.session_state.is_admin:
                             # Initialize default values
                            current_bio = ""
                            current_join_date = today
                            current_contact = ""

                            # Allow admin to add bio
                            with st.expander("Add/edit Member Bio"):
                                bio = st.text_area("Bio", value=student_bio['bio'].iloc[0] if not student_bio.empty else "")
                                join_date = st.date_input("Join Date", value=pd.to_datetime(student_bio['join_date'].iloc[0]).date() if not student_bio.empty else today)
                                contact = st.text_input("Contact Info", value=student_bio['contact'].iloc[0] if not student_bio.empty else "")
                                if st.button("Save Bio"):
                                    new_bio = pd.DataFrame([{
                                        'name': student_name,
                                        'bio': bio,
                                        'join_date': join_date.isoformat(),
                                        'contact': contact
                                    }])
                                    student_info_df = pd.concat([student_info_df[student_info_df['name'] != student_name], new_bio], 
                                              ignore_index=True)
                                    save_student_info(student_info_df)
                                    st.balloons()  # Celebration with balloons
                                    st.success("Bio added successfully!")
                                    time.sleep(2)
                                    st.rerun()

                        # Bio section
                        if not student_bio.empty:
                            st.markdown("**Bio:**")
                            st.write(student_bio['bio'].iloc[0])
                            st.markdown(f"**Joined:** {student_bio['join_date'].iloc[0]}")

                        events_attended = filtered_df[
                            (filtered_df['name'] == student_name) & 
                            (filtered_df['class_type'] == 'Event/Competition') &
                            (filtered_df['status'] == 'Present')
                        ]['event'].unique()

                        total_events = len([e for e in events_attended if pd.notna(e)])
                        # Display event participation count with emoji
                        st.markdown(f"**🏆 Events Participated:** {total_events}")

                        if total_events > 0:
                            for event in events_attended:
                                if pd.notna(event):  # Check if event is not NaN
                                    # Get event details
                                    event_details = events_df[events_df['event_name'] == event].iloc[0]
                                    event_dates = f"{event_details['start_date']} to {event_details['end_date']}"
                                    # Create expandable section for each event
                                    with st.expander(f"🎯 {event}"):
                                        st.write(f"**Dates:** {event_dates}")
                                        if pd.notna(event_details['description']):
                                            st.write(f"**Description:** {event_details['description']}")
                                        # Get attendance for this event
                                        event_attendance = filtered_df[
                                            (filtered_df['name'] == student_name) &
                                            (filtered_df['event'] == event)
                                        ]
                                        total_sessions = len(event_attendance)
                                        sessions_attended = len(event_attendance[event_attendance['status'] == 'Present'])
                                        attendance_rate = (sessions_attended / total_sessions * 100) if total_sessions > 0 else 0
                                        # Show event attendance metrics
                                        cols = st.columns(3)
                                        cols[0].metric("Total Sessions", total_sessions)
                                        cols[1].metric("Attended", sessions_attended)
                                        cols[2].metric("Attendance Rate", f"{attendance_rate:.1f}%")
                        else:
                            st.info("No events participated yet")

                    with info_col2:
                        # Attendance statistics
                        regular_matches = student_stats[student_stats['class_type'] == 'Regular']
                        special_matches = student_stats[student_stats['class_type'] == 'Special']

                        st.markdown("**Regular Classes**")
                        regular_total = len(regular_matches)
                        regular_present = len(regular_matches[regular_matches['status'] == 'Present'])
                        regular_percentage = (regular_present / regular_total * 100) if regular_total > 0 else 0
                        # loc_col1, loc_col2 = st.columns(2)
                        # with loc_col1:
                        #     st.metric("Total", regular_total)
                        # with loc_col2:
                        #     st.metric("Present", regular_present)
                        # st.metric("Percentage", f"{regular_percentage:.1f}%")

                        # Regular Classes Card
                        st.markdown("""
                            <div class="stats-card regular-card">
                                <h4>Regular Classes</h4>
                                <div class="metric-value">{:.1f}%</div>
                                <div class="metric-label">Attendance Rate</div>
                                <div style="margin-top: 1rem;">
                                    <strong>Total:</strong> {} | <strong>Present:</strong> {}
                                </div>
                            </div>
                        """.format(regular_percentage, regular_total, regular_present), unsafe_allow_html=True)

                        st.markdown("**Special Classes**")
                        special_total = len(special_matches)
                        special_present = len(special_matches[special_matches['status'] == 'Present'])
                        special_percentage = (special_present / special_total * 100) if special_total > 0 else 0
                        # loc_col1, loc_col2 = st.columns(2)
                        # with loc_col1:
                        #     st.metric("Total", special_total)
                        # with loc_col2:
                        #     st.metric("Present", special_present)
                        # st.metric("Percentage", f"{special_percentage:.1f}%")

                        # Special Classes Card
                        st.markdown("""
                            <div class="stats-card special-card">
                                <h4>Special Classes</h4>
                                <div class="metric-value">{:.1f}%</div>
                                <div class="metric-label">Attendance Rate</div>
                                <div style="margin-top: 1rem;">
                                    <strong>Total:</strong> {} | <strong>Present:</strong> {}
                                </div>
                            </div>
                        """.format(special_percentage, special_total, special_present), unsafe_allow_html=True)

                        st.markdown("**Combined**")
                        total_classes = len(student_stats)
                        total_present = len(student_stats[student_stats['status'] == 'Present'])
                        total_percentage = (total_present / total_classes * 100) if total_classes > 0 else 0
                        # loc_col1, loc_col2 = st.columns(2)
                        # with loc_col1:
                        #     st.metric("Total Classes", total_classes)
                        # with loc_col2:
                        #     st.metric("Present Days", total_present)
                        # st.metric("Percentage", f"{total_percentage:.1f}%")

                        # Combined Stats Card
                        st.markdown("""
                            <div class="stats-card combined-card">
                                <h4>Combined Statistics</h4>
                                <div class="metric-value">{:.1f}%</div>
                                <div class="metric-label">Overall Attendance Rate</div>
                                <div style="margin-top: 1rem;">
                                    <strong>Total Classes:</strong> {} | <strong>Present Days:</strong> {}
                                </div>
                            </div>
                        """.format(total_percentage, total_classes, total_present), unsafe_allow_html=True)

                    # Show attendance trend
                    st.divider()
                    st.subheader("Attendance Trend")
                    attendance_history = student_stats.sort_values('date')
                    # Create attendance plot data
                    plot_data = pd.DataFrame({
                        'date': attendance_history['date'],
                        'attendance': (attendance_history['status'] == 'Present').astype(int)
                    }).set_index('date')

                    # Display the line chart with dates
                    st.line_chart(plot_data, use_container_width=True)

                    # Add legend
                    st.markdown("""
                    **Legend:**
                    - 1: Present
                    - 0: Absent
                    """)
            else:
                # All students statistics
                st.subheader("Overall Statistics")
                
                # Calculate overall metrics
                all_stats = filtered_df.groupby('name').agg({
                    'status': ['count', lambda x: (x == 'Present').sum()]
                }).reset_index()
                all_stats.columns = ['Name', 'Total Classes', 'Present']
                all_stats['Attendance %'] = (all_stats['Present'] / 
                                          all_stats['Total Classes'] * 100).round(2)
                
                # Display overall statistics
                st.dataframe(all_stats)
                
                # Show attendance trend for all
                st.subheader("Overall Attendance Trend")
                daily_attendance = filtered_df.groupby('date').agg({
                    'status': lambda x: (x == 'Present').mean() * 100
                }).reset_index()
                st.line_chart(daily_attendance.set_index('date'))
            
            # Show detailed records
            st.subheader("Detailed Records")
            st.dataframe(filtered_df)
            
            # Download option
            st.download_button(
                "Download Records",
                filtered_df.to_csv(index=False),
                f"attendance_{start_date}_{end_date}.csv",
                "text/csv"
            )
        else:
            st.info("No records found for the selected criteria")
    else:
        st.info("No attendance records available")
    pass

# Statistics tab (available to all)
with tab4:
    # Move the original tab3 content to tab4
    st.subheader("Attendance Statistics")
    if not df.empty:
        # Calculate overall statistics
        total_days = len(df['date'].unique())
        total_regular_days = len(df[df['class_type'] == 'Regular']['date'].unique())
        total_special_days = len(df[df['class_type'] == 'Special']['date'].unique())
        total_event_days = len(df[df['class_type'] == 'Event/Competition']['date'].unique())

        # Create separate stats for regular and special classes
        def calculate_stats(data, class_type):
            if data.empty:
                # Return empty DataFrame with correct columns if no data
                return pd.DataFrame(columns=['name', 'total_classes', 'classes_present', 'attendance_percentage'])
    
            stats = data.groupby('name').agg({
                'status': ['count', lambda x: (x == 'Present').sum()]
            }).reset_index()
            
            stats.columns = ['name', 'total_classes', 'classes_present']
            # Convert columns to numeric type
            stats['total_classes'] = pd.to_numeric(stats['total_classes'])
            stats['classes_present'] = pd.to_numeric(stats['classes_present'])
            # Calculate percentage with error handling
            stats['attendance_percentage'] = (stats['classes_present'] / stats['total_classes'] * 100).fillna(0).round(2)
            
            if class_type == "Event/Competition":
                # Add event column and handle NaN values
                stats['event'] = data.groupby('name')['event'].first().reset_index()['event']
            return stats

        # Regular class stats
        regular_stats = calculate_stats(df[df['class_type'] == 'Regular'], 'Regular')
        # Special class stats
        special_stats = calculate_stats(df[df['class_type'] == 'Special'], 'Special')
        # Combined stats
        combined_stats = calculate_stats(df, 'Combined')

        # Create a summary metrics display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Classes", total_days)
        with col2:
            st.metric("Regular", total_regular_days)
        with col3:
            st.metric("Special", total_special_days)
        with col4:
            st.metric("Events", total_event_days)

        # Create tabs for different statistics views
        stat_tab1, stat_tab2, stat_tab3, stat_tab4 = st.tabs(["Regular Classes", "Special Classes", "Events", "Combined"])

        with stat_tab1:
            st.subheader("Regular Class Statistics")
            if not regular_stats.empty:
                st.dataframe(regular_stats)
                st.bar_chart(regular_stats.set_index('name')['attendance_percentage'])
            else:
                st.info("No regular classes recorded yet")

        with stat_tab2:
            st.subheader("Special Class Statistics")
            if not special_stats.empty:
                st.dataframe(special_stats)
                st.bar_chart(special_stats.set_index('name')['attendance_percentage'])
            else:
                st.info("No special classes recorded yet")

        with stat_tab3:
            st.subheader("Event/Competition Statistics")
            event_stats = calculate_stats(df[df['class_type'] == 'Event/Competition'], 'Event/Competition')
            if not event_stats.empty:
                # Filter out records with no event name
                event_stats = event_stats[event_stats['event'].notna()]
                
                if not event_stats.empty:
                    for event in event_stats['event'].unique():
                        if pd.notna(event):  # Check if event name is not NaN
                            with st.expander(f"Event: {event}"):
                                event_data = event_stats[event_stats['event'] == event]
                                st.dataframe(event_data)
                                st.bar_chart(event_data.set_index('name')['attendance_percentage'])
                else:
                    st.info("No events with attendance records found")
            else:
                st.info("No event/competition classes recorded yet")

        with stat_tab4:
            st.subheader("Combined Statistics")
            if not combined_stats.empty:
                st.dataframe(combined_stats)
                st.bar_chart(combined_stats.set_index('name')['attendance_percentage'])
            else:
                st.info("No attendance records found")

            st.subheader("Feedback Summary")

            if not combined_stats.empty:
                for _, row in combined_stats.iterrows():
                    with st.container():
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.write(f"**{row['name']}**")
                            st.progress(row['attendance_percentage'] / 100)
                        with col2:
                            st.markdown(
                                get_attendance_emoji(row['attendance_percentage']),
                                unsafe_allow_html=True
                            )

    else:
        st.info("No attendance records to show statistics")
    pass

with tab5:
    st.subheader("Events Management")
    
    # Show all events
    if not events_df.empty:
        st.write("Current Events:")
        events_view = events_df.copy()
        events_view['duration'] = (pd.to_datetime(events_view['end_date']) - 
                                 pd.to_datetime(events_view['start_date'])).dt.days
        st.dataframe(events_view)
        
        # Show event statistics
        st.divider()
        st.subheader("Event Statistics")
        for event in events_df['event_name'].unique():
            with st.expander(f"📊 {event}"):
                event_attendance = df[df['event'] == event]
                if not event_attendance.empty:
                    total_sessions = len(event_attendance['date'].unique())
                    total_participants = len(event_attendance['name'].unique())
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total Sessions", total_sessions)
                        st.metric("Total Participants", total_participants)
                    
                    # Participant attendance for this event
                    attendance_stats = (event_attendance[event_attendance['status'] == 'Present']
                                     .groupby('name')
                                     .size()
                                     .reset_index(name='sessions_attended'))
                    attendance_stats['attendance_percentage'] = (attendance_stats['sessions_attended'] / 
                                                              total_sessions * 100).round(2)
                    st.write("Participant Statistics:")
                    st.dataframe(attendance_stats)
                else:
                    st.info("No attendance records for this event yet")
    else:
        st.info("No Events records to show statistics")
    pass
