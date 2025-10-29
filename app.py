import streamlit as st
import pandas as pd
import os
from datetime import datetime, date
from config import ADMIN_CREDENTIALS
from events import load_events, add_event
from user_management import (
    add_active_user,
    remove_active_user,
    cleanup_inactive_users,
    update_user_activity,
    load_active_users
)
import time

# Initialize session state
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'last_cleanup' not in st.session_state:
    st.session_state.last_cleanup = time.time()

# File paths
DATA_FILE = "attendance.csv"
STUDENT_INFO_FILE = "student_info.csv"
EVENTS_FILE = "events.csv"

# Load attendance data
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date']).dt.date
else:
    df = pd.DataFrame(columns=['name', 'date', 'status'])


# Add at the start of your script, after loading the CSV
if 'class_type' not in df.columns:
    df['class_type'] = 'Regular'  # Set default for existing records
    df.to_csv(DATA_FILE, index=False)


# Load or create student info data
if os.path.exists(STUDENT_INFO_FILE):
    student_info_df = pd.read_csv(STUDENT_INFO_FILE)
else:
    student_info_df = pd.DataFrame(columns=['name', 'bio', 'join_date', 'contact'])

# Add after loading other DataFrames
events_df = load_events()

# Modify the login function
def login():
    st.title("Zoho Dance Crew Attendance Register - Login")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        is_admin_attempt = st.checkbox("Login as Admin")
        
        if is_admin_attempt:
            admin_name = st.text_input("Admin Username")
            admin_password = st.text_input("Password", type="password")
            
            if st.button("Login"):
                if admin_name in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[admin_name] == admin_password:
                    st.session_state.is_admin = True
                    st.session_state.current_user = f"admin:{admin_name}"
                    add_active_user(admin_name, is_admin=True)
                    st.success("Logged in as Admin")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
        else:
            viewer_name = st.text_input("Enter your name to view records")
            if st.button("Enter"):
                if viewer_name:
                    st.session_state.current_user = f"viewer:{viewer_name}"
                    add_active_user(viewer_name)
                    st.success(f"Welcome, {viewer_name}")
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

# Create tabs based on user role
if st.session_state.is_admin:
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Mark Attendance", "Mark/Edit Past Attendance", "View Records", "Statistics", "Events"])
else:
    tab3, tab4, tab5 = st.tabs(["View Records", "Statistics", "Events"])

# Get today's date
today = date.today()

# Only show attendance marking tabs for admin
if st.session_state.is_admin:
    with tab1:
        # Get list of unique names from existing records
        existing_names = sorted(df['name'].unique()) if not df.empty else []
    
        # Add new student option
        new_name = st.text_input("New to ZDC Fam?! Enroll name")
        if new_name and new_name not in existing_names:
            existing_names.append(new_name)
            st.success(f"Added new ZDC Member: {new_name}")

        # Select single student attendance
        # st.subheader("Mark Attendance")
        # student_name = st.selectbox("Select student", existing_names if existing_names else ['No students yet'])
    
        # # Mark attendance
        # status = st.radio("Attendance Status", ['Present', 'Absent'])
    
        # if st.button("Mark Attendance"):
        #     if student_name != 'No students yet':
        #         # Check if attendance already marked for today
        #         if not df.empty and len(df[(df['name'] == student_name) & (df['date'] == today)]) > 0:
        #             st.error(f"Attendance for {student_name} already marked for today!")
        #         else:
        #             new_data = {
        #                 'name': student_name,
        #                 'date': today,
        #                 'status': status
        #             }
        #             df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        #             df.to_csv(DATA_FILE, index=False)
        #             st.success(f"Attendance marked for {student_name}")
        #         pass
        
        # Add a divider
        st.divider()

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
                        df = pd.concat([df, pd.DataFrame(new_records)], ignore_index=True)
                        df.to_csv(DATA_FILE, index=False)
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
                # Check if attendance exists for selected date
                mask = (df['name'] == student_name) & (df['date'] == selected_date)
                if not df.empty and len(df[mask]) > 0:
                    # Update existing record
                    df.loc[mask, 'status'] = status
                    df.loc[mask, 'class_type'] = class_type
                    if class_type == "Event/Competition":
                        df.loc[mask, 'event'] = selected_event
                    df.to_csv(DATA_FILE, index=False)
                    st.success(f"Attendance updated for {student_name} on {selected_date}")
                else:
                    # Add new record
                    new_data = {
                        'name': student_name,
                        'date': selected_date,
                        'status': status,
                        'class_type': class_type,
                        'event': selected_event if class_type == "Event/Competition" else None
                    }
                    df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                    df.to_csv(DATA_FILE, index=False)
                    st.success(f"Attendance marked for {student_name} on {selected_date}")

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
                            student_info_df.to_csv(STUDENT_INFO_FILE, index=False)
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

        # Display statistics
        # st.write(f"Total Class Days: {total_days}")
        # st.write(f"Regular Classes: {total_regular_days}")
        # st.write(f"Special Classes: {total_special_days}")
        # st.write(f"Event Classes: {total_event_days}")

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

# # Update viewer count periodically
# if st.session_state.current_user and not st.session_state.current_user.startswith('admin:'):
#     viewer_name = st.session_state.current_user.split(':')[1]
#     if viewer_name not in st.session_state.logged_in_users:
#         st.session_state.logged_in_users.add(viewer_name)