from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# URL IS HIDDEN FOR SECTIRY

def login(driver, username, password):
    try:
        driver.get("https://example.com/login")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_string"))
        ).send_keys(username)

        driver.find_element(By.ID, "login_pass").send_keys(password)

        driver.find_element(By.XPATH, "//button[text()='Login']").click()

        # Check successful login
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "//img[@src='https://example.com/assets/images/user.png' and @width='68' and @height='68' and @alt='User']"
            ))
        )
        print("Login successful and page is loaded.")
    except Exception as e:
        print(f"Login failed: {e}")
        driver.quit()
        return False
    return True

def fetch_data_for_client(driver, client_id):
    url = f"https://example.com/clients/view/{client_id}"
    driver.get(url)

    try:
        # Wait for the page to load by checking the presence of the "Status" field
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//b[text()='Status']"))
        )

        # Fetch the required fields
        status = driver.find_element(By.XPATH, "//b[text()='Status']/following::input[1]").get_attribute('value')
        department = driver.find_element(By.XPATH, "//input[@id='department']").get_attribute('value')
        company_name = driver.find_element(By.XPATH, "//b[text()='Company Name']/following::input[1]").get_attribute('value')
        company_serial_number = driver.find_element(By.XPATH, "//b[text()='Company Serial Number']/following::input[1]").get_attribute('value')
        website = driver.find_element(By.XPATH, "//b[text()='Website']/following::input[1]").get_attribute('value')
        company_address = driver.find_element(By.XPATH, "//b[text()='Company Address']/following::input[1]").get_attribute('value')
        postal_code = driver.find_element(By.XPATH, "//b[text()='Postal Code']/following::input[1]").get_attribute('value')

        # Fetch the client holder details
        client_holder_table = driver.find_element(By.ID, "client_holder")
        client_holders = []
        for i, row in enumerate(client_holder_table.find_elements(By.XPATH, ".//tbody/tr"), start=1):
            employee_no = row.find_element(By.XPATH, "./td[1]").text
            name = row.find_element(By.XPATH, "./td[2]").text
            gender = row.find_element(By.XPATH, "./td[3]").text
            contact_number = row.find_element(By.XPATH, "./td[4]").text
            type_of_holder = row.find_element(By.XPATH, "./td[5]").text
            client_holders.append({
                f'employee_no_{i}': employee_no,
                f'name_{i}': name,
                f'gender_{i}': gender,
                f'contact_number_{i}': contact_number,
                f'type_of_holder_{i}': type_of_holder
            })

        # Fetch the person-in-charge details
        person_in_charge_table = driver.find_element(By.ID, "person_in_charge_table")
        persons_in_charge = []
        for i, row in enumerate(person_in_charge_table.find_elements(By.XPATH, ".//tbody/tr"), start=1):
            person_in_charge = row.find_element(By.XPATH, "./td[1]").text
            designation = row.find_element(By.XPATH, "./td[2]").text
            contact_no = row.find_element(By.XPATH, "./td[3]").text
            status_of_pic = row.find_element(By.XPATH, "./td[4]").text
            email = row.find_element(By.XPATH, "./td[5]/a").get_attribute('href').replace('mailto:', '')
            created_at = row.find_element(By.XPATH, "./td[6]").text
            persons_in_charge.append({
                f'person_in_charge_{i}': person_in_charge,
                f'designation_{i}': designation,
                f'contact_no_{i}': contact_no,
                f'status_of_pic_{i}': status_of_pic,
                f'email_{i}': email,
                f'created_at_{i}': created_at
            })

        print(client_id)
        
        return {
            'client_id': client_id,
            'status': status,
            'department': department,
            'company_name': company_name,
            'company_serial_number': company_serial_number,
            'website': website,
            'company_address': company_address,
            'postal_code': postal_code,
            **{k: v for d in client_holders for k, v in d.items()},
            **{k: v for d in persons_in_charge for k, v in d.items()},
        }
    except Exception as e:
        print(f"Error fetching data for client ID {client_id}: {e}")
        return None


username = 'admin'
password = ''

if login(driver, username, password):
    client_ids = range(1, 5000)
    data = []

    for client_id in client_ids:
        client_data = fetch_data_for_client(driver, client_id)
        if client_data:
            data.append(client_data)
        time.sleep(1)

    df = pd.DataFrame(data)
    df.to_excel('data.xlsx', index=False)
    print("Data has been successfully saved to 'data.xlsx'.")

driver.quit()
