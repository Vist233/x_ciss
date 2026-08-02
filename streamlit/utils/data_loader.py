"""数据加载工具模块"""
import json
import csv
from pathlib import Path
from typing import Any, Dict, List


def get_data_path(filename: str) -> Path:
    """获取数据文件路径"""
    return Path(__file__).parent.parent / "data" / filename


def load_json(filename: str) -> Any:
    """加载JSON文件
    
    Args:
        filename: JSON文件名
        
    Returns:
        解析后的Python对象
    """
    filepath = get_data_path(filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"警告: 文件 {filename} 不存在")
        return None
    except json.JSONDecodeError as e:
        print(f"警告: 文件 {filename} JSON格式错误: {e}")
        return None


def load_csv(filename: str) -> List[Dict[str, str]]:
    """加载CSV文件
    
    Args:
        filename: CSV文件名
        
    Returns:
        字典列表，每行为一个字典
    """
    filepath = get_data_path(filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print(f"警告: 文件 {filename} 不存在")
        return []


# 缓存加载的数据
_cache = {}


def load_patient_info() -> Dict:
    """加载患者基本信息"""
    if 'patient' not in _cache:
        _cache['patient'] = load_json('patient.json')
    return _cache['patient']


def load_summary() -> Dict:
    """加载快捷摘要"""
    if 'summary' not in _cache:
        _cache['summary'] = load_json('summary.json')
    return _cache['summary']


def load_transcript() -> List[Dict]:
    """加载问诊对话"""
    if 'transcript' not in _cache:
        _cache['transcript'] = load_json('transcript.json')
    return _cache['transcript']


def load_dialogue_highlights() -> List[str]:
    """加载对话要点"""
    if 'highlights' not in _cache:
        _cache['highlights'] = load_json('dialogue_highlights.json')
    return _cache['highlights']


def load_similar_cases() -> List[Dict]:
    """加载相似病例"""
    if 'cases' not in _cache:
        _cache['cases'] = load_json('similar_cases.json')
    return _cache['cases']


def load_order_sets() -> List[Dict]:
    """加载检查组套"""
    if 'order_sets' not in _cache:
        _cache['order_sets'] = load_json('order_sets.json')
    return _cache['order_sets']


def load_orders_ranked() -> List[Dict]:
    """加载推荐检查"""
    if 'orders' not in _cache:
        _cache['orders'] = load_json('orders_ranked.json')
    return _cache['orders']


def load_order_warnings() -> List[Dict]:
    """加载检查提醒"""
    if 'warnings' not in _cache:
        _cache['warnings'] = load_json('order_warnings.json')
    return _cache['warnings']


def load_order_check_rules() -> Dict:
    """加载检查规则（冲突和遗漏检测）"""
    if 'check_rules' not in _cache:
        _cache['check_rules'] = load_json('order_check_rules.json')
    return _cache['check_rules']


def load_abnormal_summary() -> Dict:
    """加载异常摘要"""
    if 'abnormal' not in _cache:
        _cache['abnormal'] = load_json('abnormal_summary.json')
    return _cache['abnormal']


def load_lab_table() -> List[Dict]:
    """加载检查报告表"""
    if 'lab_table' not in _cache:
        _cache['lab_table'] = load_csv('lab_table.csv')
    return _cache['lab_table']


def load_quote_pool() -> List[str]:
    """加载病史原句池"""
    if 'quote_pool' not in _cache:
        _cache['quote_pool'] = load_json('quote_pool_hpi.json')
    return _cache['quote_pool']


def load_pe_templates() -> List[Dict]:
    """加载体格检查模板"""
    if 'pe_templates' not in _cache:
        _cache['pe_templates'] = load_json('pe_templates.json')
    return _cache['pe_templates']


def load_sidebar_support() -> Dict:
    """加载辅助信息"""
    if 'sidebar' not in _cache:
        _cache['sidebar'] = load_json('sidebar_support.json')
    return _cache['sidebar']
