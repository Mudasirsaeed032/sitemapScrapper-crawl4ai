import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy

def fetch_dynamic_html_selenium(url):
    """Fetch HTML using Selenium for dynamic content."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run headless Chrome
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))  # Wait for content [[7]]
    )
    html = driver.page_source
    driver.quit()
    return html

async def main():
    url = "https://www.postgraduate.study.cam.ac.uk/courses"
    html = fetch_dynamic_html_selenium(url)  # Get pre-rendered HTML [[7]]

    config = CrawlerRunConfig(
        scraping_strategy=LXMLWebScrapingStrategy(),  # Static strategy [[3]]
        verbose=True
    )

    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(url, config=config, html=html)  # Pass HTML to Crawl4AI [[8]]
        
        # Save results
        data = [{"url": res.url, "content": res.content} for res in results]
        print("Crawled data:", data)

asyncio.run(main())