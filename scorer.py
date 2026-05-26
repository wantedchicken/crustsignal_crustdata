import pandas as pd
import os

# Load raw signals
df = pd.read_csv("data/raw_signals.csv")

# --- SCORING LOGIC ---
# This is the core of what Mount / Crustdata cares about
# We score each company on likelihood they need Crustdata's API RIGHT NOW

def score_company(row):
    score = 0
    reasons = []

    # Signal 1: High AI hiring activity (max 40 points)
    ai_ratio = row["ai_signal_hits"] / row["total_results"] if row["total_results"] > 0 else 0
    ai_score = round(ai_ratio * 40)
    score += ai_score
    if ai_ratio > 0.5:
        reasons.append(f"Heavy AI hiring activity ({row['ai_signal_hits']}/{row['total_results']} signals)")
    elif ai_ratio > 0.3:
        reasons.append(f"Moderate AI hiring activity ({row['ai_signal_hits']}/{row['total_results']} signals)")

    # Signal 2: Volume of search results (proxy for company activity)
    if row["total_results"] >= 9:
        score += 20
        reasons.append("High web presence — active company")
    elif row["total_results"] >= 7:
        score += 10
        reasons.append("Moderate web presence")

    # Signal 3: Absolute AI signal count
    if row["ai_signal_hits"] >= 7:
        score += 30
        reasons.append("Very high number of AI engineering signals")
    elif row["ai_signal_hits"] >= 5:
        score += 20
        reasons.append("Strong AI engineering signal count")
    elif row["ai_signal_hits"] >= 3:
        score += 10
        reasons.append("Some AI engineering signals detected")

    return score, " | ".join(reasons)

# Apply scoring
df[["score", "reasons"]] = df.apply(
    lambda row: pd.Series(score_company(row)), axis=1
)

# Normalize score to 0-100
max_score = df["score"].max()
df["score_normalized"] = (df["score"] / max_score * 100).round(1)

# Assign risk tier
def assign_tier(score):
    if score >= 70:
        return "🔴 HOT"
    elif score >= 40:
        return "🟡 WARM"
    else:
        return "🟢 COLD"

df["tier"] = df["score_normalized"].apply(assign_tier)

# Sort by score
df = df.sort_values("score_normalized", ascending=False).reset_index(drop=True)
df["rank"] = df.index + 1

# Save scored results
os.makedirs("data", exist_ok=True)
df.to_csv("data/scored_leads.csv", index=False)

# Print results
print("=" * 60)
print("CRUSTDATA LEAD SIGNAL MONITOR — SCORED RESULTS")
print("=" * 60)

for _, row in df.iterrows():
    print(f"\n#{row['rank']} {row['domain']} — {row['tier']}")
    print(f"   Score: {row['score_normalized']}/100")
    print(f"   Signals: {row['ai_signal_hits']} AI hits out of {row['total_results']} results")
    print(f"   Why: {row['reasons']}")

print("\n" + "=" * 60)
print(f"Saved to data/scored_leads.csv")