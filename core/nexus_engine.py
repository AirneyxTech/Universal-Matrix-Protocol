import pandas as pd
import requests

class NexusEngine:
    def __init__(self):
        # Fallback Jobs (if API fails)
        self.jobs_db = [
            {"title": "Python Intern", "company": "Bincom", "skills": ["Python", "Git", "Django"], "url": "https://bincom.net"},
            {"title": "Data Analyst", "company": "Kuda Bank", "skills": ["Excel", "SQL", "PowerBI"], "url": "https://kuda.com"}
        ]

    def fetch_live_jobs(self):
        """Connects to Remotive API for Real-Time Jobs"""
        try:
            url = "https://remotive.com/api/remote-jobs?search=developer&limit=15"
            resp = requests.get(url, timeout=3)
            data = resp.json()
            live_jobs = []
            if 'jobs' in data:
                for j in data['jobs']:
                    # Extract skills keywords from description
                    desc = j['description'].lower()
                    detected = [s for s in ['python', 'react', 'sql', 'excel', 'node', 'design'] if s in desc]
                    live_jobs.append({
                        "title": j['title'],
                        "company": j['company_name'],
                        "skills": detected if detected else ["General Tech"],
                        "url": j['url']
                    })
            return live_jobs if live_jobs else self.jobs_db
        except:
            return self.jobs_db

    def analyze_student_data(self, df):
        """
        SMART PARSER: Handles Google Form CSV Headers automatically
        """
        # 1. Clean Headers (Find the columns by keyword)
        name_col = next((c for c in df.columns if 'Name' in c), None)
        id_col = next((c for c in df.columns if 'Matric' in c or 'ID' in c), None)
        skill_col = next((c for c in df.columns if 'Skills' in c), None)
        level_col = next((c for c in df.columns if 'Level' in c), None)

        if not (name_col and skill_col):
            return {"error": "Could not detect 'Name' or 'Skills' columns. Check CSV."}

        # 2. Get Market Data
        market = self.fetch_live_jobs()
        report = []

        # 3. Match Logic
        for _, row in df.iterrows():
            # Parse Skills (Google Forms uses comma separation)
            raw_skills = str(row[skill_col])
            student_skills = [s.strip().lower() for s in raw_skills.split(',')]
            
            best_job = "None"
            max_score = 0
            gap = []

            for job in market:
                reqs = set([s.lower() for s in job['skills']])
                user = set(student_skills)
                if not reqs: continue
                
                match = len(user.intersection(reqs))
                score = int((match / len(reqs)) * 100)
                
                if score > max_score:
                    max_score = score
                    best_job = f"{job['title']} @ {job['company']}"
                    gap = list(reqs.difference(user))

            status = "HIRE" if max_score >= 60 else "TRAIN"
            action = f"Apply Now" if status == "HIRE" else f"Learn {gap[0].title() if gap else 'More Skills'}"

            report.append({
                "Name": row[name_col],
                "Level": row[level_col] if level_col else "N/A",
                "Best Match": best_job,
                "Score": f"{max_score}%",
                "Status": status,
                "Action": action
            })

        return pd.DataFrame(report)
