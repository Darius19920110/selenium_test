from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pprint
from accept_cookies import load_and_accept_cookies

pp = pprint.PrettyPrinter()

def get_links(driver: webdriver.Chrome) -> list:
    prop_container = driver.find_element(By.XPATH, '//*[@class="css-1itfubx e34pn540"]')
    prop_list = prop_container.find_elements(By.XPATH, "./div")
    link_list = []

    for property in prop_list:
        a_tag = property.find_element(By.TAG_NAME, "a")
        link = a_tag.get_attribute("href")
        link_list.append(link)

    return link_list

big_list = []
properties = []

driver = load_and_accept_cookies(
    URL="https://www.zoopla.co.uk/new-homes/property/london/?q=London&results_sort=newest_listings&search_source=new-homes&page_size=25&pn=1&view_type=list", 
    switch_to_frame='gdpr-consent-notice', 
    button_id="save"
    )
    
for i in range(5): # The first 5 pages only
    big_list.extend(get_links(driver)) # Call the function we just created and extend the big list with the returned list
    ## TODO: Click the next button. Don't forget to use sleeps, so the website doesn't suspect
    next_button_list = driver.find_element(By.XPATH, "//li[@class='css-qhg1xn-PaginationItemPreviousAndNext-PaginationItemNext eaoxhri2']")
    next_button_list.click()
    time.sleep(2)

    if i == 0:
        driver.implicitly_wait(3)
        pop_up = driver.find_element(By.XPATH, "//*[@data-testid='modal-close']")
        pop_up.click()
        time.sleep(1)

for link in big_list:
    ### Using while True loop, because sometimes can not find anything in DOM when searching for price or address, or description or, bedrooms. Run again, and will fix it.
    while True:
        try:
            dict_properties = {'Price': None, 'Address': None, 'Bedrooms': None, 'Description': None}

            ## TODO: Visit all the links, and extract the data. Don't forget to use sleeps, so the website doesn't suspect
            driver.get(link)
            time.sleep(2)

            price = driver.find_element(By.XPATH, "//p [@data-testid='price']").text ## Can not find this sometimes
            dict_properties["Price"] = price

            address = driver.find_element(By.XPATH, "//address[@data-testid='address-label']").text ## Can not find this sometimes
            dict_properties["Address"] = address

            bedrooms_description = driver.find_element(By.XPATH, "//*[@id='listing-summary-details-heading']").text ## Can not find this sometimes
            bedrooms = bedrooms_description.split(" ")[0]
            dict_properties["Bedrooms"] = bedrooms

            div_tag = driver.find_element(By.XPATH, "//*[@data-testid='truncated_text_container']")
            span_tag = div_tag.find_element(By.XPATH, ".//span") ## Can not find this sometimes
            description = span_tag.text
            dict_properties["Description"] = description

            properties.append(dict_properties)
            break
        except Exception as e:
            time.sleep(2)
            continue

print(len(properties))
pp.pprint(properties)


driver.quit() # Close the browser when you finish