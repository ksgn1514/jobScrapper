def save_to_file(file_name, jobs):
  file = open(f"{file_name}.csv", "w", encoding="utf-8")
  file.write("Company, Location, Title, Link\n")
  for job in jobs:
    file.write(
      f"{job['company']}, {job['location']}, {job['title']}, {job['link']}\n")
  file.close()