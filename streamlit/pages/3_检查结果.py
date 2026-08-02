"""页面3: 检查结果 - 异常指标展示"""
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import load_lab_table


def render_page3():
    """渲染检查结果页面"""
    
    st.subheader("检查结果")
    
    # === 上半部分: 异常指标截图 + 医学参考 ===
    st.markdown("### 异常指标")
    
    # 获取截图路径
    data_dir = Path(__file__).parent.parent / "data"
    screenshot1 = data_dir / "Screenshot 2026-02-01 at 11.28.11.png"
    screenshot2 = data_dir / "Screenshot 2026-02-01 at 11.28.19.png"
    
    # 显示两个异常指标
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 嗜酸小板数目")
        if screenshot1.exists():
            st.image(str(screenshot1), use_container_width=True)
        else:
            st.error("截图文件不存在")
        
        # 医学参考信息
        with st.container(border=True):
            st.markdown("**医学参考**")
            st.markdown("""
            **正常参考范围**: 30-350 cells/µL 或 0.04-0.4 × 10⁹/L
            
            **当前值**: 338.0 ×10⁹/L
            
            **临床意义**: 嗜酸性粒细胞升高常提示过敏反应，在过敏性鼻炎患者中较为常见。
            该数值接近正常上限，结合其他指标（如嗜酸性粒细胞比例）综合判断过敏严重程度。
            """)
            
            st.caption("参考来源: Cleveland Clinic, WebMD, Medical News Today")
    
    with col2:
        st.markdown("#### 嗜酸板压积")
        if screenshot2.exists():
            st.image(str(screenshot2), use_container_width=True)
        else:
            st.error("截图文件不存在")
        
        # 医学参考信息
        with st.container(border=True):
            st.markdown("**医学参考**")
            st.markdown("""
            **正常参考范围**: 0.0-6.0% (占白细胞总数的百分比)
            
            **当前值**: 32.00% 
            
            **临床意义**: 嗜酸性粒细胞比例显著升高强烈提示活跃的过敏性炎症反应。
            研究表明，该指标升高与过敏性鼻炎的严重程度呈正相关。高比例嗜酸性粒细胞
            常见于哮喘、过敏性鼻炎、特应性皮炎等过敏性疾病。
            """)
            
            st.caption("参考来源: NIH, Healthline, Cleveland Clinic")
    
    st.markdown("---")
    
    # === 下半部分: 原始检查报告 ===
    st.markdown("### 原始检查报告")
    
    # 显示原始报告截图
    original_report = data_dir / "Screenshot 2026-02-01 at 11.27.59.png"
    
    if original_report.exists():
        st.image(str(original_report), use_container_width=True)
    else:
        st.warning("原始报告截图不存在，显示数据表格")
        
        # 备用：显示数据表格
        lab_data = load_lab_table()
        
        if lab_data:
            df = pd.DataFrame(lab_data)
            
            # 样式化表格
            def highlight_abnormal(row):
                """高亮异常值"""
                if row.get('标记') == '↑':
                    return ['background-color: #FFEBEE'] * len(row)
                return [''] * len(row)
            
            if '标记' in df.columns:
                styled_df = df.style.apply(highlight_abnormal, axis=1)
                st.dataframe(styled_df, use_container_width=True, height=400)
            else:
                st.dataframe(df, use_container_width=True, height=400)
            
            # 导出按钮
            col1, col2 = st.columns([1, 5])
            with col1:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "📥 导出CSV",
                    csv,
                    "lab_results.csv",
                    "text/csv",
                    use_container_width=True
                )
        else:
            st.info("暂无检查报告数据")


if __name__ == "__main__":
    render_page3()
