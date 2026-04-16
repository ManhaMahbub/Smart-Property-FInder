def recommend(df, rl):

    df = df.copy()

    df["ml_score"] = df["predicted_price"]

    def get_rl_score(row):
        if hasattr(rl, "score"):
            try:
                return rl.score(row)
            except:
                return 0
        return 0

    df["rl_score"] = df.apply(get_rl_score, axis=1)

    def heuristic(row):
        return (
            row["bedrooms"] * 1000 +
            row["bathrooms"] * 800 -
            row["price"] * 0.001
        )

    df["heuristic"] = df.apply(heuristic, axis=1)

    def norm(col):
        return (col - col.min()) / (col.max() - col.min() + 1e-9)

    df["ml_n"] = norm(df["ml_score"])
    df["rl_n"] = norm(df["rl_score"])
    df["h_n"] = norm(df["heuristic"])


    df["final_score"] = (
        df["ml_n"] * 0.5 +
        df["rl_n"] * 0.3 +
        df["h_n"] * 0.2
    )

    ranked_df = df.sort_values(by="final_score", ascending=False)

    output = ranked_df.head(5).copy()

    output["confidence"] = (output["final_score"] * 100).clip(0, 100)

    def explain(row):
        reasons = []

        if row["price"] < df["price"].median():
            reasons.append("Good market value")

        if row["bedrooms"] >= df["bedrooms"].mean():
            reasons.append("Spacious layout")

        if row["bathrooms"] >= df["bathrooms"].mean():
            reasons.append("Comfortable facilities")

        return ", ".join(reasons) if reasons else "Balanced choice"

    output["why"] = output.apply(explain, axis=1)

    return output, ranked_df