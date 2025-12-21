import sqlite3
import logging
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._init_schema()

    def _init_schema(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                name TEXT,
                start_time TEXT,
                environment TEXT
            );
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id TEXT,
                step_name TEXT,
                target TEXT,
                red_output TEXT,
                blue_detected BOOLEAN,
                blue_evidence TEXT,
                score_fidelity REAL,
                score_ttd REAL,
                timestamp TEXT,
                FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
            );
        """)
        self.conn.commit()

    def start_campaign(self, campaign_id, name, env):
        self.cursor.execute(
            "INSERT INTO campaigns (id, name, start_time, environment) VALUES (?, ?, ?, ?)",
            (campaign_id, name, datetime.now().isoformat(), env)
        )
        self.conn.commit()

    def log_event(self, campaign_id, step, target, red_res, blue_res, score):
        self.cursor.execute("""
            INSERT INTO events 
            (campaign_id, step_name, target, red_output, blue_detected, blue_evidence, score_fidelity, score_ttd, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            campaign_id, step, target, 
            str(red_res), 
            bool(blue_res.get('detected')), 
            blue_res.get('evidence', ''), 
            score.get('fidelity', 0.0),
            score.get('ttd_score', 0.0),
            datetime.now().isoformat()
        ))
        self.conn.commit()
