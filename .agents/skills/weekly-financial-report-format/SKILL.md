---
name: weekly-financial-report-format
version: 1.0.0
description: 每週財經週報文件排版技能（限定本專案）。當使用者要求「排版新聞週報」、「整理財經週報」、「匯出成 google文件」、「排版財經筆記」、「整理這週財經週報」時載入。本技能嚴格遵循四級標題階梯（H1-H4）、內文首行縮排、最小字級 12pt、關鍵重要數字紅字粗體、以及自動同步匯出至 Google Drive 的標準作業程序。
---

# 每週財經週報文件排版規範（專案限定技能）

本技能限定於「【筆記】每週財經資訊」專案。負責將每週財經新聞週報整理、排版為結構嚴謹、適合長篇閱讀的高質感專欄式報告，並同步發布至 Google 文件與本地 Markdown 筆記。

---

## 核心排版五大黃金規範

### 1. 嚴格四級標題階梯架構（H1 / H2 / H3 / H4）
嚴禁跳級或扁平化條列。所有分析均必須收攏至以下清晰階層：
- **H1（主標題）**：`24pt` 粗體，底部實線邊框。範例：`20260921-0925 財經新聞週報：AI 狂潮與高利率下的全球經濟與台灣新局`
- **H2（主章節）**：`19pt` 粗體，左側藍色重點色塊標記。固定分為三大章節：
  - `壹、Why：為什麼會有現在這個狀況？`
  - `貳、How：這個狀況是因為什麼事情、如何產生的？`
  - `參、What：這樣的狀況接下來會造成未來什麼樣子的局面？`
- **H3（核心面向）**：`15.5pt` 粗體，國字數字編號：`一、`、`二、`、`三、`
- **H4（深度分析焦點）**：`13.5pt` 粗體，括號國字編號：`（一）`、`（二）`、`（三）`

### 2. 內文段落首行縮排
- **正文段落**：所有內文段落必須進行「首行縮排 2 個中文字元」。
  - Google Docs / HTML 格式：`<p style="text-indent: 26pt; line-height: 1.85; margin-bottom: 12pt;">`
  - Markdown 格式：每段開頭加上 `&#12288;&#12288;`
- **標題與摘要卡**：標題（H1~H4）與摘要卡（Summary Card）維持靠左對齊，不縮排。

### 3. 字級規範（最小字級 >= 12pt）
全文件**絕對禁止**出現任何小於 `12pt` 的文字：
- 正文內文：`12.5pt` ~ `13pt`（行距 1.8 ~ 1.85）
- 引言、摘要卡、副標題、註解：最低 `12pt` ~ `12.5pt`

### 4. 關鍵重要數字紅字粗體
所有核心數據、經濟統計、利率、原油價格、金額與百分比，必須統一標示為**紅字粗體**：
- HTML 格式：`<span style="color: #c00000; font-weight: bold;">數值</span>` 或 `<b style="color: #c00000;">數值</b>`
- Markdown 格式：`<span style="color: #c00000; font-weight: bold;">數值</span>`
- 標示對象包含：各國升降息碼數與政策利率（如 `一碼`、`1.25%`）、指標殖利率與商品價格（如 `5%`、`100 美元`）、進出口與 GDP 成長率（如 `1,029 億美元`、`11.48%`）、資本支出金額（如 `2,250 億美元`、`31.6 兆美元`）、企業負債與債券利率、超額儲蓄、薪資中位數與人口推估數字。

### 5. Google Drive 自動上傳與同步
- 使用專案父資料夾 ID：`1O8_AbfKDhEA_j24IsmbFwnnpgFgh-yU9`
- 透過 Drive API Multipart 上傳 HTML，指定 MIME 類型為 `application/vnd.google-apps.document`，Google Drive 會自動轉換為原生 Google 文件。
- Google Drive for Desktop 會在 5 秒內自動於專案目錄同步生成同名的 `.gdoc` 捷徑。

---

## Google Docs 專用 HTML 模板範例

```html
<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'>
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
    color: #1e293b;
    line-height: 1.85;
    font-size: 12.5pt;
    margin: 0;
    padding: 24px;
  }
  h1 {
    font-size: 24pt;
    font-weight: bold;
    color: #0f172a;
    line-height: 1.35;
    margin-top: 0;
    margin-bottom: 14pt;
    border-bottom: 3px solid #1e3a8a;
    padding-bottom: 10pt;
    text-indent: 0 !important;
  }
  .subtitle {
    font-size: 12pt;
    color: #64748b;
    margin-bottom: 20pt;
    text-indent: 0 !important;
  }
  .summary-card {
    background-color: #f8fafc;
    border-left: 6px solid #2563eb;
    border-radius: 4px;
    padding: 16pt 18pt;
    margin-bottom: 24pt;
    font-size: 12.5pt;
    line-height: 1.85;
  }
  h2 {
    font-size: 19pt;
    font-weight: bold;
    color: #1e3a8a;
    margin-top: 28pt;
    margin-bottom: 14pt;
    padding-left: 10pt;
    border-left: 5px solid #2563eb;
    line-height: 1.4;
    text-indent: 0 !important;
  }
  h3 {
    font-size: 15.5pt;
    font-weight: bold;
    color: #0f172a;
    margin-top: 20pt;
    margin-bottom: 10pt;
    line-height: 1.45;
    text-indent: 0 !important;
  }
  h4 {
    font-size: 13.5pt;
    font-weight: bold;
    color: #334155;
    margin-top: 14pt;
    margin-bottom: 8pt;
    line-height: 1.5;
    text-indent: 0 !important;
  }
  p {
    font-size: 12.5pt;
    line-height: 1.85;
    margin-top: 0;
    margin-bottom: 12pt;
    text-align: justify;
    text-indent: 26pt;
  }
  .num {
    color: #c00000;
    font-weight: bold;
  }
  hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 28pt 0;
  }
</style>
</head>
<body>
...
</body>
</html>
```

---

## 自動匯出 Python 程式碼骨架

```python
import json, urllib.parse, urllib.request

# 1. 取得 Access Token
with open('/Users/garfiwang/.clasprc.json') as f:
  tok = json.load(f)['tokens']['default']

data = urllib.parse.urlencode({
    'client_id': tok['client_id'],
    'client_secret': tok['client_secret'],
    'refresh_token': tok['refresh_token'],
    'grant_type': 'refresh_token',
}).encode()

req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data)
with urllib.request.urlopen(req) as resp:
  access_token = json.loads(resp.read().decode())['access_token']

# 2. 構建 Multipart 上傳或更新
metadata = {
    'name': '週報標題',
    'mimeType': 'application/vnd.google-apps.document',
    'parents': ['1O8_AbfKDhEA_j24IsmbFwnnpgFgh-yU9'],
}
boundary = '-------314159265358979323846'
body = (
    f'--{boundary}\r\n'
    f'Content-Type: application/json; charset=UTF-8\r\n\r\n'
    f'{json.dumps(metadata)}\r\n'
    f'--{boundary}\r\n'
    f'Content-Type: text/html; charset=UTF-8\r\n\r\n'
    f'{html_content}\r\n'
    f'--{boundary}--\r\n'
).encode('utf-8')

# 建立新文件（POST）或更新已存在文件（PATCH）
req_upload = urllib.request.Request(
    'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
    data=body,
    headers={
        'Authorization': f'Bearer {access_token}',
        'Content-Type': f'multipart/related; boundary={boundary}',
    },
)
with urllib.request.urlopen(req_upload) as resp:
  res = json.loads(resp.read().decode())
  print('Document created! URL: https://docs.google.com/document/d/' + res['id'])
```
