import re

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
headers = {"accept-language": "en-US,en;q=0.9", "accept-encoding": "gzip, deflate, br",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
           "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}





def searchGoogleForGoodBooksLinks(bookName):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    # Create a new headless Chrome session
    driver = webdriver.Chrome(options=options)

    # Construct the Google Search URL
    search_url = f"https://www.google.com/search?q={'+'.join(bookName.split())}"

    # Open the search URL in the browser
    driver.get(search_url)

    # Wait for the search results to load (adjust timeout as needed)
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "main")))
    except TimeoutException:
        print("Search results failed to load the google results page.")
        return None

    # Get the HTML content of the page
    html_content = driver.page_source
    # Close the browser window


    similarLink = re.findall(r'href="(https://www.goodreads.com/book/similar/[^"]+)"', html_content)[0]
    print("Link:", similarLink)
    driver.quit()
    return similarLink



def searchGoodReadsPage(bookURL):
    driver = webdriver.Chrome()
    # Load the webpage
    driver.get(bookURL)

    # Wait for the "More" button to become clickable
    buttons = driver.find_elements(By.CSS_SELECTOR, ".gr-buttonAsLink.u-marginLeftTiny")

    # Click buttons one by one until none are found (or another condition)
    for button in buttons:
        try:
            button.click()

        except NoSuchElementException:
            # No more buttons found, break the loop
            break
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()

    # Now you can continue parsing and extracting information from the updated HTML content using BeautifulSoup
    book_items = soup.find_all(class_="listWithDividers__item")

    for book_item in book_items:
        # Extracting book name
        book_name = book_item.select_one('.gr-h3--noMargin').text.strip()

        # Extracting book summary
        book_summary = book_item.select_one('.expandableHtml').text.strip()

        # Extracting book author
        book_author = book_item.select_one('[itemprop="author"] [itemprop="name"]').text.strip()

        # Extracting book rating
        book_rating = book_item.select_one('.communityRating').text.strip()

        print("Book Name:", book_name)
        print("Book Summary:", book_summary)
        print("Book Author:", book_author)
        print("Book Rating:", book_rating)
        print()  # Add a blank line for better readability between books


if __name__ == "__main__":
    searchGoodReadsPage(searchGoogleForGoodBooksLinks('books like Lightning Thief'))