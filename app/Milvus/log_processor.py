"""
Module for loading and processing log data.
"""
import json
import pandas as pd
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm
from app.Milvus.embedder import LogEmbedder
from app.Milvus.Milvus import MilvusStorage 

load_dotenv()


def detect_log_format(filepath):
    """
    Detect the format of the log file based on its extension.
    """
    ext = os.path.splitext(filepath)[-1].lower()
    if ext in ['.csv']:
        return "csv"
    if ext in ['.json']:
        return "json"
    return "txt"


def load_and_normalize_logs(filepath):
    """
    Load and normalize logs from various formats to match the 8-field CSV structure.
    Expected fields: id, log_message, timestamp, source, severity, anomaly_flag, anomaly_reason, target_label
    """
    fmt = detect_log_format(filepath)
    
    if fmt == "csv":
        df = pd.read_csv(filepath)
    elif fmt == "json":
        with open(filepath, 'r', encoding="utf-8") as f:
            logs_data = json.load(f)
        if isinstance(logs_data, dict):
            df = pd.DataFrame.from_dict(logs_data, orient="index")
        else:
            df = pd.DataFrame(logs_data)
    else:  # txt
        logs = []
        with open(filepath, 'r', encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:
                    logs.append({
                        "id": line_num,
                        "log_message": line,
                        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "source": "unknown",
                        "severity": "Information",
                        "anomaly_flag": False,
                        "anomaly_reason": "",
                        "target_label": "normal"
                    })
        df = pd.DataFrame(logs)

    # Normalize columns to match the expected 8-field structure
    expected_columns = ["id", "log_message", "timestamp", "source", "severity", "anomaly_flag", "anomaly_reason", "target_label"]
    
    # Map existing columns to expected names
    column_mapping = {
        # log_message variations
        "message": "log_message",
        "msg": "log_message", 
        "text": "log_message",
        "content": "log_message",
        "log": "log_message",
        
        # timestamp variations
        "time": "timestamp",
        "datetime": "timestamp",
        "date": "timestamp",
        "created_at": "timestamp",
        "log_time": "timestamp",
        
        # source variations
        "logger": "source",
        "component": "source",
        "service": "source",
        "module": "source",
        
        # severity variations
        "level": "severity",
        "loglevel": "severity",
        "log_level": "severity"
    }
    
    # Apply column mapping
    for old_col, new_col in column_mapping.items():
        if old_col in df.columns and new_col not in df.columns:
            df[new_col] = df[old_col]
    
    # Ensure all expected columns exist with default values
    for col in expected_columns:
        if col not in df.columns:
            if col == "id":
                df[col] = range(1, len(df) + 1)
            elif col == "log_message":
                # Try to find any text column
                text_col = next((c for c in df.columns if df[c].dtype == 'object'), None)
                if text_col:
                    df[col] = df[text_col]
                else:
                    df[col] = "Unknown log message"
            elif col == "timestamp":
                df[col] = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            elif col == "source":
                df[col] = "unknown"
            elif col == "severity":
                df[col] = "Information"
            elif col == "anomaly_flag":
                df[col] = False
            elif col == "anomaly_reason":
                df[col] = ""
            elif col == "target_label":
                df[col] = "normal"
    
    # Clean and validate data
    df = df[df['log_message'].notna() & (df['log_message'] != '')]
    
    # Ensure proper data types
    df['id'] = pd.to_numeric(df['id'], errors='coerce').fillna(0).astype(int)
    df['log_message'] = df['log_message'].astype(str)
    df['timestamp'] = df['timestamp'].astype(str)
    df['source'] = df['source'].astype(str)
    df['severity'] = df['severity'].astype(str)
    df['anomaly_flag'] = df['anomaly_flag'].astype(bool)
    df['anomaly_reason'] = df['anomaly_reason'].astype(str)
    df['target_label'] = df['target_label'].astype(str)
    
    # Select only the expected columns in the correct order
    df = df[expected_columns]
    df = df.reset_index(drop=True)
    
    print(f"Loaded and normalized {len(df)} log records with {len(df.columns)} fields.")
    return df


def process_logs_with_embeddings(filepath, batch_size=1000):
    """
    Complete pipeline to load logs, generate embeddings, and store in Milvus.
    """
    print(f"Processing log file: {filepath}")
    
    # Load and normalize logs
    df = load_and_normalize_logs(filepath)
    print(f"Loaded {len(df)} log records")
    print("Sample data:")
    print(df.head())
    
    # Generate embeddings
    print("\nGenerating embeddings...")
    embedder = LogEmbedder()
    df_with_embeddings = embedder.generate_embeddings_for_logs(df, text_column="log_message")
    
    if df_with_embeddings is None:
        print("Failed to generate embeddings")
        return False
    
    # Store in Milvus
    print("\nStoring in Milvus...")
    storage = MilvusStorage()
    
    # Process in batches
    n = len(df_with_embeddings)
    success_count = 0
    
    for start in tqdm(range(0, n, batch_size), desc="Storing in Milvus"):
        end = min(start + batch_size, n)
        batch = df_with_embeddings.iloc[start:end]
        
        if storage.store_logs(batch):
            success_count += len(batch)
        else:
            print(f"Failed to store batch {start}-{end}")
    
    print(f"\nProcessing complete. Successfully stored {success_count}/{n} records.")
    storage.disconnect()
    return success_count == n


if __name__ == "__main__":
    # Use the cleaned logs file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(base_dir, "..", "data", "cleanlogs.csv")
    filepath = os.path.abspath(filepath)
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        print("Please ensure the cleaned_logs.csv file is in the correct location.")
        sys.exit(1)
    
    success = process_logs_with_embeddings(filepath)
    if success:
        print("Log processing completed successfully!")
    else:
        print("Log processing failed!")

