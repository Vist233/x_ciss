# Streamlit 原型

这是医疗黑客松期间保留的原始交互原型，用于记录产品流程的早期实现。当前线上体验由仓库根目录的 `web/` 静态版本提供；本目录不参与 Cloudflare 部署。

## 运行

```bash
pip install -r requirements.txt
streamlit run app.py
```

原型使用 `data/` 下的示例数据。请在本目录内执行命令，使 Streamlit 能读取 `.streamlit/config.toml` 和相对路径数据文件。
