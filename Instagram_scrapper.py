import os   #import the neccesary libraries
import time
import shutil
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class App:
    def __init__(self,username='Username',password='Password',target_username='knotyourpal',path='D:\PARESH\IG scrapping photos'): #specify the login credentials, the target username and the path where you want to save photos
        path_check = os.path.exists(path)   #checks weather the specified path exists or not
        if path_check==False:               #make the folder if it does not exists
            os.mkdir(path)
        self.username  = username
        self.password = password
        self.target_username = target_username
        self.path = path
        self.driver = webdriver.Chrome('C:/Users/ASUS/Downloads/chromedriver_win32/chromedriver')
        self.main_url = 'https://www.instagram.com'
        self.driver.get(self.main_url)      #Visits the instagram homepage
        self.error = False
        self.all_images = []                #List to save all the image links
        self.log_in()
        time.sleep(3)
        self.close_dialog()

        if (self.error == False):
            self.open_target_profile()
            self.no_of_posts()

        self.download_images()
        print('Images Downloaded And Saved To The Desired Location')
        self.driver.close()

    def log_in(self):       #Function to lgoin the user
        try:
            time.sleep(5)
            login_in_button = self.driver.find_element_by_xpath("//span[@id='react-root']//p[@class='izU2O']//a") #Find the login page button
            login_in_button.click()         #Clicks the button found
            time.sleep(5)

            try:
                username_input = self.driver.find_element_by_class_name('_2hvTZ.pexuQ.zyHYP')           #Find text box to input username
                username_input.send_keys(self.username)                                                 #Input the username
                password_input = self.driver.find_element_by_xpath("//input[@aria-label='Password']")   #Find text box to input password
                password_input.send_keys(self.password)                                                 #Input the username
                password_input.submit()                                                                 #Press login Button
                time.sleep(3)

            except Exception:
                self.error = True
                print("Incorrect Username Or Password")

        except Exception:
            self.error = True
            print("Login Button Not Found")


    def close_dialog(self):                                                     #Function to close the dialog box
        self.driver.get(self.driver.current_url)
        not_now_button = self.driver.find_element_by_class_name("aOOlW.HoLwm")  #Find the 'Not now' button
        not_now_button.click()                                                  #Click not now button

    def open_target_profile(self):                                              #Function to open target user's profile
        try:
            target_profile_url = self.main_url+ '/' + self.target_username      #URL to get target username profile
            self.driver.get(target_profile_url)                                 #Visit the generated url

        except Exception:
            self.error = True
            print('Cannot Find Search bar')

    def no_of_posts(self):
        try:
            no_ofposts = self.driver.find_element_by_xpath('//span[@class="g47SY "]')       #Fetch the no of posts from the top of the webpage
            no_ofposts = str(no_ofposts.text).replace(',',"")
            print(no_ofposts)
            self.no_ofposts = int(no_ofposts)

            if self.no_ofposts > 12:                                                        #We don't require to scroll unless the no of posts are less than 12
                no_ofscrolls = int(self.no_ofposts/12) + 1

                for value in range(no_ofscrolls):
                    print(value)
                    self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')       #Scrolls to the bottom of the webpage
                    time.sleep(2)
                time.sleep(2)

        except Exception:
            self.error = True
            print('Cannot Find no of posts')


    def download_images(self):                                  #Function to download images
        soup = BeautifulSoup(self.driver.page_source, 'lxml')   #make soup
        self.all_images = soup.find_all('img')                  #Find all image tags
        #self.all_images = list(self.all_images)
        print('Length of all images', len(self.all_images))

        for index, image in enumerate(self.all_images):
            filename = 'image_' + str(index) + '.jpg'           #Add extension to the image
            #image_path = self.path + '/' + filename
            image_path = os.path.join(self.path, filename)      #Makes the path and takes care of the /
            link = image['src']     #Get link for the image
            print('Downloading image', index)
            response = requests.get(link, stream=True)          #Visits the image link, stream=True gets us the raw response as it is

            try:
                with open(image_path, 'wb') as file:            #'wb' opens the file in binary mode
                    shutil.copyfileobj(response.raw, file)      #copies the response from the source to the destination

            except Exception as e:
                print(e)
                print('Could not download image number ', index)
                print('Image link -->', link)

if __name__ == '__main__':      #Main Function
    app = App()