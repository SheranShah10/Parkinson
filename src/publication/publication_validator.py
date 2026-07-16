class PublicationValidator:
    @staticmethod
    def audit(leaderboard_paths):
        # Strictly ensures we only publish what physically exists
        report = []
        for path in leaderboard_paths:
            import os
            if os.path.exists(path):
                report.append(f"Valid: {path}")
            else:
                report.append(f"Missing (Will skip gracefully): {path}")
        return report
