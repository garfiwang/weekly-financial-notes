#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
財經週報匯出 Google 文件與 Gmail 寄送助手
1. 自動讀取 .clasprc.json 憑證上傳 HTML 至 Google Drive 並轉換為原生 Google 文件
2. 自動於本地專案目錄建立 .gdoc 捷徑
3. 透過 macOS Apple Mail (richnews168@gmail.com) 自動將週報寄出至指定的 Gmail
"""

import os
import sys
import json
import urllib.parse
import urllib.request
import subprocess
from datetime import datetime

PARENT_FOLDER_ID = "1O8_AbfKDhEA_j24IsmbFwnnpgFgh-yU9"
CLASPRC_PATH = os.path.expanduser("~/.clasprc.json")
DEFAULT_RECIPIENT = "richnews168@gmail.com"

def get_google_access_token():
    """從 ~/.clasprc.json 取得最新 Google OAuth Access Token"""
    if not os.path.exists(CLASPRC_PATH):
        raise FileNotFoundError(f"找不到 Google OAuth 憑證：{CLASPRC_PATH}")

    with open(CLASPRC_PATH, "r", encoding="utf-8") as f:
        tok = json.load(f)["tokens"]["default"]

    data = urllib.parse.urlencode({
        "client_id": tok["client_id"],
        "client_secret": tok["client_secret"],
        "refresh_token": tok["refresh_token"],
        "grant_type": "refresh_token",
    }).encode("utf-8")

    req = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["access_token"]

def export_google_doc(title, html_content, output_dir=".", parent_folder_id=PARENT_FOLDER_ID):
    """
    透過 Drive API Multipart 上傳 HTML 並建立 Google 文件
    同檔名格式範例："20261106 - 全球財經週報"
    """
    access_token = get_google_access_token()
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

    with urllib.request.urlopen(req) as resp:
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

def send_gmail_via_mail_app(recipient, subject, body_text):
    """透過 macOS Apple Mail 寄送郵件至指定信箱"""
    # 轉義反斜線與雙引號
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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 export_and_mail_weekly_report.py <title> <html_file> [recipient]")
        sys.exit(1)

    title_arg = sys.argv[1]
    html_file = sys.argv[2]
    recipient_arg = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_RECIPIENT

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    doc_id, doc_url = export_google_doc(title_arg, html)
    email_body = f"您好，本週最新全球財經週報已整理完成！\n\n報告標題：{title_arg}\n線上閱讀連結：{doc_url}\n\n詳細內容請參閱 Google 文件或本專案筆記。"
    send_gmail_via_mail_app(recipient_arg, f"【全球財經週報】{title_arg}", email_body)
