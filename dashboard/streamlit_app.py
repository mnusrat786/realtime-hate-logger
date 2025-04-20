import streamlit as st
import pandas as pd
import os

LOG_CSV_PATH = "log.csv"

st.set_page_config(page_title="Hate Speech Logger Dashboard", layout="wide")
st.title(" Real-time Hate Speech Log Viewer")

if not os.path.exists(LOG_CSV_PATH):
    st.warning("No logs found yet. Run main.py first to generate hate speech logs.")
else:
    df = pd.read_csv(LOG_CSV_PATH)
    st.success(f"Loaded {len(df)} logs from CSV.")

    # Format timestamp
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Filters
    col1, col2 = st.columns(2)

    with col1:
        selected_label = st.selectbox("Filter by Target Label", options=["All"] + sorted(df['label'].unique().tolist()))
        if selected_label != "All":
            df = df[df['label'] == selected_label]

    with col2:
        min_conf = st.slider("Minimum Confidence", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        df = df[df['confidence'] >= min_conf]

    # Show logs
    st.dataframe(df.sort_values(by="timestamp", ascending=False), use_container_width=True)

    # Download option
    st.download_button(
        label=" Download Log CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name="filtered_logs.csv",
        mime='text/csv'
    )
