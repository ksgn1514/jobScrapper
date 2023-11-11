from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_page_count(keyword):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지 코드
    service = Service(executable_path='C:\Python\chromedriver\chromedriver.exe')
    browser = webdriver.Chrome(service=service, options=chrome_options)

    browser.get(f"https://kr.indeed.com/jobs?q={keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", attrs={"aria-label": "pagination"})
    if pagination == None:
        browser.close()
        return 1
    pages = pagination.select("div a")
    count = len(pages)
    if count >= 5:
        browser.close()
        return 5
    else:
        browser.close()
        return count


def extract_indeed_jobs(keyword):
    results = []
    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    for page in range(pages):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) #브라우저 꺼짐 방지 코드
        service = Service(executable_path='C:\Python\chromedriver\chromedriver.exe')
        browser = webdriver.Chrome(service=service, options=chrome_options)

        ulr = f"https://kr.indeed.com/jobs?q={keyword}&start={page*10}"
        print("Requesting ", ulr)
        browser.get(ulr)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="css-zu9cdh eu4oa1w0")

        jobs = job_list.find_all('li', recursive=False)
        if jobs == None:
            browser.close()
            return results
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                if anchor != None:
                    title = anchor['aria-label']
                    link = anchor['href']
                company = job.find("span", attrs={"data-testid": "company-name"})
                location = job.find("div", attrs={"data-testid": "text-location"})
                job_data = {
                    'company': company.string,
                    'location': location.string,
                    'title': title,
                    'link': f"https://www.indeed.com{link}"
                }
                results.append(job_data)
        browser.close()
    return results


