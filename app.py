import streamlit as st
import plotly.graph_objects as go
from io import BytesIO
from docx import Document
from docx.shared import Pt, RGBColor, Inches
import json
from datetime import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Fintech IMPACT Radar",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional Custom CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1400px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }
    
    /* Headers */
    h1 {
        color: #1a1a1a;
        font-weight: 700;
        font-size: 2.5rem !important;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.5rem !important;
        margin-top: 1rem;
    }
    
    h3 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.2rem !important;
    }
    
    /* Remove default styling */
    .stSlider {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border: 1px solid #dee2e6;
        background-color: white;
        color: #495057;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #f8f9fa;
        border-color: #adb5bd;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #0d6efd;
        color: white;
        border-color: #0d6efd;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #0b5ed7;
        border-color: #0a58ca;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background-color: #0d6efd;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        padding: 0.5rem 1rem;
    }
    
    .stDownloadButton > button:hover {
        background-color: #0b5ed7;
    }
    
    /* Text input */
    .stTextInput > div > div > input {
        border-radius: 6px;
        border: 1px solid #ced4da;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #0d6efd;
        box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
    }
    
    /* Text area */
    .stTextArea textarea {
        border-radius: 6px;
        border: 1px solid #ced4da;
        font-size: 0.9rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #0d6efd;
        box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 500;
        border: 1px solid #dee2e6;
    }
    
    /* Metric */
    [data-testid="stMetricValue"] {
        font-size: 1.75rem;
        font-weight: 600;
        color: #1a1a1a;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Rubric Table */
    .rubric-table { 
        font-size: 0.875rem; 
        width: 100%; 
        border-collapse: collapse;
        margin-top: 0.5rem;
    }
    
    .rubric-table td { 
        padding: 0.75rem; 
        border: 1px solid #dee2e6;
        vertical-align: top;
        background-color: white;
    }
    
    .rubric-header { 
        font-weight: 600; 
        color: #495057;
        background-color: #f8f9fa;
        width: 100px;
    }
    
    /* Card Container */
    .card-container {
        background-color: white;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    /* Score badge */
    .score-display {
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        padding: 0.5rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    
    .score-low {
        background-color: #fff5f5;
        color: #c53030;
        border: 2px solid #fc8181;
    }
    
    .score-medium {
        background-color: #fffbf0;
        color: #c05621;
        border: 2px solid #f6ad55;
    }
    
    .score-high {
        background-color: #f0fdf4;
        color: #15803d;
        border: 2px solid #4ade80;
    }
    
    /* Dimension card */
    .dimension-card {
        background: white;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        padding: 1.25rem;
        height: 100%;
        transition: box-shadow 0.2s;
    }
    
    .dimension-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    }
    
    .dimension-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.25rem;
    }
    
    .dimension-question {
        font-size: 0.875rem;
        color: #6c757d;
        font-style: italic;
        margin-bottom: 1rem;
    }
    
    /* Labels */
    .slider-label {
        font-size: 0.8rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

# --- Data Definitions ---
DIMENSIONS = [
    {
        'id': 'integration',
        'letter': 'I',
        'icon': '🔗',
        'title': 'Integration',
        'subtitle': 'Connectivity',
        'color': '#0d6efd',
        'lightColor': '#e7f1ff',
        'question': 'Is it an Island or an Ecosystem?',
        'leftLabel': 'Closed / Island',
        'rightLabel': 'Open API Platform',
        'rubric': {
            'low': 'Closed system. No APIs. Hard to export data. "Walled Garden."',
            'medium': 'Some integrations (e.g., connects to Xero), but largely self-contained.',
            'high': 'API-first architecture. Allows developers to build on top. Two-way data flow.'
        }
    },
    {
        'id': 'monetization',
        'letter': 'M',
        'icon': '💰',
        'title': 'Monetization',
        'subtitle': 'Unit Economics',
        'color': '#198754',
        'lightColor': '#d1f4e8',
        'question': 'Growth at all costs or sustainable?',
        'leftLabel': 'Burning Cash',
        'rightLabel': 'Sustainable Profit',
        'rubric': {
            'low': 'Freemium with no clear upsell. High burn. Subsidized by VC money.',
            'medium': 'Generating revenue (interchange fees), but barely covering costs.',
            'high': 'Strong LTV > CAC. Diversified revenue (Sub + Trans + Data).'
        }
    },
    {
        'id': 'painPoint',
        'letter': 'P',
        'icon': '🩹',
        'title': 'Pain Point',
        'subtitle': 'Differentiation',
        'color': '#dc3545',
        'lightColor': '#ffe5e8',
        'question': 'Vitamin or Painkiller?',
        'leftLabel': 'Nice-to-have (UI)',
        'rightLabel': '10x Solution',
        'rubric': {
            'low': 'Cosmetic changes. Just a prettier app for a standard bank account.',
            'medium': 'Reduces friction (faster onboarding), but core product is standard.',
            'high': 'Solves deep friction (e.g., instant cross-border). Users cannot go back.'
        }
    },
    {
        'id': 'automation',
        'letter': 'A',
        'icon': '🤖',
        'title': 'Automation',
        'subtitle': 'Tech Depth',
        'color': '#6610f2',
        'lightColor': '#f0e7ff',
        'question': 'Wrapper or Deep Tech?',
        'leftLabel': 'Human/Manual',
        'rightLabel': 'AI/Algorithmic',
        'rubric': {
            'low': 'Manual processes behind scenes. Rule-based logic only.',
            'medium': 'Some automation in KYC, but support is human-heavy.',
            'high': 'Proprietary AI/ML models. Algorithmic underwriting. Self-driving finance.'
        }
    },
    {
        'id': 'compliance',
        'letter': 'C',
        'icon': '⚖️',
        'title': 'Compliance',
        'subtitle': 'Trust',
        'color': '#fd7e14',
        'lightColor': '#fff3e6',
        'question': 'Regulatory Arbitrage or Trust?',
        'leftLabel': 'Grey Area',
        'rightLabel': 'Fully Licensed',
        'rubric': {
            'low': 'Unregulated. Operating across borders to avoid rules.',
            'medium': 'Partnering with a sponsor bank (BaaS) to rent a license.',
            'high': 'Full Banking Charter. Direct regulator relationship. Heavy compliance.'
        }
    },
    {
        'id': 'target',
        'letter': 'T',
        'icon': '🎯',
        'title': 'Target',
        'subtitle': 'Inclusion',
        'color': '#0dcaf0',
        'lightColor': '#e7f8fc',
        'question': 'Mass Market or Niche?',
        'leftLabel': 'Mass Market',
        'rightLabel': 'Underserved Niche',
        'rubric': {
            'low': 'Competing for prime customers (High FICO) like major banks.',
            'medium': 'Millennials/Gen-Z focus, but still generally bankable.',
            'high': 'Unbanked, gig-workers, immigrants, or specific vertical niches.'
        }
    }
]

# --- Helper Functions ---
def get_score_color(score):
    if score < 30: return "#c53030"
    if score < 70: return "#c05621"
    return "#15803d"

def get_score_class(score):
    if score < 30: return "score-low"
    if score < 70: return "score-medium"
    return "score-high"

def get_score_label(score):
    if score < 30: return "Low Impact"
    if score < 70: return "Medium Impact"
    return "High Impact"

def create_radar_chart(values, show_benchmark):
    categories = [d['title'] for d in DIMENSIONS]
    
    r_values = list(values) + [values[0]]
    theta_values = categories + [categories[0]]
    
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=r_values,
        theta=theta_values,
        fill='toself',
        name='Current Analysis',
        line=dict(color='#0d6efd', width=2),
        fillcolor='rgba(13, 110, 253, 0.2)',
        marker=dict(size=8, color='#0d6efd')
    ))

    if show_benchmark:
        bank_values = [20, 80, 20, 30, 95, 20] 
        bank_r = bank_values + [bank_values[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=bank_r,
            theta=theta_values,
            fill='toself',
            name='Traditional Bank',
            line=dict(color='#6c757d', width=2, dash='dash'),
            fillcolor='rgba(108, 117, 125, 0.1)',
            marker=dict(size=6, color='#6c757d')
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=11, color='#495057'),
                gridcolor='#dee2e6',
                linecolor='#dee2e6'
            ),
            angularaxis=dict(
                gridcolor='#dee2e6',
                linecolor='#dee2e6',
                tickfont=dict(size=11, color='#495057', weight=600)
            ),
            bgcolor='white'
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=12, color='#495057')
        ),
        margin=dict(l=80, r=80, t=40, b=80),
        height=500,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="system-ui, -apple-system, sans-serif", color='#495057')
    )
    return fig

def generate_word_doc(company_name, avg_score, timestamp):
    doc = Document()
    
    heading = doc.add_heading('FINTECH IMPACT RADAR ANALYSIS', 0)
    heading.alignment = 1
    
    doc.add_paragraph()
    p = doc.add_paragraph()
    run = p.add_run(f"Company: {company_name if company_name else 'Not specified'}")
    run.bold = True
    run.font.size = Pt(14)
    
    p2 = doc.add_paragraph()
    run2 = p2.add_run(f"Analysis Date: {timestamp}")
    run2.font.size = Pt(10)
    run2.font.color.rgb = RGBColor(108, 117, 125)
    
    doc.add_heading(f'Overall IMPACT Score: {avg_score}/100', level=1)
    score_label = get_score_label(avg_score)
    p3 = doc.add_paragraph(f"Assessment: {score_label}")
    p3.runs[0].italic = True
    
    doc.add_page_break()
    
    for dim in DIMENSIONS:
        score = st.session_state[f"score_{dim['id']}"]
        notes = st.session_state[f"note_{dim['id']}"]
        
        doc.add_heading(f"{dim['icon']} {dim['title']} - {score}/100", level=2)
        doc.add_paragraph(f"Focus: {dim['subtitle']}")
        doc.add_paragraph(f"Key Question: {dim['question']}")
        
        doc.add_heading('Scoring Rubric:', level=3)
        doc.add_paragraph(f"Low (0-30): {dim['rubric']['low']}")
        doc.add_paragraph(f"Medium (31-70): {dim['rubric']['medium']}")
        doc.add_paragraph(f"High (71-100): {dim['rubric']['high']}")
        
        doc.add_heading('Analysis & Evidence:', level=3)
        if notes:
            doc.add_paragraph(notes)
        else:
            doc.add_paragraph("No notes recorded.")
        
        doc.add_paragraph("_" * 70)
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

def export_json():
    data = {
        'company_name': st.session_state.company_name,
        'timestamp': datetime.now().isoformat(),
        'overall_score': round(sum([st.session_state[f"score_{d['id']}"] for d in DIMENSIONS]) / 6),
        'dimensions': {}
    }
    
    for dim in DIMENSIONS:
        data['dimensions'][dim['id']] = {
            'title': dim['title'],
            'score': st.session_state[f"score_{dim['id']}"],
            'notes': st.session_state[f"note_{dim['id']}"]
        }
    
    return json.dumps(data, indent=2)

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

# Calculate metrics
current_scores = [st.session_state[f"score_{d['id']}"] for d in DIMENSIONS]
avg_score = round(sum(current_scores) / 6)

# --- SIDEBAR ---
with st.sidebar:
    st.title("📡 Analysis Controls")
    
    st.markdown("### Company Information")
    st.text_input("Company Name", placeholder="e.g., Revolut", key="company_name")
    
    st.markdown("")
    st.markdown("### Display Options")
    show_benchmark = st.checkbox("Show Traditional Bank Benchmark", value=True)
    
    st.markdown("---")
    
    st.markdown("### Summary Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Overall Score", f"{avg_score}")
    with col2:
        high_scores = sum(1 for s in current_scores if s >= 70)
        st.metric("High Scores", f"{high_scores}/6")
    
    st.markdown("---")
    
    st.markdown("### Export Options")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    docx_file = generate_word_doc(st.session_state.company_name, avg_score, timestamp)
    st.download_button(
        label="Download Report (DOCX)", 
        data=docx_file,
        file_name=f"IMPACT_Analysis_{st.session_state.company_name or 'Company'}_{datetime.now().strftime('%Y%m%d')}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        use_container_width=True
    )
    
    json_data = export_json()
    st.download_button(
        label="Download Data (JSON)",
        data=json_data,
        file_name=f"IMPACT_Data_{st.session_state.company_name or 'Company'}_{datetime.now().strftime('%Y%m%d')}.json",
        mime="application/json",
        use_container_width=True
    )
    
    st.markdown("")
    
    if st.button("Reset Analysis", use_container_width=True):
        reset_state()
        st.rerun()
    
    st.markdown("---")
    
    with st.expander("About IMPACT Framework"):
        st.markdown("""
        **IMPACT** is a framework for analyzing fintech companies across six key dimensions:
        
        - **Integration**: Connectivity & ecosystem
        - **Monetization**: Unit economics
        - **Pain Point**: Differentiation
        - **Automation**: Tech depth
        - **Compliance**: Trust & regulation
        - **Target**: Market inclusion
        """)

# --- MAIN CONTENT ---
st.title("Fintech IMPACT Radar")
st.markdown("A comprehensive framework for evaluating fintech innovation and disruption potential")

st.markdown("")

# Top section with chart and overview
col1, col2 = st.columns([1.5, 1])

with col1:
    st.markdown("### Radar Visualization")
    radar_fig = create_radar_chart(current_scores, show_benchmark)
    st.plotly_chart(radar_fig, use_container_width=True)

with col2:
    st.markdown("### Overall Assessment")
    
    score_class = get_score_class(avg_score)
    st.markdown(f"""
        <div class='score-display {score_class}'>
            {avg_score} / 100
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"**Classification:** {get_score_label(avg_score)}")
    
    st.markdown("")
    st.markdown("**Dimension Scores:**")
    
    for dim in DIMENSIONS:
        score = st.session_state[f"score_{dim['id']}"]
        
        col_icon, col_name, col_score = st.columns([0.5, 3, 1])
        with col_icon:
            st.markdown(f"<div style='color: {dim['color']}; font-size: 1.2rem;'>{dim['icon']}</div>", unsafe_allow_html=True)
        with col_name:
            st.markdown(f"**{dim['title']}**")
        with col_score:
            st.markdown(f"<span style='color: {dim['color']}; font-weight: 700;'>{score}</span>", unsafe_allow_html=True)

st.markdown("---")

# Dimension analysis grid
st.markdown("### Dimension Analysis")
st.markdown("Score each dimension from 0 (low) to 100 (high) based on the evidence and rubric provided")

st.markdown("")

# Create 2x3 grid
for row in range(3):
    cols = st.columns(2)
    for col_idx in range(2):
        dim_idx = row * 2 + col_idx
        if dim_idx < len(DIMENSIONS):
            dim = DIMENSIONS[dim_idx]
            
            with cols[col_idx]:
                # Color-coded header bar
                st.markdown(f"""
                    <div style='background: {dim['lightColor']}; padding: 0.75rem 1rem; 
                                border-radius: 8px 8px 0 0; border-left: 4px solid {dim['color']};'>
                        <div style='display: flex; justify-content: space-between; align-items: center;'>
                            <div>
                                <div style='font-size: 1.1rem; font-weight: 600; color: #2d3748;'>
                                    {dim['icon']} {dim['title']}
                                </div>
                                <div style='font-size: 0.85rem; color: #6c757d; margin-top: 0.15rem;'>
                                    {dim['subtitle']}
                                </div>
                            </div>
                            <div style='font-size: 1.5rem; font-weight: 700; color: {dim['color']};'>
                                {st.session_state[f"score_{dim['id']}"]}
                            </div>
                        </div>
                    </div>
                    <div style='background: white; border: 1px solid #e9ecef; 
                                border-top: none; border-radius: 0 0 8px 8px; padding: 1rem;'>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<div class='dimension-question'>{dim['question']}</div>", unsafe_allow_html=True)
                
                # Slider
                st.slider(
                    f"Score for {dim['title']}", 
                    0, 100, 
                    key=f"score_{dim['id']}", 
                    label_visibility="collapsed"
                )
                
                # Labels
                l, r = st.columns(2)
                with l:
                    st.markdown(f"<div class='slider-label'>← {dim['leftLabel']}</div>", unsafe_allow_html=True)
                with r:
                    st.markdown(f"<div class='slider-label' style='text-align: right;'>{dim['rightLabel']} →</div>", unsafe_allow_html=True)
                
                # Expander for rubric and notes
                with st.expander("View Rubric & Add Notes"):
                    st.markdown("**Scoring Rubric**")
                    st.markdown(f"""
                    <table class="rubric-table">
                        <tr>
                            <td class="rubric-header">Low (0-30)</td>
                            <td>{dim['rubric']['low']}</td>
                        </tr>
                        <tr>
                            <td class="rubric-header">Medium (31-70)</td>
                            <td>{dim['rubric']['medium']}</td>
                        </tr>
                        <tr>
                            <td class="rubric-header">High (71-100)</td>
                            <td>{dim['rubric']['high']}</td>
                        </tr>
                    </table>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("")
                    st.markdown("**Evidence & Notes**")
                    st.text_area(
                        "Notes", 
                        key=f"note_{dim['id']}", 
                        height=100, 
                        placeholder="Document your reasoning and evidence for this score...",
                        label_visibility="collapsed"
                    )
                
                st.markdown("</div></div>", unsafe_allow_html=True)
                st.markdown("")

st.markdown("---")
st.markdown(f"""
<div style='text-align: center; color: #6c757d; padding: 1rem;'>
    <p style='margin: 0; font-size: 0.9rem;'>Fintech IMPACT Radar | Analysis Date: {datetime.now().strftime("%Y-%m-%d")}</p>
</div>
""", unsafe_allow_html=True)