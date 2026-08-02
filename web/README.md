# 线上静态演示

`web/` 是 [智能医生工作台](https://zhangyvjing.com/x_ciss/) 的线上静态演示。它由原生 HTML、CSS 和 JavaScript 构成，浏览器直接读取 `data/` 中的示例 JSON 与图片并完成交互。

## 本地预览

```bash
python3 -m http.server 8787
```

打开 `http://127.0.0.1:8787/`。
