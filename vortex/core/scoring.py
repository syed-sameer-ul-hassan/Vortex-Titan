class ScoringEngine:
    @staticmethod
    def calculate(red_ts, blue_ts, detection_quality):
        delta = (blue_ts - red_ts).total_seconds()
        ttd_score = max(100 - (abs(delta) * 0.5), 0)

        fidelity = 0
        if detection_quality.get('detected'):
            fidelity += 20
            if 'src_ip' in detection_quality: fidelity += 20
            if 'user' in detection_quality: fidelity += 20
            if 'process' in detection_quality: fidelity += 20
        
        return {
            "total": (ttd_score + fidelity) / 2,
            "ttd_score": ttd_score,
            "fidelity": fidelity
        }
