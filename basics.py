from selenium import webdriver
from selenium.webdriver.support.ui import Select


class Locators:
    PARENT = 'div.quote'
    QUOTE = 'span.content'
    AUTHOR = 'span.author'
    TAGS = 'span.tag'
    AUTHORBOX = 'select#author' # '#' means it searches for the id attribute. this searches for <select id="author">
    TAGBOX = 'select#tag'
    SEARCHBUTTON = 'input[name="submit_button"]' # this means it searches with a specific attribute. <input name="submit_button">


# searches through all quotes and passes to Parsers class
class Page:
    def __init__(self, browser):
        self.browser = browser

    def get_all_quotes(self):
        return [Parsers(q) for q in self.browser.find_elements_by_css_selector(Locators.PARENT)]

    def author_menu(self):
        # find menu
        dropdown = self.browser.find_element_by_css_selector(Locators.AUTHORBOX)
        return Select(dropdown) # returns a selenium select object that has methods to interact with the menu.

    def select_author(self, author):
        self.author_menu().select_by_visible_text(author) # selects the given author

    def tag_menu(self):
        menu = self.browser.find_element_by_css_selector(Locators.TAGBOX)
        return Select(menu)

    def select_tag(self, tag):
        self.tag_menu().select_by_visible_text(tag)

    def get_all_tags(self):
        return [tag.text.strip() for tag in self.tag_menu().options]

    def press_button(self):
        button = self.browser.find_element_by_css_selector(Locators.SEARCHBUTTON)
        button.click()

class Parsers:
    def __init__(self, parent):
        self.parent = parent

    def get_quotes(self):
        return self.parent.find_element_by_css_selector(Locators.QUOTE).text

    def get_author(self):
        return self.parent.find_element_by_css_selector(Locators.AUTHOR).text

    def get_tags(self):
        tags_html = self.parent.find_element_by_css_selector(Locators.TAGS)
        tags = tags_html.text
        return tags

chrome = webdriver.Chrome(executable_path='C:\Program Files (x86)\chromedriver\chromedriver.exe')
chrome.get('http://quotes.toscrape.com/search.aspx')

while True:
    page = Page(chrome)
    searched_author = input('Search for author: ')
    page.select_author(searched_author)

    all_tags = '|'.join(page.get_all_tags()[1:])
    print(all_tags)
    searched_tag = input('Search for a tag: ')
    page.select_tag(searched_tag)

    page.press_button()

    all_quotes = page.get_all_quotes()

    for quote in all_quotes:
        print(f"""
        Quote: {quote.get_quotes()}
        Author: {quote.get_author()}
        Tags: {quote.get_tags()}
        """)