"""页面4: 病历单 - 自动生成门诊病历"""
import streamlit as st
import sys
from pathlib import Path
from typing import Dict, List

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import (
    load_patient_info,
    load_transcript,
    load_lab_table,
    load_sidebar_support,
    load_abnormal_summary
)


def extract_chief_complaint(transcript: List[Dict]) -> str:
    """从对话中提取主诉 - 病人第一次描述症状"""
    if not transcript:
        return ""
    
    # 找到病人第一次说的症状描述
    for msg in transcript:
        if msg.get('role') == '病人':
            text = msg.get('text', '')
            # 跳过简单的"没有"等回答
            if len(text) > 5 and '没有' not in text:
                return text
    
    return ""


def extract_present_illness(transcript: List[Dict]) -> str:
    """从对话中提取现病史 - 保留所有病人的陈述，原文不变"""
    if not transcript:
        return ""
    
    patient_statements = []
    for msg in transcript:
        if msg.get('role') == '病人':
            text = msg.get('text', '').strip()
            if text:
                patient_statements.append(text)
    
    # 保留换行，每条陈述独立一行
    return '\n'.join(patient_statements)


def extract_past_history(transcript: List[Dict]) -> str:
    """从对话中提取既往史"""
    if not transcript:
        return "既往体健，否认药敏史"
    
    # 查找是否有关于既往史、过敏史的问答
    for i, msg in enumerate(transcript):
        if msg.get('role') == '医生':
            text = msg.get('text', '')
            if '以前' in text or '过敏' in text or '既往' in text:
                # 获取病人的回答
                if i + 1 < len(transcript) and transcript[i + 1].get('role') == '病人':
                    patient_response = transcript[i + 1].get('text', '').strip()
                    if patient_response:
                        # 如果病人说没有，使用标准表述
                        if '没有' in patient_response:
                            return "既往体健，否认药敏史"
                        else:
                            return patient_response
    
    return "既往体健，否认药敏史"


def extract_physical_examination() -> str:
    """提取体格检查结果"""
    # 根据检查结果提取
    # 这里应该从检查报告中提取，目前使用示例数据
    return "鼻黏膜苍白，双侧下鼻甲肿大，总鼻道可见清水样鼻涕。"


def extract_vital_signs() -> str:
    """提取生命体征"""
    # 这里可以从patient数据或检查结果中提取
    return "收缩压:120mmHg、舒张压:78mmHg"


def extract_auxiliary_exams() -> str:
    """提取辅助检查"""
    # 从已选检查项目中提取
    if 'selected_items' in st.session_state and st.session_state['selected_items']:
        return '、'.join(st.session_state['selected_items'])
    return "过敏原检测、血常规"


def extract_suggestions() -> str:
    """从检查报告中提取建议"""
    # 这里可以从检查报告数据中提取
    return "避开过敏原，不适随诊。"


def format_medical_record(patient: Dict, chief_complaint: str, present_illness: str, 
                          past_history: str, physical_exam: str, vital_signs: str,
                          auxiliary_exams: str, suggestions: str) -> str:
    """格式化完整病历"""
    
    # 患者基本信息行
    header = f"姓名:{patient.get('name', '')}                         "
    header += f"性别:{patient.get('gender', '')}                     "
    header += f"年龄:{patient.get('age', '')}岁                    "
    header += f"门诊号:{patient.get('patient_id', '')} "
    header += f"就诊科室:{patient.get('department', '')}"
    
    # 组装病历内容
    record = f"{header}\n"
    record += f"主诉:         {chief_complaint}\n"
    record += f"现病史:       {present_illness}\n"
    record += f"既往史:       {past_history}\n"
    record += f"体格检查:     {physical_exam}\n"
    record += f"生命体征:     {vital_signs}\n"
    record += f"辅助检查:     {auxiliary_exams}\n"
    record += f"建议:         {suggestions}\n"
    
    return record


def render_page4():
    """渲染病历单页面"""
    
    st.subheader("病历撰写")
    
    # 加载基础数据
    patient_info = load_patient_info()
    transcript_data = load_transcript()
    
    # 初始化 session state 用于存储生成的病历
    if 'medical_record_text' not in st.session_state:
        chief_complaint = extract_chief_complaint(transcript_data)
        present_illness = extract_present_illness(transcript_data)
        past_history = extract_past_history(transcript_data)
        physical_exam = extract_physical_examination()
        vital_signs = extract_vital_signs()
        auxiliary_exams = extract_auxiliary_exams()
        suggestions = extract_suggestions()
        
        st.session_state['medical_record_text'] = format_medical_record(
            patient_info,
            chief_complaint,
            present_illness,
            past_history,
            physical_exam,
            vital_signs,
            auxiliary_exams,
            suggestions
        )
    
    # === 两栏布局 ===
    col_left, col_right = st.columns([7, 3])
    
    # --- 左侧：病历编辑区 ---
    with col_left:
        st.markdown("### 门诊病历")
        
        # 计算行数以自适应高度
        num_lines = st.session_state['medical_record_text'].count('\n') + 2
        
        edited_record = st.text_area(
            label="病历内容编辑",
            value=st.session_state['medical_record_text'],
            height=max(450, num_lines * 22),
            key="medical_record_editor",
            label_visibility="collapsed"
        )
        
        # 更新记录
        st.session_state['medical_record_text'] = edited_record
        
        # 操作按钮
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📋 复制病历", use_container_width=True):
                st.toast("✓ 已复制", icon="📋")
        with c2:
            if st.button("🖨️ 打印病历", use_container_width=True):
                st.toast("✓ 正在打印...", icon="🖨️")
        with c3:
            st.download_button(
                "📥 导出病历",
                st.session_state['medical_record_text'],
                "medical_record.md",
                "text/markdown",
                use_container_width=True
            )

    # --- 右侧：辅助参考栏 ---
    with col_right:
        st.markdown("### 🔍 辅助参考")
        
        # 1. 基本信息
        with st.container(border=True):
            st.markdown(f"**患者：{patient_info.get('name')} ({patient_info.get('gender')})**")
            st.caption(f"年龄：{patient_info.get('age')}岁 | ID：{patient_info.get('patient_id')}")
        
        # 2. 对话原句 (5行滚动)
        st.markdown("#### 💬 对话原文")
        dialogue_text = ""
        for msg in transcript_data:
            dialogue_text += f"{msg.get('text')}\n\n"
        
        st.text_area("对话内容", value=dialogue_text, height=200, disabled=True, label_visibility="collapsed")
        
        # 3. 检查关键线索
        st.markdown("#### 💡 关键线索")
        support = load_sidebar_support()
        abnormal = load_abnormal_summary()
        
        findings = []
        if support:
            findings.extend(support.get('key_tests', []))
        if abnormal:
            for item in abnormal.get('abnormal_items', []):
                findings.append(f"{item['name']}: {item['value']}")
        
        if findings:
            for finding in list(dict.fromkeys(findings))[:6]: # 去重并限额
                st.info(finding)
        else:
            st.caption("暂无关键线索")


if __name__ == "__main__":
    render_page4()
