from bs4 import BeautifulSoup
import requests


def extract_remoteok_jobs(keyword):
    base_url = "https://remoteok.com/"
    request = requests.get(f"{base_url}remote-{keyword}-jobs",headers={"User-Agent": "Kimchi"})
    if request.status_code != 200:
        print(f"Error: {request.status_code}")
    else:
        results = []
        soup = BeautifulSoup(request.text, "html.parser")
        job_posts = soup.find_all('tr', class_="job")
        for posts in job_posts:
            jobs = posts.find_all('td', class_="company")
            for job in jobs:
                company = job.find("h3", itemprop="name")
                title = job.find("h2", itemprop="title")
                location = job.find_all("div", class_="location")
                link = job.find("a", itemprop="url")['href']
                location.pop(-1)
                
                if company and title and location:
                    job = {
                        'title': title.string,
                        'company': company.string,
                        'location': location[0].string,
                        'link': base_url + link
                    }
                    results.append(job)
        return results


