def get_client_data():
    #!Important! Put updated Meevo username and password here in quotes and overwrite (save) this file in the same folder.
    meevo_user = "willc0691"
    meevo_pw = "Wi11C1ine&"

    #---------------------------------------------------Delete previous files that will interfere with default download name of new ones-----------------------------------------
    import os
    # #delete tomorrow's appointments' raw xls
    # if os.path.exists(r"C:\Users\frontdesk\Downloads\AQ065.xls"):
    #     os.remove(r"C:\Users\frontdesk\Downloads\AQ065.xls")
    # #delete previous formatted csv
    # if os.path.exists(r"C:\Users\frontdesk\Downloads\apt_confirmations.csv"):
    #     os.remove(r"C:\Users\frontdesk\Downloads\apt_confirmations.csv")

    #-------------------------------------------------------------Download tomorrow's confirmations from Meevo-------------------------------------------------------------------
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://me.meevo.com/login/2")
    driver.maximize_window()

    #login Credentials
    user = driver.find_element_by_name("userNameField")
    pw = driver.find_element_by_name("passwordField")

    user.clear()
    user.send_keys(meevo_user)
    pw.clear()
    pw.send_keys(meevo_pw)
    pw.send_keys(Keys.ENTER)

    #delete welcome popup window
    import time
    time.sleep(15)
    try:
        exit_welcome_popup = driver.find_element_by_xpath("//*[@id=\"wm-shoutout-71462\"]/div[1]").click()
    except:
        pass

    driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div[1]/div").click()

    #reports in sidemenu
    driver.find_element_by_xpath("/html/body/meevo-side-menu/div/md-sidenav[1]/div[9]").click()


    #Appointment related reports
    time.sleep(4)
    driver.find_element_by_xpath("/html/body/meevo-side-menu/div/md-sidenav[2]/div/div[2]").click()

    #appointment confirmation form
    time.sleep(4)
    # /html/body/div[1]/div[2]/div[2]/section/form/div[1]/div/div[2]/div/div[7]/div
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/section/form/div[1]/div/div[2]/div/div[7]/div").click()

    #open time span drop down
    time.sleep(4)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/section/form/div[1]/div/div[2]/div[2]/div/div[2]/meevo-report-control[1]/div/div/meevo-date-range-with-presets/ng-form/div[1]/div[1]/div/md-select").click()

    #select tomorrow
    time.sleep(4)
    driver.find_element_by_xpath("/html/body/div[5]/md-select-menu/md-content/md-option[9]").click()

    #select sort report by drop down
    time.sleep(4)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/section/form/div[1]/div/div[2]/div[2]/div/div[2]/meevo-report-control[3]/div/div/div/md-select").click()

    #select confirmation status
    time.sleep(4)
    driver.find_element_by_xpath("/html/body/div[6]/md-select-menu/md-content/md-option[3]").click()

    #run report button
    time.sleep(4)
    driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/section/form/div[2]/div/div[2]/button").click()

    time.sleep(5)
    driver.switch_to.frame("reportContent")

    #hover over download options dropdown
    time.sleep(4)
    from selenium.webdriver.common.action_chains import ActionChains
    element_to_hover_over = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/ul[1]/li[10]")
    ActionChains(driver).move_to_element(element_to_hover_over).perform()

    #xls file option
    time.sleep(4)
    driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/ul[1]/li[10]/div/ul/li[2]/a").click()

    time.sleep(8)
    driver.close()

    #-------------------------------------------------------------Clean and reformat AQ065 from XLS to csv-----------------------------------------------------------------
    import pandas as pd
    df = pd.DataFrame(pd.read_excel(r"/Users/willcline/Downloads/AQ065.xls"))
    df.rename(columns={'Unnamed: 19':'service', 'Unnamed: 17':'employee', 'Unnamed: 10':'datetime', 'Unnamed: 13':'datetime1', 'Unnamed: 4':'phone', 'Unnamed: 2':'client','Unnamed: 1':'confirmation_status'}, inplace=True)
    df = df[['client','phone','datetime', 'datetime1', 'employee', 'service', 'confirmation_status']]
    # df.head(50)
    df['datetime1'] = df['datetime1'].shift(-1)
    # df['datetime'] = df['datetime'].shift(1)
    df.dropna(subset=['client','phone','datetime','datetime1','employee', 'service', 'confirmation_status'], how='all', inplace=True)
    df.dropna(subset=['employee', 'datetime', 'confirmation_status'], how='all', inplace=True)
    #drop a header row
    df = df[df.employee != 'Employee']
    df = df[df.phone != 'Phone Number']
    df['confirmation_status'] = df['confirmation_status'].ffill()
    df.dropna(subset=['client','phone','datetime','datetime1','employee', 'service'], how='all', inplace=True)
    #get rid of those who opted out of phone confirmations??
    df.dropna(subset=['phone'], how='all',inplace=True)
    df = df.ffill()

    #data altering
    #phone
    df['phone'] = df['phone'].str.replace(r"[a-zA-Z]",'').str.replace('(','').str.replace(')','').str.replace(':','').str.replace('-','').str.replace(' ','')
    #times
    df['time'] = df['datetime'].str.split(' ').str[1:3].apply(', '.join).str.replace(',','')
    #employee firstname
    df['employee_firstname'] = df['employee'].str.split(', ').str[-1]
    #service
    df['service'] = df['service'].str.replace('Massage 60 Min Custom Session', '60 minute massage').str.replace('Massage 90 Min Custom Session', '90 minute massage').str.replace('60 Min Customized Facial', '60 minute facial')
    df = df[df['confirmation_status'] == 'Unconfirmed']
    #change phone to str
    df['phone'] = df['phone'].astype('str')

    import numpy as np
    #add column for recording client's desired confirmation status
    df['client_response'] = np.nan
    df['client_response_ts'] = np.nan
    #add column for recording whether anything has been done in meevo to reflect prior column
    df['meevo_status_change'] = np.nan
    df['meevo_status_change_ts'] = np.nan

    df.to_csv()