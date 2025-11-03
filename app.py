import streamlit as st
import pandas as pd
import os
import supabase
from datetime import datetime, date
from supabase import create_client, Client
import time

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
df = load_attendance_data()
student_info_df = load_student_info()

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

def save_student_info(df):
    supabase.table('student_info').delete().neq('id', 0).execute()
    if not df.empty:
        records = df.to_dict('records')
        supabase.table('student_info').insert(records).execute()

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
events_df = load_events()

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
                    st.success(f"Logged in as Admin: {admin_name}")
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
                    st.success(f"Welcome, {member_name}")
                    st.rerun()
        
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
                    st.success(f"Updated status for {member_to_update}")
                    st.rerun()

# View Records tab (available to all)
with tab3:
    # Rename the original tab2 content to tab3
    st.subheader("Attendance Records")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        search_name = st.text_input("Search by name")
    with col2:
        date_filter = st.date_input("Select date", today)
    
    # Apply filters
    filtered_df = df.copy()
    if search_name:
        filtered_df = filtered_df[filtered_df['name'].str.contains(search_name, case=False, na=False)]

        # If exact match found, show detailed statistics
        exact_matches = df[df['name'].str.lower() == search_name.lower()]
        if not exact_matches.empty:
            student_name = exact_matches['name'].iloc[0]
            
            # Create student info card
            st.divider()
            st.subheader(f"Student Details: {student_name}")
            
            # Get student bio
            student_bio = student_info_df[student_info_df['name'] == student_name] if not student_info_df.empty else pd.DataFrame()
            
            # Display student info in columns
            info_col1, info_col2 = st.columns([2, 1])
            
            with info_col1:
                # Bio section
                if not student_bio.empty:
                    st.markdown("**Bio:**")
                    st.write(student_bio['bio'].iloc[0])
                    st.markdown(f"**Joined:** {student_bio['join_date'].iloc[0]}")
                elif st.session_state.is_admin:
                    # Allow admin to add bio
                    with st.expander("Add Student Bio"):
                        bio = st.text_area("Bio")
                        join_date = st.date_input("Join Date", today)
                        contact = st.text_input("Contact Info")
                        if st.button("Save Bio"):
                            new_bio = pd.DataFrame([{
                                'name': student_name,
                                'bio': bio,
                                'join_date': join_date,
                                'contact': contact
                            }])
                            student_info_df = pd.concat([student_info_df, new_bio], ignore_index=True)
                            save_student_info(student_info_df)
                            st.success("Bio added successfully!")
                            st.rerun()
            
            with info_col2:
                # Attendance statistics
                regular_matches = exact_matches[exact_matches['class_type'] == 'Regular']
                special_matches = exact_matches[exact_matches['class_type'] == 'Special']

                st.markdown("**Regular Classes**")
                regular_total = len(regular_matches)
                regular_present = len(regular_matches[regular_matches['status'] == 'Present'])
                regular_percentage = (regular_present / regular_total * 100) if regular_total > 0 else 0
                loc_col1, loc_col2 = st.columns(2)
                with loc_col1:
                    st.metric("Total", regular_total)
                with loc_col2:
                    st.metric("Present", regular_present)
                st.metric("Percentage", f"{regular_percentage:.1f}%")

                st.markdown("**Special Classes**")
                special_total = len(special_matches)
                special_present = len(special_matches[special_matches['status'] == 'Present'])
                special_percentage = (special_present / special_total * 100) if special_total > 0 else 0
                loc_col1, loc_col2 = st.columns(2)
                with loc_col1:
                    st.metric("Total", special_total)
                with loc_col2:
                    st.metric("Present", special_present)
                st.metric("Percentage", f"{special_percentage:.1f}%")

                st.markdown("**Combined**")
                total_classes = len(exact_matches)
                total_present = len(exact_matches[exact_matches['status'] == 'Present'])
                total_percentage = (total_present / total_classes * 100) if total_classes > 0 else 0
                loc_col1, loc_col2 = st.columns(2)
                with loc_col1:
                    st.metric("Total Classes", total_classes)
                with loc_col2:
                    st.metric("Present Days", total_present)
                st.metric("Percentage", f"{total_percentage:.1f}%")

            # Show attendance trend
            st.divider()
            st.subheader("Attendance History")
            attendance_history = exact_matches.sort_values('date')
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

    if date_filter:
        filtered_df = filtered_df[filtered_df['date'] == date_filter]
    
    if not filtered_df.empty:
        st.divider()
        st.subheader("Attendance Records")
        st.dataframe(filtered_df)
        
        # Download filtered data
        st.download_button(
            label="Download Records",
            data=filtered_df.to_csv(index=False),
            file_name=f'attendance_export_{date.today()}.csv',
            mime='text/csv'
        )
    else:
        st.info("No records found")
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
