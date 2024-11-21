"""
Here I will do testing on test_original_3. test_original_3 is almost ready.
I will continue to work with this file.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import itertools
import pandas as pd


class InsomniaCrawler:
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")

    def __init__(self):
        self.crawl_category_of_products()
        self.save_to_excel_file()

    def go_to_reviews_tab_and_return_source_code(self, url_of_reviews_tab):
        driver = webdriver.Chrome(options=self.chrome_options, executable_path="chromedriver.exe")
        driver.get(url_of_reviews_tab)  # went to reviews tab
        source_code_val = driver.page_source
        driver.close()
        return source_code_val

    def go_to_reviews_tab_from_products_page_and_get_source_code(self, url_str):
        """
        Accepts as an input parameter the url of the individual page of the product
        Returns the html code of the page where the reviews exist and the url that leads to the reviews page
        """
        # go to the sellers profile
        driver = webdriver.Chrome(options=self.chrome_options, executable_path="chromedriver.exe")
        driver.get(url_str)
        user_info = driver.find_elements(By.CLASS_NAME, 'classifieds-seller-author')
        user_prof_url = user_info[0].find_element(By.CLASS_NAME, 'ipsUserPhoto.ipsUserPhoto_medium').get_attribute(
            "href")  # got link
        driver.get(user_prof_url)
        time.sleep(2)  # wait for js to load
        # get reviews tab link, click it
        url_of_reviews_tab = driver.find_elements(By.ID, "elProfileTab_node_feedback_Feedback")[0].get_attribute(
            "href")  # got link
        driver.close()
        source_code_val = self.go_to_reviews_tab_and_return_source_code(url_of_reviews_tab)

        return source_code_val, url_of_reviews_tab

    def navigate_to_page_and_return_source_code(self, url_to_navigate):
        """
        Function that accepts as an input the url of the page to navigate and returns the html code of that page
        """
        driver = webdriver.Chrome(options=self.chrome_options, executable_path="chromedriver.exe")
        driver.get(url_to_navigate)
        source_code_val = driver.page_source
        driver.close()
        return source_code_val

    def get_reviews(self, page_code):
        """
        Gets as an input attribute the html code where the reviews exist (or not).
        Returns a list with the type of the reviews e.g ["positive", "negative", e.t.c ]
        """
        soup_var = BeautifulSoup(page_code, 'html.parser')
        # Find the "li" elements
        i_elements = soup_var.find_all("i")
        i_elements_class_ls = [el_i["class"] for el_i in i_elements]
        filtered_list = [lst for lst in i_elements_class_ls if all(isinstance(item, str) for item in lst) and any(
            "positive" in item.lower() or "negative" in item.lower() for item in lst)]
        filtered_list_final = []
        for lst in filtered_list:
            if all(isinstance(item, str) for item in lst) and any("positive" in item.lower() for item in lst):
                filtered_list_final.append("positive")
            elif all(isinstance(item, str) for item in lst) and any("negative" in item.lower() for item in lst):
                filtered_list_final.append("negative")

        return filtered_list_final


    def check_if_pagination_exists(self, page_code):
        """
        Gets as an input attribute the html code of a page.
        Returns True or False regarding if pagination exists in the page
        """
        soup_var = BeautifulSoup(page_code, 'html.parser')
        pagination_exists = soup_var.find("ul", {"class": "ipsPagination"})
        if pagination_exists:
            return True
        else:
            return False


    def get_num_of_pages_from_pagination_bar(self, page_code):
        """
        Accepts as parameter the html code of a page.
        Returns the last number of the pagination bar.
        """
        try:
            soup_var = BeautifulSoup(page_code, 'html.parser')
            pagination_elm = soup_var.find("ul", {"class": "ipsPagination"})
            num_of_pages = int(pagination_elm["data-ipspagination-pages"])  # get number of pages from pagination bar
        except:
            return 0

        return num_of_pages

    def check_if_reviews_exist(self, page_code):
        """
        Accepts as an attribute the html code of a page.
        If a profile has reviews return True, else return False.
        """
        soup_var = BeautifulSoup(page_code, 'html.parser')
        reviews = soup_var.find_all("li", {"class": "ipsDataItem"})
        if reviews:
            return True
        else:
            return False

    def get_list_with_type_of_reviews(self, page_code, url_of_reviews_tab):
        """
        Gets as attributes the html code of the profile page and the url where the reviews tab exists.
        Returns a list that contains str values that depict the type of reviews this profile has e.g ["positive", "negative", ...]
        """
        reviews_exist = self.check_if_reviews_exist(page_code)

        if reviews_exist and (not self.check_if_pagination_exists(page_code)):
            return self.get_reviews(page_code)
        elif reviews_exist and self.check_if_pagination_exists(page_code):
            type_of_reviews_list = []
            num_of_pages = self.get_num_of_pages_from_pagination_bar(page_code)
            for i in range(1, num_of_pages + 1):
                page_code = self.navigate_to_page_and_return_source_code(url_of_reviews_tab + f"&feedbackPage={i}")
                type_of_reviews_list.append(self.get_reviews(page_code))
            return list(itertools.chain(*type_of_reviews_list))
        else:
            return []

    def get_reviewers_prof_url(self, page_code):
        """
        Accepts as an input the html code of the reviews tab.
        For each review, get the url that leads to the profile of the reviewer.
        Return a list with these urls.
        """
        soup_var = BeautifulSoup(page_code, 'html.parser')
        # Find the "a" elements
        a_elements = soup_var.find_all("a", {"class": "ipsUserPhoto ipsUserPhoto_tiny"})
        reviewer_prof_list = []
        for a in a_elements:
            reviewer_prof_list.append(a["href"])
        return reviewer_prof_list

    def get_percent_of_positives_over_negative_reviews(self, reviews_list):
        """
        Returns the percent of positive over negative reviews.
        """
        if len(reviews_list) > 0:
            return (reviews_list.count("positive") / len(reviews_list)) * 100
        else:
            return 0

    def get_list_with_all_reviewers_prof_urls(self, page_code, url_of_reviews_tab):
        """
        Accepts as input the html code of the profile page of a user and the url that leads to the reviews tab.
        Returns a list with the all the urls of the profiles of each reviewer.
        """
        reviews_exist = self.check_if_reviews_exist(page_code)
        reviewers_prof_urls = []  # list with the profile urls of each reviewer

        if reviews_exist and (not self.check_if_reviews_exist(page_code)):
            return self.get_reviewers_prof_url(page_code)
        elif reviews_exist and self.check_if_pagination_exists(page_code):
            num_of_pages = self.get_num_of_pages_from_pagination_bar(page_code)
            for i in range(1, num_of_pages + 1):
                page_code = self.navigate_to_page_and_return_source_code(url_of_reviews_tab + f"&feedbackPage={i}")
                reviewers_prof_urls.append(self.get_reviewers_prof_url(page_code))
            return list(itertools.chain(*reviewers_prof_urls))
        else:
            return []

    def get_review_quality_of_each_reviewer(self, reviewers_prof_urls_ls):
        """
        Function that accepts as an input a list with all the urls of the reviewers profiles.
        Returns a list with the rank of each reviewer
        """
        # I added the following if-statement in order for the crawler to run faster. Might remove in later version.
        reviewers_rank = []
        if len(reviewers_prof_urls_ls) <= 3:
            for lnk in reviewers_prof_urls_ls:

                page_code, url_str = self.go_to_reviews_tab_and_get_source_code_from_profile_page(lnk)
                if page_code == "error" and url_str == "404":
                    continue
                temp_ls = self.get_list_with_type_of_reviews(page_code, url_str)
                print(temp_ls)
                reviewers_rank.append(self.get_percent_of_positives_over_negative_reviews(temp_ls))
        else:
            for lnk in reviewers_prof_urls_ls[:3]:
                page_code, url_str = self.go_to_reviews_tab_and_get_source_code_from_profile_page(lnk)
                if page_code == "error" and url_str == "404":
                    continue
                temp_ls = self.get_list_with_type_of_reviews(page_code, url_str)
                print(temp_ls)
                reviewers_rank.append(self.get_percent_of_positives_over_negative_reviews(temp_ls))

        return reviewers_rank

    def go_to_reviews_tab_and_get_source_code_from_profile_page(self, url_prof_link):

        driver = webdriver.Chrome(options=self.chrome_options, executable_path="chromedriver.exe")
        try:
            driver.get(url_prof_link)
            time.sleep(2)  # otherwise driver doesn't function properly
            url_of_reviews_tab = driver.find_elements(By.ID, "elProfileTab_node_feedback_Feedback")[0].get_attribute(
                "href")  # got link
            source_code = self.go_to_reviews_tab_and_return_source_code(url_of_reviews_tab)
            driver.close()
        except:
            driver.close()
            return "error", "404"

        return source_code, url_of_reviews_tab

    def get_urls_for_the_page_of_each_category(self):
        """
        Returns a list that contains the urls that lead to the products of each category that exists in insomnia.gr
        """
        driver = webdriver.Chrome(options=self.chrome_options, executable_path="chromedriver.exe")
        url_str = "https://www.insomnia.gr/classifieds/"
        driver.get(url_str)
        category_elm = driver.find_element(By.ID, "elCatMenu3")
        category_elm.click()
        # Wait for the pop-up window to appear
        WebDriverWait(driver, 5)
        driver.find_element(By.CLASS_NAME,
                            "insDropDown_largeMenou.insDropDown.mdInsDropDown.insCenterDropDown.ipsMenu.ipsHide.ipsPadding\:half.ipsMenu_bottomCenter")
        source_code = driver.page_source
        soup_var = BeautifulSoup(source_code, "html.parser")
        li_elements = soup_var.find_all("li", {"class": "ipsMargin_right:none ipsPadding:none ipsMenu_item"})
        li_elements_filtered = [str(elm) for elm in li_elements if "περιεχόμενο" in str(elm)]
        urls_for_the_page_of_each_category_ls = []
        for elm in li_elements_filtered:
            soup_var = BeautifulSoup(elm, "html.parser")
            a_tag = soup_var.find("a")
            urls_for_the_page_of_each_category_ls.append(a_tag["href"])

        return urls_for_the_page_of_each_category_ls

    def go_to_page_of_category_and_return_the_html(self, url_var):
        """
        Gets as attribute the url of the category of products
        Returns the html code of the page that these products exist
        """
        driver = webdriver.Chrome(options=self.chrome_options, executable_path="chromedriver.exe")
        driver.get(url_var)
        source_code = driver.page_source
        driver.close()
        return source_code

    def get_products_of_page(self, page_code):
        """
        Gets as attribute the html code of the page that the products exist.
        Returns a list that contains the urls for the individual page of each product
        """
        soup_var = BeautifulSoup(page_code, "html.parser")
        products_ls = soup_var.find_all("a", {"class": "ipsThumb ipsThumb_classified-thumb-240 ipsThumb_bg"})
        urls_for_products_page_ls = [elm["href"] for elm in products_ls]
        return urls_for_products_page_ls

    def get_user_input_about_which_category_page_to_crawl(self):
        """
        Returns the url of the products of the specific category the user chose
        """
        ls_of_categories_urls = self.get_urls_for_the_page_of_each_category()
        while True:
            print("Enter the number of the category you want to crawl\n")
            print(
                "1: Hardware\n2: Apple\n3: Laptops\n4: Video Games\n5: Gadgets\n6: Tables\n7: Διάφορα\n8: Mobile phones\n")
            try:
                user_ans = int(input("Enter your answer: "))
            except:
                print("Please provide a number in the range [1-8] as an answer\n")
                continue

            if not (user_ans in list(range(1, len(ls_of_categories_urls) + 1))):
                print("Wrong input please provide a number in the range [1-8]\n")
                continue
            else:
                break
        return ls_of_categories_urls[user_ans - 1]

    def retrieve_info(self, products_of_page_ls):
        """
        Accepts as an input parameter a list that contains the urls that lead to the individual page of each product.
        Returns a list of lists where each list contains the  title of the product, the price of the product,
        the image of the products, the name of the seller, the rank of the seller, the reviews_quality_rank
        which is the rank the seller and takes also into consideration the review quality (quality of the reviewer)
        """
        info = []
        for prod in products_of_page_ls:
            driver = webdriver.Chrome(options=self.chrome_options, executable_path="chromedriver.exe")
            try:
                driver.get(prod)  # maybe the product doesn't exist anymore
            except:
                continue
            source_code = driver.page_source  # html code from the individual page of the product
            current_url = driver.current_url  # keep url where the page of the product exists
            driver.close()
            soup_var = BeautifulSoup(source_code, "html.parser")
            title_of_product = soup_var.find("h4", {
                "class": "ipsType_sectionHead ipsType_break ipsType_bold ipsTruncate ipsSpacer_bottom ipsType_reset"})[
                "title"]  # get the title of the product
            price_of_product = soup_var.find("span", {"class": "cFilePrice"}).string  # Get the price of the product
            sellers_rank = soup_var.find("h1", {
                "class": "ipsType_reset"}).string  # Get the rank of the seller (100%, 90%, e.t.c)
            sellers_name = soup_var.find("a", {"class": "ipsType_break"}).string  # Get the name of the seller
            products_image = soup_var.find("img", {"class", "classifieds-rounded"})[
                "src"]  # Get the image of the product
            if sellers_rank == "0%":
                reviews_quality_rank = "0%"
            else:
                html, reviews_tab_url = self.go_to_reviews_tab_from_products_page_and_get_source_code(current_url)
                list_of_reviewers_prof_urls = self.get_list_with_all_reviewers_prof_urls(html, reviews_tab_url)  # get list with the urls from the profiles of the reviewers
                get_review_quality_of_each_reviewer_ls = self.get_review_quality_of_each_reviewer(list_of_reviewers_prof_urls)
                try:
                    reviews_quality_rank = str(round(sum(get_review_quality_of_each_reviewer_ls) / len(get_review_quality_of_each_reviewer_ls), 2))
                except:
                    # This means that the reviewers are unranked
                    reviews_quality_rank = "0%"
            info.append(
                [title_of_product, price_of_product, products_image, sellers_name, sellers_rank, reviews_quality_rank])
        return info

    def crawl_category_of_products(self):
        category_url_to_crawl = self.get_user_input_about_which_category_page_to_crawl()
        page_code = self.go_to_page_of_category_and_return_the_html(category_url_to_crawl)
        pages_num = int(self.get_num_of_pages_from_pagination_bar(page_code))  # get the pagination number
        products_of_page_ls = self.get_products_of_page(page_code)  # a list that contains the urls for the individual page of each product
        information_ls = [ls for ls in self.retrieve_info(products_of_page_ls)]

        # if pages_num > 1:
        #     for i in range(2, pages_num+1):
        #         category_url_to_crawl = category_url_to_crawl+f"page/{i}/"
        #         page_code = go_to_page_of_category_and_return_the_html(category_url_to_crawl)
        #         products_of_page_ls = get_products_of_page(page_code)
        #         information_ls = [ls for ls in retrieve_info(products_of_page_ls)]

        return information_ls


    def save_to_excel_file(self):
        df = pd.DataFrame(self.crawl_category_of_products(), columns=['Product Title', 'Product Price', 'Product Image', 'Seller Name', 'Seller Rank', 'Review Quality'])
        # save the DataFrame as an Excel file
        df.to_excel('output.xlsx', index=False)

if __name__ == '__main__':
    InsomniaCrawler()

# html, reviews_tab_url = go_to_reviews_tab_from_products_page_and_get_source_code(url)
# list_of_reviews = get_list_with_type_of_reviews(html, reviews_tab_url)
# print(list_of_reviews)
# list_of_reviewers_prof_urls = get_list_with_all_reviewers_prof_urls(html, reviews_tab_url)  # get list with the urls from the profiles of the reviewers
# print(list_of_reviewers_prof_urls)
# print(get_review_quality_of_each_reviewer(list_of_reviewers_prof_urls))
