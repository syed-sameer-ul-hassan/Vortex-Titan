import yaml
import logging
import argparse
import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from vortex.core.engine import TitanEngine
from vortex.reporting.dashboard_gen import generate_dashboard

# --- LOGO ADDED HERE ---
BANNER = r"""
░██╗   ░██╗░██████╗ ░██████╗ ████████╗████████╗██╗  ██╗
░██║   ░██║██╔═══██╗██╔══██╗╚══██╔══╝╚══██╔══╝╚██╗██╔╝
░██║   ░██║██║   ██║██████╔╝   ██║      ██║    ╚███╔╝ 
░╚██╗ ██╔╝██║   ██║██╔══██╗   ██║      ██║    ██╔██╗ 
░░╚████╔╝ ╚██████╔╝██║  ██║   ██║      ████████╗██║╚██╗
░░░╚═══╝░░ ╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░░░░╚═══════╝╚═╝░╚═╝
         [ JOINT OPERATIONS PLATFORM ]
"""

def main():
    # --- PRINT LOGO START ---
    print(BANNER)
    # --- PRINT LOGO END ---

    parser = argparse.ArgumentParser(description="VORTEX TITAN Enterprise CLI")
    parser.add_argument("--scenario", default="scenarios/demo.yaml", help="Path to scenario file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    
    try:
        with open('config/vortex.yaml') as f: cfg = yaml.safe_load(f)
        with open('config/inventory.yaml') as f: inv = yaml.safe_load(f)
        with open('config/safety.yaml') as f: safe = yaml.safe_load(f)
    except FileNotFoundError as e:
        print(f"Config Error: {e}")
        sys.exit(1)
    
    engine = TitanEngine(cfg, inv, safe)
    
    try:
        engine.run_campaign(args.scenario)
    except Exception as e:
        logging.error(f"Campaign Failed: {e}")
    
    generate_dashboard(cfg['system']['db_path'], cfg['reporting']['dashboard_path'])

if __name__ == "__main__":
    main()