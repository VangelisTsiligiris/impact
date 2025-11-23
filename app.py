import streamlit as st
import plotly.graph_objects as go
from io import BytesIO
from docx import Document
from docx.shared import Pt, RGBColor, Inches

# --- Page Configuration ---
st.set_page_config(
    page_title="Fintech IMPACT Radar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for "Dashboard" Look ---
st.markdown("""
    <style>
    /* Main Background adjustments */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Card Styling */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background-color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }

    /* Slider adjustments */
    .stSlider { padding-top: 0.5rem; padding-bottom: 0.5rem; }
    
    /* Headers */
    h1, h2, h3 { color: #0f172a; }
    
    /* Metric styling */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f1f5f9;
        border-radius: 5px;
        font-size: 0.9rem;
    }
    
    /* Rubric Table Styling */
    .rubric-table { 
        font-size: 0.85rem; 
        width: 100%; 
        border-collapse: collapse; 
        font-family: sans-serif;
    }
    .rubric-table td { 
        padding: 8px; 
        border-bottom: 1px solid #e2e8f0; 
        vertical-align: top; 
        color: #334155;
    }
    .rubric-header { 
        font-weight: 700; 
        color: #1e293b; 
        background-color: #f8fafc; 
        border-right: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Definitions ---
DIMENSIONS = [
    {
        'id': 'integration',
        'letter': 'I',
        'icon': '🔗',
        'title': 'INTEGRATION',
        'subtitle': 'Connectivity',
        'question': 'Is it an Island or an Ecosystem?',
        'leftLabel': 'Closed / Island',
        'rightLabel': 'Open API Platform',
        'rubric': {
            'low': 'Closed system. No APIs. Hard to export data. "Walled Garden."',
            'medium': 'Some integrations (e.g., connects to Xero), but largely self-contained.',
            'high': 'API-first architecture. Allows developers to build on top. Two-way data flow.'
        },
        'challengePrompts': ['Evidence of API documentation?', 'Are integrations bidirectional?']
    },
    {
        'id': 'monetization',
        'letter': 'M',
        'icon': '💰',
        'title': 'MONETIZATION',
        'subtitle': 'Unit Economics',
        'question': 'Growth at all costs or sustainable?',
        'leftLabel': 'Burning Cash',
        'rightLabel': 'Sustainable Profit',
        'rubric': {
            'low': 'Freemium with no clear upsell. High burn. Subsidized by VC money.',
            'medium': 'Generating revenue (interchange fees), but barely covering costs.',
            'high': 'Strong LTV > CAC. Diversified revenue (Sub + Trans + Data).'
        },
        'challengePrompts': ['Path to profitability?', 'LTV vs CAC ratio?']
    },
    {
        'id': 'painPoint',
        'letter': 'P',
        'icon': '🩹',
        'title': 'PAIN POINT',
        'subtitle': 'Differentiation',
        'question': 'Vitamin or Painkiller?',
        'leftLabel': 'Nice-to-have (UI)',
        'rightLabel': '10x Solution',
        'rubric': {
            'low': 'Cosmetic changes. Just a prettier app for a standard bank account.',
            'medium': 'Reduces friction (faster onboarding), but core product is standard.',
            'high': 'Solves deep friction (e.g., instant cross-border). Users cannot go back.'
        },
        'challengePrompts': ['Is it 10% better or 10x better?', 'What is the incumbent solution?']
    },
    {
        'id': 'automation',
        'letter': 'A',
        'icon': '🤖',
        'title': 'AUTOMATION',
        'subtitle': 'Tech Depth',
        'question': 'Wrapper or Deep Tech?',
        'leftLabel': 'Human/Manual',
        'rightLabel': 'AI/Algorithmic',
        'rubric': {
            'low': 'Manual processes behind scenes. Rule-based logic only.',
            'medium': 'Some automation in KYC, but support is human-heavy.',
            'high': 'Proprietary AI/ML models. Algorithmic underwriting. Self-driving finance.'
        },
        'challengePrompts': ['Real ML or just rules?', 'Proprietary tech ownership?']
    },
    {
        'id': 'compliance',
        'letter': 'C',
        'icon': '⚖️',
        'title': 'COMPLIANCE',
        'subtitle': 'Trust',
        'question': 'Regulatory Arbitrage or Trust?',
        'leftLabel': 'Grey Area',
        'rightLabel': 'Fully Licensed',
        'rubric': {
            'low': 'Unregulated. Operating across borders to avoid rules.',
            'medium': 'Partnering with a sponsor bank (BaaS) to rent a license.',
            'high': 'Full Banking Charter. Direct regulator relationship. Heavy compliance.'
        },
        'challengePrompts': ['Licenses held?', 'Regulatory scrutiny history?']
    },
    {
        'id': 'target',
        'letter': 'T',
        'icon': '🎯',
        'title': 'TARGET',
        'subtitle': 'Inclusion',
        'question': 'Mass Market or Niche?',
        'leftLabel': 'Mass Market',
        'rightLabel': 'Underserved Niche',
        'rubric': {
            'low': 'Competing for prime customers (High FICO) like major banks.',
            'medium': 'Millennials/Gen-Z focus, but still generally bankable.',
            'high': 'Unbanked, gig-workers, immigrants, or specific vertical niches.'
        },
        'challengePrompts': ['Who is excluded by banks?', 'Is the niche defensible?']
    }
]

# --- Helper Functions ---
def get_score_color(score):
    if score < 30: return "#ef4444" # Red
    if score < 70: return "#f59e0b" # Orange
    return "#22c55e" # Green

def create_radar_chart(values, show_benchmark):
    categories = [d['title'] for d in DIMENSIONS]
    
    # Close the loop for the chart
    r_values = list(values) + [values[0]]
    theta_values = categories + [categories[0]]
    
    fig = go.Figure()

    # User Data
    fig.add_trace(go.Scatterpolar(
        r=r_values,
        theta=theta_values,
        fill='toself',
        name='Your Analysis',
        line_color='#2563eb',
        fillcolor='rgba(37, 99, 235, 0.2)'
    ))

    # Benchmark Data (Traditional Bank Archetype)
    if show_benchmark:
        # Banks: Low Integration, Low Pain Point diff, Low Automation, High Compliance, Low Target Niche
        bank_values = [20, 80, 20, 30, 95, 20] 
        bank_r = bank_values + [bank_values[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=bank_r,
            theta=theta_values,
            fill='toself',
            name='Traditional Bank',
            line_color='#94a3b8',
            fillcolor='rgba(148, 163, 184, 0.1)',
            line_dash='dot'
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        margin=dict(l=40, r=40, t=20, b=20),
        height=400,
        paper_bgcolor="rgba(0,0,0,0)", # Transparent
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig

def generate_word_doc(company_name, avg_score):
    doc = Document()
    doc.add_heading('FINTECH IMPACT RADAR ANALYSIS', 0)
    
    p = doc.add_paragraph()
    run = p.add_run(f"Company: {company_name if company_name else 'Not specified'}")
    run.bold = True
    
    doc.add_heading(f'Overall Impact Score: {avg_score}/100', level=1)
    
    for dim in DIMENSIONS:
        score = st.session_state[f"score_{dim['id']}"]
        notes = st.session_state[f"note_{dim['id']}"]
        
        doc.add_heading(f"{dim['title']} ({score}/100)", level=2)
        doc.add_paragraph(f"Question: {dim['question']}")
        
        doc.add_heading('Analysis / Evidence:', level=3)
        if notes:
            doc.add_paragraph(notes)
        else:
            doc.add_paragraph("No notes recorded.", style='No Spacing')
        doc.add_paragraph("_" * 50) 
        
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def reset_state():
    st.session_state.company_name = ""
    for dim in DIMENSIONS:
        st.session_state[f"score_{dim['id']}"] = 50
        st.session_state[f"note_{dim['id']}"] = ""

# --- Initialize Session State ---
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
for dim in DIMENSIONS:
    if f"score_{dim['id']}" not in st.session_state:
        st.session_state[f"score_{dim['id']}"] = 50
    if f"note_{dim['id']}" not in st.session_state:
        st.session_state[f"note_{dim['id']}"] = ""

# --- SIDEBAR ---
with st.sidebar:
    st.title("📡 Controls")
    
    st.markdown("### 1. Analysis Setup")
    # Input: Company Name
    st.text_input("Company Name", placeholder="e.g., Revolut", key="company_name")
    
    show_benchmark = st.checkbox("Compare vs. Traditional Bank", value=False)
    
    st.markdown("---")
    st.markdown("### 2. Export")
    
    # Calculations for Export
    current_scores = [st.session_state[f"score_{d['id']}"] for d in DIMENSIONS]
    avg_score = round(sum(current_scores) / 6)
    
    docx_file = generate_word_doc(st.session_state.company_name, avg_score)
    st.download_button(
        label="📄 Download Report (.docx)", 
        data=docx_file,
        file_name=f"{st.session_state.company_name or 'analysis'}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        type="primary", 
        use_container_width=True
    )
    
    if st.button("🔄 Reset Analysis", use_container_width=True):
        reset_state()
        st.rerun()

    st.markdown("---")
    with st.expander("📚 Definition Guide"):
        for dim in DIMENSIONS:
            st.markdown(f"**{dim['title']}**: {dim['subtitle']}")

# --- MAIN LAYOUT ---

st.title("The Fintech :blue[IMPACT] Radar")

# Top Section: Dashboard Header
col_chart, col_stats = st.columns([1.2, 2])

with col_chart:
    st.markdown("### Visual Profile")
    # Generate and display Radar Chart
    radar_fig = create_radar_chart(current_scores, show_benchmark)
    st.plotly_chart(radar_fig, use_container_width=True)

with col_stats:
    st.markdown("### Analysis Grid")
    
    # Create a 2x3 Grid for the Inputs
    grid_row1 = st.columns(2)
    grid_row2 = st.columns(2)
    grid_row3 = st.columns(2)
    
    grid_cols = grid_row1 + grid_row2 + grid_row3
    
    for i, dim in enumerate(DIMENSIONS):
        with grid_cols[i]:
            with st.container(border=True):
                # Header
                c_head, c_val = st.columns([4, 1])
                with c_head:
                    st.markdown(f"**{dim['icon']} {dim['title']}**")
                    st.caption(dim['question'])
                with c_val:
                    score = st.session_state[f"score_{dim['id']}"]
                    st.markdown(f"<span style='color:{get_score_color(score)}; font-weight:bold; font-size:1.2rem'>{score}</span>", unsafe_allow_html=True)
                
                # Slider
                st.slider(
                    "Score", 0, 100, 
                    key=f"score_{dim['id']}", 
                    label_visibility="collapsed"
                )
                
                # Labels
                l, r = st.columns(2)
                l.caption(f"◀ {dim['leftLabel']}")
                r.caption(f"<div style='text-align:right'>{dim['rightLabel']} ▶</div>", unsafe_allow_html=True)
                
                # Expander for Details
                with st.expander("📝 Rubric & Notes"):
                    st.markdown("#### 📏 Rubric")
                    st.markdown(f"""
                    <table class="rubric-table">
                        <tr><td class="rubric-header" width="25%">Low</td><td>{dim['rubric']['low']}</td></tr>
                        <tr><td class="rubric-header">Med</td><td>{dim['rubric']['medium']}</td></tr>
                        <tr><td class="rubric-header">High</td><td>{dim['rubric']['high']}</td></tr>
                    </table>
                    """, unsafe_allow_html=True)
                    
                    st.text_area("Evidence:", key=f"note_{dim['id']}", height=80, placeholder="Why this score?")

# --- Footer ---
st.markdown("---")
st.markdown(f"<div style='text-align: center; font-size: 2rem;'>Overall Impact Score: <b>{avg_score}/100</b></div>", unsafe_allow_html=True)