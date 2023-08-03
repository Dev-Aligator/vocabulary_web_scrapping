import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def fetch_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(url)

    # Get the updated HTML content after JavaScript execution
    html_content = driver.page_source

    # Close the browser
    driver.quit()

    return html_content

def parse_data(html_content, default_title=""):
    soup = BeautifulSoup(html_content, "html.parser")
    data = []
    title_data = []
    # Find the div with class "WordSection1" which contains the unit title <p>
    container_div = soup.find("div", { "id" : "box-content" })
    title_div = container_div.find("div", class_="WordSection1")
    try:
        title = title_div.find("p").text.strip()
    except:
        title = default_title
    title_data.append("GETTING STARTED")
    data.append(title)
    data.append([])
    data[-1].append(["GETTING STARTED"])
    # Find the div with class "voca-left" which contains the vocabulary entries
    vocabulary_divs = soup.find_all("p", class_="block-vocabulary")

    # Extract each vocabulary entry and its definition
    for vocabulary_div in vocabulary_divs:
        entry = vocabulary_div.find("p", class_="voca-word")
        word = entry.find("b").text.strip()
        definition = entry.find_next_sibling("p").text.strip()
        english_example = entry.find_next_sibling("p").find_next_sibling("p").text.strip()
        try:
            vietnamese_example = entry.find_next_sibling("p", style="font-style: italic;color: #656565;").text.strip()
        except:
            vietnamese_example = ""
        data[-1][-1].append({"word": word, "definition": definition, "english_example": english_example, "vietnamese_example" : vietnamese_example})


        if vocabulary_div.find_next_sibling("p") and not vocabulary_div.find_next_sibling("p").get("class"):
            title_text = vocabulary_div.find_next_sibling("p").text.strip()
            if (title_data.count(title_text) == 0):
                title_data.append(title_text)
                data[-1].append([title_text])
        elif vocabulary_div.find_next_sibling() and vocabulary_div.find_next_sibling().name == "div" and not vocabulary_div.find_next_sibling().get("class"):
            if vocabulary_div.find_next_sibling().find("p", class_=""):
                title_text = vocabulary_div.find_next_sibling().find("p", class_="").text.strip()
                if (title_data.count(title_text) == 0):
                    title_data.append(title_text)
                    data[-1].append([title_text])
    return data
