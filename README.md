This README is specifically crafted for the **WahidSaeed/Revisor---Scrapper** repository. It highlights the use of the Scrapy framework and the integration with MongoDB for movie data analysis.

---

# Revisor - Movie Data Scraper

A robust web scraping demonstration built with the **Scrapy** framework. The primary goal of this project is to aggregate movie information from top-tier review platforms and store it in a structured format for deep data analysis.

## 🚀 Overview

The "Revisor" scraper is designed to crawl and extract relevant movie metadata, including ratings, cast details, and synopses. It demonstrates how to handle large-scale data extraction across multiple domains and consolidate that information into a single database.

## 🛠️ Tech Stack

* **Python**: Core programming language.
* **Scrapy**: High-level web crawling and scraping framework.
* **MongoDB**: NoSQL database used to store extracted movie data in JSON-like document format.
* **XPath/CSS Selectors**: Used for precise navigation and data extraction from target HTML.

## ✨ Features

* **Multi-Source Scraping**: Extracts data from:
* **IMDb**: Popularity, ratings, and technical specs.
* **Rotten Tomatoes**: Critic and audience "Tomatometer" scores.
* **Metacritic**: Weighted average scores and reviews.


* **Automated Data Pipeline**: Seamlessly cleans and exports scraped data directly into a MongoDB collection.
* **Efficient Crawling**: Built to follow pagination and related links to build a comprehensive dataset.

## 📂 Project Structure

```text
├── scrapper/
│   ├── spiders/          # Site-specific scraping logic (IMDb, RT, Metacritic)
│   ├── items.py          # Definitions for the scraped data objects
│   ├── pipelines.py      # Logic for MongoDB connection and data cleaning
│   └── settings.py       # Scrapy configuration (User-Agents, Delays, etc.)
├── test.py               # Unit tests or quick execution scripts
└── venv/                 # Virtual environment files

```

## 💻 Getting Started

### Prerequisites

* Python 3.x
* MongoDB (Running locally or on a cloud instance like Atlas)

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/WahidSaeed/Revisor---Scrapper.git
cd Revisor---Scrapper

```


2. **Install dependencies**:
```bash
pip install scrapy pymongo

```


3. **Configure MongoDB**:
Ensure your MongoDB service is running. You can update the connection string and database name in `scrapper/settings.py` or `scrapper/pipelines.py`.

### Running the Scraper

To start the crawling process, navigate to the project directory and run:

```bash
scrapy crawl <spider_name>

```

*(Replace `<spider_name>` with the name defined in the respective spider files, e.g., `imdb` or `metacritic`.)*

## 📊 Data Storage

Data is saved in MongoDB as documents, making it ideal for future analysis using Python tools like **Pandas** or **Matplotlib** to compare ratings across different platforms.

## 📜 License

This project is open-source and available under the [MIT License](https://www.google.com/search?q=LICENSE).

---

**Maintained by [Wahid Saeed**](https://github.com/WahidSaeed)
