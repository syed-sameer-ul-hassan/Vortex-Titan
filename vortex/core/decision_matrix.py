class DecisionMatrix:
    @staticmethod
    def decide(blue_outcome):
        if not blue_outcome.get('detected'):
            return "escalate_privileges"
        
        evidence = blue_outcome.get('evidence', '').lower()
        if "firewall" in evidence or "block" in evidence:
            return "switch_transport_https"
        elif "edr" in evidence or "antivirus" in evidence:
            return "pause_execution"
            
        return "abort_campaign"
