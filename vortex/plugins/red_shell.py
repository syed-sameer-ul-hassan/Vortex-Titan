import subprocess
from .base import BasePlugin

class RedShell(BasePlugin):
    def run(self, args):
        cmd = args['cmd']
        try:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return {"status": "success", "out": res.stdout.strip()}
        except Exception as e:
            return {"status": "error", "err": str(e)}
