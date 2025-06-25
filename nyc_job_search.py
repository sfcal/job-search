#!/usr/bin/env python3
"""
Simple job search - filters out senior and director positions
"""

import requests
import json
from datetime import datetime

# Search for jobs
response = requests.get(
    "http://localhost:8000/api/v1/search_jobs",
    params={
        "site_name": ["linkedin", "indeed", "glassdoor", "google", "zip_recruiter"],
        "search_term": "infrastructure OR devops OR kubernetes OR SRE OR platform engineer",
        "location": "New York, NY",
        "distance": 10,
        "results_wanted": 50,
        "hours_old": 168,  # Last week
        "country_indeed": "USA"  # Required for Indeed/Glassdoor
    },
    headers={"x-api-key": "test-key-123"},
    timeout=60
)

if response.status_code == 200:
    data = response.json()
    jobs = data.get("jobs", [])
    
    print(f"✅ Found {len(jobs)} total jobs")
    
    # Filter out senior, director, hourly, and NJ positions
    filtered_jobs = []
    removed_counts = {'senior': 0, 'director': 0, 'hourly': 0, 'nj': 0, 'sr.': 0, 'lead': 0, 'ii': 0, 'distinguished': 0, 'staff': 0, 'chief': 0, 'manager': 0, 'executive': 0}
    
    for job in jobs:
        title = (job.get('title') or '').lower()
        location = (job.get('location') or '').lower()
        interval = (job.get('interval') or '').lower()
        
        # Check all filter conditions
        if 'manager' in title:
            removed_counts['manager'] += 1
            continue
        if 'chief' in title:
            removed_counts['chief'] += 1
            continue
        if 'executive' in title:
            removed_counts['executive'] += 1
            continue
        if 'lead' in title:
            removed_counts['lead'] += 1
            continue
        if 'sr.' in title or ' sr ' in title:
            removed_counts['sr.'] += 1
            continue
        if 'senior' in title:
            removed_counts['senior'] += 1
            continue
        if ' ii' in title or ' ii ' in title:
            removed_counts['ii'] += 1
            continue
        if 'distinguished' in title:
            removed_counts['distinguished'] += 1
            continue
        if 'staff' in title:
            removed_counts['staff'] += 1
            continue
        if 'director' in title:
            removed_counts['director'] += 1
            continue
        if interval == 'hourly' or 'hour' in interval:
            removed_counts['hourly'] += 1
            continue
        if 'nj' in location or 'new jersey' in location or ', nj' in location:
            removed_counts['nj'] += 1
            continue
            
        filtered_jobs.append(job)
    
    print(f"📋 After filtering: {len(filtered_jobs)} jobs")
    print(f"   Removed seniority: {removed_counts['senior']} senior, {removed_counts['sr.']} sr., {removed_counts['lead']} lead, {removed_counts['ii']} II, {removed_counts['distinguished']} distinguished, {removed_counts['staff']} staff, {removed_counts['director']} director")
    print(f"   Removed other: {removed_counts['hourly']} hourly, {removed_counts['nj']} NJ")
    print(f"   Total removed: {len(jobs) - len(filtered_jobs)} jobs")
    
    # Update data with filtered jobs
    data['jobs'] = filtered_jobs
    data['count'] = len(filtered_jobs)
    
    # Save everything
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nyc_jobs_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"💾 Saved {len(filtered_jobs)} filtered jobs to {filename}")
    
    # Quick preview
    print("\nFirst 5 jobs:")
    for i, job in enumerate(filtered_jobs[:5], 1):
        print(f"{i}. {job.get('title')} at {job.get('company')}")
else:
    print(f"❌ Error: {response.status_code}")
    print(f"Details: {response.text}")
