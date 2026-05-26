import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

df = pd.read_csv("data/scored_leads.csv")

def generate_brief(row):
    prompt = f"""
You are a senior sales intelligence analyst at Crustdata, a company that provides real-time data APIs for AI agents and sales teams.

Analyze this company and write a 3-sentence intelligence brief:

Company: {row['domain']}
AI Signal Score: {row['score_normalized']}/100
Tier: {row['tier']}
AI Hiring Signals: {row['ai_signal_hits']} out of {row['total_results']} search results
Signal Reasons: {row['reasons']}

Write exactly 3 sentences:
1. What this company is building (based on their domain and signals)
2. Why they will need Crustdata's real-time data API specifically
3. The best outreach angle for Crustdata's sales team

Be specific, confident, and concise. No fluff.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200
    )

    return response.choices[0].message.content.strip()

print("Generating intelligence briefs...\n")

briefs = []
for _, row in df.iterrows():
    print(f"Analyzing {row['domain']}...")
    brief = generate_brief(row)
    briefs.append(brief)
    print(f"✅ Done\n")

df["intelligence_brief"] = briefs

# Save final output
df.to_csv("data/final_leads.csv", index=False)

print("\n=== FINAL INTELLIGENCE REPORT ===\n")
for _, row in df.iterrows():
    print(f"{'='*60}")
    print(f"#{row['rank']} {row['domain']} — {row['tier']} — Score: {row['score_normalized']}/100")
    print(f"\n{row['intelligence_brief']}")
    print()

print(f"\nSaved to data/final_leads.csv")