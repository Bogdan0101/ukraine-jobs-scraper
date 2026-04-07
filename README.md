[![Ukraine jobs scraper tests](https://github.com/Bogdan0101/ukraine-jobs-scraper/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Bogdan0101/ukraine-jobs-scraper/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/Bogdan0101/ukraine-jobs-scraper/graph/badge.svg?token=PP296SOCNR)](https://codecov.io/github/Bogdan0101/ukraine-jobs-scraper)

# Project description

Automated data pipeline for scraping, processing,  
and visualizing the Python job market in Ukraine.  
Built with **Scrapy**, **Playwright**, **PostgreSQL**, **Docker** and **Jupyter**.  
This tool provides deep insights into required  
skills for **Junior**, **Middle**, **Senior** and **Overall** developers.  
At the time of project creation, the system successfully analyzed  
a comprehensive dataset of **~500** unique Python job vacancies.

# Features

* **Automated Data Extraction**: Leveraging Scrapy and Playwright to crawl  
  and collect live job market data from top-tier Ukrainian tech platforms.
* **Smart Parsing & Classification**: Utilizing Regex and TextBlob for precise
  skill extraction and automated experience-level filtering (Junior, Middle, Senior).
* **Data Storage**: Seamlessly saving processed information into a PostgreSQL database,  
  fully optimized for a Docker-containerized environment.
* **Insightful Visualization**: Using Jupyter Lab and Matplotlib to generate   
  comparative analytics, including top skill trends and historical data comparisons.
* **CI/CD Pipeline**: Integrated **GitHub Actions** workflow for automated testing (Pytest),  
  database integration testing (PostgreSQL) and code quality enforcement (Flake8) on every push.

# Technologies used

1. **Core**: Python (3.12)
2. **Scraping**: Scrapy (2.14.2), scrapy-playwright (0.0.46), Playwright (1.58.0)
3. **Parsing**: TextBlob (0.19.0), Regex (2026.2.28)
4. **Database**: PostgreSQL (16-alpine), SQLAlchemy (2.0.48), psycopg-binary (2.9.11)
5. **Analysis**: Pandas (3.0.1), NumPy (2.4.3)
6. **Visualization**: JupyterLab (4.5.6), Matplotlib (3.10.8)
7. **Environment**: Docker, Docker Compose, python-dotenv (1.2.2)
8. **Testing**: Pytest (9.0.2), Pytest-cov (7.1.0)
9. **DevOps & CI/CD**: GitHub Actions, Codecov (Coverage reporting), Flake8

# Installation instructions

1. **git clone https://github.com/Bogdan0101/ukraine-jobs-scraper.git**
2. **cd ukraine-jobs-scraper**
3. **python -m venv .venv**
4. for Windows: **./.venv/Scripts/activate** (for Linux/Mac: **source .venv/bin/activate**)
5. create a **.env** file using the example **.env.sample**
6. **pip install -r requirements.txt**

# For local PostgreSQL

7. Create db with name **job_parser**
8. Set your *POSTGRES_USER* and *POSTGRES_PASSWORD* in **.env** file
9. Start Scraper point in **run_spiders.py**:  
   <img width="523" height="104" alt="image" src="https://github.com/user-attachments/assets/18d72e9d-1936-436e-993e-0a853048bb68" />

**OR** Start Scraper command in terminal:

```
python run_spiders.py
```  

10. Analyze data in file **data_analysis.ipynb** notebook

# For Docker container PostgreSQL

**Important: Ensure Docker Desktop is running**

7. Set your *POSTGRES_USER* and *POSTGRES_PASSWORD* in **.env** file
8. For container build use command in terminal:

```
docker-compose build
```

9. For container up and start the Scraper use command in terminal:

```
docker-compose up
```

10. Analyze data in file **data_analysis.ipynb** notebook

# Screenshots

<img width="1171" height="833" alt="image" src="https://github.com/user-attachments/assets/18786a4e-8821-4fcb-9d87-0303f924d833" />  
<img width="830" height="328" alt="image" src="https://github.com/user-attachments/assets/6b642186-ece5-441a-9af1-416feb1baa51" />  
<img width="816" height="859" alt="image" src="https://github.com/user-attachments/assets/f20772fd-7b27-474c-a0bf-115fbb523ee5" />  
<img width="1395" height="750" alt="image" src="https://github.com/user-attachments/assets/d037ad9b-8d50-4b90-8cc4-af83c9109f1d" />  
<img width="1262" height="298" alt="image" src="https://github.com/user-attachments/assets/4515a893-57ee-4b5d-ab9d-96f302ca3db3" />  
<img width="924" height="873" alt="image" src="https://github.com/user-attachments/assets/20b27513-1a25-4694-af1c-5d518524f6d0" />  
<img width="1799" height="734" alt="image" src="https://github.com/user-attachments/assets/098630a5-a538-4fa8-bd71-00b2889a4211" />  

<img width="1224" height="733" alt="image" src="https://github.com/user-attachments/assets/b3e58bc1-1e78-4d61-9627-ce9d3ed191b3" />  
<img width="1226" height="697" alt="image" src="https://github.com/user-attachments/assets/103c56fe-5ca5-412a-87e0-ada57de61a0e" />  
<img width="1232" height="710" alt="image" src="https://github.com/user-attachments/assets/515403a4-c041-4034-b06b-62da8b874097" />   

<img width="1200" height="721" alt="image" src="https://github.com/user-attachments/assets/9ccf10f4-9b75-448a-aa47-d16ec44487dc" />  
<img width="1249" height="737" alt="image" src="https://github.com/user-attachments/assets/b79643c8-59b1-4936-9656-a895e98d2275" />   
<img width="1223" height="722" alt="image" src="https://github.com/user-attachments/assets/bf078751-0145-4a47-8bf0-7f55fdf52cb1" />  