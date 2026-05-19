from src.scoring.job_classifier import JobClassifier


class RelevanceEngine:

    def __init__(self):
        self.classifier = JobClassifier()

    def score(self, job):

        title = job.title.lower()

        domain = self.classifier.classify_domain(title)
        seniority = self.classifier.classify_seniority(title)

        score = 0
        reasons = []

        # ----------------------------
        # 1. DOMAIN SCORE (CORE INTENT)
        # ----------------------------

        if domain == "CLOUD_CORE":
            score += 6
            reasons.append("+6 cloud core domain")

        elif domain == "ENGINEERING":
            score += 4
            reasons.append("+4 engineering domain")

        elif domain == "PLATFORM":
            score += 3
            reasons.append("+3 platform domain")

        elif domain == "UNKNOWN":
            score -= 2
            reasons.append("-2 unknown domain")

        elif domain == "NOISE":
            score -= 10
            reasons.append("-10 noise domain")
        
        elif domain == "LEADERSHIP":
            score += 3
            reasons.append("+3 leadership engineering role")

        # ----------------------------
        # 2. SENIORITY SCORE (CRITICAL FIX)
        # ----------------------------

        if seniority == "FRESHER":
            score += 3
            reasons.append("+3 fresher boost")

        elif seniority == "SENIOR":
            score += 0
            reasons.append("+0 senior neutral")

        elif seniority == "MANAGER":
            if domain == "CLOUD_CORE":
                score += 1   # allow infra managers
                reasons.append("+1 allowed cloud leadership")
            else:
                score -= 3
                reasons.append("-3 non-cloud manager penalty")

        elif seniority == "STAFF":
            score -= 3
            reasons.append("-3 staff penalty")

        # ----------------------------
        # 3. SIGNAL BOOSTERS
        # ----------------------------

        signals = {
            "aws": 3,
            "cloud": 2,
            "devops": 3,
            "sre": 4,
            "security": 3,
            "linux": 2,
            "kubernetes": 3,
            "infra": 1,
            "platform": 1
        }

        for k, v in signals.items():
            if k in title:
                score += v
                reasons.append(f"+{v} {k}")

        # ----------------------------
        # FINAL BOUNDING
        # ----------------------------

        if score < 1:
            score = 1
        elif score > 10:
            score = 10

        return {
            "score": score,
            "domain": domain,
            "seniority": seniority,
            "reasons": reasons
        }