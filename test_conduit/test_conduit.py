import time


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import csv
from functions import sign_in, wait_for_element, URL
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager



class TestConduit(object):

    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.driver.get(URL)
        time.sleep(1)

    def teardown(self):
        self.driver.quit()

    def test_home_page_appearances(self):
        time.sleep(1)
        assert self.driver.find_element_by_xpath("//h1[contains(text(), 'conduit')]").text == "conduit"

    # Adatkezelési nyilatkozat használata
    def test_accept_cookies(self):
        self.driver.find_element_by_xpath("//div[contains(text(),' I accept')]").click()
        time.sleep(1)

        cookies = self.driver.get_cookies()
        for cookie in cookies:
            if cookie['value'] == 'accept':
                accepted = True
                assert accepted != False

    # Regisztráció
    def test_sign_up(self):
        self.driver.find_element_by_xpath("//a[@href='#/register']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Username']").send_keys("papp.emese1")
        self.driver.find_element_by_xpath("//input[@placeholder='Email']").send_keys("papp.emese9013+3@gmail.com")
        self.driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Jelszó123")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Sign up')]").click()
        element = wait_for_element(self.driver, "//div[contains(text(), 'Your registration was successful!')]")
        assert element.text == "Your registration was successful!"
        self.driver.find_element_by_xpath("//button[contains(text(), 'OK')]").click()


    #Bejelentkezés
    def test_login(self):
        self.driver.find_element_by_xpath("//a[@href='#/login']").click()
        element = wait_for_element(self.driver, "//h1[contains(text(),'Sign in')]")
        self.driver.find_element_by_xpath("//input[@placeholder='Email']").send_keys("papp.emese9013+3@gmail.com")
        self.driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys("Jelszó123")
        self.driver.find_element_by_xpath("//button[contains(text(),'Sign in')]").click()
        time.sleep(3)
        assert self.driver.find_element_by_xpath("//a[@active-class='active'][@class='nav-link']").is_displayed() == True

    #Kijelentkezés

    def test_logout(self):
        sign_in(self.driver)
        time.sleep(1)
        self.driver.find_element_by_xpath("//a[@active-class='active'][@class='nav-link']").click()
        time.sleep(1)
        assert self.driver.find_element_by_xpath("//a[@href='#/login']").is_displayed() == True



    #Adatok listázása
    def test_data_list(self):
        sign_in(self.driver)
        art_titles = self.driver.find_elements_by_xpath("//h1")
        titles_of_articles = []
        for i in art_titles:
            titles_of_articles.append(i.text)
        assert len(titles_of_articles) == len(art_titles)


    #Új adatbevitel
    def test_new_post(self):
        sign_in(self.driver)
        self.driver.find_element_by_xpath("//a[@href='#/editor']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//input[@placeholder="Article Title"]').send_keys(
            "Walesi bárdok")
        self.driver.find_element_by_xpath('//input[@placeholder="What\'s this article about?"]').send_keys("Egy szép vers")
        self.driver.find_element_by_xpath("//textarea[@placeholder='Write your article (in markdown)']").send_keys("Edward király..")
        self.driver.find_element_by_xpath("//input[@placeholder='Enter tags']").send_keys("AranyJanos")
        self.driver.find_element_by_xpath("//button[contains(text(),'Publish Article')]").click()
        time.sleep(3)
        self.driver.find_element_by_xpath("//a[@href='#/']").click()
        time.sleep(3)
        titles = self.driver.find_elements_by_xpath("//a[@class='preview-link']/h1")
        last_post = titles[-1]
        assert "Walesi bárdok" == last_post.text


    #Több oldalas lista bejárása
    def test_pages(self):
        sign_in(self.driver)
        self.driver.find_element_by_xpath("//a[@class='page-link'][contains(text(),'2')]").click()
        time.sleep(1)
        assert self.driver.find_element_by_xpath("//h1[contains(text(), 'Walesi bárdok')]").is_displayed() == True

    # Ismételt és sorozatos adatbevitel adatforrásból
    def test_new_comments(self):
        sign_in(self.driver)
        self.driver.refresh()
        time.sleep(1)
        self.driver.find_element_by_xpath("//h1[contains(text(), 'Walesi bárdok')]").click()
        time.sleep(1)
        textbox = self.driver.find_element_by_xpath("//textarea")
        with open('comments.csv', 'r', encoding='utf-8') as f:
            csvreader=csv.reader(f, delimiter=',')
            next(csvreader)
            for row in csvreader:
                textbox.send_keys(row[0])
                self.driver.find_element_by_xpath("//button[contains(text(),'Post Comment')]").click()
                time.sleep(3)
                comments_=self.driver.find_elements_by_xpath("//p[@class='card-text']")
                for i in comments_:
                    assert comments_[0].text == row[0]


    # Adatok lementése felületről - Global feed bejegyzések címei
    def test_save_data(self):
        sign_in(self.driver)
        time.sleep(1)
        with open("data.csv", "w", newline='') as f:
            csvwriter=csv.writer(f, delimiter=',')
            csvwriter.writerow(["Article Title", "Preview"])
            article_title = self.driver.find_element_by_xpath("//h1[contains(text(), 'Walesi bárdok')]").text
            preview = self.driver.find_element_by_xpath("//p[contains(text(),'Egy szép vers')]").text
            csvwriter.writerow([f"{article_title}",f"{preview}"])
        with open("data.csv", "r") as k:
            csvreader=csv.reader(k, delimiter=',')
            next(csvreader)
            for row in csvreader:
                assert row[0] == article_title
                assert row[1] == preview

    #Meglévő adat módosítása
    def test_change_bio(self):
        sign_in(self.driver)
        time.sleep(1)
        self.driver.find_element_by_xpath("//a[@href='#/settings']").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("// textarea").clear()
        self.driver.find_element_by_xpath("// textarea").send_keys("Emese vagyok")
        self.driver.find_element_by_xpath("//button").click()
        element = wait_for_element(self.driver, "//div[contains(text(),'Update successful!')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'OK')]").click()
        time.sleep(1)
        assert self.driver.find_element_by_xpath("//textarea").get_attribute("value") == "Emese vagyok"





    #Adat törlése
    def test_delete_article(self):
        sign_in(self.driver)
        time.sleep(1)
        self.driver.find_element_by_xpath("//h1[contains(text(), 'Walesi bárdok')]").click()
        time.sleep(1)
        self.driver.find_element_by_xpath("//button[@class='btn btn-outline-danger btn-sm']").click()
        time.sleep(1)
        art_titles = self.driver.find_elements_by_xpath("//h1")
        for i in art_titles:
            assert i.text != "Walesi bárdok"






