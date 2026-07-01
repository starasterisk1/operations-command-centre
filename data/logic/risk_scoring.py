def calculate_risk(row):
    score = 0

    if row["revenue_change"] < -5:
        score += 2

    if row["staffing_level"] < 80:
        score += 2

    if row["complaints"] >= 5:
        score += 2

    if row["compliance_overdue"] > 0:
        score += 2

    if row["client_satisfaction"] < 85:
        score += 1

    if row["manager_vacancy"] == "Yes":
        score += 2

    if score >= 7:
        level = "High"
    elif score >= 4:
        level = "Medium"
    else:
        level = "Low"

    return score, level
