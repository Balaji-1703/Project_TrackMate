import pandas as pd
import os

EVENTS_FILE = "events.csv"

def load_events():
    if os.path.exists(EVENTS_FILE):
        return pd.read_csv(EVENTS_FILE)
    return pd.DataFrame(columns=['event_name', 'start_date', 'end_date', 'description', 'status'])

def add_event(event_name, start_date, end_date, description):
    events_df = load_events()
    new_event = pd.DataFrame([{
        'event_name': event_name,
        'start_date': start_date,
        'end_date': end_date,
        'description': description,
        'status': 'Active'
    }])
    events_df = pd.concat([events_df, new_event], ignore_index=True)
    events_df.to_csv(EVENTS_FILE, index=False)
    return events_df