import sqlite3
import json
import datetime

class DatabaseManager:
    def __init__(self, db_file_path):
        self.db_file = db_file_path
        self._setup_database()

    def _setup_database(self):
        """Creates the necessary tables if they don't exist."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            benchmark_function TEXT NOT NULL,
            epochs INTEGER NOT NULL,
            config_json TEXT NOT NULL
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            result_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER NOT NULL,
            epoch INTEGER NOT NULL,
            best_fitness REAL NOT NULL,
            avg_fitness REAL NOT NULL,
            std_dev REAL NOT NULL,
            FOREIGN KEY (run_id) REFERENCES runs (run_id)
        )
        """)
        conn.commit()
        conn.close()

    def save_run_results(self, config, epochs, func_name, history):
        """Saves a complete run (config + all epoch results) to the database."""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        run_time = datetime.datetime.now().isoformat()
        config_to_save = config.copy()
        config_to_save['bounds'] = list(config_to_save['bounds'])
        config_str = json.dumps(config_to_save, indent=2)
        
        cursor.execute(
            "INSERT INTO runs (timestamp, benchmark_function, epochs, config_json) VALUES (?, ?, ?, ?)",
            (run_time, func_name, epochs, config_str)
        )
        run_id = cursor.lastrowid

        if not history or not isinstance(history, list) or not isinstance(history[0], dict):
            raise TypeError("History format is incorrect. Expected a list of dictionaries.")

        results_data = [
            (run_id, h['epoch'], h['best_fitness'], h['average_fitness'], h['std_fitness'])
            for h in history
        ]
        
        cursor.executemany(
            "INSERT INTO results (run_id, epoch, best_fitness, avg_fitness, std_dev) VALUES (?, ?, ?, ?, ?)",
            results_data
        )

        conn.commit()
        conn.close()
        print(f"Results successfully saved to {self.db_file} (Run ID: {run_id})")
        