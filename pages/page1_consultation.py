"""页面1: 问诊 (录音文本 + 相似病例推荐)"""
import streamlit as st
import sys
from pathlib import Path

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import (
    load_transcript,
    load_dialogue_highlights,
    load_similar_cases
)
from utils.ui_components import render_case_card


def render_page1():
    """渲染问诊页面"""
    
    # === 状态指示区 ===
    st.markdown(f"""
    <div class="status-panel">
        <div style="display: flex; align-items: center;">
            <span class="recording-dot"></span>
            <span style="font-weight: 600; color: #ff4b4b;">实时录音中...</span>
        </div>
        <div class="searching-text">
            <span class="searching-dots"></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # === 对话摘要区 ===
    st.subheader("对话摘要")
    st.caption("以下内容完全引用自原句要点")
    
    # 加载对话数据（用于统计）
    transcript = load_transcript()
    
    highlights = load_dialogue_highlights()
    if highlights:
        for highlight in highlights:
            st.markdown(f"{highlight}")
    else:
        st.info("暂无要点摘要")
    
    # 统计信息
    # st.markdown("<br>", unsafe_allow_html=True)
    
    # === 分隔线 ===
    st.markdown("---")
    
    # === 下半部分: 相似病例区 (30% 高度) ===
    st.subheader("相似病例")
    
    cases = load_similar_cases()
    if cases:
        # 一块是一行，横着铺开
        for idx, case in enumerate(cases):
            with st.container():
                render_case_card(case)
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("暂无相似病例")


@st.dialog("病例详情")
def show_case_detail(case: dict):
    """显示病例详细信息的模态框"""
    st.markdown(f"### 病例 #{case.get('case_id', 'N/A')}")
    st.markdown(f"**相似度**: {case.get('similarity', 0):.2f}")
    st.markdown("---")
    st.markdown(f"**主诉**: {case.get('chief_complaint', 'N/A')}")
    st.markdown(f"**时间线**: {case.get('timeline', 'N/A')}")
    st.markdown(f"**关键发现**: {case.get('key_findings', 'N/A')}")
    st.markdown(f"**最终诊断**: {case.get('diagnosis', 'N/A')}")
    st.markdown(f"**转归**: {case.get('outcome', 'N/A')}")


if __name__ == "__main__":
    render_page1()
