# job-search
This uses https://github.com/rainmanjam/jobspy-api Dockerized version of the jobspy-api to search popular listing sites.

# 1. Start the API
docker run -d --name jobspy-api -p 8000:8000 \
  -e API_KEYS=test-key-123 \
  -e ENABLE_API_KEY_AUTH=true \
  rainmanjam/jobspy-api:latest

# 2. Run any of the Python scripts
python nyc_job_search.py
