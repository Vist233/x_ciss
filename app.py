"""医生工作台 - Streamlit Demo 主应用"""
import streamlit as st
from utils.data_loader import load_patient_info
from utils.ui_components import (
    apply_custom_css,
    render_patient_card,
    render_progress_steps
)
from pages.page1_consultation import render_page1
from pages.page2_orders import render_page2
from pages.page3_results import render_page3
from pages.page4_record import render_page4


# 页面配置
st.set_page_config(
    page_title="Demo",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """主函数"""
    
    # 应用自定义CSS
    # 应用自定义CSS
    # apply_custom_css()
    
    # === 顶部固定区: 患者信息卡 ===
    patient = load_patient_info()
    # if patient:
    #     render_patient_card(patient)
    
    # === 左侧导航栏 ===
    # with st.sidebar:
    #     st.markdown("## 导航菜单")
    #     
    #     page = st.radio(
    #         "选择功能模块",
    #         options=[
    #             ("page1", "问诊"),
    #             ("page2", "开检查"),
    #             ("page3", "检查结果"),
    #             ("page4", "病历单")
    #         ],
    #         format_func=lambda x: x[1],
    #         key="page_selector"
    #     )
    #     
    #     current_page = page[0]
    
    current_page = "page4"
        
    
    # === 主内容区: 根据选择渲染对应页面 ===
    if current_page == "page1":
        render_page1()
    elif current_page == "page2":
        render_page2()
    elif current_page == "page3":
        render_page3()
    elif current_page == "page4":
        render_page4()


if __name__ == "__main__":
    main()
