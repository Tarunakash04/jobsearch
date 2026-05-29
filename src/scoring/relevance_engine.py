from src.scoring.job_classifier import JobClassifier


class RelevanceEngine:

    def __init__(self):
        self.classifier = JobClassifier()

    def score(self, job):

        title = (job.title or "").lower()

        domain = self.classifier.classify_domain(title)
        seniority = self.classifier.classify_seniority(title)

        score = 0
        reasons = []

        # -------------------------------------------------
        # DOMAIN SCORE
        # -------------------------------------------------

        if domain == "CLOUD_CORE":
            score += 6
            reasons.append("+6 cloud core")

        elif domain == "PLATFORM":
            score += 5
            reasons.append("+5 platform")

        elif domain == "ENGINEERING":
            score += 4
            reasons.append("+4 engineering")

        elif domain == "LEADERSHIP":
            score += 2
            reasons.append("+2 engineering leadership")

        elif domain == "NOISE":
            score -= 10
            reasons.append("-10 noise role")

        else:
            score -= 2
            reasons.append("-2 unknown")

        # -------------------------------------------------
        # SENIORITY
        # -------------------------------------------------

        if seniority == "FRESHER":
            score += 3
            reasons.append("+3 fresher")

        elif seniority == "SENIOR":
            score += 1
            reasons.append("+1 senior")

        elif seniority == "MANAGER":

            if domain in ["CLOUD_CORE", "PLATFORM"]:
                score += 1
                reasons.append("+1 infra manager")
            else:
                score -= 3
                reasons.append("-3 manager penalty")

        elif seniority == "STAFF":
            score -= 2
            reasons.append("-2 staff")

        # -------------------------------------------------
        # SIGNAL BOOSTERS
        # -------------------------------------------------

        signals = {
            "aws": 3,
            "azure": 3,
            "gcp": 3,
            "cloud": 2,
            "devops": 3,
            "sre": 4,
            "linux": 2,
            "kubernetes": 3,
            "docker": 2,
            "terraform": 3,
            "platform": 2,
            "infrastructure": 2,
            "backend": 1,
            "java": 1,
            "python": 1
        }

        for k, v in signals.items():
            if k in title:
                score += v
                reasons.append(f"+{v} {k}")

        # -------------------------------------------------
        # FINAL BOUNDING
        # -------------------------------------------------

        score = max(min(score, 10), -10)

        return {
            "score": score,
            "domain": domain,
            "seniority": seniority,
            "reasons": reasons
        }