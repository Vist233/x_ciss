# 线上静态演示

`web/` 是部署到 `hospital.zhangyvjing.com` 的唯一线上版本。它由原生 HTML、CSS 和 JavaScript 构成，浏览器直接读取 `data/` 中的示例 JSON 与图片并完成交互。

它不运行 Python、Streamlit、数据库或模型服务；`worker.js` 只通过 Cloudflare ASSETS 分发本目录资源。

## 本地预览

```bash
python3 -m http.server 8787
```

打开 `http://127.0.0.1:8787/`。

## 发布

从仓库根目录执行：

```bash
node scripts/verify-static-assets.mjs
npx wrangler deploy
```

发布前的完整性检查会确认页面使用的全部 JSON 与 WebP 资源均在本目录内。
