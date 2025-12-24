import pandas as pd
import os

def save_to_local(job_data, filename="scraped_jobs.csv"):
    # 1. Convert the list of dictionaries into a Table (DataFrame)
    df = pd.DataFrame(job_data)
    
    # 2. Check if file exists to append or create new
    if not os.path.isfile(filename):
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)
        
    print(f"✅ Saved {len(job_data)} jobs to {filename}")