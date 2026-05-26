import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="CrustSignal",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS — Dark Premium Design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

* { font-family: 'Space Grotesk', sans-serif; }

/* Dark background */
.stApp {
    background: #0a0a0f;
    color: #e2e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f0f1a !important;
    border-right: 1px solid #1e1e3a;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Metric cards */
[data-testid="metric-container"] {
    background: #0f0f1a;
    border: 1px solid #1e1e3a;
    border-radius: 12px;
    padding: 20px;
}

[data-testid="metric-container"]:hover {
    border-color: #4f46e5;
    transition: all 0.3s ease;
}

/* Expander styling */
[data-testid="stExpander"] {
    background: #0f0f1a !important;
    border: 1px solid #1e1e3a !important;
    border-radius: 12px !important;
    margin-bottom: 8px !important;
}

[data-testid="stExpander"]:hover {
    border-color: #4f46e5 !important;
    transition: all 0.3s ease;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg, #4f46e5, #7c3aed);
    border-radius: 10px;
}

/* Info boxes */
.stAlert {
    background: #13131f !important;
    border: 1px solid #2d2d4e !important;
    border-radius: 10px !important;
    color: #a5b4fc !important;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #1e1e3a;
    border-radius: 12px;
}

/* Divider */
hr { border-color: #1e1e3a; }

/* Sidebar text */
[data-testid="stSidebar"] label {
    color: #94a3b8 !important;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div style='text-align: center; padding: 40px 0 20px 0;'>
    <div style='display: inline-block; background: linear-gradient(135deg, #4f46e5, #7c3aed); 
                padding: 10px 20px; border-radius: 8px; margin-bottom: 16px;'>
        <span style='font-family: JetBrains Mono; font-size: 12px; color: #c4b5fd; letter-spacing: 3px;'>
            POWERED BY CRUSTDATA API
        </span>
    </div>
    <h1 style='font-size: 52px; font-weight: 700; margin: 0;
               background: linear-gradient(135deg, #e2e8f0 0%, #a5b4fc 50%, #7c3aed 100%);
               -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
        📡 CrustSignal
    </h1>
    <p style='color: #64748b; font-size: 18px; margin-top: 12px; font-weight: 300;'>
        Predicts which companies are about to need Crustdata's API —<br>
        <span style='color: #a5b4fc;'>before they start looking</span>
    </p>
</div>
<hr>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("data/final_leads.csv")

df = load_data()

# Sidebar
st.sidebar.markdown("""
<div style='padding: 10px 0;'>
    <p style='color: #4f46e5; font-size: 11px; letter-spacing: 2px; font-weight: 600;'>
        SIGNAL FILTERS
    </p>
</div>
""", unsafe_allow_html=True)

tier_filter = st.sidebar.multiselect(
    "Filter by Tier",
    options=["🔴 HOT", "🟡 WARM", "🟢 COLD"],
    default=["🔴 HOT", "🟡 WARM", "🟢 COLD"]
)

min_score = st.sidebar.slider("Minimum Score", 0, 100, 0)

st.sidebar.markdown("<hr style='border-color: #1e1e3a;'>", unsafe_allow_html=True)
st.sidebar.markdown("""
<div style='padding: 10px 0;'>
    <p style='color: #64748b; font-size: 11px; letter-spacing: 2px;'>HOW IT WORKS</p>
    <p style='color: #475569; font-size: 12px; line-height: 1.6;'>
        CrustSignal uses Crustdata's web search API to detect AI hiring signals across 
        target companies, scores them on likelihood of needing real-time data APIs, 
        and generates GPT-powered intelligence briefs.
    </p>
</div>
""", unsafe_allow_html=True)

# Apply filters
filtered_df = df[
    (df["tier"].isin(tier_filter)) &
    (df["score_normalized"] >= min_score)
]

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏢 Companies Tracked", len(df))
col2.metric("🔴 HOT Leads", len(df[df["tier"] == "🔴 HOT"]))
col3.metric("🟡 WARM Leads", len(df[df["tier"] == "🟡 WARM"]))
col4.metric("🟢 COLD Leads", len(df[df["tier"] == "🟢 COLD"]))

st.markdown("<br>", unsafe_allow_html=True)

# Section header
st.markdown(f"""
<div style='display: flex; align-items: center; gap: 12px; margin-bottom: 20px;'>
    <div style='width: 4px; height: 24px; background: linear-gradient(180deg, #4f46e5, #7c3aed); border-radius: 2px;'></div>
    <h3 style='margin: 0; color: #e2e8f0;'>Lead Pipeline</h3>
    <span style='background: #1e1e3a; color: #a5b4fc; padding: 4px 12px; 
                 border-radius: 20px; font-size: 13px;'>
        {len(filtered_df)} companies
    </span>
</div>
""", unsafe_allow_html=True)

# Lead cards
for _, row in filtered_df.iterrows():
    tier_colors = {
        "🔴 HOT": "#ef4444",
        "🟡 WARM": "#f59e0b",
        "🟢 COLD": "#10b981"
    }
    tier_bg = {
        "🔴 HOT": "rgba(239,68,68,0.1)",
        "🟡 WARM": "rgba(245,158,11,0.1)",
        "🟢 COLD": "rgba(16,185,129,0.1)"
    }
    color = tier_colors.get(row["tier"], "#666")
    bg = tier_bg.get(row["tier"], "rgba(100,100,100,0.1)")
    tier_label = {"🔴 HOT": "HOT", "🟡 WARM": "WARM", "🟢 COLD": "COLD"}.get(row["tier"], "")
    with st.expander(
    f"#{row['rank']}  {row['domain']}  ·  {tier_label}  ·  {row['score_normalized']}/100"
    ):
        col1, col2 = st.columns([1, 2])

        with col1:
            st.markdown(f"""
            <div style='background: #13131f; border-radius: 10px; padding: 16px;'>
                <p style='color: #64748b; font-size: 11px; letter-spacing: 2px; margin: 0 0 4px 0;'>DOMAIN</p>
                <p style='color: #e2e8f0; font-size: 18px; font-weight: 600; margin: 0 0 16px 0;'>{row['domain']}</p>
                
                <p style='color: #64748b; font-size: 11px; letter-spacing: 2px; margin: 0 0 4px 0;'>TIER</p>
                <div style='background: {bg}; border: 1px solid {color}; border-radius: 6px; 
                            padding: 4px 12px; display: inline-block; margin-bottom: 16px;'>
                    <span style='color: {color}; font-weight: 600;'>{row['tier']}</span>
                </div>
                
                <p style='color: #64748b; font-size: 11px; letter-spacing: 2px; margin: 0 0 8px 0;'>SIGNAL SCORE</p>
                <p style='color: #a5b4fc; font-size: 28px; font-weight: 700; margin: 0 0 8px 0;
                          font-family: JetBrains Mono;'>{row['score_normalized']}<span style='font-size: 14px; color: #475569;'>/100</span></p>
            </div>
            """, unsafe_allow_html=True)

            st.progress(int(row["score_normalized"]) / 100)

            st.markdown(f"""
            <div style='margin-top: 12px; background: #13131f; border-radius: 10px; padding: 16px;'>
                <p style='color: #64748b; font-size: 11px; letter-spacing: 2px; margin: 0 0 8px 0;'>AI SIGNALS DETECTED</p>
                <p style='color: #e2e8f0; font-size: 15px; margin: 0;'>
                    <span style='color: #a5b4fc; font-weight: 700; font-size: 20px;'>{row['ai_signal_hits']}</span>
                    <span style='color: #475569;'> / {row['total_results']} results</span>
                </p>
                <p style='color: #475569; font-size: 12px; margin-top: 8px;'>{row['reasons']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <p style='color: #64748b; font-size: 11px; letter-spacing: 2px; margin: 0 0 12px 0;'>
                🧠 INTELLIGENCE BRIEF
            </p>
            """, unsafe_allow_html=True)
            st.info(row["intelligence_brief"])

st.markdown("<br><hr>", unsafe_allow_html=True)

# Data table
st.markdown("""
<div style='display: flex; align-items: center; gap: 12px; margin-bottom: 20px;'>
    <div style='width: 4px; height: 24px; background: linear-gradient(180deg, #4f46e5, #7c3aed); border-radius: 2px;'></div>
    <h3 style='margin: 0; color: #e2e8f0;'>Full Data Table</h3>
</div>
""", unsafe_allow_html=True)

st.dataframe(
    filtered_df[["rank", "domain", "tier", "score_normalized", "ai_signal_hits", "total_results"]].rename(columns={
        "rank": "Rank",
        "domain": "Company",
        "tier": "Tier",
        "score_normalized": "Score",
        "ai_signal_hits": "AI Signals",
        "total_results": "Total Results"
    }),
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown("""
<br>
<div style='text-align: center; padding: 20px;'>
    <p style='color: #1e1e3a; font-size: 12px; font-family: JetBrains Mono;'>
        ████████████████████████████████████████████████████████████
    </p>
    <p style='color: #334155; font-size: 13px;'>
        CrustSignal · Built with Crustdata API + OpenAI GPT-4o-mini · by Sohith Sai M
    </p>
</div>
""", unsafe_allow_html=True)