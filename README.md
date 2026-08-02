# 智能医生工作台

面向南京医疗黑客松的一日产品流程演示。项目以医生的信息化操作台为原型，串联问诊信息整理、检查开单提醒、检查结果查看与病历草稿四个基础步骤，验证这类连续操作流程的交互形态。

本项目仅展示产品流程设计。由于黑客松开发周期只有一天，线上版本采用预置示例数据构成可交互前端演示，不接入真实患者数据、模型服务或临床系统。

**个人职责：产品流程设计。**

## 在线体验

- 主站：[hospital.zhangyvjing.com](https://hospital.zhangyvjing.com/)
- 备用地址：[ciss-101.pages.dev](https://ciss-101.pages.dev/)

## 如何体验

从左侧导航依次进入四个演示步骤：

1. **问诊**：查看示例问诊信息与相似病例卡片。
2. **开检查**：搜索、选择检查项目，并触发规则化的检查提醒。
3. **查结果**：查看示例异常指标、参考信息与原始检查报告。
4. **写病历**：根据示例信息生成可编辑、复制、打印或导出的病历草稿。

页面内所有数据均为演示数据；其中的提示、建议和结果不构成诊断、治疗建议或临床决策依据。

## 项目构成

| 部分 | 作用 | 如何运行 |
| --- | --- | --- |
| `web/` | 当前线上静态演示。浏览器读取 JSON 和图片示例数据，在本地完成页面交互。 | 任意静态服务器，或由 Cloudflare 分发。 |
| `worker.js` + `wrangler.jsonc` | Cloudflare Worker 配置。Worker 仅将请求交给 `web/` 静态资源。 | `npx wrangler deploy` |
| `streamlit/` | 黑客松期间的 Streamlit 原型，保留作流程来源与本地参考，不参与线上部署。 | 进入目录后运行 `streamlit run app.py`。 |
| `scripts/verify-static-assets.mjs` | 发布前检查线上演示所需的静态数据是否齐全。 | `node scripts/verify-static-assets.mjs` |

## 本地运行与发布

运行线上静态演示：

```bash
cd web
python3 -m http.server 8787
```

打开 `http://127.0.0.1:8787/`。

发布前校验和部署：

```bash
node scripts/verify-static-assets.mjs
npx wrangler deploy
```

运行保留的 Streamlit 原型：

```bash
cd streamlit
pip install -r requirements.txt
streamlit run app.py
```

## 演示边界

- 这是产品流程演示，不是临床系统。
- 不处理真实患者数据，也不连接医院信息系统。
- 不提供诊断、处方或医疗决策能力。
