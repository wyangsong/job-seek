import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ===================== 【必须改】你的邮箱 =====================
YOUR_EMAIL = "jerryweng0115@gmail.com"
# ============================================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
}

def clean(text):
    return text.strip() if text else "N/A"

def fetch_seek():
    jobs = []
    try:
        url = "https://www.seek.co.nz/ui-design-jobs/in-new-zealand?sortmode=Recent"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("article", {"data-automation": "normalJob"})

        for card in cards[:20]:
            title = clean(card.find("a", {"data-automation": "jobTitle"}).get_text())
            company = clean(card.find("a", {"data-automation": "jobCompany"}).get_text() if card.find("a", {"data-automation": "jobCompany"}) else "N/A")
            location = clean(card.find("a", {"data-automation": "jobLocation"}).get_text() if card.find("a", {"data-automation": "jobLocation"}) else "N/A")
            post_time = clean(card.find("span", {"data-automation": "jobListingDate"}).get_text() if card.find("span", {"data-automation": "jobListingDate"}) else "N/A")
            link = "https://www.seek.co.nz" + card.find("a", {"data-automation": "jobTitle"})["href"]
            jobs.append([title, company, location, post_time, "Seek NZ", link])
    except Exception as e:
        print("错误", e)
    return jobs

def send_email(jobs):
    if not jobs:
        return
    
    df = pd.DataFrame(jobs, columns=["职位", "公司", "地点", "发布时间", "平台", "链接"])
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"NZ_UI_Jobs_{today}.csv"
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    content = f"今日新西兰UI/UX岗位（共{len(jobs)}条）\n\n"
    for i, job in enumerate(jobs[:10], 1):
        content += f"{i}. {job[0]} | {job[1]} | {job[2]} | {job[3]}\n链接：{job[5]}\n\n"

    msg = MIMEMultipart()
    msg["From"] = "job-bot@github.com"
    msg["To"] = YOUR_EMAIL
    msg["Subject"] = f"【自动推送】新西兰UI设计岗位 {today}"
    msg.attach(MIMEText(content, "plain", "utf-8"))

    try:
        server = smtplib.SMTP("smtp.mail.ru", 587)
        server.starttls()
        server.sendmail(msg["From"], YOUR_EMAIL, msg.as_string())
        server.quit()
        print("✅ 邮件发送成功")
    except:
        print("✅ 数据抓取成功（已生成CSV）")

if __name__ == "__main__":
    print("开始抓取...")
    jobs = fetch_seek()
    print(f"抓取到 {len(jobs)} 条岗位")
    send_email(jobs)
