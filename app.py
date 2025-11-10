import streamlit as st
import pandas as pd
import os
import supabase
import plotly.express as px
from datetime import datetime, date
from supabase import create_client, Client
from typing import List, Dict
import time
import random
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
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.8) 100%);
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 
                0 4px 6px rgba(0, 0, 0, 0.1),
                inset 0 -4px 8px rgba(0, 0, 0, 0.05),
                inset 0 2px 4px rgba(255, 255, 255, 0.9);
            transition: all 0.3s ease-in-out;
            backdrop-filter: blur(10px);
            position: relative;
            overflow: hidden;
        }

        .stats-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 50%;
            background: linear-gradient(180deg, 
                rgba(255, 255, 255, 0.3) 0%, 
                rgba(255, 255, 255, 0.1) 100%);
            border-radius: 10px 10px 0 0;
        }

        .stats-card:hover {
            transform: translateY(-5px);
            box-shadow: 
                0 6px 12px rgba(0, 0, 0, 0.15),
                inset 0 -4px 8px rgba(0, 0, 0, 0.08),
                inset 0 2px 4px rgba(255, 255, 255, 0.9);
        }

        .stats-card h4 {
            color: #1E1E1E;
            margin-bottom: 1rem;
            font-size: 1.2rem;
            font-weight: 600;
            position: relative;
            z-index: 1;
        }

        .stats-card .metric-value {
            color: #1E1E1E;
            font-size: 2rem;
            font-weight: bold;
            position: relative;
            z-index: 1;
            text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.5);
        }

        .stats-card .metric-label {
            font-size: 0.9rem;
            color: #1E1E1E;
            margin-top: 0.5rem;
            position: relative;
            z-index: 1;
        }

        /* Different colors for different stat types */
        .regular-card {
            border-left-color: #95B8D1;
            background: linear-gradient(135deg, #E8F4F8 0%, #4fbcf0 100%);
        }
        .regular-card .metric-value {
            color: #5B8BA0;
        }

        .special-card {
            border-left-color: #E8B4BC;
            background: linear-gradient(135deg, #FFF0F3 0%, #f78198 100%);
        }
        .special-card .metric-value {
            color: #D16277;
        }

        .combined-card {
            border-left-color: #B4D6B4;
            background: linear-gradient(135deg, #F0F7F0 0%, #68d468 100%);
        }
        .combined-card .metric-value {
            color: #5E8C5E;
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
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

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

# Add these functions after your existing functions
def get_user_role(username: str) -> str:
    """Get user role"""
    response = supabase.table('member_credentials')\
        .select('role')\
        .eq('username', username)\
        .execute()
    
    if response.data:
        return response.data[0]['role']
    return 'member'

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
    
def delete_attendance_by_date(date, names_list=None):
    """
    Delete attendance records for a specific date
    Args:
        date: The date to delete records from
        names_list: Optional list of specific names to delete. If None, deletes all records for the date
    """
    try:
        # Convert date to ISO format string
        date_str = str(date)
        
        # Build the delete query
        delete_query = supabase.table('attendance').delete()
        
        # Add date condition
        delete_query = delete_query.eq('date', date_str)
        
        # If specific names are provided, add names condition
        if names_list and len(names_list) > 0:
            st.warning(f"Deleting attendance records for {len(names_list)} members on {date}")
            delete_query = delete_query.in_('name', names_list)
        else:
            st.warning(f"Deleting ALL attendance records for {date}")
        
        # Execute the delete operation
        response = delete_query.execute()
        
        if response.data:
            records_deleted = len(response.data)
            if names_list:
                st.success(f"Deleted {records_deleted} attendance records for selected members on {date}")
            else:
                st.success(f"Deleted all attendance records ({records_deleted} records) for {date}")
            return True
        else:
            st.warning(f"No matching attendance records found to delete")
            return False
            
    except Exception as e:
        st.error(f"Error deleting attendance: {str(e)}")
        return False

def save_student_info(df):
    try:
        # Create a copy of the DataFrame
        df_to_save = df.copy()
        
        # Handle any numeric columns - convert to finite values
        numeric_cols = df_to_save.select_dtypes(include=['float64', 'int64']).columns
        for col in numeric_cols:
            df_to_save[col] = df_to_save[col].fillna(0).astype(int)
        
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
    threshold = (datetime.now() - pd.Timedelta(minutes=15)).isoformat()
    supabase.table('active_users').delete().lt('last_active', threshold).execute()

# Modify event functions
def load_events():
    response = supabase.table('events').select('*').execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame(columns=['event_name', 'start_date', 'end_date', 'description', 'participating_members', 'dri_members'])

def add_event(name, start, end, desc, participating_members=None, dri_members=None):
    """Add new event or update existing event with participating members and DRIs"""
    try:
        # Check if event exists
        response = supabase.table('events')\
            .select('*')\
            .eq('event_name', name)\
            .execute()
        
        event_data = {
            'event_name': name,
            'start_date': start.isoformat(),
            'end_date': end.isoformat(),
            'description': desc,
            'participating_members': participating_members or [],
            'dri_members': dri_members or []
        }
        
        if response.data:
            # Update existing event
            supabase.table('events')\
                .update(event_data)\
                .eq('event_name', name)\
                .execute()
            st.info(f"Event '{name}' already exists and was updated successfully!")
        else:
            # Insert new event
            supabase.table('events')\
                .insert(event_data)\
                .execute()
            st.success(f"Event '{name}' added successfully!")
            
        return load_events()
    except Exception as e:
        st.error(f"Error managing event: {str(e)}")
        return None

def update_event(original_event_name, new_event_name, start_date, end_date, description, participants=None, dri_members=None):
    """Update existing event details"""
    try:
        event_data = {
            'event_name': new_event_name,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'description': description,
            'participating_members': participants or [],
            'dri_members': dri_members or []
        }

        # Update event in database
        response = supabase.table('events')\
            .update(event_data)\
            .eq('event_name', original_event_name)\
            .execute()

        if response.data:
            # If event name was changed, update attendance records
            if original_event_name != new_event_name:
                supabase.table('attendance')\
                    .update({'event': new_event_name})\
                    .eq('event', original_event_name)\
                    .execute()
            
            # Reload events
            return load_events()
        else:
            st.error("Event not found")
            return None

    except Exception as e:
        st.error(f"Error updating event: {str(e)}")
        return None
# Add after loading other DataFrames
#events_df = load_events()

def verify_member(username, password):
    try:
        response = supabase.table('member_credentials')\
            .select('username, is_active, role')\
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
                    st.session_state.current_user = f"admin:{admin_name}"
                    st.session_state.user_role = 'master_admin'
                    st.session_state.is_admin = True
                    add_active_user(admin_name, is_admin=True)
                    st.balloons()  # Celebration with balloons
                    st.success(f"Logged in as Master Admin: {admin_name}")
                    time.sleep(2)
                    st.rerun()
                else:
                    # Check for super admin or admin
                    response = supabase.table('member_credentials')\
                        .select('*')\
                        .eq('username', admin_name)\
                        .eq('password', admin_password)\
                        .execute()
                    
                    if response.data:
                        user_role = get_user_role(admin_name)
                        if user_role in ['super_admin', 'admin']:
                            st.session_state.current_user = f"admin:{admin_name}"
                            st.session_state.user_role = user_role
                            st.session_state.is_admin = True
                            add_active_user(admin_name, is_admin=True)
                            st.balloons()
                            st.success(f"Welcome {user_role.replace('_', ' ').title()}: {admin_name}")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("User does not have admin privileges")
                    else:
                        st.error("Invalid admin credentials")
        else:
            member_name = st.text_input("Member Username")
            member_password = st.text_input("Member Password", type="password")

            if st.button("Login as Member"):
                if verify_member(member_name, member_password):
                    st.session_state.current_user = f"viewer:{member_name}"
                    st.session_state.user_role = 'member'
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
    st.sidebar.markdown(f"**Current User:** {username}")
    st.sidebar.markdown(f"**Role:** {'Master Admin' if st.session_state.user_role == 'master_admin' else 'Super Admin' if st.session_state.user_role == 'super_admin' else 'Admin' if st.session_state.user_role == 'admin' else 'Member'}")
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

    # Add after the logout button in the sidebar section, before loading data

if st.session_state.current_user:
    st.sidebar.divider()
    with st.sidebar.expander("🔑 Change Password"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.button("Update Password"):
            try:
                # Get current user's credentials
                username = st.session_state.current_user.split(':')[1]
                
                # Verify current password
                response = supabase.table('member_credentials')\
                    .select('*')\
                    .eq('username', username)\
                    .eq('password', current_password)\
                    .execute()
                
                if len(response.data) > 0:
                    if new_password == confirm_password:
                        if new_password != current_password:
                            # Update password
                            supabase.table('member_credentials')\
                                .update({'password': new_password})\
                                .eq('username', username)\
                                .execute()
                            
                            st.sidebar.success("Password updated successfully!")
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.sidebar.error("New password must be different from current password")
                    else:
                        st.sidebar.error("New passwords don't match")
                else:
                    st.sidebar.error("Current password is incorrect")
            except Exception as e:
                st.sidebar.error(f"Error updating password: {str(e)}")

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
    
def update_member_password(username, new_password):
    try:
        supabase.table('member_credentials')\
            .update({'password': new_password})\
            .eq('username', username)\
            .execute()
        return True
    except Exception as e:
        st.error(f"Error updating member password: {str(e)}")
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

def update_member_role(username, role):
    try:
        supabase.table('member_credentials')\
            .update({'role': role})\
            .eq('username', username)\
            .execute()
        return True
    except Exception as e:
        st.error(f"Error updating member status: {str(e)}")
        return False

# Convert database format to display format
def format_role(role):
    role_mapping = {
        "member": "Member",
        "admin": "Admin",
        "super_admin": "Super Admin"
    }
    return role_mapping.get(role, role)

# Add after welcome header in both member and admin views
def get_dance_quote():
    dance_quotes = [
        "\"Dance is the hidden language of the soul.\" - Martha Graham",
        "\"Life is short, dancing makes it longer.\" - Vicki Baum",
        "\"Dance first. Think later. It's the natural order.\" - Samuel Beckett",
        "\"Dance is the joy of movement and the heart of life.\" - Unknown",
        "\"When you dance, your purpose is not to get to a certain place on the floor. It's to enjoy each step along the way.\" - Wayne Dyer",
        "\"Everything in the universe has rhythm. Everything dances.\" - Maya Angelou",
        "\"Those who dance are considered insane by those who cannot hear the music.\" - Friedrich Nietzsche",
        "\"Dance is music made visible.\" - George Balanchine",
        "\"To dance is to be out of yourself. Larger, more beautiful, more powerful.\" - Agnes de Mille",
        "\"Dancing is creating a sculpture that is visible only for a moment.\" - Erol Ozan"
    ]
    return random.choice(dance_quotes)

# Get today's date
today = date.today()

if st.session_state.user_role == 'member':

    st.subheader(f"Welcome {st.session_state.current_user.split(':')[1]}!")

    st.markdown(f"<div style='padding: 1rem; margin: 1rem 0; border-radius: 10px; background: rgba(255,255,255,0.1); text-align: center; font-style: italic;'>{get_dance_quote()}</div>", unsafe_allow_html=True)
    
    # Add period selection
    period_options = ["This Month", "Last Month", "Last 3 Months", 
                     "Last 6 Months", "Last Year", "Custom"]
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

    current_user = st.session_state.current_user.split(':')[1]
    search_name = current_user

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
        filtered_df = filtered_df[
                filtered_df['name'] == search_name
            ]
            
        if not filtered_df.empty:
            # Calculate statistics
            total_days = len(filtered_df['date'].unique())

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
                    if is_own_profile or st.session_state.user_role == 'master_admin' or st.session_state.user_role == 'super_admin':
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
                        (filtered_df['class_type'] == 'Event/Competition')
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
                    # Regular Classes Card
                    st.markdown("""
                        <div class="stats-card regular-card">
                            <h4>Regular Classes</h4>
                            <div class="metric-value">{:.1f}%</div>
                            <div class="metric-label">Attendance Rate</div>
                            <div style="margin-top: 1rem; color: #1E1E1E;">
                                <strong>Total:</strong> {} | <strong>Present:</strong> {}
                            </div>
                        </div>
                    """.format(regular_percentage, regular_total, regular_present), unsafe_allow_html=True)
                    st.markdown("**Special Classes**")
                    special_total = len(special_matches)
                    special_present = len(special_matches[special_matches['status'] == 'Present'])
                    special_percentage = (special_present / special_total * 100) if special_total > 0 else 0
                    # Special Classes Card
                    st.markdown("""
                        <div class="stats-card special-card">
                            <h4>Special Classes</h4>
                            <div class="metric-value">{:.1f}%</div>
                            <div class="metric-label">Attendance Rate</div>
                            <div style="margin-top: 1rem; color: #1E1E1E;">
                                <strong>Total:</strong> {} | <strong>Present:</strong> {}
                            </div>
                        </div>
                    """.format(special_percentage, special_total, special_present), unsafe_allow_html=True)
                    st.markdown("**Combined**")
                    total_classes = len(student_stats)
                    total_present = len(student_stats[student_stats['status'] == 'Present'])
                    total_percentage = (total_present / total_classes * 100) if total_classes > 0 else 0
                    # Combined Stats Card
                    st.markdown("""
                        <div class="stats-card combined-card">
                            <h4>Combined Statistics</h4>
                            <div class="metric-value">{:.1f}%</div>
                            <div class="metric-label">Overall Attendance Rate</div>
                            <div style="margin-top: 1rem; color: #1E1E1E;">
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
                st.line_chart(plot_data, width='stretch')
                # Add legend
                st.markdown("""
                **Legend:**
                - 1: Present
                - 0: Absent
                """)
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

else:

    st.subheader(f"Welcome {st.session_state.current_user.split(':')[1]}!")

    st.markdown(f"<div style='padding: 1rem; margin: 1rem 0; border-radius: 10px; background: rgba(255,255,255,0.1); text-align: center; font-style: italic;'>{get_dance_quote()}</div>", unsafe_allow_html=True)
    
    available_tabs = []

    # Replace the tab creation code
    if st.session_state.current_user:
        username = st.session_state.current_user.split(':')[1]
        user_role = st.session_state.user_role

        # Define available tabs based on role
        available_tabs = ["Mark Attendance", "Mark/Edit Past Attendance", 
                             "View Records", "Statistics", "Events", "Manage Members"]

        tabs = st.tabs(available_tabs)

    # Then access each tab using its index from the tabs list
    for i, tab_name in enumerate(available_tabs):
        with tabs[i]:
            if tab_name == "Mark Attendance" and st.session_state.user_role in ['master_admin', 'super_admin', 'admin']:
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
                                        event_details = events_df[events_df['event_name'] == selected_event].iloc[0]
                                        participating_members = event_details['participating_members']
                                        dri_members = event_details['dri_members']
                                        existing_names = [name for name in existing_names if name in participating_members]
                                        if dri_members:
                                            st.info(f"Event DRIs: {', '.join(dri_members)}")
                                    else:
                                        st.warning("No events found. Create a new event.")
                                        event_option = "Create New"

                                if event_option == "Create New":
                                    with st.expander("Create New Event"):
                                        new_event_name = st.text_input("Event Name")
                                        event_start = st.date_input("Start Date")
                                        event_end = st.date_input("End Date")
                                        event_desc = st.text_area("Description")

                                        col1, col2 = st.columns(2)

                                        with col1:
                                            participating_members = st.multiselect(
                                                "Select Participating Members",
                                                options=existing_names,
                                                default=[],
                                                key="participating_members_multiselect"
                                            )

                                        with col2:
                                            dri_members = st.multiselect(
                                                "Select DRIs (Event Leaders)",
                                                options=participating_members,  # Only show selected participating members
                                                default=[],
                                                key="dri_members_multiselect"
                                            )

                                        if st.button("Add Event", key="add_new_member_btn"):
                                            if new_event_name and event_start and event_end:
                                                events_df = add_event(
                                                    new_event_name, 
                                                    event_start, 
                                                    event_end, 
                                                    event_desc,
                                                    participating_members,
                                                    dri_members
                                                )
                                                if events_df is not None:
                                                    st.balloons()
                                                    st.success("Event added successfully!")
                                                    st.write("Event Details:")
                                                    st.write(f"- Total participants: {len(participating_members)}")
                                                    st.write(f"- DRIs: {', '.join(dri_members)}")
                                                    selected_event = new_event_name
                                                    existing_names = [name for name in existing_names if name in participating_members]
                                                    if dri_members:
                                                        st.info(f"Event DRIs: {', '.join(dri_members)}")
                                            else:
                                                st.error("Please fill all required fields")


                        st.write("Select Present Students")
                        present_students = st.multiselect(
                            "Present",
                            options=existing_names,
                            default=[],
                            key="present_multiselect"
                        )

                        absent_students = [name for name in existing_names if name not in present_students]

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

            elif tab_name == "Mark/Edit Past Attendance":

                st.subheader("Mark/Edit Past Attendance")

                # Select date
                selected_date = st.date_input("Select date for attendance", today)

                # Check if attendance exists for selected date
                date_records = df[df['date'] == selected_date]

                if date_records.empty:
                    st.warning("⚠️ No attendance records found for selected date. Please mark attendance first in the 'Mark Attendance' tab.")
                else:
                    # Get class type and event name from the existing records
                    existing_class_type = date_records['class_type'].iloc[0]
                    event_name = date_records['event'].iloc[0] if 'event' in date_records.columns else None

                    existing_events = events_df['event_name'].unique().tolist() if not events_df.empty else []
                    delete_attendance_list = []

                    # Class type selection
                    class_type = st.selectbox(
                        "Class Type",
                        ["Regular", "Special", "Event/Competition"],
                        index=["Regular", "Special", "Event/Competition"].index(existing_class_type),
                        help="Select the type of class",
                        key="event_class_type"  # Add unique key
                    )

                    if class_type == 'Event/Competition':
                        if existing_class_type == 'Event/Competition' and event_name:
                            event_name = st.selectbox("Select Event", existing_events, index=existing_events.index(event_name), key="edit_event_name")
                        else:
                            event_name = st.selectbox("Select Event", existing_events, key="edit_event_name")

                        event_details = events_df[events_df['event_name'] == event_name].iloc[0]
                        existing_names = event_details['participating_members']

                        if 'dri_members' in event_details and event_details['dri_members']:
                            st.info(f"DRIs: {', '.join(event_details['dri_members'])}")
                    else:
                        # For regular/special classes, show all active members
                        response = supabase.table('member_credentials')\
                            .select('username')\
                            .eq('is_active', True)\
                            .execute()
                        existing_names = sorted([member['username'] for member in response.data])

                    # Get currently present members for that date
                    currently_present = date_records[date_records['status'] == 'Present']['name'].tolist()

                    # Get members who are both present and in existing_names (for default selection)
                    default_present = [name for name in currently_present if name in existing_names]

                    # Get members who's attendance is marked but not in existing_names (for deletion)
                    delete_attendance_list = [name for name in date_records['name'].tolist() if name not in existing_names]

                    editable_marked_present_members = st.multiselect(
                        "Add / Remove Present Members", 
                        options=existing_names, 
                        default=default_present
                    )

                    editable_marked_absent_members = [name for name in existing_names if name not in editable_marked_present_members]
                    st.info(f"Absent Members: {', '.join(editable_marked_absent_members) if editable_marked_absent_members else 'None'}")

                    if st.button("Mark/Update Attendance"):
                        updated_records = []
                        new_records = []

                        # Add present students
                        for members in editable_marked_present_members:
                            exists = check_existing_attendance(members, selected_date)
                            if not exists:
                                new_records.append({
                                    'name': members,
                                    'date': selected_date,
                                    'status': 'Present',
                                    'class_type': class_type,
                                    'event': event_name if class_type == "Event/Competition" else None
                                })
                            else:
                                updated_records.append({
                                    'name': members,
                                    'date': selected_date,
                                    'status': 'Present',
                                    'class_type': class_type,
                                    'event': event_name if class_type == "Event/Competition" else None
                                })

                        # Add present students
                        for members in editable_marked_absent_members:
                            exists = check_existing_attendance(members, selected_date)
                            if not exists:
                                new_records.append({
                                    'name': members,
                                    'date': selected_date,
                                    'status': 'Absent',
                                    'class_type': class_type,
                                    'event': event_name if class_type == "Event/Competition" else None
                                })
                            else:
                                updated_records.append({
                                    'name': members,
                                    'date': selected_date,
                                    'status': 'Absent',
                                    'class_type': class_type,
                                    'event': event_name if class_type == "Event/Competition" else None
                                })

                        if updated_records:
                            if save_attendance(pd.DataFrame(updated_records), is_edit_mode=True):
                                st.balloons()  # Celebration with balloons
                                st.success(f"Bulk attendance Updated for {len(updated_records)} Members on {selected_date}")
                            else:
                                st.error("Failed to update attendance")

                        if new_records:
                            if save_attendance(pd.DataFrame(new_records), is_edit_mode=False):
                                st.balloons()  # Celebration with balloons
                                st.success(f"Bulk attendance marked for {len(new_records)} Members on {selected_date}")
                            else:
                                st.error("Failed to mark new attendance")

                        if delete_attendance_list:
                            st.warning(f"Note: The following members had attendance records but are no longer part of the class/event and these records will be deleted: {', '.join(delete_attendance_list)}.")
                            delete_attendance_by_date(selected_date, delete_attendance_list)

                        # Refresh data after marking attendance
                        st.info("Attendance records have been refreshed in the sidebar.")

                    # Replace the delete section in Mark/Edit Past Attendance tab
                    st.divider()
                    delete_col1, delete_col2 = st.columns([3, 1])

                    # Initialize state for delete confirmation
                    if 'show_delete_confirm' not in st.session_state:
                        st.session_state.show_delete_confirm = False

                    if st.session_state.user_role in ['master_admin', 'super_admin']:
                        with delete_col1:
                            st.error("⚠️ Danger Zone")
                            st.warning(f"This will delete ALL attendance records for {selected_date}")

                        if not st.session_state.show_delete_confirm:
                            if st.button("🗑️ Delete Records"):
                                st.session_state.show_delete_confirm = True

                        if st.session_state.show_delete_confirm:
                            st.warning("Are you sure? This action cannot be undone!")
                            col1, col2 = st.columns([1,1])
                            with col1:
                                if st.button("✔️ Yes, Delete"):
                                    if delete_attendance_by_date(selected_date):
                                        st.success(f"Successfully deleted attendance records for {selected_date}")
                                        st.session_state.show_delete_confirm = False
                                        time.sleep(2)
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete attendance records")
                            with col2:
                                if st.button("❌ No, Cancel"):
                                    st.session_state.show_delete_confirm = False
                                    st.rerun()
                    else:
                        st.error("You don't have permission to delete attendance records")

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
                
            elif tab_name == "View Records":
                st.subheader(f"Welcome {st.session_state.current_user.split(':')[1]}!")

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

                if st.session_state.user_role in ['master_admin', 'super_admin']:
                    names = sorted(df['name'].unique()) if not df.empty else []
                    search_options = ['View All'] + names  # Add 'View All' as first option

                    # Create dropdown for name selection
                    search_name = st.selectbox("Select name (or View All)", search_options)
                else:
                    current_user = st.session_state.current_user.split(':')[1]
                    search_name = current_user

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

                        if search_name != 'View All':
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
                                        (filtered_df['class_type'] == 'Event/Competition')
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

                                    # Regular Classes Card
                                    st.markdown("""
                                        <div class="stats-card regular-card">
                                            <h4>Regular Classes</h4>
                                            <div class="metric-value">{:.1f}%</div>
                                            <div class="metric-label">Attendance Rate</div>
                                            <div style="margin-top: 1rem; color: #1E1E1E;">
                                                <strong>Total:</strong> {} | <strong>Present:</strong> {}
                                            </div>
                                        </div>
                                    """.format(regular_percentage, regular_total, regular_present), unsafe_allow_html=True)

                                    st.markdown("**Special Classes**")
                                    special_total = len(special_matches)
                                    special_present = len(special_matches[special_matches['status'] == 'Present'])
                                    special_percentage = (special_present / special_total * 100) if special_total > 0 else 0

                                    # Special Classes Card
                                    st.markdown("""
                                        <div class="stats-card special-card">
                                            <h4>Special Classes</h4>
                                            <div class="metric-value">{:.1f}%</div>
                                            <div class="metric-label">Attendance Rate</div>
                                            <div style="margin-top: 1rem; color: #1E1E1E;">
                                                <strong>Total:</strong> {} | <strong>Present:</strong> {}
                                            </div>
                                        </div>
                                    """.format(special_percentage, special_total, special_present), unsafe_allow_html=True)

                                    st.markdown("**Combined**")
                                    total_classes = len(student_stats)
                                    total_present = len(student_stats[student_stats['status'] == 'Present'])
                                    total_percentage = (total_present / total_classes * 100) if total_classes > 0 else 0

                                    # Combined Stats Card
                                    st.markdown("""
                                        <div class="stats-card combined-card">
                                            <h4>Combined Statistics</h4>
                                            <div class="metric-value">{:.1f}%</div>
                                            <div class="metric-label">Overall Attendance Rate</div>
                                            <div style="margin-top: 1rem; color: #1E1E1E;">
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
                                st.line_chart(plot_data, width='stretch')

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
                            all_stats['attendance_percentage'] = (all_stats['Present'] / 
                                                      all_stats['Total Classes'] * 100).round(2)

                            # Display overall statistics
                            all_stats = all_stats.sort_values('attendance_percentage', ascending=False)

                            st.dataframe(
                                    all_stats,
                                    column_config={
                                        "Name": st.column_config.TextColumn(
                                            "Member",
                                            help="Member name"
                                        ),
                                        "Total Classes": st.column_config.NumberColumn(
                                            "Commited Classes",
                                            help="Total number of classes"
                                        ),
                                        "Present": st.column_config.NumberColumn(
                                            "Classes Present",
                                            help="Number of classes attended"
                                        ),
                                        "attendance_percentage": st.column_config.ProgressColumn(
                                            "Attendance %",
                                            help="Attendance percentage",
                                            format="%.1f%%",
                                            min_value=0,
                                            max_value=100
                                        )
                                    }
                                )

                            # Add daily attendance bar graph
                            st.subheader("Daily Attendance Overview")

                            # Calculate daily attendance counts
                            daily_attendance = filtered_df.groupby(['date', 'status']).size().unstack(fill_value=0)
                            if 'Present' not in daily_attendance.columns:
                                daily_attendance['Present'] = 0
                            if 'Absent' not in daily_attendance.columns:
                                daily_attendance['Absent'] = 0

                            # Prepare data for plotting
                            plot_df = pd.DataFrame({
                                'Date': daily_attendance.index,
                                'Present': daily_attendance['Present'],
                                'Total': daily_attendance['Present'] + daily_attendance['Absent']
                            })

                            # Create bar chart
                            fig = px.bar(
                                plot_df,
                                x='Date',
                                y=['Present', 'Total'],
                                title='Daily Attendance Count',
                                labels={'value': 'Number of Students', 'Date': 'Date', 'variable': 'Category'},
                                barmode='group',
                                color_discrete_map={'Present': '#4CAF50', 'Total': '#90CAF9'}
                            )

                            # Customize layout
                            fig.update_layout(
                                xaxis_tickangle=-45,
                                legend_title_text='',
                                hovermode='x unified',
                                height=400,
                                showlegend=True
                            )

                            # Add hover template
                            fig.update_traces(
                                hovertemplate="<br>".join([
                                    "%{data.name} Members: %{y}",
                                    "<extra></extra>"
                                ])
                            )

                            # Display the plot
                            st.plotly_chart(fig, width='stretch')

                            # Add percentage line chart
                            attendance_percentage = (plot_df['Present'] / plot_df['Total'] * 100).round(2)

                            # Create percentage line chart
                            fig2 = px.line(
                                x=plot_df['Date'],
                                y=attendance_percentage,
                                title='Daily Attendance Percentage',
                                labels={'x': 'Date', 'y': 'Attendance %'},
                                line_shape='linear'
                            )

                            # Customize layout
                            fig2.update_layout(
                                xaxis_tickangle=-45,
                                hovermode='x unified',
                                height=400,
                                showlegend=False,
                                yaxis_range=[0, 100]
                            )

                            # Add percentage sign to y-axis
                            fig2.update_layout(yaxis_ticksuffix='%')

                            # Display the plot
                            st.plotly_chart(fig2, width='stretch')

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
            
            elif tab_name == "Statistics":
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
                    stat_tab1, stat_tab2, stat_tab3, stat_tab4 = st.tabs(["Regular Classes", "Special Classes", "Events", "Combined Feedback"])

                    with stat_tab1:
                        st.subheader("Regular Class Statistics")
                        if not regular_stats.empty:
                            # Sort by attendance percentage in descending order
                            regular_stats = regular_stats.sort_values('attendance_percentage', ascending=False)
                            # Display the styled dataframe
                            st.dataframe(
                                regular_stats,
                                column_config={
                                    "name": st.column_config.TextColumn(
                                        "Member",
                                        help="Member name"
                                    ),
                                    "total_classes": st.column_config.NumberColumn(
                                        "Total Classes",
                                        help="Total number of classes"
                                    ),
                                    "classes_present": st.column_config.NumberColumn(
                                        "Classes Present",
                                        help="Number of classes attended"
                                    ),
                                    "attendance_percentage": st.column_config.ProgressColumn(
                                        "Attendance %",
                                        help="Attendance percentage",
                                        format="%.1f%%",
                                        min_value=0,
                                        max_value=100
                                    )
                                }
                            )

                            # Create a bar chart using plotly
                            fig = px.bar(
                                regular_stats,
                                x='name',
                                y='attendance_percentage',
                                labels={'name': 'Member', 'attendance_percentage': 'Attendance %'},
                                title='Regular Classes Attendance Overview',
                            )
                            # Customize the layout
                            fig.update_layout(
                                xaxis=dict(
                                    fixedrange=True,  # Disable x-axis zoom
                                    tickangle=-90,    # Rotate labels 90 degrees
                                    automargin=True   # Automatically adjust margin to fit labels
                                ),  # Disable x-axis zoom
                                yaxis=dict(
                                    fixedrange=True,  # Disable y-axis zoom
                                    range=[0, 100],   # Fix y-axis range from 0-100%
                                    ticksuffix='%'    # Add % to y-axis values
                                ),
                                height=400,
                                showlegend=False,
                                margin=dict(t=30, b=100, l=0, r=0),  # Adjust margins
                                hovermode='x unified'
                            )
                            # Update bar colors and add hover template
                            fig.update_traces(
                                marker_color="#8fdbf7",
                                hovertemplate="<br>".join([
                                    "<b>%{x}</b>",
                                    "Attendance: %{y:.1f}%",
                                    "<extra></extra>"
                                ])
                            )
                            # Display the chart with config options
                            st.plotly_chart(
                                fig, 
                                width='stretch',
                                config={
                                    'displayModeBar': True,
                                    'displaylogo': False,
                                    'modeBarButtonsToRemove': [
                                        'zoom', 'pan', 'select', 'lasso2d', 
                                        'zoomIn', 'zoomOut', 'autoScale', 'resetScale'
                                    ],
                                    'modeBarButtonsToAdd': ['fullscreen']
                                },
                                key="regular_attendance_chart"
                            )

                            st.divider()
                            st.subheader("⚠️ Low Attendance Members (Below 80%)")
                            low_attendance = regular_stats[regular_stats['attendance_percentage'] < 80].sort_values('attendance_percentage')
                            if not low_attendance.empty:
                                st.dataframe(
                                    low_attendance,
                                    column_config={
                                        "name": st.column_config.TextColumn(
                                            "Member",
                                            help="Member name"
                                        ),
                                        "total_classes": st.column_config.NumberColumn(
                                            "Total Classes",
                                            help="Total number of classes"
                                        ),
                                        "classes_present": st.column_config.NumberColumn(
                                            "Classes Present",
                                            help="Number of classes attended"
                                        ),
                                        "attendance_percentage": st.column_config.ProgressColumn(
                                            "Attendance %",
                                            help="Attendance percentage",
                                            format="%.1f%%",
                                            min_value=0,
                                            max_value=100
                                        )
                                    }
                                )
                            else:
                                st.success("No members with attendance below 80% 🎉")
                        else:
                            st.info("No regular classes recorded yet")

                    with stat_tab2:
                        st.subheader("Special Class Statistics")
                        if not special_stats.empty:
                            # Sort by attendance percentage in descending order
                            special_stats = special_stats.sort_values('attendance_percentage', ascending=False)
                            # Display the styled dataframe
                            st.dataframe(
                                special_stats,
                                column_config={
                                    "name": st.column_config.TextColumn(
                                        "Member",
                                        help="Member name"
                                    ),
                                    "total_classes": st.column_config.NumberColumn(
                                        "Total Classes",
                                        help="Total number of classes"
                                    ),
                                    "classes_present": st.column_config.NumberColumn(
                                        "Classes Present",
                                        help="Number of classes attended"
                                    ),
                                    "attendance_percentage": st.column_config.ProgressColumn(
                                        "Attendance %",
                                        help="Attendance percentage",
                                        format="%.1f%%",
                                        min_value=0,
                                        max_value=100
                                    )
                                }
                            )

                            # Create a bar chart using plotly
                            fig = px.bar(
                                special_stats,
                                x='name',
                                y='attendance_percentage',
                                labels={'name': 'Member', 'attendance_percentage': 'Attendance %'},
                                title='Special Classes Attendance Overview',
                            )
                            # Customize the layout
                            fig.update_layout(
                                xaxis=dict(
                                    fixedrange=True,  # Disable x-axis zoom
                                    tickangle=-90,    # Rotate labels 90 degrees
                                    automargin=True   # Automatically adjust margin to fit labels
                                ),  # Disable x-axis zoom
                                yaxis=dict(
                                    fixedrange=True,  # Disable y-axis zoom
                                    range=[0, 100],   # Fix y-axis range from 0-100%
                                    ticksuffix='%'    # Add % to y-axis values
                                ),
                                height=400,
                                showlegend=False,
                                margin=dict(t=30, b=100, l=0, r=0),  # Adjust margins
                                hovermode='x unified'
                            )
                            # Update bar colors and add hover template
                            fig.update_traces(
                                marker_color="#8fdbf7",
                                hovertemplate="<br>".join([
                                    "<b>%{x}</b>",
                                    "Attendance: %{y:.1f}%",
                                    "<extra></extra>"
                                ])
                            )
                            # Display the chart with config options
                            st.plotly_chart(
                                fig, 
                                width='stretch',
                                config={
                                    'displayModeBar': True,
                                    'displaylogo': False,
                                    'modeBarButtonsToRemove': [
                                        'zoom', 'pan', 'select', 'lasso2d', 
                                        'zoomIn', 'zoomOut', 'autoScale', 'resetScale'
                                    ],
                                    'modeBarButtonsToAdd': ['fullscreen']
                                },
                                key="special_attendance_chart"
                            )

                            st.divider()
                            st.subheader("⚠️ Low Attendance Members (Below 80%)")
                            low_attendance = special_stats[special_stats['attendance_percentage'] < 80].sort_values('attendance_percentage')
                            if not low_attendance.empty:
                                st.dataframe(
                                    low_attendance,
                                    column_config={
                                        "name": st.column_config.TextColumn(
                                            "Member",
                                            help="Member name"
                                        ),
                                        "total_classes": st.column_config.NumberColumn(
                                            "Total Classes",
                                            help="Total number of classes"
                                        ),
                                        "classes_present": st.column_config.NumberColumn(
                                            "Classes Present",
                                            help="Number of classes attended"
                                        ),
                                        "attendance_percentage": st.column_config.ProgressColumn(
                                            "Attendance %",
                                            help="Attendance percentage",
                                            format="%.1f%%",
                                            min_value=0,
                                            max_value=100
                                        )
                                    }
                                )
                            else:
                                st.success("No members with attendance below 80% 🎉")

                        else:
                            st.info("No special classes recorded yet")

                    with stat_tab3:
                        # Get current date for comparison
                        current_date = date.today()
                        # Display Events Overview

                        if not events_df.empty:
                            # Convert date columns to datetime
                            events_view = events_df.copy()
                            events_view['start_date'] = pd.to_datetime(events_view['start_date'])
                            events_view['end_date'] = pd.to_datetime(events_view['end_date'])
                            events_view['duration'] = (events_view['end_date'] - events_view['start_date']).dt.days

                            # Split events into ongoing and completed
                            current_events = events_view[events_view['end_date'].dt.date >= current_date]
                            completed_events = events_view[events_view['end_date'].dt.date < current_date]

                            # Inside Events tab, replace the Current & Upcoming Events section with:
                            st.subheader("🎯 Current & Upcoming Events")
                            if not current_events.empty:
                                for _, event in current_events.iterrows():
                                    status = 'Upcoming' if pd.to_datetime(event['start_date']).date() > current_date else 'Ongoing'
                                    with st.expander(f"{status} - {event['event_name']}"):
                                        # Event Details
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.write("**📅 Event Period**")
                                            st.write(f"Start Date: {pd.to_datetime(event['start_date']).date()}")
                                            st.write(f"End Date: {pd.to_datetime(event['end_date']).date()}")
                                            st.write(f"Duration: {event['duration']} days")

                                        with col2:
                                            # st.write("**👥 Participants** :")
                                            # st.write(f"Total Participants: {len(event['participating_members'])} : {', '.join(event['participating_members'])}")
                                            st.metric("Total Participants", len(event['participating_members']))
                                            if event['dri_members']:
                                                st.write("**🎯 DRIs:**")
                                                st.write(", ".join(event['dri_members']))

                                        # Description
                                        if pd.notna(event['description']):
                                            st.write("**📝 Description**")
                                            st.write(event['description'])

                                        st.write("**👥 Participants:**")
                                        st.write(", ".join(event['participating_members']))

                                        event_attendance = df[df['event'] == event['event_name']]

                                        if event_attendance.empty:
                                            st.info("No attendance records for this event yet")
                                        else:
                                        
                                            # Calculate statistics specifically for this event's participants
                                            event_stats = pd.DataFrame()

                                            total_sessions = len(event_attendance['date'].unique())

                                            # Calculate attendance for each participant
                                            for participant in event['participating_members']:
                                                participant_attendance = event_attendance[event_attendance['name'] == participant]
                                                sessions_present = len(participant_attendance[participant_attendance['status'] == 'Present'])

                                                # Add participant stats to DataFrame
                                                event_stats = pd.concat([event_stats, pd.DataFrame({
                                                    'name': [participant],
                                                    'classes_present': [sessions_present],
                                                    'attendance_percentage': [(sessions_present / total_sessions * 100) if total_sessions > 0 else 0]
                                                })], ignore_index=True)

                                            # Sort by attendance percentage in descending order
                                            event_stats = event_stats.sort_values('attendance_percentage', ascending=False)

                                            st.markdown("""
                                                <div style='
                                                    background-color: rgba(255, 255, 255, 0.1);
                                                    padding: 20px;
                                                    border-radius: 10px;
                                                    margin: 10px 0;
                                                    text-align: center;
                                                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                                                '>
                                                    <h3 style='color: #1E1E1E; margin-bottom: 10px;'>📊 Sessions Overview</h3>
                                                    <div style='
                                                        font-size: 48px;
                                                        font-weight: bold;
                                                        color: #2196F3;
                                                        margin: 10px 0;
                                                    '>{}</div>
                                                    <div style='color: #666; font-size: 16px;'>Total Sessions Conducted</div>
                                                </div>
                                            """.format(total_sessions), unsafe_allow_html=True)

                                            st.write("Participant Statistics:")

                                            # Display the styled dataframe
                                            st.dataframe(
                                                event_stats,
                                                column_config={
                                                    "name": st.column_config.TextColumn(
                                                        "Participant",
                                                        help="Member name"
                                                    ),
                                                    "classes_present": st.column_config.NumberColumn(
                                                        "Sessions Present",
                                                        help="Number of sessions attended"
                                                    ),
                                                    "attendance_percentage": st.column_config.ProgressColumn(
                                                        "Attendance %",
                                                        help="Attendance percentage",
                                                        format="%.1f%%",
                                                        min_value=0,
                                                        max_value=100
                                                    )
                                                }
                                            )

                                            # Create a bar chart using plotly
                                            fig = px.bar(
                                                event_stats,
                                                x='name',
                                                y='attendance_percentage',
                                                labels={'name': 'Participant', 'attendance_percentage': 'Attendance %'},
                                                title='Participant Attendance Overview for ' + event['event_name'],
                                            )

                                            # Customize the layout
                                            fig.update_layout(
                                                xaxis=dict(
                                                    fixedrange=True,  # Disable x-axis zoom
                                                    tickangle=-90,    # Rotate labels 90 degrees
                                                    automargin=True   # Automatically adjust margin to fit labels
                                                ),  # Disable x-axis zoom
                                                yaxis=dict(
                                                    fixedrange=True,  # Disable y-axis zoom
                                                    range=[0, 100],   # Fix y-axis range from 0-100%
                                                    ticksuffix='%'    # Add % to y-axis values
                                                ),
                                                height=400,
                                                showlegend=False,
                                                margin=dict(t=30, b=100, l=0, r=0),  # Adjust margins
                                                hovermode='x unified'
                                            )

                                            # Update bar colors and add hover template
                                            fig.update_traces(
                                                marker_color="#8fdbf7",
                                                hovertemplate="<br>".join([
                                                    "<b>%{x}</b>",
                                                    "Attendance: %{y:.1f}%",
                                                    "<extra></extra>"
                                                ])
                                            )

                                            # Display the chart with config options
                                            st.plotly_chart(
                                                fig, 
                                                width='stretch',
                                                config={
                                                    'displayModeBar': True,
                                                    'displaylogo': False,
                                                    'modeBarButtonsToRemove': [
                                                        'zoom', 'pan', 'select', 'lasso2d', 
                                                        'zoomIn', 'zoomOut', 'autoScale', 'resetScale'
                                                    ],
                                                    'modeBarButtonsToAdd': ['fullscreen']
                                                }
                                            )
                            else:
                                st.info("No current or upcoming events")


                            # Show Completed Events
                            st.subheader("🏆 Completed Events")
                            if not completed_events.empty:
                                for _, event in completed_events.iterrows():
                                    with st.expander(f"Completed - {event['event_name']}"):
                                        # Event Details
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.write("**📅 Event Period**")
                                            st.write(f"Start Date: {pd.to_datetime(event['start_date']).date()}")
                                            st.write(f"End Date: {pd.to_datetime(event['end_date']).date()}")
                                            st.write(f"Duration: {event['duration']} days")

                                        with col2:
                                            # st.write("**👥 Participants** :")
                                            # st.write(f"Total Participants: {len(event['participating_members'])} : {', '.join(event['participating_members'])}")
                                            st.metric("Total Participants", len(event['participating_members']))
                                            if event['dri_members']:
                                                st.write("**🎯 DRIs:**")
                                                st.write(", ".join(event['dri_members']))

                                        # Description
                                        if pd.notna(event['description']):
                                            st.write("**📝 Description**")
                                            st.write(event['description'])

                                        st.write("**👥 Participants:**")
                                        st.write(", ".join(event['participating_members']))

                                        # Event Statistics
                                        event_attendance = df[df['event'] == event['event_name']]
                                        if event_attendance.empty:
                                            st.info("No attendance records for this event yet")
                                        else:
                                            # Calculate statistics specifically for this event's participants
                                            event_stats = pd.DataFrame()

                                            total_sessions = len(event_attendance['date'].unique())

                                            # Calculate attendance for each participant
                                            for participant in event['participating_members']:
                                                participant_attendance = event_attendance[event_attendance['name'] == participant]
                                                sessions_present = len(participant_attendance[participant_attendance['status'] == 'Present'])

                                                # Add participant stats to DataFrame
                                                event_stats = pd.concat([event_stats, pd.DataFrame({
                                                    'name': [participant],
                                                    'classes_present': [sessions_present],
                                                    'attendance_percentage': [(sessions_present / total_sessions * 100) if total_sessions > 0 else 0]
                                                })], ignore_index=True)

                                            # Sort by attendance percentage in descending order
                                            event_stats = event_stats.sort_values('attendance_percentage', ascending=False)

                                            st.markdown("""
                                                <div style='
                                                    background-color: rgba(255, 255, 255, 0.1);
                                                    padding: 20px;
                                                    border-radius: 10px;
                                                    margin: 10px 0;
                                                    text-align: center;
                                                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                                                '>
                                                    <h3 style='color: #1E1E1E; margin-bottom: 10px;'>📊 Sessions Overview</h3>
                                                    <div style='
                                                        font-size: 48px;
                                                        font-weight: bold;
                                                        color: #2196F3;
                                                        margin: 10px 0;
                                                    '>{}</div>
                                                    <div style='color: #666; font-size: 16px;'>Total Sessions Conducted</div>
                                                </div>
                                            """.format(total_sessions), unsafe_allow_html=True)

                                            st.write("Participant Statistics:")

                                            # Display the styled dataframe
                                            st.dataframe(
                                                event_stats,
                                                column_config={
                                                    "name": st.column_config.TextColumn(
                                                        "Participant",
                                                        help="Member name"
                                                    ),
                                                    "classes_present": st.column_config.NumberColumn(
                                                        "Sessions Present",
                                                        help="Number of sessions attended"
                                                    ),
                                                    "attendance_percentage": st.column_config.ProgressColumn(
                                                        "Attendance %",
                                                        help="Attendance percentage",
                                                        format="%.1f%%",
                                                        min_value=0,
                                                        max_value=100
                                                    )
                                                }
                                            )

                                            # Create a bar chart using plotly
                                            fig = px.bar(
                                                event_stats,
                                                x='name',
                                                y='attendance_percentage',
                                                labels={'name': 'Participant', 'attendance_percentage': 'Attendance %'},
                                                title='Participant Attendance Overview for ' + event['event_name'],
                                            )

                                            # Customize the layout
                                            fig.update_layout(
                                                xaxis=dict(
                                                    fixedrange=True,  # Disable x-axis zoom
                                                    tickangle=-90,    # Rotate labels 90 degrees
                                                    automargin=True   # Automatically adjust margin to fit labels
                                                ),  # Disable x-axis zoom
                                                yaxis=dict(
                                                    fixedrange=True,  # Disable y-axis zoom
                                                    range=[0, 100],   # Fix y-axis range from 0-100%
                                                    ticksuffix='%'    # Add % to y-axis values
                                                ),
                                                height=400,
                                                showlegend=False,
                                                margin=dict(t=30, b=100, l=0, r=0),  # Adjust margins
                                                hovermode='x unified'
                                            )

                                            # Update bar colors and add hover template
                                            fig.update_traces(
                                                marker_color="#8fdbf7",
                                                hovertemplate="<br>".join([
                                                    "<b>%{x}</b>",
                                                    "Attendance: %{y:.1f}%",
                                                    "<extra></extra>"
                                                ])
                                            )

                                            # Display the chart with config options
                                            st.plotly_chart(
                                                fig, 
                                                width='stretch',
                                                config={
                                                    'displayModeBar': True,
                                                    'displaylogo': False,
                                                    'modeBarButtonsToRemove': [
                                                        'zoom', 'pan', 'select', 'lasso2d', 
                                                        'zoomIn', 'zoomOut', 'autoScale', 'resetScale'
                                                    ],
                                                    'modeBarButtonsToAdd': ['fullscreen']
                                                }
                                            )
                            else:
                                st.info("No completed events")
                        else:
                            st.info("No Events records to show statistics")
                        pass

                    with stat_tab4:
                        st.subheader("Combined Statistics")
                        if not combined_stats.empty:
                            # Calculate total classes held for each class type
                            total_regular = len(df[df['class_type'] == 'Regular']['date'].unique())
                            total_special = len(df[df['class_type'] == 'Special']['date'].unique())
                            total_events = len(df[df['class_type'] == 'Event/Competition']['date'].unique())
                            total_classes_held = total_regular + total_special + total_events

                            # Add stars calculation
                            combined_stats['Stars'] = combined_stats.apply(
                                lambda x: f"{'⭐' * int((x['classes_present'] / total_classes_held) * 5)}" + 
                                         f" ({((x['classes_present'] / total_classes_held) * 100):.1f}%)", 
                                axis=1
                            )

                            # Display the updated dataframe with custom formatting
                            st.dataframe(
                                combined_stats,
                                column_config={
                                    "name": "Name",
                                    "total_classes": "Committed Classes",
                                    "classes_present": "Present",
                                    "attendance_percentage": st.column_config.NumberColumn(
                                        "Personal Attendance %",
                                        format="%.1f%%"
                                    ),
                                    "Stars": st.column_config.TextColumn(
                                        "Overall Attendance Rating",
                                        help="Stars based on total classes held"
                                    )
                                }
                            )

                else:
                    st.info("No attendance records to show statistics")
                pass

            elif tab_name == "Events":
                st.subheader("Events Management")

                # Get current date for comparison
                current_date = date.today()

                event_action = st.radio("Create / Edit Event :", ["Create New Event", "Edit Existing Event"], horizontal=True)

                # Get all active members for selection
                response = supabase.table('member_credentials')\
                            .select('username')\
                            .eq('is_active', True)\
                            .execute()

                active_members = [member['username'] for member in response.data]

                if event_action == "Create New Event":
                    with st.expander("Create New Event"):
                        new_event_name = st.text_input("Event Name", key="create_event_name")
                        event_start = st.date_input("Start Date", key="create_event_start")
                        event_end = st.date_input("End Date", key="create_event_end")
                        event_desc = st.text_area("Description", key="create_event_desc")

                        col1, col2 = st.columns(2)

                        with col1:
                            participating_members = st.multiselect(
                                "Select Participating Members",
                                options=active_members,
                                default=[]
                            )

                        with col2:
                            dri_members = st.multiselect(
                                "Select DRIs (Event Leaders)",
                                options=participating_members,  # Only show selected participating members
                                default=[]
                            )

                        if st.button("Add Event"):
                            if new_event_name and event_start and event_end:
                                events_df = add_event(
                                    new_event_name, 
                                    event_start, 
                                    event_end, 
                                    event_desc,
                                    participating_members,
                                    dri_members
                                )
                                if events_df is not None:
                                    st.balloons()
                                    st.success("Event added successfully!")
                                    st.write("Event Details:")
                                    st.write(f"- Total participants: {len(participating_members)}")
                                    st.write(f"- DRIs: {', '.join(dri_members)}")
                            else:
                                st.error("Please fill all required fields")
                elif event_action == "Edit Existing Event":
                    existing_events = events_df['event_name'].unique().tolist() if not events_df.empty else []
                    if existing_events:
                        selected_event = st.selectbox("Select Event to Edit", existing_events)

                        event_to_edit = events_df[events_df['event_name'] == selected_event].iloc[0]

                        with st.expander("Edit Event Details"):
                            edited_event_name = st.text_input("Event Name", value=event_to_edit['event_name'])
                            edited_start = st.date_input("Start Date", value=pd.to_datetime(event_to_edit['start_date']).date())
                            edited_end = st.date_input("End Date", value=pd.to_datetime(event_to_edit['end_date']).date())
                            edited_desc = st.text_area("Description", value=event_to_edit['description'])
                            edited_participants = st.multiselect("Select Participants", options=active_members, default=event_to_edit['participating_members'] if 'participating_members' in event_to_edit else [])
                            edited_dris = st.multiselect("Select DRIs (Event Leaders)", options=edited_participants, default=event_to_edit['dri_members'] if 'dri_members' in event_to_edit else [])

                            if st.button("Save Changes"):
                                events_df = update_event(
                                    original_event_name=selected_event,
                                    new_event_name=edited_event_name,
                                    start_date=edited_start,
                                    end_date=edited_end,
                                    description=edited_desc,
                                    participants=edited_participants,
                                    dri_members=edited_dris
                                )
                                if events_df is not None:
                                    st.balloons()
                                    st.success("Event updated successfully!")
                    else:
                        st.info("No existing events to edit")

                # Inside Events tab, after Edit Event section
                if st.session_state.user_role in ['master_admin', 'super_admin']:
                    with st.expander("🗑️ Delete Event"):
                        st.error("⚠️ Danger Zone")
                        event_to_delete = st.selectbox("Select Event to Delete", events_df['event_name'].unique().tolist() if not events_df.empty else [])

                        if event_to_delete:
                            st.warning(f"This will permanently delete the event '{event_to_delete}' and all its attendance records!")

                            # Add confirmation input
                            confirm_text = st.text_input("Type DELETE to confirm", key="delete_event_confirm")

                            if st.button("Delete Event", type="primary"):
                                if confirm_text == "DELETE":
                                    try:
                                        # First delete attendance records for this event
                                        supabase.table('attendance')\
                                            .delete()\
                                            .eq('event', event_to_delete)\
                                            .execute()

                                        # Then delete the event
                                        supabase.table('events')\
                                            .delete()\
                                            .eq('event_name', event_to_delete)\
                                            .execute()

                                        st.success(f"Successfully deleted event: {event_to_delete}")
                                        time.sleep(2)
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Error deleting event: {str(e)}")
                                else:
                                    st.error("Please type DELETE to confirm")

                # Display Events Overview
                st.divider()
                if not events_df.empty:
                    # Convert date columns to datetime
                    events_view = events_df.copy()
                    events_view['start_date'] = pd.to_datetime(events_view['start_date'])
                    events_view['end_date'] = pd.to_datetime(events_view['end_date'])
                    events_view['duration'] = (events_view['end_date'] - events_view['start_date']).dt.days

                    # Split events into ongoing and completed
                    current_events = events_view[events_view['end_date'].dt.date >= current_date]
                    completed_events = events_view[events_view['end_date'].dt.date < current_date]

                    # Inside Events tab, replace the Current & Upcoming Events section with:
                    st.subheader("🎯 Current & Upcoming Events")
                    if not current_events.empty:
                        for _, event in current_events.iterrows():
                            status = 'Upcoming' if pd.to_datetime(event['start_date']).date() > current_date else 'Ongoing'
                            with st.expander(f"{status} - {event['event_name']}"):
                                # Event Details
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("**📅 Event Period**")
                                    st.write(f"Start Date: {pd.to_datetime(event['start_date']).date()}")
                                    st.write(f"End Date: {pd.to_datetime(event['end_date']).date()}")
                                    st.write(f"Duration: {event['duration']} days")

                                with col2:
                                    # st.write("**👥 Participants** :")
                                    # st.write(f"Total Participants: {len(event['participating_members'])} : {', '.join(event['participating_members'])}")
                                    st.metric("Total Participants", len(event['participating_members']))
                                    if event['dri_members']:
                                        st.write("**🎯 DRIs:**")
                                        st.write(", ".join(event['dri_members']))

                                # Description
                                if pd.notna(event['description']):
                                    st.write("**📝 Description**")
                                    st.write(event['description'])

                                st.write("**👥 Participants:**")
                                st.write(", ".join(event['participating_members']))

                                event_attendance = df[df['event'] == event['event_name']]

                                if event_attendance.empty:
                                    st.info("No attendance records for this event yet")
                                else:

                                    # Calculate statistics specifically for this event's participants
                                    event_stats = pd.DataFrame()

                                    total_sessions = len(event_attendance['date'].unique())

                                    # Calculate attendance for each participant
                                    for participant in event['participating_members']:
                                        participant_attendance = event_attendance[event_attendance['name'] == participant]
                                        sessions_present = len(participant_attendance[participant_attendance['status'] == 'Present'])

                                        # Add participant stats to DataFrame
                                        event_stats = pd.concat([event_stats, pd.DataFrame({
                                            'name': [participant],
                                            'classes_present': [sessions_present],
                                            'attendance_percentage': [(sessions_present / total_sessions * 100) if total_sessions > 0 else 0]
                                        })], ignore_index=True)

                                    # Sort by attendance percentage in descending order
                                    event_stats = event_stats.sort_values('attendance_percentage', ascending=False)

                                    st.markdown("""
                                        <div style='
                                            background-color: rgba(255, 255, 255, 0.1);
                                            padding: 20px;
                                            border-radius: 10px;
                                            margin: 10px 0;
                                            text-align: center;
                                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                                        '>
                                            <h3 style='color: #1E1E1E; margin-bottom: 10px;'>📊 Sessions Overview</h3>
                                            <div style='
                                                font-size: 48px;
                                                font-weight: bold;
                                                color: #2196F3;
                                                margin: 10px 0;
                                            '>{}</div>
                                            <div style='color: #666; font-size: 16px;'>Total Sessions Conducted</div>
                                        </div>
                                    """.format(total_sessions), unsafe_allow_html=True)

                                    st.write("Participant Statistics:")

                                    # Display the styled dataframe
                                    st.dataframe(
                                        event_stats,
                                        column_config={
                                            "name": st.column_config.TextColumn(
                                                "Participant",
                                                help="Member name"
                                            ),
                                            "classes_present": st.column_config.NumberColumn(
                                                "Sessions Present",
                                                help="Number of sessions attended"
                                            ),
                                            "attendance_percentage": st.column_config.ProgressColumn(
                                                "Attendance %",
                                                help="Attendance percentage",
                                                format="%.1f%%",
                                                min_value=0,
                                                max_value=100
                                            )
                                        }
                                    )

                                    # Create a bar chart using plotly
                                    fig = px.bar(
                                        event_stats,
                                        x='name',
                                        y='attendance_percentage',
                                        labels={'name': 'Participant', 'attendance_percentage': 'Attendance %'},
                                        title='Participant Attendance Overview for ' + event['event_name'],
                                    )

                                    # Customize the layout
                                    fig.update_layout(
                                        xaxis=dict(
                                            fixedrange=True,  # Disable x-axis zoom
                                            tickangle=-90,    # Rotate labels 90 degrees
                                            automargin=True   # Automatically adjust margin to fit labels
                                        ),  # Disable x-axis zoom
                                        yaxis=dict(
                                            fixedrange=True,  # Disable y-axis zoom
                                            range=[0, 100],   # Fix y-axis range from 0-100%
                                            ticksuffix='%'    # Add % to y-axis values
                                        ),
                                        height=400,
                                        showlegend=False,
                                        margin=dict(t=30, b=100, l=0, r=0),  # Adjust margins
                                        hovermode='x unified'
                                    )

                                    # Update bar colors and add hover template
                                    fig.update_traces(
                                        marker_color="#8fdbf7",
                                        hovertemplate="<br>".join([
                                            "<b>%{x}</b>",
                                            "Attendance: %{y:.1f}%",
                                            "<extra></extra>"
                                        ])
                                    )

                                    # Display the chart with config options
                                    st.plotly_chart(
                                        fig, 
                                        width='stretch',
                                        config={
                                            'displayModeBar': True,
                                            'displaylogo': False,
                                            'modeBarButtonsToRemove': [
                                                'zoom', 'pan', 'select', 'lasso2d', 
                                                'zoomIn', 'zoomOut', 'autoScale', 'resetScale'
                                            ],
                                            'modeBarButtonsToAdd': ['fullscreen']
                                        },
                                        key=f"current_event_chart_{event['event_name'].lower().replace(' ', '_')}"
                                    )
                    else:
                        st.info("No current or upcoming events")


                    # Show Completed Events
                    st.subheader("🏆 Completed Events")
                    if not completed_events.empty:
                        for _, event in completed_events.iterrows():
                            with st.expander(f"Completed - {event['event_name']}"):
                                # Event Details
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.write("**📅 Event Period**")
                                    st.write(f"Start Date: {pd.to_datetime(event['start_date']).date()}")
                                    st.write(f"End Date: {pd.to_datetime(event['end_date']).date()}")
                                    st.write(f"Duration: {event['duration']} days")

                                with col2:
                                    # st.write("**👥 Participants** :")
                                    # st.write(f"Total Participants: {len(event['participating_members'])} : {', '.join(event['participating_members'])}")
                                    st.metric("Total Participants", len(event['participating_members']))
                                    if event['dri_members']:
                                        st.write("**🎯 DRIs:**")
                                        st.write(", ".join(event['dri_members']))

                                # Description
                                if pd.notna(event['description']):
                                    st.write("**📝 Description**")
                                    st.write(event['description'])

                                st.write("**👥 Participants:**")
                                st.write(", ".join(event['participating_members']))

                                # Event Statistics
                                event_attendance = df[df['event'] == event['event_name']]
                                if event_attendance.empty:
                                    st.info("No attendance records for this event yet")
                                else:
                                    # Calculate statistics specifically for this event's participants
                                    event_stats = pd.DataFrame()

                                    total_sessions = len(event_attendance['date'].unique())

                                    # Calculate attendance for each participant
                                    for participant in event['participating_members']:
                                        participant_attendance = event_attendance[event_attendance['name'] == participant]
                                        sessions_present = len(participant_attendance[participant_attendance['status'] == 'Present'])

                                        # Add participant stats to DataFrame
                                        event_stats = pd.concat([event_stats, pd.DataFrame({
                                            'name': [participant],
                                            'classes_present': [sessions_present],
                                            'attendance_percentage': [(sessions_present / total_sessions * 100) if total_sessions > 0 else 0]
                                        })], ignore_index=True)

                                    # Sort by attendance percentage in descending order
                                    event_stats = event_stats.sort_values('attendance_percentage', ascending=False)

                                    st.markdown("""
                                        <div style='
                                            background-color: rgba(255, 255, 255, 0.1);
                                            padding: 20px;
                                            border-radius: 10px;
                                            margin: 10px 0;
                                            text-align: center;
                                            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                                        '>
                                            <h3 style='color: #1E1E1E; margin-bottom: 10px;'>📊 Sessions Overview</h3>
                                            <div style='
                                                font-size: 48px;
                                                font-weight: bold;
                                                color: #2196F3;
                                                margin: 10px 0;
                                            '>{}</div>
                                            <div style='color: #666; font-size: 16px;'>Total Sessions Conducted</div>
                                        </div>
                                    """.format(total_sessions), unsafe_allow_html=True)

                                    st.write("Participant Statistics:")

                                    # Display the styled dataframe
                                    st.dataframe(
                                        event_stats,
                                        column_config={
                                            "name": st.column_config.TextColumn(
                                                "Participant",
                                                help="Member name"
                                            ),
                                            "classes_present": st.column_config.NumberColumn(
                                                "Sessions Present",
                                                help="Number of sessions attended"
                                            ),
                                            "attendance_percentage": st.column_config.ProgressColumn(
                                                "Attendance %",
                                                help="Attendance percentage",
                                                format="%.1f%%",
                                                min_value=0,
                                                max_value=100
                                            )
                                        }
                                    )

                                    # Create a bar chart using plotly
                                    fig = px.bar(
                                        event_stats,
                                        x='name',
                                        y='attendance_percentage',
                                        labels={'name': 'Participant', 'attendance_percentage': 'Attendance %'},
                                        title='Participant Attendance Overview for ' + event['event_name'],
                                    )

                                    # Customize the layout
                                    fig.update_layout(
                                        xaxis=dict(
                                            fixedrange=True,  # Disable x-axis zoom
                                            tickangle=-90,    # Rotate labels 90 degrees
                                            automargin=True   # Automatically adjust margin to fit labels
                                        ),  # Disable x-axis zoom
                                        yaxis=dict(
                                            fixedrange=True,  # Disable y-axis zoom
                                            range=[0, 100],   # Fix y-axis range from 0-100%
                                            ticksuffix='%'    # Add % to y-axis values
                                        ),
                                        height=400,
                                        showlegend=False,
                                        margin=dict(t=30, b=100, l=0, r=0),  # Adjust margins
                                        hovermode='x unified'
                                    )

                                    # Update bar colors and add hover template
                                    fig.update_traces(
                                        marker_color="#8fdbf7",
                                        hovertemplate="<br>".join([
                                            "<b>%{x}</b>",
                                            "Attendance: %{y:.1f}%",
                                            "<extra></extra>"
                                        ])
                                    )

                                    # Display the chart with config options
                                    st.plotly_chart(
                                        fig, 
                                        width='stretch',
                                        config={
                                            'displayModeBar': True,
                                            'displaylogo': False,
                                            'modeBarButtonsToRemove': [
                                                'zoom', 'pan', 'select', 'lasso2d', 
                                                'zoomIn', 'zoomOut', 'autoScale', 'resetScale'
                                            ],
                                            'modeBarButtonsToAdd': ['fullscreen']
                                        },
                                        key=f"completed_event_chart_{event['event_name'].lower().replace(' ', '_')}"
                                    )
                    else:
                        st.info("No completed events")
                else:
                    st.info("No Events records to show statistics")
                pass

            elif tab_name == "Manage Members":
                st.subheader("Admin Console - Manage Members")

                # View/manage existing members
                response = supabase.table('member_credentials').select('*').execute()

                if response.data:
                    members_df = pd.DataFrame(response.data)

                    total_members = len(members_df)
                    active_members = len(members_df[members_df['is_active'] == True])
                    inactive_members = total_members - active_members

                    # Display metrics in columns
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Members", total_members)
                    with col2:
                        st.metric("Active Members", active_members, 
                                 f"{(active_members/total_members*100):.1f}%" if total_members > 0 else "0%", delta_color="normal")
                    with col3:
                        st.metric("Inactive Members", inactive_members,
                                 f"{(inactive_members/total_members*100):.1f}%" if total_members > 0 else "0%", delta_color="inverse")

                # Add new member
                with st.expander("Add New Member"):
                    new_username = st.text_input("Username")
                    new_password = st.text_input("Password", type="password", key="new_member_password_input")

                    if st.session_state.user_role == 'super_admin' or st.session_state.user_role == 'master_admin':
                        user_role_option = st.radio("Member role : ", ["Member", "Admin", "Super Admin"], horizontal=True, key="new_member_role_radio")

                    if st.button("Add Member"):
                        if new_username and new_password:
                            if add_member_credentials(new_username, new_password):
                                if user_role_option:
                                    update_member_role(new_username, user_role_option.lower().replace(' ', '_'))
                                st.balloons()  # Celebration with balloons
                                st.success(f"Added member: {new_username}")
                        else:
                            st.error("Please provide both username and password")

                st.divider()
                st.subheader("Team ZDC")
                # View/manage existing members
                response = supabase.table('member_credentials').select('*').execute()

                if response.data:
                    members_df = pd.DataFrame(response.data)

                    # Create a styled dataframe
                    styled_df = members_df[['username', 'role', 'is_active', 'created_at']].copy()

                    # Format created_at to show only date
                    styled_df['created_at'] = pd.to_datetime(styled_df['created_at']).dt.date

                    styled_df['status_order'] = styled_df['is_active'].astype(int)  # True=1, False=0

                    # Convert is_active to colored text
                    styled_df['is_active'] = styled_df['is_active'].apply(
                        lambda x: f"🟢 Active" if x else f"🔴 Inactive"
                    )

                    # Add a numeric column for sorting roles
                    role_order = {
                        'super_admin': 1,
                        'admin': 2,
                        'member': 3
                    }
                    styled_df['role_order'] = styled_df['role'].map(role_order)

                    # Sort by active status first (descending), then role, then username
                    styled_df = styled_df.sort_values(
                        ['status_order', 'role_order', 'username'], 
                        ascending=[False, True, True]
                    )

                    # Format role display
                    styled_df['role'] = styled_df['role'].apply(format_role)

                    # Drop the sorting column
                    styled_df = styled_df.drop(['role_order', 'status_order'], axis=1)

                    # Rename columns for better display
                    styled_df.columns = ['Username', 'Role', 'Status', 'Created At']
                    # Display the styled dataframe
                    st.dataframe(
                        styled_df,
                        column_config={
                            "Status": st.column_config.TextColumn(
                                "Status",
                                help="Member account status",
                                width="medium"
                            ),
                            "Role": st.column_config.TextColumn(
                                "Role",
                                help="Member role in the system"
                            )
                        }
                    )

                    if st.session_state.user_role == 'super_admin' or st.session_state.user_role == 'master_admin':
                        st.divider()
                        st.subheader("Update Member Profile")

                        response = supabase.table('member_credentials').select('*').execute()
                        members_df = pd.DataFrame(response.data)

                        # Manage member profile
                        member_to_update = st.selectbox("Select member to update", members_df['username'])

                        # Get current role from database and convert to display format
                        current_role = members_df[members_df['username'] == member_to_update]['role'].iloc[0]

                        current_role_display = format_role(current_role)

                        # Create radio with display values
                        role_options = ["Member", "Admin", "Super Admin"]
                        update_user_role_option = st.radio(
                            "Member role : ", 
                            role_options,
                            horizontal=True,
                            index=role_options.index(current_role_display)
                        )

                        with st.expander("🔑 Change Password"):
                            new_password = st.text_input("New Password", type="password")
                            if st.button("Update Password"):
                                if update_member_password(member_to_update, new_password):
                                    st.success(f"Updated password for {member_to_update}")

                        current_status = members_df[members_df['username'] == member_to_update]['is_active'].iloc[0]
                        new_status = st.checkbox("Is Active", value=current_status)
                        if st.button("Update Profile"):
                            if update_user_role_option:
                                update_member_role(member_to_update, update_user_role_option.lower().replace(' ', '_'))
                                st.success(f"Updated member: {member_to_update} to role {update_user_role_option}")

                            if update_member_status(member_to_update, new_status):
                                st.balloons()  # Celebration with balloons
                                st.success(f"Updated status for {member_to_update}")
                                time.sleep(2)
                                st.rerun()
