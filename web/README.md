# 智能医生工作台 · 静态演示版（x_ciss-static）

一个面向路演/评委演示的 **AI 辅助门诊工作台** 前端 Demo。纯静态、**秒开**、免服务器、免运维。

线上地址：<https://ciss-101.pages.dev>

---

## ⚠️ 重要：这是一次“重写”，不是“打包”

**你现在看到的这个网页，和原始的 Streamlit 应用是两套完全独立的实现，只是长得一样、功能等价。**

| | 原始版本 | 本静态版本（本目录） |
|---|---|---|
| 技术栈 | **Python + Streamlit** | **原生 HTML / CSS / JavaScript** |
| 运行方式 | 需要一个**常驻的 Python 服务器进程**，浏览器通过 WebSocket 与之通信 | 浏览器直接运行，**没有任何后端** |
| 界面由谁渲染 | 服务器端 Python 每次交互重跑脚本，再把界面推给浏览器 | 浏览器端 JS 直接渲染 |
| 打开速度 | 取决于服务器 | **基本瞬开**（首屏 ~30KB） |
| 部署要求 | 需要能长期跑 Python 的主机（云主机 / Streamlit Cloud / HF Spaces） | 任意静态托管（Cloudflare Pages / GitHub Pages…） |

**换句话说：** 本目录里的代码**没有运行任何 Streamlit / Python**。它是照着原 Streamlit Demo 的界面与交互逻辑，用浏览器原生技术**逐页重新实现**的一份等价前端。两者共享同一批静态数据（`data/*.json`），因此内容、交互结果一致，但底层是两个不同的程序。

### 为什么要重写？

原始 Streamlit 应用**无法直接部署到纯静态托管**：Streamlit 本质是一个“必须一直活着”的服务器程序，而 Cloudflare Pages 只发静态文件、Workers 只跑短小的边缘函数，都装不下一个常驻的 Python 进程。

曾尝试用 [stlite](https://github.com/whitphx/stlite)（把 CPython 编译成 WebAssembly，塞进浏览器里跑）来免服务器部署——能跑，但每次打开都要**现下载并启动几十 MB 的 Python 运行时，耗时 10–30 秒**，演示体验极差。

本 Demo 全程**只读静态数据**（JSON / 图片），无后端、无数据库、无密钥，所有逻辑都是纯计算。因此最优解是把它**重写成原生静态网页**：一次性的人工改写成本，换来运行时的秒开、免费、免运维。

---

## 页面与功能

导航（左侧）对应原应用的 4 个页面，逻辑与原 Streamlit 代码一一对应：

| 页面 | 内容 |
|---|---|
| 🩺 问诊 | 实时录音状态、对话摘要（末 5 句）、AI 检索的相似病例卡片 |
| 📝 开检查 | 检查项目搜索/勾选、**AI 检查提醒弹窗**（冲突检测 + 遗漏检测，规则与原版一致） |
| 📊 查结果 | 异常指标截图 + 医学参考、原始化验单 |
| 📄 写病历 | 依据对话**自动生成门诊病历**（主诉/现病史/既往史提取逻辑照搬）、复制/打印/导出、对话原文与关键线索 |

> 顶部患者信息卡 + 步骤导航来自原《设计文档》的设计意图（原 Streamlit 代码未接线，本静态版按设计补全）。

---

## 目录结构

```
x_ciss-static/ (仓库内位于 web/)
├── index.html      # 页面骨架（侧边导航 + 内容容器）
├── styles.css      # 全部样式（医疗工作台主题）
├── app.js          # 路由 + 4 个页面的渲染与交互逻辑（复刻自原 Python）
├── data/           # 静态数据（与原 Streamlit 应用共享）
│   ├── *.json      # 患者、对话、相似病例、检查项目、规则等
│   └── *.webp      # 化验单/异常指标截图（见下方“图片压缩”）
└── README.md
```

数据均为**示例数据**，仅用于产品演示。

---

## 本地运行

任意静态服务器即可，无需安装依赖：

```bash
cd web
python3 -m http.server 8787
# 打开 http://127.0.0.1:8787/
```

## 部署

部署到 Cloudflare Pages 项目 `ciss`：

```bash
node web/verify-static-assets.mjs
wrangler pages deploy web --project-name=ciss --branch=main
```

个人域名 `hospital.zhangyvjing.com` 由仓库根目录的 Cloudflare Worker 配置托管：

```bash
npx wrangler deploy
```

该 Worker 仅分发同一份 `web/` 静态资源；`custom_domain` 会由 Cloudflare 自动配置代理 DNS 与 TLS。Pages 地址继续保留为备用入口。

### 发布前完整性检查

部署前运行 `node web/verify-static-assets.mjs`。它会确认页面依赖的 JSON 和 WebP
静态资源都在 `web/data/` 中，避免只发布页面骨架、遗漏数据文件。

---

## 图片压缩说明

原始化验单截图为 macOS Retina 截图（2816×1504，约 **6.24MB**），是全站唯一的“重量级”资源。已压缩为 WebP：

| 图片 | 原始 (PNG) | 压缩后 (WebP) | 方式 |
|---|---|---|---|
| 原始化验单 `11.27.59` | 6.24 MB | **203 KB** | 有损 q90 |
| 异常指标 `11.28.11` | 40 KB | 22 KB | 无损 |
| 异常指标 `11.28.19` | 37 KB | 19 KB | 无损 |

大图选用 q90 有损 WebP，已逐区域（含红色异常指标行）与原图比对，**文字锐利、颜色一致、肉眼无差别**；两张小图用无损 WebP，逐像素与原图一致。所有现代浏览器均原生支持 WebP。
