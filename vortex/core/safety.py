class SafetyMonitor:
    def __init__(self, config, policy):
        self.env = config['system']['environment']
        self.policy = policy

    def check_command(self, cmd):
        blocklist = self.policy.get('blocked_lab', [])
        if self.env == 'prod':
            blocklist.extend(self.policy.get('blocked_prod', []))

        for bad in blocklist:
            if bad in cmd:
                raise RuntimeError(f"SAFETY VIOLATION [{self.env}]: Command '{bad}' blocked.")
