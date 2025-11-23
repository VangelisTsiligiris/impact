import streamlit as st
from io import BytesIO
from docx import Document
from docx.shared import Pt, RGBColor, Inches

# --- Page Configuration ---
st.set_page_config(
    page_title="Fintech IMPACT Radar",
    page_icon="📊",
    layout="wide" # Switched to wide layout for better sidebar usage
)

# --- CSS Tweaks ---
st.markdown("""
    <style>
    .stSlider { padding-top: 1rem; padding-bottom: 1rem; }
    div[data-testid="stExpander"] details summary p { font-weight: 600; font-size: 1rem; }
    .rubric-table { font-size: 0.9rem; width: 100%; border-collapse: collapse; }
    .rubric-table td { padding: 8px; border-bottom: 1px solid #eee; vertical-align: top; }
    .rubric-header { font-weight: bold; color: #555; background-color: #f9f9f9; }
    </style>
""", unsafe_allow_html=True)

# --- Extended Data Definitions with Rubrics ---
DIMENSIONS = [
    {
        'id': 'integration',
        'letter': 'I',
        'icon': '🔗',
        'title': 'INTEGRATION',
        'subtitle': 'Platform Theory & Connectivity',
        'question': 'Is it a standalone "island" or does it connect openly with others?',
        'leftLabel': 'Standalone App (Island)',
        'rightLabel': 'Open Ecosystem / API Platform',
        'definition': 'Measures how easily the fintech connects with the broader financial ecosystem. High scores indicate an "Open Banking" mindset.',
        'rubric': {
            'low': 'Closed system. No APIs. Hard to export data. "Walled Garden."',
            'medium': 'Some integrations (e.g., connects to Xero/Quickbooks), but largely self-contained.',
            'high': 'API-first architecture. Allows developers to build on top (Platform theory). Two-way data flow.'
        },
        'challengePrompts': [
            'What evidence do they provide about their API partnerships?',
            'Are their integrations truly bidirectional or just cosmetic?',
            'Do they have a documented developer platform?'
        ]
    },
    {
        'id': 'monetization',
        'letter': 'M',
        'icon': '💰',
        'title': 'MONETIZATION',
        'subtitle': 'Viability & Unit Economics',
        'question': 'Is the model based on "growth at all costs" or sustainable revenue?',
        'leftLabel': 'Unclear / Burning Cash',
        'rightLabel': 'Clear / Sustainable Economics',
        'definition': 'Assesses the path to profitability. High scores indicate healthy margins and clear revenue per user (ARPU).',
        'rubric': {
            'low': 'Freemium with no clear upsell. High cash burn. Subsidizing users with VC money.',
            'medium': 'Generating revenue (interchange fees), but barely covering operating costs.',
            'high': 'Strong unit economics (LTV > 3x CAC). Diversified revenue streams (Sub + Trans + Data).'
        },
        'challengePrompts': [
            'Can they articulate their unit economics clearly?',
            'What is their path to profitability?',
            'How do customer acquisition costs compare to lifetime value?'
        ]
    },
    {
        'id': 'painPoint',
        'letter': 'P',
        'icon': '🩹',
        'title': 'PAIN POINT',
        'subtitle': 'Differentiation Strategy',
        'question': 'Are they solving a slightly better digital experience, or a fundamentally broken process?',
        'leftLabel': 'Nice-to-have (Better UI)',
        'rightLabel': 'Must-have (10x Solution)',
        'definition': 'Distinguishes between "Vitamins" (nice to have) and "Painkillers" (must have).',
        'rubric': {
            'low': 'Cosmetic changes. Just a prettier app for an existing bank account.',
            'medium': 'Reduces friction (e.g., faster onboarding), but same underlying core service.',
            'high': 'Solves a deep friction (e.g., cross-border remittance, instant lending). Users cannot go back.'
        },
        'challengePrompts': [
            'What is the incumbent solution they\'re replacing?',
            'Is this 10% better or 10x better?',
            'What happens if users go back to the old way?'
        ]
    },
    {
        'id': 'automation',
        'letter': 'A',
        'icon': '🤖',
        'title': 'AUTOMATION',
        'subtitle': 'Technology Depth',
        'question': 'Is the "tech" just a nice mobile interface, or genuine deep technology?',
        'leftLabel': 'Basic App "Wrapper"',
        'rightLabel': 'Genuine Deep Tech / AI Engine',
        'definition': 'Evaluates if the company is a "Tech" company or a "Service" company wrapped in an app.',
        'rubric': {
            'low': 'Manual processes behind the scenes. Rule-based logic (If X then Y).',
            'medium': 'Some automation in onboarding/KYC, but support is human-heavy.',
            'high': 'Proprietary AI/ML models. Algorithmic underwriting. Self-driving finance.'
        },
        'challengePrompts': [
            'What proprietary technology do they actually own?',
            'Is there real machine learning or just rule-based logic?',
            'Could this be replicated easily by competitors?'
        ]
    },
    {
        'id': 'compliance',
        'letter': 'C',
        'icon': '⚖️',
        'title': 'COMPLIANCE',
        'subtitle': 'Trust & Regulatory Stance',
        'question': 'How do they build trust without a 100-year history? Do they operate in grey areas?',
        'leftLabel': 'Regulatory "Grey Area"',
        'rightLabel': 'Highly Compliant / Licensed',
        'definition': 'Measures regulatory maturity. Fintechs often start in grey areas ("Regulatory Arbitrage") and move toward compliance.',
        'rubric': {
            'low': 'Unregulated crypto/DeFi. Operating across borders to avoid rules. "Move fast and break things."',
            'medium': 'Partnering with a sponsor bank (BaaS) to rent a license.',
            'high': 'Full Banking Charter/License. Direct relationship with regulators. Heavy compliance investment.'
        },
        'challengePrompts': [
            'What licenses do they hold?',
            'Have they faced regulatory scrutiny?',
            'How do they signal trustworthiness to users?'
        ]
    },
    {
        'id': 'target',
        'letter': 'T',
        'icon': '🎯',
        'title': 'TARGET',
        'subtitle': 'Inclusion & The "Long Tail"',
        'question': 'Are they competing for the same customers as major banks, or serving segments banks ignore?',
        'leftLabel': 'Serving the Mass Market',
        'rightLabel': 'Serving the Underserved Niche',
        'definition': 'Looks at Financial Inclusion. Are they fighting for the top 1% or serving the "Long Tail"?',
        'rubric': {
            'low': 'Competing for prime customers (High FICO scores) just like Chase/HSBC.',
            'medium': 'Millennials/Gen-Z focus, but still generally bankable customers.',
            'high': 'Unbanked, gig-workers, immigrants, or very specific niches (e.g., dentists, creators).'
        },
        'challengePrompts': [
            'Who specifically is being underserved?',
            'Why have traditional providers ignored this segment?',
            'Is this truly underserved or just a marketing claim?'
        ]
    }
]

# --- Helper Functions ---
def get_score_interpretation(score):
    if score < 30: return "Low", "red"
    if score < 70: return "Medium", "orange"
    return "High", "green"

def reset_state():
    st.session_state.company_name = ""
    for dim in DIMENSIONS:
        st.session_state[f"score_{dim['id']}"] = 50
        st.session_state[f"note_{dim['id']}"] = ""

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
        interp, _ = get_score_interpretation(score)
        
        doc.add_heading(f"{dim['title']} ({score}/100 - {interp})", level=2)
        doc.add_paragraph(f"{dim['subtitle']}", style='Intense Quote')
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

# --- Initialize Session State ---
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""
for dim in DIMENSIONS:
    score_key = f"score_{dim['id']}"
    note_key = f"note_{dim['id']}"
    if score_key not in st.session_state: st.session_state[score_key] = 50
    if note_key not in st.session_state: st.session_state[note_key] = ""

# --- Sidebar: Educational Context ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2620/2620630.png", width=80)
    st.title("Framework Guide")
    st.markdown("### The IMPACT Model")
    st.info("This framework evaluates fintech maturity across 6 key dimensions.")
    
    st.markdown("---")
    
    for dim in DIMENSIONS:
        with st.expander(f"{dim['letter']} - {dim['title']}"):
            st.markdown(f"**{dim['subtitle']}**")
            st.caption(dim['definition'])
            st.markdown(f"*Example:* {dim['question']}")

# --- Main Content ---

st.title("The Fintech :blue[IMPACT] Radar")
st.markdown("Use the sliders below to score your company. Expand the cards to see the **Scoring Rubric**.")

col_main, col_padding = st.columns([4, 1])

with col_main:
    # Input: Company Name
    st.text_input("Company/Example Name", placeholder="e.g., Stripe, Revolut...", key="company_name")
    
    st.markdown("---")

    # Loop through dimensions
    for dim in DIMENSIONS:
        with st.container(border=True):
            # Top Row: Header & Score
            col_info, col_score = st.columns([3, 1.2])
            current_score = st.session_state[f"score_{dim['id']}"]
            interp_text, interp_color = get_score_interpretation(current_score)

            with col_info:
                st.subheader(f"{dim['icon']} {dim['title']}")
                st.caption(f"**{dim['subtitle']}**")
                st.markdown(f"_{dim['question']}_")

            with col_score:
                st.markdown(
                    f"<div style='text-align: center; background-color: #f8f9fa; padding: 10px; border-radius: 10px;'>"
                    f"<h2 style='color:{interp_color}; margin:0; font-size: 2.2em;'>{current_score}</h2>"
                    f"<span style='color:{interp_color}; font-weight:bold; font-size: 0.9em;'>{interp_text}</span></div>", 
                    unsafe_allow_html=True
                )

            st.write("") 

            # Middle Row: Slider
            c_left, c_right = st.columns([1, 1])
            c_left.markdown(f"<small>◀ {dim['leftLabel']}</small>", unsafe_allow_html=True)
            c_right.markdown(f"<div style='text-align: right;'><small>{dim['rightLabel']} ▶</small></div>", unsafe_allow_html=True)
            
            st.slider(
                label=f"Score for {dim['title']}", label_visibility="collapsed",
                min_value=0, max_value=100, key=f"score_{dim['id']}"
            )

            # Bottom Row: Expander with RUBRIC
            st.markdown("---") 
            with st.expander(f"📝 Scoring Guide & Evidence for {dim['title']}"):
                
                # THE NEW RUBRIC TABLE
                st.markdown("#### 📏 Scoring Rubric")
                st.markdown(f"""
                <table class="rubric-table">
                    <tr>
                        <td class="rubric-header" width="20%">Low (0-30)</td>
                        <td width="80%">{dim['rubric']['low']}</td>
                    </tr>
                    <tr>
                        <td class="rubric-header">Med (31-70)</td>
                        <td>{dim['rubric']['medium']}</td>
                    </tr>
                    <tr>
                        <td class="rubric-header">High (71-100)</td>
                        <td>{dim['rubric']['high']}</td>
                    </tr>
                </table>
                """, unsafe_allow_html=True)
                
                st.markdown("#### 🕵️ Critical Questions")
                for prompt in dim['challengePrompts']:
                    st.markdown(f"- {prompt}")
                
                st.write("")
                st.text_area(label="Your Analysis", placeholder="Paste your evidence here...", key=f"note_{dim['id']}", height=100)

    # --- Footer Analysis Section ---
    st.header("Analysis Summary")
    total_score = sum(st.session_state[f"score_{dim['id']}"] for dim in DIMENSIONS)
    avg_score = round(total_score / 6)

    with st.container(border=True):
        f_col1, f_col2 = st.columns([1, 3])
        with f_col1:
             st.markdown(f"<div style='text-align:center'><h1 style='font-size: 4.5rem; color: #2563eb; margin: 0;'>{avg_score}</h1><strong>AVG SCORE</strong></div>", unsafe_allow_html=True)
        with f_col2:
            cols = st.columns(6)
            for idx, dim in enumerate(DIMENSIONS):
                with cols[idx]:
                    st.markdown(f"<div style='text-align: center;'><b>{dim['letter']}</b><br>{st.session_state[f'score_{dim['id']}']}</div>", unsafe_allow_html=True)

    # --- Export & Reset ---
    st.markdown("---")
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        docx_file = generate_word_doc(st.session_state.company_name, avg_score)
        st.download_button(
            label="📄 Download Word Doc (.docx)", data=docx_file,
            file_name=f"{st.session_state.company_name or 'fintech'}-impact-radar.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary", use_container_width=True
        )
    with btn_col2:
        if st.button("🔄 Reset All", use_container_width=True):
            reset_state()
            st.rerun()