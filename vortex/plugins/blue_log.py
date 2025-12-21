import os
from .base import BasePlugin

class BlueLog(BasePlugin):
    def run(self, args):
        path = args.get('path')
        pattern = args.get('pattern')
        
        if not os.path.exists(path):
            return {"detected": False, "evidence": "Log missing"}
            
        with open(path, 'r', errors='ignore') as f:
            if pattern in f.read():
                return {
                    "detected": True, 
                    "evidence": f"Found {pattern}",
                    "src_ip": "127.0.0.1",
                    "user": "root"
                }
        return {"detected": False}
