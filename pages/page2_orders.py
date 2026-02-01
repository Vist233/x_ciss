"""页面2: 开检查 (排序选择列表 + 提交弹窗提醒 + 书本引用)"""
import streamlit as st
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import (
    load_order_sets,
    load_orders_ranked,
    load_order_warnings
)
from utils.ui_components import render_badge, render_reference_card


def render_page2():
    """渲染开检查页面"""
    
    # 顶部工具栏：搜索
    col_search, col_filter = st.columns([4, 1])
    with col_search:
        search_query = st.text_input("搜索", placeholder="输入关键词快速查找检查项目...", label_visibility="collapsed")
    with col_filter:
        # 占位，可以放筛选器
        st.markdown("")

    st.markdown("<br>", unsafe_allow_html=True)

    # 初始化已选检查
    if 'selected_items' not in st.session_state:
        st.session_state['selected_items'] = []
    
    # 加载所有检查数据
    orders = load_orders_ranked()
    
    # 按照order字段排序（从小到大，即从最相关到最不相关）
    if orders:
        orders = sorted(orders, key=lambda x: x.get('order', 999))
    
    # 过滤逻辑
    if search_query:
        orders = [o for o in orders if search_query in o.get('order_name', '')]
    
    if orders:
        st.markdown(f"### 检查项目列表 ({len(orders)})")
        
        # 两栏布局
        for i in range(0, len(orders), 2):
            col1, col2 = st.columns(2)
            
            # 左列
            with col1:
                order = orders[i]
                order_name = order.get('order_name', '')
                reason = order.get('reason', '')
                priority = order.get('priority', '中')
                
                # 使用容器包裹每一行，增加视觉层级
                with st.container(border=True):
                    # 调整列比例，让复选框更紧凑，右侧增加Tag位置
                    col_check, col_info, col_tag = st.columns([0.5, 7, 1.5])
                    
                    with col_check:
                        # 使用空的markdown调整垂直对齐
                        st.markdown('<div style="height: 6px;"></div>', unsafe_allow_html=True)
                        is_selected = st.checkbox(
                            "选",
                            value=order_name in st.session_state['selected_items'],
                            key=f"check_{order_name}",
                            label_visibility="hidden"
                        )
                    
                    with col_info:
                        # 优化排版：加大加粗名称，理由用灰色小字
                        st.markdown(f"<div style='font-size: 1.05rem; font-weight: 600; color: #1f2937;'>{order_name}</div>", unsafe_allow_html=True)

                    with col_tag:
                        st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)
                    # 处理选择逻辑
                    if is_selected and order_name not in st.session_state['selected_items']:
                        st.session_state['selected_items'].append(order_name)
                    elif not is_selected and order_name in st.session_state['selected_items']:
                        st.session_state['selected_items'].remove(order_name)
            
            # 右列（如果存在）
            if i + 1 < len(orders):
                with col2:
                    order = orders[i + 1]
                    order_name = order.get('order_name', '')
                    reason = order.get('reason', '')
                    priority = order.get('priority', '中')
                    
                    # 使用容器包裹每一行，增加视觉层级
                    with st.container(border=True):
                        # 调整列比例，让复选框更紧凑，右侧增加Tag位置
                        col_check, col_info, col_tag = st.columns([0.5, 7, 1.5])
                        
                        with col_check:
                            # 使用空的markdown调整垂直对齐
                            st.markdown('<div style="height: 6px;"></div>', unsafe_allow_html=True)
                            is_selected = st.checkbox(
                                "选",
                                value=order_name in st.session_state['selected_items'],
                                key=f"check_{order_name}",
                                label_visibility="hidden"
                            )
                        
                        with col_info:
                            # 优化排版：加大加粗名称，理由用灰色小字
                            st.markdown(f"<div style='font-size: 1.05rem; font-weight: 600; color: #1f2937;'>{order_name}</div>", unsafe_allow_html=True)

                        with col_tag:
                            st.markdown('<div style="height: 4px;"></div>', unsafe_allow_html=True)
                        # 处理选择逻辑
                        if is_selected and order_name not in st.session_state['selected_items']:
                            st.session_state['selected_items'].append(order_name)
                        elif not is_selected and order_name in st.session_state['selected_items']:
                            st.session_state['selected_items'].remove(order_name)

    else:
        st.info("未找到匹配的检查项目")
    
    st.markdown("---")
    
    # === 底部提交区 ===
    # 增加顶部间距，让按钮区域更独立
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("提交检查申请", type="primary", use_container_width=True):
        if st.session_state['selected_items']:
            show_order_warnings()
        else:
            st.warning("⚠️ 请至少选择一项检查项目")


@st.dialog("AI检查提醒", width="large")
def show_order_warnings():
    """显示检查提醒模态框 - 基于智能规则"""
    from utils.data_loader import load_order_check_rules, load_transcript
    
    # 加载规则和对话
    rules = load_order_check_rules()
    transcript = load_transcript()
    
    # 获取用户选择的检查项目
    selected = st.session_state.get('selected_items', [])
    
    if not rules:
        st.error("规则文件加载失败")
        return
    
    # 提取病人症状关键词（从对话中）
    patient_keywords = []
    if transcript:
        for msg in transcript:
            if msg.get('role') == '病人':
                patient_keywords.append(msg.get('text', ''))
    patient_text = ' '.join(patient_keywords)
    
    # === 1. 检查冲突 ===
    conflicts_found = []
    for conflict in rules.get('conflicts', []):
        conflict_items = conflict.get('items', [])
        # 检查是否同时选择了冲突组中的多个项目
        selected_in_group = [item for item in conflict_items if item in selected]
        if len(selected_in_group) >= 2:
            conflicts_found.append({
                'group': conflict.get('group'),
                'items': selected_in_group,
                'reason': conflict.get('reason'),
                'suggestion': conflict.get('suggestion')
            })
    
    # === 2. 检查遗漏 ===
    missing_found = []
    for missing in rules.get('missing_checks', []):
        item_name = missing.get('missing_item')
        keywords = missing.get('symptom_keywords', [])
        
        # 如果该项目没被选择，且病人症状匹配关键词
        if item_name not in selected:
            # 检查是否有关键词匹配
            if any(kw in patient_text for kw in keywords):
                missing_found.append({
                    'item': item_name,
                    'reason': missing.get('reason'),
                    'priority': missing.get('priority'),
                    'warning': missing.get('warning')
                })
    
    # === 显示提示 ===
    has_issues = len(conflicts_found) > 0 or len(missing_found) > 0
    
    if has_issues:
        st.markdown("### 请您再次检查！")
        
        # 显示冲突
        if conflicts_found:
            st.markdown("#### 检查项目可能冲突")
            for idx, conflict in enumerate(conflicts_found):
                with st.container(border=True):
                    st.markdown(f"**{conflict['group']}**")
                    st.markdown(f"冲突项目: {', '.join(conflict['items'])}")
                    # st.caption(f"原因: {conflict['reason']}")
                    # st.info(conflict['suggestion'])
        
        # 显示遗漏
        if missing_found:
            st.markdown("#### 可能遗漏的检查")
            # 按优先级排序
            priority_order = {'高': 1, '中': 2, '低': 3}
            missing_found.sort(key=lambda x: priority_order.get(x.get('priority', '低'), 4))
            
            for idx, missing in enumerate(missing_found):
                with st.container(border=True):
                    priority_color = {
                        '高': ':red',
                        '中': ':orange',
                        '低': ':gray'
                    }.get(missing['priority'], '')
                    
                    st.markdown(f"{priority_color}[**{missing['item']}**]")
        
        # 操作按钮
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("继续提交", type="primary", use_container_width=True):
                st.toast("✓ 检查单已提交", icon="✅")
                st.session_state['selected_items'] = []
                st.rerun()
        with col2:
            if st.button("返回调整", use_container_width=True):
                st.rerun()
    else:
        st.success("✓ 未发现需要特别提醒的事项")
        if st.button("确认提交", type="primary", use_container_width=True):
            st.toast("✓ 检查单已提交", icon="✅")
            st.session_state['selected_items'] = []
            st.rerun()


if __name__ == "__main__":
    render_page2()
