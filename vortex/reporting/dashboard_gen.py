import sqlite3
import pandas as pd
import os

def generate_dashboard(db_path, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query("SELECT * FROM events", conn)
    except:
        print("No events found to report.")
        return

    html = f"""
    <html>
    <head><title>VORTEX TITAN Dashboard</title>
    <style>
        body {{ font-family: sans-serif; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #333; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
    </head>
    <body>
        <h1>VORTEX TITAN: Operations Report</h1>
        <h3>Total Events: {len(df)}</h3>
        <h3>Detection Rate: {df['blue_detected'].mean() * 100:.1f}%</h3>
        {df.to_html(classes='table', index=False)}
    </body>
    </html>
    """
    
    with open(out_path, 'w') as f:
        f.write(html)
    print(f"[*] Dashboard generated at {out_path}")
