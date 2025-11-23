import streamlit as st
import io

# --- Page Configuration ---
st.set_page_config(
    page_title="Fintech IMPACT Radar",
    page_icon="📊",
    layout="centered"
)

# --- Data Definitions (Translated from React) ---
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
        'challengePrompts': [
            'Who specifically is being underserved?',
            'Why have traditional providers ignored this segment?',
            'Is this truly underserved or just a marketing claim?'
        ]
    }
]

# --- Helper Functions ---
def get_score_interpretation(score):
    if score < 30:
        return "Low", "red"
    if score < 70:
        return "Medium", "orange"
    return "High", "green"

def reset_state():
    """Resets all session state variables to default."""
    st.session_state.company_name = ""
    for dim in DIMENSIONS:
        st.session_state[f"score_{dim['id']}"] = 50
        st.session_state[f"note_{dim['id']}"] = ""

# --- Initialize Session State ---
# We use a unique key for every widget to persist data
if 'company_name' not in st.session_state:
    st.session_state.company_name = ""

for dim in DIMENSIONS:
    score_key = f"score_{dim['id']}"
    note_key = f"note_{dim['id']}"
    if score_key not in st.session_state:
        st.session_state[score_key] = 50
    if note_key not in st.session_state:
        st.session_state[note_key] = ""

# --- Main Layout ---

st.title("The Fintech :blue[IMPACT] Radar")
st.markdown("""
Where does your fintech example sit on these six theoretical dimensions?
""")

# Input: Company Name
st.text_input(
    "Company/Example Name",
    placeholder="e.g., Stripe, Revolut, Klarna...",
    key="company_name"
)

st.markdown("---")

# Loop through dimensions to create UI cards
for dim in DIMENSIONS:
    # Create a container for the visual "card" effect
    with st.container(border=True):
        # Top Section: Header & Score Display
        col_info, col_score = st.columns([3, 1])
        
        current_score = st.session_state[f"score_{dim['id']}"]
        interp_text, interp_color = get_score_interpretation(current_score)

        with col_info:
            st.subheader(f"{dim['icon']} {dim['title']}")
            st.caption(dim['subtitle'])
            st.markdown(f"*{dim['question']}*")

        with col_score:
            st.markdown(
                f"<div style='text-align: center;'>"
                f"<h2 style='color:{interp_color}; margin:0;'>{current_score}</h2>"
                f"<span style='color:{interp_color}; font-weight:bold;'>{interp_text}</span>"
                f"</div>", 
                unsafe_allow_html=True
            )

        # Middle Section: Slider
        st.write("") # Spacer
        
        # Labels above slider
        c_left, c_right = st.columns(2)
        c_left.caption(f"◀ {dim['leftLabel']}")
        c_right.caption(f"<div style='text-align: right;'>{dim['rightLabel']} ▶</div>", unsafe_allow_html=True)
        
        st.slider(
            label=f"Score for {dim['title']}",
            label_visibility="collapsed", # Hide label as we have custom ones
            min_value=0,
            max_value=100,
            key=f"score_{dim['id']}" # Binds directly to session state
        )

        # Bottom Section: Expandable Details
        with st.expander("🤔 Challenge Prompts & Notes"):
            st.markdown("**Critical Questions:**")
            for prompt in dim['challengePrompts']:
                st.markdown(f"- {prompt}")
            
            st.markdown("**Your Evidence/Notes:**")
            st.text_area(
                label=f"Notes for {dim['title']}",
                label_visibility="collapsed",
                placeholder="Record your justification and evidence here...",
                key=f"note_{dim['id']}"
            )

# --- Footer Analysis Section ---
st.markdown("### Overall IMPACT Score")

total_score = sum(st.session_state[f"score_{dim['id']}"] for dim in DIMENSIONS)
avg_score = round(total_score / 6)

# Display Big Average Score
with st.container(border=True):
    f_col1, f_col2 = st.columns([1, 3])
    
    with f_col1:
         st.markdown(f"<h1 style='text-align: center; font-size: 4rem; color: #2563eb;'>{avg_score}</h1>", unsafe_allow_html=True)
    
    with f_col2:
        # Mini grid of scores
        cols = st.columns(6)
        for idx, dim in enumerate(DIMENSIONS):
            with cols[idx]:
                st.caption(dim['letter'])
                st.markdown(f"**{st.session_state[f'score_{dim['id']}']}**")
        
        st.caption("Be prepared to justify each placement with evidence from your research.")

# --- Export & Reset Logic ---
st.markdown("---")
btn_col1, btn_col2 = st.columns([1, 1])

with btn_col1:
    # Generate the text for download
    results_text = f"FINTECH IMPACT RADAR ANALYSIS\n"
    results_text += f"Company: {st.session_state.company_name or 'Not specified'}\n\n"
    
    for dim in DIMENSIONS:
        s = st.session_state[f"score_{dim['id']}"]
        n = st.session_state[f"note_{dim['id']}"] or "No notes"
        i_text, _ = get_score_interpretation(s)
        results_text += f"[{dim['letter']}] {dim['title']}: {s}/100 ({i_text})\n"
        results_text += f"Notes: {n}\n\n"
    
    results_text += f"Overall Assessment Average Score: {avg_score}"

    st.download_button(
        label="📥 Export Analysis",
        data=results_text,
        file_name=f"{st.session_state.company_name or 'fintech'}-impact-radar.txt",
        mime="text/plain",
        type="primary"
    )

with btn_col2:
    if st.button("🔄 Reset All"):
        reset_state()
        st.rerun()

# --- Teacher Note ---
st.info(
    "**Teacher Note:** After presentations, challenge students on their highest scores. "
    "Ask for concrete evidence rather than accepting general claims. This transforms descriptive "
    "presentations into critical analysis exercises."
)