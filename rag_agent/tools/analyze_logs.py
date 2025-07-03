import os
import io
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from typing import Optional
import matplotlib.dates as mdates

from google.adk.tools.tool_context import ToolContext


def analyze_logs(
        corpus_name: str,
        tool_context: Optional[ToolContext] = None,
        log_content: Optional[str] = None
) -> dict:
    print("Starting analyze_logs")
    if log_content is not None:
        log_stream = io.StringIO(log_content)
        prefix = corpus_name or "corpus_log"
        print("Log content provided, prefix set to:", prefix)
    else:
        print("No log content provided.")
        return {
            "status": "error",
            "message": "No log content provided.",
            "corpus_name": corpus_name,
        }

    try:
        print("Reading log content into DataFrame...")
        log_df = pd.read_csv(
            log_stream,
            sep='|',
            names=['timestamp', 'level', 'message'],
            parse_dates=['timestamp'],
            engine='python'
        )
        print("DataFrame shape:", log_df.shape)
        if log_df.empty or not {'timestamp', 'level', 'message'}.issubset(log_df.columns):
            print("Log file is empty or has invalid format.")
            return {
                "status": "error",
                "message": "Log file is empty or has invalid format.",
                "corpus_name": corpus_name,
            }

        errors = log_df[log_df['level'] == 'ERROR']
        print("Number of error rows:", errors.shape[0])

        # Error Trends Over Time
        print("Generating error trends plot...")
        error_trends = errors.groupby(errors['timestamp'].dt.hour).size()
        print("Error trends data:", error_trends)
        error_trends_path = f'{prefix}_error_trends.png'
        plt.figure(figsize=(10, 5))
        error_trends.plot(kind='line', marker='o', color='red')
        plt.title('Error Trends by Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Number of Errors')
        plt.grid()
        plt.tight_layout()
        plt.savefig(error_trends_path)
        plt.close()
        print("Saved error trends plot to", error_trends_path)

        # Error Distribution by Type
        print("Extracting error types...")
        log_df['error_type'] = log_df['message'].str.extract(r'(ERROR_\w+)')
        error_distribution = log_df['error_type'].value_counts()
        print("Error distribution data:", error_distribution)
        error_dist_path = f'{prefix}_error_distribution.png'
        plt.figure(figsize=(8, 8))
        error_distribution.plot(kind='pie', autopct='%1.1f%%', startangle=90, colormap='Reds')
        plt.title('Error Distribution by Type')
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(error_dist_path)
        plt.close()
        print("Saved error distribution plot to", error_dist_path)

        # Heatmap of Errors by Day and Hour
        print("Generating error heatmap...")
        log_df['day'] = log_df['timestamp'].dt.day_name()
        log_df['hour'] = log_df['timestamp'].dt.hour
        heatmap_data = log_df[log_df['level'] == 'ERROR'].pivot_table(
            index='day', columns='hour', aggfunc='size', fill_value=0
        )
        print("Heatmap data shape:", heatmap_data.shape)
        heatmap_path = f'{prefix}_error_heatmap.png'
        plt.figure(figsize=(12, 6))
        sns.heatmap(heatmap_data, cmap='Reds', annot=True, fmt='d')
        plt.title('Error Heatmap by Day and Hour')
        plt.xlabel('Hour of Day')
        plt.ylabel('Day of Week')
        plt.tight_layout()
        plt.savefig(heatmap_path)
        plt.close()
        print("Saved heatmap plot to", heatmap_path)

        # Unauthenticated Users Analysis
        print("Analyzing unauthenticated users...")
        unauth_pattern = r'Failed login.*user (.*@.*)'
        unauth_users = log_df['message'].str.extractall(unauth_pattern)[0].value_counts()
        print("Unauthenticated users data:", unauth_users)
        unauth_users_path = f'{prefix}_unauth_users.png'
        plt.figure(figsize=(10, 6))
        unauth_users.plot(kind='bar', color='orange')
        plt.title('Unauthenticated Users')
        plt.xlabel('User')
        plt.ylabel('Number of Failed Logins')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(unauth_users_path)
        plt.close()
        print("Saved unauthenticated users plot to", unauth_users_path)

        # Timeline Analysis (all events)
        print("Generating timeline plot...")
        timeline_path = f'{prefix}_timeline.png'
        plt.figure(figsize=(15, 5))
        plt.plot(log_df['timestamp'], [1] * len(log_df), marker='o', linestyle='', color='blue')
        plt.yticks([])
        plt.xlabel('Time')
        plt.title('Log Event Timeline')
        plt.grid(True)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(timeline_path)
        plt.close()
        print("Saved timeline plot to", timeline_path)

        # Unauthorized Events Timeline
        print("Generating unauthorized events timeline...")
        unauthorized_mask = log_df['message'].str.contains('Blocked login|Login denied', case=False, na=False)
        unauthorized_events = log_df[unauthorized_mask]
        unauthorized_timeline_path = f'{prefix}_unauthorized_timeline.png'
        if not unauthorized_events.empty:
            print("Unauthorized events found:", unauthorized_events.shape[0])
            plt.figure(figsize=(15, 3))
            plt.plot(unauthorized_events['timestamp'], [1]*len(unauthorized_events), 'ro', label='Unauthorized Event')
            for idx, row in unauthorized_events.iterrows():
                plt.text(row['timestamp'], 1.02, row['message'][:40], rotation=45, fontsize=8, ha='left', va='bottom')
            plt.yticks([])
            plt.xlabel('Time')
            plt.title('Unauthorized Events Timeline')
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M:%S'))
            plt.grid(True, axis='x')
            plt.tight_layout()
            plt.savefig(unauthorized_timeline_path)
            plt.close()
            print("Saved unauthorized events timeline plot to", unauthorized_timeline_path)
        else:
            print("No unauthorized events found.")
            unauthorized_timeline_path = None

        # Collect plot paths
        plots = {
            "error_trends": error_trends_path,
            "error_distribution": error_dist_path,
            "error_heatmap": heatmap_path,
            "unauth_users": unauth_users_path,
            "timeline": timeline_path
        }
        if unauthorized_timeline_path:
            plots["unauthorized_timeline"] = unauthorized_timeline_path

        print("All plots generated successfully.")
        return {
            "status": "success",
            "summary": {
                "total_errors": int(errors.shape[0]),
                "error_types": error_distribution.to_dict(),
                "plots": plots
            },
            "corpus_name": corpus_name,
        }
    except Exception as e:
        print("Exception occurred:", str(e))
        return {
            "status": "error",
            "message": f"Exception occurred: {str(e)}",
            "corpus_name": corpus_name,
        }