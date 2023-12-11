import os
import time
import logging
import undetected_chromedriver as uc
import pyperclip
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException


class AutoLeetCode:
    def __init__(self, 
                 driver_executable_path : str = None,
                 driver_arguments : str = None,
                 headless : bool = False,
                 username : str = None,
                 password : str = None,
                 url : str = None,
                 verbose: bool = False,
                 incognito : bool = False,
                 skip_login : bool = False,
                 user_data_dir : str = None,
                 login_type : str = 'normal'):
        self.headless = headless

        if not skip_login:
            if not username or not password:
                logging.warning(
                    "The username and password parameters are deprecated and will be removed soon."
                    " Please adjust your environment variables to pass username and password."
                )
                raise NameError(
                    f'Either provide username or password.')
            username = username
            password = password

        self.url = url or "https://leetcode.com/accounts/login"
        self.task_url = "https://leetcode.com/problems/"
        if verbose:
            logging.getLogger().setLevel(logging.INFO)
            logging.info('Verbose mode active')
        options = uc.ChromeOptions()
        options.headless = self.headless  
        if incognito:
            options.add_argument('--incognito')
        if driver_arguments:
            for _arg in driver_arguments:
                options.add_argument(_arg)

        logging.info('Loading undetected Chrome')
        self.browser = uc.Chrome(
            user_data_dir = user_data_dir,
            driver_executable_path = driver_executable_path,
            options = options,
            headless = headless,
            log_level = 10,
        )
        agent = self.browser.execute_script("return navigator.userAgent")
        self.browser.execute_cdp_cmd(
            'Network.setUserAgentOverride',
            {"userAgent": agent.replace('Headless', '')}
        )
        self.browser.set_page_load_timeout(15)

        logging.info('Loaded undetected Chrome')
        logging.info('Opening LeetCode')
        self.browser.get(self.url)

        if not skip_login and login_type == 'normal':
            self.login(username, password)
        elif not skip_login and login_type == 'manully':
            self.login_manully(username, password)



    def login(self, username, password):
        """
        Performs the login process with the provided username and password.

        This function operates on the login page.
        It fills in the username and password fields. 
        It finds and clicks the login button 
        """
        time.sleep(2)
        # Find the email textbox and fill it with the username
        email_box = self.sleepy_find_element(By.ID, 'id_login')
        email_box.send_keys(username)
        logging.info('Email box filled')
        
        # Find the password textbox and fill it with the password
        password_box = self.sleepy_find_element(By.ID, 'id_password')
        password_box.send_keys(password)
        logging.info('Password box filled')

        # Find the login button and click it
        login_button = self.sleepy_find_element(By.ID, 'signin_btn')
        login_button.click()
        logging.info('Login button clicked')
        time.sleep(1)
    
    def login_manully(self, username, password, timeout : int = 15):
        if "login" in self.browser.current_url:
            time.sleep(2)
            # Find the email textbox and fill it with the username
            email_box = self.sleepy_find_element(By.ID, 'id_login')
            email_box.send_keys(username)
            logging.info('Email box filled')
            
            # Find the password textbox and fill it with the password
            password_box = self.sleepy_find_element(By.ID, 'id_password')
            password_box.send_keys(password)
            logging.info('Password box filled')

        try: 
            WebDriverWait(self.browser, timeout).until(
                lambda driver: self.check_login_success_condition()
            )
            logging.info('Login process is completed manually')
        except TimeoutError:
            logging.error('Login process is not completed manually')

    def check_login_success_condition(self):
        return "login" not in self.browser.current_url and "error" not in self.browser.current_url and "leetcode.com" in self.browser.current_url



    def run_and_collect(self, problem_id : str, language : str, code : str):
        """
        run the code to the problem.

        This function operates on the problem page.
        It fills in the code editor with the provided code.
        It finds and clicks the submit button.
        It waits for the submission to complete.
        """
        logging.info('Submitting code')
        task_url = self.task_url + problem_id
        self.browser.get(task_url)
        logging.info('Opening %s', task_url)
        time.sleep(1)

        return_result_status, return_result_details = "", ""

        # check if need change language
        code_editor = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-keybinding-context='1']"))
        )
        current_language = code_editor.get_attribute("data-mode-id")

        if current_language != language.lower():

            # Find the language dropdown and click it
            language_dropdown_button_selector = "button.rounded.items-center.whitespace-nowrap.focus\:outline-none.inline-flex.bg-transparent"
            language_dropdown_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, language_dropdown_button_selector))
            )
            language_dropdown_button.click()
        

            # Find the language dropdown and click it
            csharp_option_xpath = "//div[contains(text(), '"+language+"')]"
            csharp_option = WebDriverWait(self.browser, 3).until(
                EC.element_to_be_clickable((By.XPATH, csharp_option_xpath))
            )
            csharp_option.click()

        # Find the code editor and fill it with the code
        code_textarea_selector = "textarea.inputarea"
        code_textarea = WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, code_textarea_selector))
        )
        code_textarea.click()

        # Use ActionChains to select all text
        actions = ActionChains(self.browser)
        # For Windows/Linux, use CTRL. For Mac, use COMMAND.
        modifier_key = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL
        actions.key_down(modifier_key).send_keys('a').key_up(modifier_key).perform()
        # Wait briefly to ensure the action is completed
        time.sleep(0.5)

        # Delete the selected text
        actions = ActionChains(self.browser)
        actions.send_keys(Keys.DELETE).perform()

        # Copy your new code to clipboard
        pyperclip.copy(code)
        # Paste the new code into the editor
        actions = ActionChains(self.browser)
        actions.key_down(modifier_key).send_keys('v').key_up(modifier_key).perform()
        time.sleep(1)

        # Find the submit button and click it
        submit_button_selector = "button[data-e2e-locator='console-run-button']"
        submit_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector))
        )
        submit_button.click()


        # Wait for the submission to complete
        logging.info('Waiting for submission to complete')
        try:
            result_element = WebDriverWait(self.browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e-locator='console-result'], span[data-e2e-locator='console-result']"))
            )
            result_text = result_element.text
            logging.info('Submission result: %s', result_text)
            return_result_status = result_text

            if "Error" in result_text:
                try:
                    # Using a more general CSS selector
                    runtime_error_elements = self.browser.find_elements(By.CSS_SELECTOR, ".font-menlo.text-red-3.dark\\:text-dark-red-3.whitespace-pre-wrap.break-all.text-xs")
                    print(len(runtime_error_elements))
                    return_result_details = runtime_error_elements[0].text
                    # if len(runtime_error_elements) > 0:
                    #     logging.error('Runtime error details: %s', runtime_error_elements[0].text)
                except NoSuchElementException:
                    logging.error('Error details not found')        

        except TimeoutException:
            logging.error('Timed out waiting for submission result')
            # Handle the timeout situation

        return return_result_status, return_result_details


    def submit_and_collect(self, problem_id : str, language : str, code : str):
        """
        Submits the code to the problem.

        This function operates on the problem page.
        It fills in the code editor with the provided code.
        It finds and clicks the submit button.
        It waits for the submission to complete.
        """
        logging.info('Submitting code')
        task_url = self.task_url + problem_id
        self.browser.get(task_url)
        logging.info('Opening %s', task_url)
        time.sleep(1)

        # check if need change language
        code_editor = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-keybinding-context='1']"))
        )
        current_language = code_editor.get_attribute("data-mode-id")

        if current_language != language.lower():

            # Find the language dropdown and click it
            language_dropdown_button_selector = "button.rounded.items-center.whitespace-nowrap.focus\:outline-none.inline-flex.bg-transparent"
            language_dropdown_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, language_dropdown_button_selector))
            )
            language_dropdown_button.click()
        

            # Find the language dropdown and click it
            csharp_option_xpath = "//div[contains(text(), '"+language+"')]"
            csharp_option = WebDriverWait(self.browser, 3).until(
                EC.element_to_be_clickable((By.XPATH, csharp_option_xpath))
            )
            csharp_option.click()

        # Find the code editor and fill it with the code
        code_textarea_selector = "textarea.inputarea"
        code_textarea = WebDriverWait(self.browser, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, code_textarea_selector))
        )
        code_textarea.click()

        # Use ActionChains to select all text
        actions = ActionChains(self.browser)
        # For Windows/Linux, use CTRL. For Mac, use COMMAND.
        modifier_key = Keys.COMMAND if platform.system() == 'Darwin' else Keys.CONTROL
        actions.key_down(modifier_key).send_keys('a').key_up(modifier_key).perform()
        # Wait briefly to ensure the action is completed
        time.sleep(0.5)

        # Delete the selected text
        actions = ActionChains(self.browser)
        actions.send_keys(Keys.DELETE).perform()

        # Copy your new code to clipboard
        pyperclip.copy(code)
        # Paste the new code into the editor
        actions = ActionChains(self.browser)
        actions.key_down(modifier_key).send_keys('v').key_up(modifier_key).perform()
        time.sleep(1)

        # Find the submit button and click it
        submit_button_selector = "button[data-e2e-locator='console-submit-button']"
        submit_button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, submit_button_selector))
        )
        submit_button.click()

        # Wait for the submission to complete
        logging.info('Waiting for submission to complete')
        try:
            result_element = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-e2e-locator='console-result'], span[data-e2e-locator='console-result']"))
            )
            result_text = result_element.text
            logging.info('Submission result: %s', result_text)


            if "Error" in result_text:
                try:
                    # Using a more general CSS selector
                    runtime_error_elements = self.browser.find_elements(By.CSS_SELECTOR, ".font-menlo.text-red-3.dark\\:text-dark-red-3.whitespace-pre-wrap.break-all.text-xs")
                    print(len(runtime_error_elements))
                    if len(runtime_error_elements) > 0:
                        logging.error('Runtime error details: %s', runtime_error_elements[0].text)
                except NoSuchElementException:
                    logging.error('Error details not found')        

        except TimeoutException:
            logging.error('Timed out waiting for submission result')
            # Handle the timeout situation




    def sleepy_find_element(self, by: By, query : str, attempt_count : int = 20, sleep_duration : int = 1):
        '''
        Finds the web element using the locator and query.

        This function attempts to find the element multiple times with a specified
        sleep duration between attempts. If the element is found, the function returns the element.

        Args:
            by (selenium.webdriver.common.by.By): The method used to locate the element.
            query (str): The query string to locate the element.
            attempt_count (int, optional): The number of attempts to find the element. Default: 20.
            sleep_duration (int, optional): The duration to sleep between attempts. Default: 1.

        Returns:
            selenium.webdriver.remote.webelement.WebElement: Web element or None if not found.
        '''
        for _count in range(attempt_count):
            item = self.browser.find_elements(by, query)
            if len(item) > 0:
                item = item[0]
                logging.info('Element %s has found', query)
                break
            logging.info('Element %s is not present, attempt: %d', query, _count+1)
            time.sleep(sleep_duration)
        return item



if __name__ == '__main__':
    autoleet = AutoLeetCode(
        headless = False,
        username = "your_username",
        password = "your_password",
        verbose = False,
        incognito = False,
        skip_login = False,
        user_data_dir = "data/profile/",
        login_type = 'manully'
    )
    time.sleep(2)

    chatgpt_generated_code = "xxxxxxxxxxxx"
    task_name = "Two Sum"
    language = "Python3"

    # if only run code and collect
    result_status, result_details = autoleet.run_and_collect(task_name, language, chatgpt_generated_code)

    # if submit codd and collect
    result_status, result_details = autoleet.submit_and_collect(task_name, language, chatgpt_generated_code)
