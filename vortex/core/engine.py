import logging
import uuid
import yaml
import time
from datetime import datetime
from vortex.core.db import DatabaseManager
from vortex.core.scoring import ScoringEngine
from vortex.core.safety import SafetyMonitor
from vortex.core.decision_matrix import DecisionMatrix

from vortex.plugins.red_shell import RedShell
from vortex.plugins.blue_log import BlueLog
from vortex.plugins.red_sim_exploit import RedSimExploit

class TitanEngine:
    def __init__(self, config, inventory, safety_policy):
        self.logger = logging.getLogger("VORTEX")
        self.cfg = config
        self.inventory = inventory
        self.db = DatabaseManager(config['system']['db_path'])
        self.safety = SafetyMonitor(config, safety_policy)
        
        self.plugins = {
            'red_shell': RedShell(),
            'blue_log': BlueLog(),
            'red_sim_exploit': RedSimExploit()
        }

    def run_campaign(self, scenario_path):
        with open(scenario_path) as f:
            profile = yaml.safe_load(f)

        campaign_id = str(uuid.uuid4())
        self.db.start_campaign(campaign_id, profile['meta']['name'], self.cfg['system']['environment'])
        self.logger.info(f"STARTING CAMPAIGN: {campaign_id}")

        current_step_id = profile['entry_point']
        steps_map = {s['id']: s for s in profile['steps']}

        while current_step_id:
            step = steps_map.get(current_step_id)
            if not step: break

            self.logger.info(f"EXECUTING STEP: {step['id']}")
            
            targets = self._resolve_targets(step.get('target_role', 'web_servers'))

            for target in targets:
                # 1. Red
                red_res = self._exec_red(step, target)
                red_ts = datetime.now()

                # 2. Blue
                time.sleep(step.get('delay', 1))
                blue_res = self._exec_blue(step, target)
                blue_ts = datetime.now()

                # 3. Score
                score = ScoringEngine.calculate(red_ts, blue_ts, blue_res)
                
                # 4. Log
                self.db.log_event(
                    campaign_id, step['id'], target['host'], red_res, blue_res, score
                )

                # 5. Branch
                if blue_res.get('detected'):
                    current_step_id = step.get('next_if_detected')
                else:
                    current_step_id = step.get('next_if_missed')
                
                if current_step_id == 'AUTO':
                    decision = DecisionMatrix.decide(blue_res)
                    self.logger.info(f"Auto-Decision: {decision}")
                    # In this demo, AUTO breaks the loop
                    current_step_id = None
                
                break 

    def _resolve_targets(self, role):
        return self.inventory['groups'].get(role, [])

    def _exec_red(self, step, target):
        plugin = self.plugins[step['red']['plugin']]
        args = step['red']['args']
        if 'cmd' in args:
            self.safety.check_command(args['cmd'])
        return plugin.run(args)

    def _exec_blue(self, step, target):
        plugin = self.plugins[step['blue']['plugin']]
        return plugin.run(step['blue']['args'])
