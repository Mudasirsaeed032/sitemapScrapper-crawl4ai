import asyncio
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy

async def main():
    target_url = "https://www.postgraduate.study.cam.ac.uk/courses"

    print("Setting up dynamic JavaScript scraping using BrowserConfig...")

    browser_config = BrowserConfig(
        headless=True, 
        java_script_enabled=True
    )

    # JavaScript to wait for full page load
    js_wait_for_load = """
    (async () => {
        await new Promise(r => setTimeout(r, 5000));  // Wait 5 seconds for JS content
    })();
    """

    config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=0, include_external=False),
        js_code=[js_wait_for_load],  # Execute this JavaScript on the page
        verbose=True
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        print("Starting the crawl...")

        results = await crawler.arun(target_url, config=config)

        print(f"Crawled {len(results)} pages in total")

        data = [{"url": result.url, "depth": result.metadata.get("depth", 0), "content": result.markdown}
                for result in results]

        with open("BrowserConfigData.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("Crawled data has been saved to deep_crawl_results.json")

asyncio.run(main())
