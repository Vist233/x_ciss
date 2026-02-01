"""可复用UI组件模块"""
import streamlit as st
from typing import Dict, List, Optional


def apply_custom_css():
    """应用自定义CSS样式"""
    st.markdown("""
    <style>
    /* 全局样式 - 强制全宽 */
    .main {
        padding-top: 0rem;
    }
    .block-container {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    section.main > div {
        max-width: 100% !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }
    div[data-testid="stAppViewContainer"] > section {
        max-width: 100% !important;
    }
    div[data-testid="stVerticalBlock"] {
        max-width: 100% !important;
    }
    
    /* 患者信息卡片 */
    .patient-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .patient-card h3 {
        margin: 0;
        font-size: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .patient-info {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .patient-info-item {
        display: flex;
        flex-direction: column;
    }
    
    .patient-info-label {
        font-size: 0.85rem;
        opacity: 0.9;
        margin-bottom: 0.25rem;
    }
    
    .patient-info-value {
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* 进度条 */
    .progress-steps {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
        position: relative;
    }
    
    .progress-step {
        flex: 1;
        text-align: center;
        position: relative;
        padding: 0.5rem;
    }
    
    .progress-step.active {
        font-weight: 700;
        color: #FFD700;
    }
    
    .progress-step.completed {
        opacity: 0.8;
    }
    
    /* 对话气泡 */
    .chat-message {
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 10px;
        max-width: 80%;
    }
    
    .chat-doctor {
        background-color: #E3F2FD;
        margin-right: auto;
        border-left: 4px solid #2196F3;
    }
    
    .chat-patient {
        background-color: #F3E5F5;
        margin-left: auto;
        border-left: 4px solid #9C27B0;
    }
    
    .chat-timestamp {
        font-size: 0.75rem;
        color: #666;
        margin-bottom: 0.25rem;
    }
    
    .chat-role {
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    /* 病例卡片 */
    .case-card {
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .case-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .case-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;
    }
    
    .case-id {
        font-weight: 600;
        color: #1976D2;
    }
    
    .similarity-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* 标签 */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.85rem;
        font-weight: 500;
        margin: 0.25rem;
    }
    
    .badge-high {
        background-color: #FFEBEE;
        color: #C62828;
    }
    
    .badge-medium {
        background-color: #FFF3E0;
        color: #E65100;
    }
    
    .badge-low {
        background-color: #E8F5E9;
        color: #2E7D32;
    }
    
    .badge-success {
        background-color: #E8F5E9;
        color: #2E7D32;
    }
    
    .badge-info {
        background-color: #E3F2FD;
        color: #1565C0;
    }
    
    .badge-warning {
        background-color: #FFF3E0;
        color: #E65100;
    }
    
    /* 异常指标卡片 */
    .abnormal-card {
        border-left: 4px solid #F44336;
        background-color: #FFEBEE;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    .abnormal-name {
        font-weight: 600;
        font-size: 1.1rem;
        color: #C62828;
        margin-bottom: 0.5rem;
    }
    
    .abnormal-value {
        font-size: 1.3rem;
        font-weight: 700;
        color: #D32F2F;
        margin-bottom: 0.5rem;
    }
    
    /* 引用卡片 */
    .reference-card {
        background-color: #F5F5F5;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    
    .reference-quote {
        font-style: italic;
        color: #424242;
        margin-bottom: 0.5rem;
    }
    
    .reference-source {
        font-size: 0.85rem;
        color: #666;
    }

    /* 录音指示器样式 */
    .recording-dot {
        height: 12px;
        width: 12px;
        background-color: #ff4b4b;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 0 rgba(255, 75, 75, 0.4);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(255, 75, 75, 0); }
        100% { box-shadow: 0 0 0 0 rgba(255, 75, 75, 0); }
    }

    .status-panel {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: center;
        align-items: center;
        position: relative;
    }

    .searching-text {
        color: #667eea;
        font-weight: 500;
        display: flex;
        align-items: center;
        position: absolute;
        right: 1rem;
    }

    .searching-dots:after {
        content: ' .';
        animation: dots 1.5s steps(5, end) infinite;
    }

    @keyframes dots {
        0%, 20% { content: ' .'; }
        40% { content: ' . .'; }
        60% { content: ' . . .'; }
        80%, 100% { content: ''; }
    }
    </style>
    """, unsafe_allow_html=True)


def render_patient_card(patient: Dict):
    """渲染患者信息卡片"""
    st.markdown(f"""
    <div class="patient-card">
        <h3>🏥 医生工作台 (Demo)</h3>
        <div class="patient-info">
            <div class="patient-info-item">
                <span class="patient-info-label">患者ID</span>
                <span class="patient-info-value">{patient.get('patient_id', 'N/A')}</span>
            </div>
            <div class="patient-info-item">
                <span class="patient-info-label">姓名</span>
                <span class="patient-info-value">{patient.get('name', 'N/A')}</span>
            </div>
            <div class="patient-info-item">
                <span class="patient-info-label">性别</span>
                <span class="patient-info-value">{patient.get('gender', 'N/A')}</span>
            </div>
            <div class="patient-info-item">
                <span class="patient-info-label">年龄</span>
                <span class="patient-info-value">{patient.get('age', 'N/A')}岁</span>
            </div>
            <div class="patient-info-item">
                <span class="patient-info-label">就诊科室</span>
                <span class="patient-info-value">{patient.get('department', 'N/A')}</span>
            </div>
            <div class="patient-info-item">
                <span class="patient-info-label">就诊日期</span>
                <span class="patient-info-value">{patient.get('visit_date', 'N/A')}</span>
            </div>
        </div>
        <div style="margin-top: 1rem;">
            <span class="patient-info-label">主诉</span>
            <div style="font-size: 1.1rem; margin-top: 0.5rem;">{patient.get('chief_complaint', 'N/A')}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_progress_steps(current_page: str):
    """渲染进度条"""
    steps = [
        ("问诊", "page1"),
        ("开检查", "page2"),
        ("查结果", "page3"),
        ("写病历", "page4")
    ]
    
    step_html = '<div class="progress-steps">'
    for step_name, step_id in steps:
        class_name = "progress-step"
        if step_id == current_page:
            class_name += " active"
        step_html += f'<div class="{class_name}">{step_name}</div>'
    step_html += '</div>'
    
    st.markdown(step_html, unsafe_allow_html=True)


def render_badge(text: str, badge_type: str = "info") -> str:
    """生成标签HTML
    
    Args:
        text: 标签文本
        badge_type: 标签类型 (high/medium/low/success/info/warning)
        
    Returns:
        HTML字符串
    """
    return f'<span class="badge badge-{badge_type}">{text}</span>'


def render_case_card(case: Dict):
    """渲染相似病例卡片 - 标准病历格式（使用原生Streamlit组件）"""
    # 头部信息
    header_text = f"姓名:{case.get('patient_name', 'N/A')}　　性别:{case.get('gender', 'N/A')}　　年龄:{case.get('age', 'N/A')}　　门诊号:{case.get('case_id', 'N/A')}　　就诊科室:{case.get('department', 'N/A')}　　相似度:{case.get('similarity', 0):.2f}"
    
    with st.container(border=True):
        st.markdown(f"**{header_text}**")
        st.divider()
        
        # 使用两列布局展示病历内容
        col1, col2 = st.columns([1, 4])
        
        fields = [
            ("主诉:", case.get('chief_complaint', 'N/A')),
            ("现病史:", case.get('history_present', 'N/A')),
            ("既往史:", case.get('history_past', 'N/A')),
            ("中医四诊:", case.get('tcm_diagnosis_info', 'N/A')),
            ("体格检查:", case.get('physical_exam', 'N/A')),
            ("生命体征:", case.get('vital_signs', 'N/A')),
            ("西医诊断:", case.get('western_diagnosis', 'N/A')),
            ("中医诊断:", case.get('tcm_diagnosis', 'N/A')),
            ("辅助检查:", case.get('auxiliary_exam', 'N/A')),
            ("药品处方:", case.get('prescription', 'N/A')),
            ("建议:", case.get('advice', 'N/A')),
            ("治疗效果:", case.get('treatment_effect', 'N/A')),
        ]
        
        for label, value in fields:
            c1, c2 = st.columns([1, 5])
            with c1:
                st.markdown(f"**{label}**")
            with c2:
                st.markdown(value)


def render_abnormal_card(item: Dict):
    """渲染异常指标卡片"""
    st.markdown(f"""
    <div class="abnormal-card">
        <div class="abnormal-name">{item.get('name', 'N/A')}</div>
        <div class="abnormal-value">{item.get('value', 'N/A')}</div>
        <div style="margin-bottom: 0.5rem;">
            <strong>临床含义:</strong> {item.get('meaning', 'N/A')}
        </div>
        <div style="font-size: 0.9rem; color: #666;">
            <strong>需要关注:</strong> {item.get('attention', 'N/A')}
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_reference_card(reference: Dict, quote: str):
    """渲染引用卡片"""
    st.markdown(f"""
    <div class="reference-card">
        <div class="reference-quote">"{quote}"</div>
        <div class="reference-source">
            — {reference.get('book', 'N/A')} · {reference.get('chapter', 'N/A')}
        </div>
    </div>
    """, unsafe_allow_html=True)
