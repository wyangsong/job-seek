from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

def get_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def fetch_seek():
    print("开始抓取 Seek NZ (真实浏览器模式)")
    jobs = []
    driver = get_browser()
    
    try:
        driver.get("https://www.seek.co.nz/ui-design-jobs/in-new-zealand?sortmode=Recent")
        driver.implicitly_wait(10)
        cards = driver.find_elements("css selector", "article[data-automation='normalJob']")

        for card in cards[:20]:
            try:
                title = card.find_element("css selector", "a[data-automation='jobTitle']").text.strip()
                company = card.find_element("css selector", "a[data-automation='jobCompany']").text.strip()
                location = card.find_element("css selector", "a[data-automation='jobLocation']").text.strip()
                post = card.find_element("css selector", "span[data-automation='jobListingDate']").text.strip()
                link = card.find_element("css selector", "a[data-automation='jobTitle']").get_attribute("href")
                jobs.append([title, company, location, post, link])
            except:
                continue
    finally:
        driver.quit()
    
    return jobs

if __name__ == "__main__":
    data = fetch_seek()
    print(f"\n✅ 抓取完成：共 {len(data)} 条岗位")

    # 直接打印所有岗位（日志里可见）
    for i, item in enumerate(data, 1):
        print(f"{i}. {item[0]} | {item[1]} | {item[2]} | {item[3]}")
        print(f"   链接：{item[4]}")
        print("-" * 50)
