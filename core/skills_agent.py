import random
import time

class SkillsAgent:
    def __init__(self):
        self.cert_db = {
            "CCNA": {"issuer": "Cisco", "badge": "🛡️", "value": 0.9},
            "CEH": {"issuer": "EC-Council", "badge": "🔓", "value": 0.95},
            "Python Pro": {"issuer": "Credly", "badge": "🐍", "value": 0.85},
            "Data Science": {"issuer": "LASUSTECH", "badge": "🎓", "value": 0.8}
        }
        self.job_market = [
            {"role": "Cyber Security Analyst", "company": "Interswitch", "req": ["CCNA", "CEH"], "salary": "₦450k"},
            {"role": "Network Engineer", "company": "MTN Nigeria", "req": ["CCNA"], "salary": "₦300k"},
            {"role": "AI Python Dev", "company": "Omnix Labs", "req": ["Python Pro"], "salary": "₦600k"},
            {"role": "Data Entry", "company": "Lagos State Govt", "req": [], "salary": "₦150k"}
        ]

    def verify_identity(self, nin_id):
        time.sleep(1.5)
        if len(str(nin_id)) != 11: return None
        return {"name": "Verified Citizen", "status": "VALID", "academic_record": "LASUSTECH (200L Math)"}

    def fetch_certificates(self, nin_id):
        found_certs = []
        keys = list(self.cert_db.keys())
        random.shuffle(keys)
        for k in keys[:3]:
            cert = self.cert_db[k]
            found_certs.append({"name": k, "issuer": cert['issuer'], "badge": cert['badge'], "score": cert['value']})
        return found_certs

    def match_jobs(self, user_certs):
        matches = []
        user_skills = [c['name'] for c in user_certs]
        for job in self.job_market:
            reqs = job['req']
            if not reqs: match_score = 40
            else:
                overlap = set(user_skills).intersection(reqs)
                match_score = int((len(overlap) / len(reqs)) * 100)
            if match_score > 0:
                matches.append({"role": job['role'], "company": job['company'], "salary": job['salary'], "match": match_score})
        return sorted(matches, key=lambda x: x['match'], reverse=True)
