# **Insomnia Crawler**

## **Project Overview**
The **Insomnia Crawler** is a Python-based web scraping tool designed to extract detailed information about products, sellers, and reviews from the popular Greek e-commerce platform, **insomnia.gr**. This crawler not only automates data collection but also **analyzes and calculates review quality scores**, providing a deeper understanding of both sellers and their reviewers. It is ideal for assessing seller reliability and conducting product research.

---

## **Key Features**
- **Product Data Extraction**:
  - Collects product details, such as titles, prices, and images.
- **Seller Information Retrieval**:
  - Extracts seller names, ranks, and **review quality metrics**.
- **Review Quality Analysis**:
  - Calculates the percentage of positive and negative reviews for sellers.
  - Evaluates reviewers' reliability and quality based on their review history.
- **Pagination Handling**:
  - Automatically navigates through multiple pages of results.
- **Category-Specific Crawling**:
  - Allows users to crawl specific product categories (e.g., Hardware, Mobile Phones).
- **Data Export**:
  - Saves the scraped data to an Excel file for further analysis.

---

## **Why Review Quality Matters**
This tool stands out by emphasizing the **calculation of review quality scores**:
- **Seller Reviews**: Helps identify trustworthy sellers by analyzing their feedback.
- **Reviewer Scores**: Accounts for the quality of each reviewer, ensuring more accurate seller rankings.
- This feature is particularly useful for identifying **reliable sellers** and avoiding fraudulent or low-quality listings.

---

## **Technologies Used**
- **Python Libraries**:
  - `selenium`: For browser automation and interaction.
  - `BeautifulSoup`: For parsing and extracting HTML data.
  - `pandas`: For organizing and exporting data to Excel.
- **Browser Automation**:
  - ChromeDriver is used for navigating and interacting with web pages.

---

## **Usage Instructions**
1. **Install Dependencies**:
   Ensure you have Python installed, then install the required dependencies:
   - **bash**
   - pip install selenium beautifulsoup4 pandas

Set Up ChromeDriver:

Download and place chromedriver.exe in the project directory.
Ensure the ChromeDriver version matches your Chrome browser version.
Run the Crawler: Execute the script in the terminal:

bash
Copy code
python main.py
Choose a Category: The program will prompt you to select a product category (e.g., Hardware, Mobile Phones).

Export Data: The collected data will be saved to an Excel file named output.xlsx in the project directory.
