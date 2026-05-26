import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

CRUSTDATA_API_KEY = os.getenv("CRUSTDATA_API_KEY")

headers = {
    "Authorization": f"Token {CRUSTDATA_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

TARGET_COMPANIES = [
    "scale.ai",
    "cohere.com",
    "mistral.ai",
    "together.ai",
    "perplexity.ai",
    "anyscale.com",
    "langchain.com",
    "llamaindex.ai",
    "fixie.ai",
    "adept.ai"
]

AI_SIGNAL_KEYWORDS = [
    "data infrastructure", "ml platform", "ai engineer",
    "data engineer", "machine learning", "llm", "agent",
    "real-time data", "pipeline", "data platform",
    "backend engineer", "api engineer"
]

results = []

print(f"Pulling AI hiring signals for {len(TARGET_COMPANIES)} companies...\n")

for domain in TARGET_COMPANIES:
    company_name = domain.split(".")[0].capitalize()
    try:
        # Search for AI/data engineering jobs at this company
        query = f"{company_name} hiring data engineer OR ml engineer OR ai engineer OR data infrastructure 2024 2025"

        payload = {
            "query": query,
            "geolocation": "US"
        }

        response = requests.post(
            "https://api.crustdata.com/screener/web-search",
            headers=headers,
            json=payload
        )

        if response.status_code == 200:
            data = response.json()
            results_list = data.get("results", [])

            # Count how many results mention AI signal keywords
            signal_count = 0
            signal_snippets = []

            for result in results_list:
                title = result.get("title", "").lower()
                snippet = result.get("snippet", "").lower()
                combined = title + " " + snippet

                for keyword in AI_SIGNAL_KEYWORDS:
                    if keyword in combined:
                        signal_count += 1
                        signal_snippets.append(result.get("title", "")[:60])
                        break

            results.append({
                "domain": domain,
                "company": company_name,
                "total_results": len(results_list),
                "ai_signal_hits": signal_count,
                "signal_snippets": " | ".join(signal_snippets[:2]),
                "status": "✅"
            })

            print(f"✅ {domain}: {len(results_list)} results, {signal_count} AI signals")

        else:
            print(f"❌ {domain}: HTTP {response.status_code} - {response.text[:100]}")
            results.append({
                "domain": domain,
                "company": company_name,
                "total_results": 0,
                "ai_signal_hits": 0,
                "signal_snippets": "",
                "status": f"❌ {response.status_code}"
            })

    except Exception as e:
        print(f"❌ {domain}: Exception - {e}")

# Save results
os.makedirs("data", exist_ok=True)
df = pd.DataFrame(results)

if not df.empty:
    df.to_csv("data/raw_signals.csv", index=False)
    print(f"\n=== SIGNAL SUMMARY ===")
    print(df[["domain", "total_results", "ai_signal_hits"]].to_string(index=False))
    print(f"\nSaved to data/raw_signals.csv")
else:
    print("\nNo results collected.")