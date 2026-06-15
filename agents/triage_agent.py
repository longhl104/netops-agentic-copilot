class TriageAgent:
    def process_log(self, network_log: dict) -> dict:
        """
        Receives the raw network log JSON and categorizes the severity and type of issue.
        """
        # Placeholder for actual AI logic
        print(f"Triage Agent processing log: {network_log}")
        severity = "high" if "down" in network_log.get("description", "").lower() else "medium"
        issue_type = "Routing Issue" if "bgp" in network_log.get("description", "").lower() else "General Network Issue"
        return {"severity": severity, "issue_type": issue_type, "original_log": network_log}
