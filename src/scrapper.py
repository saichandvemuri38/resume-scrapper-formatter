from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_jobs(job_title, location="Remote"):
    # 1. Setup Chrome
    options = Options()
    # options.add_argument("--headless") # Comment this out to SEE the browser work
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    job_list = []

    try:
        # 2. Construct Search URL (Example: Indeed)
        formatted_title = job_title.replace(" ", "+")
        url = f"https://www.indeed.com/jobs?q={formatted_title}&l={location}"
        driver.get(url)
        time.sleep(5) # Wait for page load/anti-bot checks

        # 3. Find Job Cards (Indeed uses 'jobsearch-ResultsList')
        # Note: Selectors change often, this is the 'Greenhouse/Workday' style logic
        cards = driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

        for card in cards[:10]: # Let's start with the first 10
            title = card.find_element(By.CSS_SELECTOR, "h2.jobTitle").text
            company = card.find_element(By.CSS_SELECTOR, "[data-testid='company-name']").text
            link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            
            job_list.append({
                "title": title,
                "company": company,
                "link": link
            })
            
    except Exception as e:
        print(f"Scraping Error: {e}")
    finally:
        driver.quit()

    return job_list