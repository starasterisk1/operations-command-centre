def generate_recommendations(row):
    recommendations = []

    if row["revenue_change"] < -5:
        recommendations.append("Review revenue decline and identify whether this is linked to pricing, visits, or missed charges.")

    if row["staffing_level"] < 80:
        recommendations.append("Review rota coverage and assess whether staffing is affecting service delivery.")

    if row["complaints"] >= 5:
        recommendations.append("Review complaint themes and identify any repeated client experience issues.")

    if row["compliance_overdue"] > 0:
        recommendations.append("Escalate overdue compliance actions and confirm ownership.")

    if row["client_satisfaction"] < 85:
        recommendations.append("Review client satisfaction feedback and agree local improvement actions.")

    if row["manager_vacancy"] == "Yes":
        recommendations.append("Confirm interim leadership support while the manager vacancy is open.")

    if not recommendations:
        recommendations.append("No immediate intervention required. Continue routine monitoring.")

    return recommendations
