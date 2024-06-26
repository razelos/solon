import os
import time
import pygame
from tkinter import messagebox
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

# File Paths that are needed 
# Get the current directory of your script
current_dir = os.path.dirname(__file__)

# Navigate up one level to the parent directory, which is 'solon search'
parent_dir = os.path.dirname(current_dir)

# Define the path to the 'info.csv' file in the 'data' folder
INPATH = os.path.join(parent_dir, 'data', 'input_data.csv')
INFOPATH = os.path.join(parent_dir, 'data', 'info_data.csv')
OUTPATH = os.path.join(parent_dir, 'data', 'output_data.csv')
TIMEPATH = os.path.join(parent_dir, 'data', 'timestamps.csv')
CHROMEDRIVER_PATH = os.path.join(parent_dir, 'chromedriver-win64', 'chromedriver.exe')
CHROME_PATH = os.path.join(parent_dir, "chrome-win64", "chrome.exe")
SOUND_PATH = os.path.join(parent_dir, "ui", "ping.mp3")
# got the sound from: https://pixabay.com/sound-effects/ping-82822/

URL = 'https://extapps.solon.gov.gr/mojwp/faces/TrackLdoPublic'


from logic.search_status import stop_search, cancel_search_var
from logic.solon_load import load_csv
from ui.solon_show_data import show_data
from logic.timestamp import time_stamp, get_timestamp, saved_time
from logic.write_data import write_data


# Peform the search
def solon_search(input_data, progress_var, n, progress_window, tree, timestamp_label, search_time_label, total_searches_label):
  try:
    pygame.mixer.init()

    output_data = []

    # initalize web driver and settings
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    # next line to stop DevTools listening on ws://127.0.0.1:65051/devtools/browser/1e12e06b-e9f3-40fc-953d-7e116e6241e1
    # from appearing
    chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    chromeOptions.binary_location = (CHROME_PATH)

    service_obj = Service(CHROMEDRIVER_PATH, HideCommandPromptWindow=True, verbose=False)
    driver = webdriver.Chrome(service=service_obj, options=chromeOptions)
    wait = WebDriverWait(driver, 20) # number of seconds to wait 
    driver.get(URL)

    # handle one exception - error box
    # example ΕΙΡΗΝΟΔΙΚΕΙΟ ΕΛΕΥΣΙΝΑΣ / 1235 / 2021
    def handle_error_box():
      try:
        # Check if an error box is present
        ok_button_xpath = '//*[@id="pdSaveFirst_ok"]/a/span'
        ok_box = wait.until(EC.presence_of_element_located((By.XPATH, ok_button_xpath)))
        if ok_box:
          # Click the OK button to dismiss the error box
          driver.find_element(By.XPATH, ok_button_xpath).click()
          output_data.append(['ΕΛΕΓΞΤΕ ΣΤΟΙΧΕΙΑ ΕΙΣΑΓΩΓΗΣ'])
      except(TimeoutException, WebDriverException) as e:
        messagebox.showerror("Σφάλμα", "Αδύνατη η σύνδεση στο δίκτυο.")
        output_data.append(['ΥΠΗΡΞΕ ΚΑΠΟΙΟ ΣΦΑΛΜΑ'])
        progress_window.destroy()
        cancel_search_var()
      except Exception as E:
        output_data.append(['ΥΠΗΡΞΕ ΚΑΠΟΙΟ ΣΦΑΛΜΑ'])
        progress_window.destroy()
        cancel_search_var()

    i = 0
    while not(stop_search) and i < n:
      try:
        # dropdown court menu
        wait.until(EC.presence_of_element_located((By.ID, 'courtOfficeOC::content')))

        katastima = input_data[i][0]
        GakNumber = input_data[i][1]
        YearNumber = input_data[i][2]

        # find and select dropdownbox
        dropdownbox = driver.find_element(By.ID, 'courtOfficeOC::content')
        select = Select(dropdownbox)
        select.select_by_value("0")
        select.select_by_visible_text(katastima)

        # find and click Gak button
        GakButton = driver.find_element(By.XPATH, '//*[@id="socSelectedSearchOption:_0"]')
        GakButton.click()

        # find and fill out gak
        gak = driver.find_element(By.XPATH, '//*[@id="it1::content"]')
        gak.clear()
        gak.send_keys(GakNumber)

        # find and fill out year
        year = driver.find_element(By.XPATH, '//*[@id="it2::content"]')
        year.clear()
        year.send_keys(YearNumber)

        #find and click search button
        Submit = driver.find_element(By.XPATH, '//*[@id="ldoSearch"]')
        Submit.click()
        # if testtext is going to be the same as previous entry then wait a bit for the search to be completed
        if i > 0:
          if GakNumber == input_data[i-1][1] and YearNumber == input_data[i - 1][2]:
            time.sleep(10)
        # box with gak number / year number to be equal to the input_data
        testtext = GakNumber + '/' + YearNumber
        wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="pc1:ldoTable::db"]/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/span'), testtext))
        
        #find and print the decision
        decision = driver.find_element(By.XPATH, '//*[@id="pc1:ldoTable::db"]/table/tbody/tr/td[2]/div/table/tbody/tr/td[7]')
        dtext = decision.get_attribute('innerText')

        # add decision to output data
        if dtext.isspace():
          output_data.append(['ΕΚΚΡΕΜΕΙ ΑΠΟΦΑΣΗ'])
        else:
          output_data.append([dtext])

      except TimeoutException as TE:
        handle_error_box()
      # # Update the progress bar
      finally:
        i += 1
        progress_var.set(i + 1)

    driver.quit()
    time_stamp(n)
    
    def play_sound():
      try:
        pygame.mixer.music.load(SOUND_PATH)
        pygame.mixer.music.play()
      except Exception as E:
        pass
    
    play_sound()
    progress_var.set(n + 1)
    
    write_data(OUTPATH, output_data)

    timestamp, total_searches = get_timestamp()

    hours, minutes = saved_time(total_searches[0])
    timestamp_label.config(text="ΤΕΛΕΥΤΑΙΑ ΑΝΑΖΗΤΗΣΗ: " + timestamp[0])
    search_time_label.config(text = "ΕΧΕΤΕ ΓΛΥΤΩΣΕΙ ΣΥΝΟΛΙΚΑ " + hours + " ΩΡΕΣ ΚΑΙ " + minutes + " ΛΕΠΤΑ ΑΝΑΖΗΤΗΣΗΣ")
    total_searches_label.config(text = "ΕΧΕΤΕ ΠΡΑΓΜΑΤΟΠΟΙΗΣΕΙ ΣΥΝΟΛΙΚΑ " + total_searches[0] + " ΑΝΑΖΗΤΗΣΕΙΣ")
    progress_window.destroy()
    cancel_search_var()
    data = load_csv()
    show_data(data, tree)

  except (TimeoutException) as E:
    handle_error_box(stop_search)
  except(WebDriverException) as E:
    messagebox.showerror("Σφάλμα", "Αδύνατη η σύνδεση στο δίκτυο.")
    progress_window.destroy()
    cancel_search_var()
  except Exception as E:
    progress_window.destroy()
    cancel_search_var()
