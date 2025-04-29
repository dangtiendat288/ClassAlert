import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from twilio.rest import Client

classNbr = "63161"


def send_sms(body):
    # Twilio account credentials
    account_sid = "___________________________________"
    auth_token = "___________________________________"

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    # Send SMS
    message = client.messages.create(
        from_="whatsapp:+14155238886", body=body, to="whatsapp:+14807433265"
    )

    print("Message SID:", message.sid)


# Example usage

url = f"https://catalog.apps.asu.edu/catalog/classes/classlist?advanced=true&campusOrOnlineSelection=C&classNbr={classNbr}&honors=F&promod=F&searchType=all&session=C&term=2247"

# Create a WebDriver instance
driver = webdriver.Firefox()

# Load the webpage
driver.get(url)

# Define the condition for the while loop
condition_met = False

while not condition_met:
    try:
        # Wait for some time to allow JavaScript to execute (adjust as needed)
        element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "class-results"))
        )

        # Get the page source after JavaScript execution
        page_source = driver.page_source

        # Parse the HTML content of the webpage
        soup = BeautifulSoup(page_source, "html.parser")

        # Find the div tag with class="class-results-cell seats"
        div_results_cell = soup.find("div", class_="class-results-cell seats")

        # Check if the div was found
        if div_results_cell:
            # Find the div tag with class="text-nowrap" inside the div_results_cell
            div_text = div_results_cell.find("div", class_="text-nowrap")

            # Check if the inner div was found
            if div_text:
                # Extract the text from the inner div tag
                text = div_text.get_text(strip=True)
                print(text)

                # Check if the condition is met
                if text != "0 of 165open seats":
                    print("Condition met. Call twilio API.")
                    send_sms(f"Class {classNbr} is available now!")
                    condition_met = True
            else:
                print("Inner div with class 'text-nowrap' not found.")
        else:
            print("Outer div with class 'class-results-cell seats' not found.")

    finally:
        # Refresh the page for the next iteration
        driver.refresh()

# Close the WebDriver
driver.quit()
