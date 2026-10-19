class ReportBuilder:
    @staticmethod
    def format_match_card(index, match):
        home = match["home_team"]
        away = match["away_team"]
        league = match["league"]
        prob = match["prediction"]["probability"]
        h_stats = match["home_stats"]
        a_stats = match["away_stats"]

        return (
            f"⚽ **Match {index} — {league}**\n\n"
            f"🔹 **Rencontre :** {home} vs {away}\n"
            f"🎯 **Pronostic :** Over 1,5 buts\n"
            f"📊 **Probabilité estimée :** {prob}%\n"
            f"📈 **Chiffres clés :**\n"
            f"  - Domicile : {h_stats['over_15_count']}/{h_stats['valid_matches']} Over 1,5\n"
            f"  - Extérieur : {a_stats['over_15_count']}/{a_stats['valid_matches']} Over 1,5\n"
            f"  - Moy. buts : Dom ({h_stats['avg_scored']:.1f}/{h_stats['avg_conceded']:.1f}) | Ext ({a_stats['avg_scored']:.1f}/{a_stats['avg_conceded']:.1f})\n\n"
            f"💡 **Raisons :**\n"
            f"1. Fréquence historique d'Over 1,5 très élevée.\n"
            f"2. Moyennes offensives régulières.\n"
            f"3. Indicateur de buts attendus favorable.\n\n"
            f"⚠️ **Risque :** Aléa du football (carton rouge, manque d'efficacité).\n"
            f"────────────────────────\n"
        )

    @classmethod
    def format_daily_report(cls, date_str, result):
        matches = result["matches"]
        header = f"📋 **Rapport Over 1,5 — {date_str}**\n\n"
        header += f"🔍 Analysés : {result['analyzed']} | ✅ Retenus : {result['retained']} | ❌ Rejetés : {result['rejected']}\n\n"

        if not matches:
          header += "Aucun match ne satisfait pleinement nos critères de fiabilité aujourd'hui."
          return header

        body = ""
        for i, m in enumerate(matches, 1):
            body += cls.format_match_card(i, m)

        return header + body
