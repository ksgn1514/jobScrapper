from flask import Flask, render_template, request, redirect, send_file
from extractors.indeed import extract_indeed_jobs
from extractors.wwr import extract_wwr_jobs
from extractors.remoteok import extract_remoteok_jobs
from file import save_to_file

app = Flask("JobScrapper") 

db = {}


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    keyword = request.args.get('keyword')
    if keyword == None:
        return redirect("/")
    if keyword in db:
        jobs = db[keyword]
    else:
        # indeed_jobs = extract_indeed_jobs(keyword)
        wwr_jobs = extract_wwr_jobs(keyword)
        remoteok_jobs = extract_remoteok_jobs(keyword)
        jobs =  wwr_jobs + remoteok_jobs
        db[keyword] = jobs
    return render_template('search.html', keyword=keyword, jobs=jobs)

@app.route('/export')
def export():
    try:
        keyword = request.args.get("keyword")
        if not keyword:
            return redirect("/")
        if keyword not in db:
            return redirect(f"/search?keyword={keyword}")
        save_to_file(keyword, db[keyword])
        return send_file(f"{keyword}.csv", as_attachment=True)
    except:
        return redirect("/")
    

