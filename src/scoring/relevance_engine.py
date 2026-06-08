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
            score += 7
            reasons.append("+7 cloud core")

        elif domain == "PLATFORM":
            score += 5
            reasons.append("+5 platform")

        elif domain == "ENGINEERING":
            score += 3
            reasons.append("+3 engineering")

        elif domain == "LEADERSHIP":
            score += 1
            reasons.append("+1 leadership")

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
            score += 4
            reasons.append("+4 fresher")

        elif seniority == "MID":
            score += 2
            reasons.append("+2 mid-level")

        elif seniority == "SENIOR":
            score -= 1
            reasons.append("-1 senior")

        elif seniority == "MANAGER":

            if domain in ["CLOUD_CORE", "PLATFORM"]:
                score -= 3
                reasons.append("-3 infra manager")
            else:
                score -= 6
                reasons.append("-6 manager")

        elif seniority == "STAFF":
            score -= 4
            reasons.append("-4 staff")

        elif seniority == "EXECUTIVE":
            score -= 10
            reasons.append("-10 executive")

        # -------------------------------------------------
        # SIGNAL BOOSTERS
        # -------------------------------------------------

        signals = {

            # Primary targets
            "aws": 5,
            "azure": 5,
            "gcp": 5,

            # Cloud / Platform
            "cloud": 4,
            "platform": 3,
            "infrastructure": 3,
            "infra": 3,

            # DevOps / SRE
            "devops": 5,
            "sre": 5,
            "site reliability": 5,

            # Core tooling
            "terraform": 4,
            "kubernetes": 4,
            "docker": 3,
            "linux": 3,
            "ansible": 3,

            # Security
            "security": 2,
            "splunk": 2,

            # Engineering
            "backend": 2,
            "python": 2,
            "java": 1,

            # Data
            "data engineer": 2,

            "prometheus": 3,
            "grafana": 3,
            "jenkins": 3,

            "helm": 3,
            "argocd": 4,

            "eks": 4,
            "ecs": 3,
            "lambda": 4,

            "terraform": 4,
            "cloudformation": 4,

            "observability": 3,
            "monitoring": 3,

            "networking": 2,
            "network": 2,

            "identity": 2,
            "iam": 3,

            "containers": 3,
            "container": 3,
            "mainframe": -2,
            "zos": -2,
            "db2": -2,
            "cobol": -3,

            "flutter": -3,
            "android": -3,
            "ios": -3,

            "react native": -3,

            "business analyst": -10,
            "product owner": -4,
            "scrum master": -4,

            "workday": -4,
            "sql": 2,
            "spark": 3,
            "hadoop": 2,
            "databricks": 4,
            "airflow": 4,
            "kafka": 4,
        }

        for keyword, value in signals.items():

            if keyword in title:
                score += value
                reasons.append(f"+{value} {keyword}")

        # -------------------------------------------------
        # NEGATIVE SIGNALS
        # -------------------------------------------------

        penalties = {

            "flutter": -3,
            "ios": -3,
            "android": -3,
            "react native": -3,
            "ui": -2,
            "ux": -2,
            "frontend": -2,

            "business analyst": -10,
            "data scientist": -4,
            "product owner": -4,
            "scrum master": -4,

            "workday": -4,
            "sap": -2
        }

        for keyword, value in penalties.items():

            if keyword in title:
                score += value
                reasons.append(f"{value} {keyword}")

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