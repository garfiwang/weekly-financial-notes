#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每週全球財經週報自動生成、匯出 Google 文件與派送助手
支援環境：
1. 本地 macOS（讀取 ~/.clasprc.json 與 Apple Mail 寄送）
2. 雲端 GitHub Actions（讀取 Secrets: CLASPRC_JSON, GEMINI_API_KEY）
"""

import os
import re
import sys
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import subprocess
from datetime import datetime, timezone, timedelta

PARENT_FOLDER_ID = "1O8_AbfKDhEA_j24IsmbFwnnpgFgh-yU9"
CLASPRC_PATH = os.path.expanduser("~/.clasprc.json")
DEFAULT_RECIPIENT = "richnews168@gmail.com"

def get_taipei_now():
    tz = timezone(timedelta(hours=8))
    return datetime.now(tz)

def get_google_access_token():
    """從環境變數 CLASPRC_JSON 或 ~/.clasprc.json 取得 Google OAuth Access Token"""
    tok = None
    if "CLASPRC_JSON" in os.environ and os.environ["CLASPRC_JSON"].strip():
        try:
            clasprc_data = json.loads(os.environ["CLASPRC_JSON"])
            tok = clasprc_data["tokens"]["default"]
        except Exception as e:
            print(f"[WARN] 解析 CLASPRC_JSON 環境變數失敗：{e}")

    if not tok and os.path.exists(CLASPRC_PATH):
        with open(CLASPRC_PATH, "r", encoding="utf-8") as f:
            tok = json.load(f)["tokens"]["default"]

    if not tok:
        print("[WARN] 未找到有效的 Google OAuth 憑證，將跳過 Google Drive 上傳。")
        return None

    data = urllib.parse.urlencode({
        "client_id": tok["client_id"],
        "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")

    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res["access_token"]
    except Exception as e:
        print(f"[ERROR] 取得 Google Access Token 失敗：{e}")
        return None

def fetch_financial_news_rss():
    """從權威財經 RSS 來源抓取過去 7 天重點新聞"""
    queries = [
        "global+economy+fed+interest+rates+treasury+yields+when:7d",
        "nvidia+tech+semiconductor+earnings+capex+when:7d",
        "crude+oil+energy+inflation+when:7d"
    ]
    articles = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for q in queries:
        url = f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                tree = ET.fromstring(resp.read())
                for item in tree.findall(".//item")[:4]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    pub_elem = item.find("pubDate")
                    source_elem = item.find("source")
                    if title_elem is not None:
                        articles.append({
                            "title": title_elem.text,
                            "link": link_elem.text if link_elem is not None else "",
                            "source": source_elem.text if source_elem is not None else "Financial Media",
                            "pubDate": pub_elem.text if pub_elem is not None else ""
                        })
        except Exception as e:
            print(f"[WARN] 抓取新聞 RSS 失敗 ({q})：{e}")

    return articles

def export_google_doc(title, html_content, output_dir=".", parent_folder_id=PARENT_FOLDER_ID):
    """透過 Google Drive API Multipart 上傳 HTML 並建立 Google 文件"""
    access_token = get_google_access_token()
    if not access_token:
        print("[INFO] 無 Access Token，跳過 Google 文件匯出。")
        return None, None

    metadata = {
        "name": title,
        "mimeType": "application/vnd.google-apps.document",
        "parents": [parent_folder_id],
    }
    boundary = "-------314159265358979323846"
    body = (
        f"--{boundary}\r\n"
        f"Content-Type: application/json; charset=UTF-8\r\n\r\n"
        f"{json.dumps(metadata)}\r\n"
        f"--{boundary}\r\n"
        f"Content-Type: text/html; charset=UTF-8\r\n\r\n"
        f"{html_content}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    req = urllib.request.Request(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        data=body,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": f"multipart/related; boundary={boundary}",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            doc_id = res["id"]
            doc_url = f"https://docs.google.com/document/d/{doc_id}"
            print(f"[SUCCESS] Google 文件建立成功：{doc_url}")

            # 建立本地 .gdoc 捷徑
            gdoc_path = os.path.join(output_dir, f"{title}.gdoc")
            with open(gdoc_path, "w", encoding="utf-8") as f:
                json.dump({"url": doc_url, "doc_id": doc_id, "email": DEFAULT_RECIPIENT}, f)
            print(f"[SUCCESS] 本地 .gdoc 捷徑已建立：{gdoc_path}")
            return doc_id, doc_url
    except Exception as e:
        print(f"[ERROR] 匯出 Google 文件失敗：{e}")
        return None, None

def send_gmail_via_mail_app(recipient, subject, body_text):
    """透過 macOS Apple Mail 寄送郵件（僅 macOS 本地有效）"""
    if sys.platform != "darwin":
        print("[INFO] 非 macOS 環境，跳過 Apple Mail 寄送。")
        return False

    safe_subject = subject.replace('\\', '\\\\').replace('"', '\\"')
    safe_body = body_text.replace('\\', '\\\\').replace('"', '\\"')
    safe_recipient = recipient.replace('\\', '\\\\').replace('"', '\\"')

    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{safe_subject}", content:"{safe_body}", visible:false}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{safe_recipient}"}}
            send
        end tell
    end tell
    '''
    res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"[SUCCESS] 郵件已成功透過 Apple Mail 寄送至 {recipient}")
        return True
    else:
        print(f"[ERROR] 寄送郵件失敗：{res.stderr}")
        return False

def convert_markdown_to_gdoc_html(title, md_content):
    """將 Markdown 轉換為嚴格符合專案五大黃金規範之 Google Docs HTML"""
    lines = md_content.split("\n")
    html_lines = []
    
    html_lines.append("<!DOCTYPE html><html><head><meta charset='UTF-8'><style>")
    html_lines.append("body { font-family: 'Arial', 'PingFang TC', 'Microsoft JhengHei', sans-serif; font-size: 12.5pt; line-height: 1.85; color: #1a1a1a; margin: 30pt; }")
    html_lines.append("h1 { font-size: 24pt; font-weight: bold; color: #0d233a; margin-top: 24pt; margin-bottom: 12pt; line-height: 1.3; }")
    html_lines.append("h2 { font-size: 19pt; font-weight: bold; color: #1b4461; margin-top: 20pt; margin-bottom: 10pt; line-height: 1.35; border-bottom: 1.5pt solid #1b4461; padding-bottom: 4pt; }")
    html_lines.append("h3 { font-size: 15.5pt; font-weight: bold; color: #2c3e50; margin-top: 16pt; margin-bottom: 8pt; line-height: 1.4; }")
    html_lines.append("h4 { font-size: 13.5pt; font-weight: bold; color: #34495e; margin-top: 12pt; margin-bottom: 6pt; line-height: 1.45; }")
    html_lines.append("p { text-indent: 26pt; margin-top: 6pt; margin-bottom: 8pt; font-size: 12.5pt; line-height: 1.85; }")
    html_lines.append(".summary-box { background-color: #f8f9fa; border-left: 4.5pt solid #c00000; padding: 12pt 16pt; margin-bottom: 18pt; font-size: 12pt; line-height: 1.75; }")
    html_lines.append(".red-bold { color: #c00000; font-weight: bold; }")
    html_lines.append("ul, ol { margin-left: 20pt; margin-bottom: 8pt; }")
    html_lines.append("li { font-size: 12.5pt; line-height: 1.75; margin-bottom: 4pt; }")
    html_lines.append("</style></head><body>")

    in_summary = False
    summary_buffer = []

    for line in lines:
        line_s = line.strip()
        if not line_s:
            continue

        # 核心摘要引用區塊
        if line_s.startswith("> **📌【本週核心摘要】**") or (line_s.startswith(">") and in_summary):
            in_summary = True
            clean_s = re.sub(r"^>\s*", "", line_s)
            summary_buffer.append(clean_s)
            continue
        elif in_summary:
            in_summary = False
            html_lines.append("<div class='summary-box'>" + "".join(summary_buffer) + "</div>")
            summary_buffer = []

        if line_s.startswith("# "):
            html_lines.append(f"<h1>{line_s[2:]}</h1>")
        elif line_s.startswith("## "):
            html_lines.append(f"<h2>{line_s[3:]}</h2>")
        elif line_s.startswith("### "):
            html_lines.append(f"<h3>{line_s[4:]}</h3>")
        elif line_s.startswith("#### "):
            html_lines.append(f"<h4>{line_s[5:]}</h4>")
        elif line_s.startswith("- ") or line_s.startswith("* "):
            html_lines.append(f"<li>{line_s[2:]}</li>")
        elif line_s.startswith("---"):
            html_lines.append("<hr style='border: none; border-top: 1pt solid #ddd; margin: 20pt 0;'>")
        else:
            # 內文段落
            p_text = line_s
            # 移除開頭全形空白（因為 CSS 已有 text-indent: 26pt）
            p_text = re.sub(r"^[\s　]+", "", p_text)
            html_lines.append(f"<p>{p_text}</p>")

    if summary_buffer:
        html_lines.append("<div class='summary-box'>" + "".join(summary_buffer) + "</div>")

    html_lines.append("</body></html>")
    return "\n".join(html_lines)

def process_report_file(md_file_path, recipient=DEFAULT_RECIPIENT):
    """處理單一週報檔案：轉 HTML -> 匯出 Google 文件 -> 發信"""
    if not os.path.exists(md_file_path):
        print(f"[ERROR] 找不到檔案：{md_file_path}")
        return False

    with open(md_file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    fname = os.path.basename(md_file_path)
    date_match = re.match(r"(2026\d{4})", fname)
    date_prefix = date_match.group(1) if date_match else get_taipei_now().strftime("%Y%m%d")
    
    # 依標準規範建立標題：yyyymmdd - 全球財經週報
    gdoc_title = f"{date_prefix} - 全球財經週報"
    html_content = convert_markdown_to_gdoc_html(gdoc_title, md_content)

    output_dir = os.path.dirname(md_file_path) or "."
    doc_id, doc_url = export_google_doc(gdoc_title, html_content, output_dir=output_dir)

    if doc_url:
        email_body = f"您好，最新全球財經週報已整理完成！\n\n報告標題：{gdoc_title}\n線上閱讀連結：{doc_url}\n\n詳細內容請參閱 Google 文件或本專案筆記。"
        send_gmail_via_mail_app(recipient, f"【全球財經週報】{gdoc_title}", email_body)
    return True

if __name__ == "__main__":
    target_md = sys.argv[1] if len(sys.argv) > 1 else None
    target_recipient = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_RECIPIENT

    if target_md:
        process_report_file(target_md, target_recipient)
    else:
        # 自動尋找專案內最新日期的週報
        import glob
        pattern = "2026*.md"
        candidates = [f for f in glob.glob(pattern) if "知識庫" not in f and "總綱" not in f]
        if candidates:
            latest = sorted(candidates)[-1]
            print(f"[INFO] 未指定檔案，自動處理最新週報：{latest}")
            process_report_file(latest, target_recipient)
        else:
            print("[INFO] 專案內尚未找到財經週報 Markdown 檔案。")

