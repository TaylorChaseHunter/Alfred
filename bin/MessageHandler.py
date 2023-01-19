from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from discord import Message, Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time
import sys
import os
import random

BOOKS = ["2021:", "Incognito", "Flowers for Algernon", "Mice of men", "1984",
         "Brave New World", "Fahrenheit 451", "Cold Mountain", "Slaughterhouse 5",
         "In Cold Blood", "Myth of Sisyphus", "Picture of Dorian Grey", "Outsiders",
         "Bury my Heart at Wounded Knee", "\n2022:", "Grapes of wrath", "Moby dick", "Swerve",
         "Cats cradle", "Cosmos", "Born to Run", "Farewell to Arms", "The Right Stuff",
         "The Hitchikers Guide to the Galaxy"]


class MessageHandler:

    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.driver = None
        self.drive_path = r'../chromedriver.exe'

    def handle_fetch(self, message: Message) -> str:
        """
            Initial logic to handle a selenium 'fetch' call.
        """

        self.driver = webdriver.Chrome(executable_path=self.drive_path, options=self.options)

        # Create url to search #
        book_title = message.content.lower()[6:]
        search_string = f"https://www.goodreads.com/search?q={book_title}"
        self.driver.get(search_string)

        # Sleep to avoid errors due to slow loading
        time.sleep(1)

        rating = self.find_rating()
        summary = self.find_summary()
        self.driver.quit()
        return self.create_return_fetch(book_title, rating, summary)

    def create_return_fetch(self, book_title: str, rating: str, summary: str) -> str:
        response = f"{book_title.title()}:\n\n Goodreads rates the book: {rating}\n" \
                   f"\nSummary:\n{summary}"
        return response

    def find_rating(self) -> str:
        """
            Grabs the star rating from goodreads website.
        """

        # Click the first option from the search list
        book_link = self.driver.find_elements_by_class_name("bookTitle")[0]
        book_link.click()

        # Sleep to allow page to load
        time.sleep(1)

        # Deals with pop-ups and ever-changing goodreads layouts.
        try:
            rating = self.driver.find_element_by_xpath("//span[contains(@itemprop, 'ratingValue')]").text
        except NoSuchElementException:
            try:
                self.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/button").click()
                rating = self.driver.find_element_by_xpath("//span[contains(@itemprop, 'ratingValue')]").text
            except NoSuchElementException:
                self.driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div").click()
                rating = self.driver.find_element_by_xpath(
                    "//*[@id=\"ReviewsSection\"]/div[4]/div[1]/div[1]/div/div[1]/div"
                ).text

        return rating

    def find_summary(self) -> str:
        """
            Grabs the summary section from goodreads page
        """

        # Tries to close out any add that might be blocking the screen #
        try:
            self.driver.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div/button").click()
        except NoSuchElementException:
            self.driver.find_element_by_xpath("/html/body/div[3]/div/div/div[1]/button").click()
        except ElementNotInteractableException:
            pass

        # Sleep to allow the page to load #
        time.sleep(1)

        # Tries to identify the summary section for both goodreads layouts that might occur #
        try:
            summary = self.driver.find_element_by_xpath("//*[@id=\"description\"]").text
        except NoSuchElementException:
            try:
                summary = self.driver.find_element_by_xpath("//span[contains(@class,'Formatted')]").text
            except NoSuchElementException:
                summary = self.driver.find_element_by_xpath(
                    "//*[@id=\"__next\"]/div/main/div[1]/div[2]/div[2]/div[2]/div[4]"
                ).text
        return summary

    def handle_message(self, message: Message, client: Client) -> str:
        """
            Manually checks content of every discord message and heuristically decides action.
        """

        if message.author == client.user:
            return ""

        # Retrieve  #
        elif message.content.lower()[:5] == "fetch":
            try:
                return self.handle_fetch(message)
            except Exception as e:
                print("ERROR: ", e)
                if self.driver is not None:
                    self.driver.quit()
                return "I could not find that master."
    
        elif message.content.lower() == "hello alfred":
            return "Good morrow"

        elif message.content.lower() == "speak alfred":
            return "I live"

        elif message.content.lower() == "alfred, grab the books":
            return "Right away master.\n" + "`" + "\n".join(BOOKS) + "`"

        elif message.content.lower() == "alfred, what is your favorite book?":
            return "I must say, slaugherhouse-5 is incredibly, but personally the " \
                   "truth and passion behind Myth of Sisyphus makes it unmatched to me."

        elif message.content.lower() == "alfred, what is your least favorite book?":
            return "All books are good books my dear masters, but if I had to " \
                   "pick one that I did not enjoy as much as others, I'd sadly say Cold Mountain."

        elif message.content.lower() == "alfred, list the constitution":
            dir_list = os.listdir('../constitution')
            for file in dir_list:
                with open('constitution/' + file, 'r') as r:
                    data = r.read()
                r.close()
                return data

        elif "alfred, list article" in message.content.lower():
            _, _, after_keyword = message.content.lower().partition("article")
            location = "constitution/article" + after_keyword.strip()
            with open(location) as r:
                data = r.read()
            r.close()
            return data

        elif message.content.lower() == "alfred, list the preamble":
            location = "constitution/Apreamble"
            with open(location) as r:
                data = r.read()
            r.close()
            return data

        elif message.content.lower() == "alfred, list the poem":
            location = "constitution/Apoem"
            with open(location) as r:
                data = r.read()
            r.close()
            return data

        elif message.content.lower() == "alfred, flip a coin":
            content = random.choice(["Heads", "Tails"])
            return content

        elif message.content.lower() == "thank you alfred" or message.content.lower() == "thanks alfred":
            responses = ["Twas no problem.",
                         "Isn't a worry masters.",
                         "I live to serve the hobos.",
                         "Please, it was my pleasure.",
                         "As always my dear friends."]
            response = random.choice(responses)
            return response

        elif "alfred" in message.content.lower() or " al " in message.content.lower():
            responses = ["I have no opinion on this matter.",
                         "I am busy making tea, what is it masters?",
                         "The hobos are an important group that I strive to serve.",
                         "I often think of myself as Ishmael as well.",
                         "Is one not just a rat in a maze? Maybe not, but it is worth the thought.",
                         "Is desertion a crime if it saves one's life? How can a man be blamed for such reasons?",
                         "The worst crime man can commit is not educating himself.",
                         "I defer to Grond.",
                         "I relate most to captain Ahab. Do we all not chase some White Whale? "
                         "What are we doing otherwise?",
                         "If life is meaningless, we must create the meaning. That is a great thing.",
                         "NFTs are a scam.",
                         "What would one give to live in a perfect society?",
                         "Is man just a mouse running along his wheel, simply awaiting death? Is this bad?",
                         "Something something war something something supreme court.",
                         "Not enough people know of Sandy Creek.",
                         "The power of the human brain is incalculable, yet we must try to number it.",
                         "Space is the final frontier, and we must find our way amongst the stars.",
                         "Only the very weak-minded refuse to be influenced by literature and poetry.",
                         "You talk when you cease to be at peace with your thoughts.",
                         "Every heart sings a song, incomplete, until another heart whispers back. "
                         "Those who wish to sing always find a song. At the touch of a lover, everyone becomes a poet."]
            response = random.choice(responses)
            return response

        return ""
