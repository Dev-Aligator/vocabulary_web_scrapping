from data_scrapping import *
from docx_converter import *

if __name__ == "__main__":
    URL_TO_SCRAPE = "https://loigiaihay.com/tieng-anh-7-unit-12-tu-vung-a109952.html"
    html_content = fetch_data(URL_TO_SCRAPE)
    if html_content:
        scraped_data = parse_data(html_content, "Unit 12. English-speaking countries")
        convert_docx(scraped_data)

        
