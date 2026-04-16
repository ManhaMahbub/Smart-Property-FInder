from preprocessing.data_preprocessing import load_and_preprocess
from models.model import train_model
from core.recommender import recommend
from rl.rl import UserPreferenceRL
from utils.utils import show_title, print_results, show_section
from rich.console import Console

console = Console()


def main():
    show_title()

    print("⌛ Loading data...")
    df, X, y, preprocessor = load_and_preprocess("data/dataset.xlsx")

    print("🤖 Training model...")
    model, mae, r2 = train_model(X, y)

    print(f"\n✅ Model Ready!")
    print(f"📊 MAE: {mae:.2f} | R²: {r2:.2f}")

    # 🔮 Predict once
    df["predicted_price"] = model.predict(X)

    rl = UserPreferenceRL()

    while True:
        print("\n--- Smart Property Finder ---")

        show_section("Market Overview")
        console.print(
            f"[green]💰 Price Range:[/green] {df['price'].min():.0f} - {df['price'].max():.0f}"
            )
        
        show_section("Enter Your Preferences")
        min_budget = float(input("💰 Min Budget: "))
        max_budget = float(input("💰 Max Budget: "))
    
        df_filtered = df[
            (df["price"] >= min_budget) &
            (df["price"] <= max_budget)
        ]


        if df_filtered.empty:
            print("\n⚠ No properties in exact range. Expanding search...\n")

            margin = (max_budget - min_budget) * 0.2

            df_filtered = df[
                (df["price"] >= min_budget - margin) &
                (df["price"] <= max_budget + margin)
            ]

            if df_filtered.empty:
                print("🔍 Showing closest matches based on your budget...\n")

                target_price = (min_budget + max_budget) / 2

                df_filtered = df.iloc[
                    (df["price"] - target_price).abs().argsort()
                ].head(10)

        show_section("Available Options")

        console.print(f"🛏 Bedrooms: {df_filtered['bedrooms'].min()} - {df_filtered['bedrooms'].max()}")
        console.print(f"🛁 Bathrooms: {df_filtered['bathrooms'].min()} - {df_filtered['bathrooms'].max()}")
        console.print(f"🏘 Suburbs: {df_filtered['suburb'].nunique()}")

        min_bed = int(input("🛏 Min Bedrooms: "))
        max_bed = int(input("🛏 Max Bedrooms: "))

        min_bath = int(input("🛁 Min Bathrooms: "))
        max_bath = int(input("🛁 Max Bathrooms: "))


        final_filtered = df_filtered[
            (df_filtered["bedrooms"] >= min_bed) &
            (df_filtered["bedrooms"] <= max_bed) &
            (df_filtered["bathrooms"] >= min_bath) &
            (df_filtered["bathrooms"] <= max_bath)
        ]

        if final_filtered.empty:
            print("\n⚠ No exact match found. Showing closest alternatives...\n")
            final_filtered = df_filtered.head(5)

        # RECOMMENDATION
        results, ranked_df = recommend(final_filtered, rl)

        show_section("Top Recommendations")
        print_results(results)

        show_section("Feedback")

        feedback = input("Did you like the top result? (like/dislike): ")

        try:
            top_row = ranked_df.iloc[0].to_dict()
            rl.update(top_row, feedback)
        except:
            print("⚠ RL update skipped.")

        
        choice = input("\nSearch again? (yes/no): ").lower()
        if choice != "yes":
            print("\n👋 Thank you for using Smart Property Finder!")
            break


if __name__ == "__main__":
    main()