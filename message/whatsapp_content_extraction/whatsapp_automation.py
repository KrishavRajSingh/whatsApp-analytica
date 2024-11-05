from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from django.conf import settings
import os
import time
import base64
import re
from datetime import datetime
from django.utils import timezone
from .whatsapp_db import WhatsAppDB

class WhatsAppAutomation:
    def __init__(self):
        print("Initializing chrome webDriver")
        # save chrome profile
        chrome_options = webdriver.ChromeOptions()
        user_data_dir = os.path.join(settings.BASE_DIR, 'chrome_profile')
        chrome_options.add_argument(f"user-data-dir={user_data_dir}")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 60)
        self.db = WhatsAppDB()
        os.makedirs("whatsapp_images", exist_ok=True)

    def whatsapp_login(self):
        print("Opening Whatsapp Web")
        self.driver.get("https://web.whatsapp.com")
        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Chat list"]')))
            print("Successfully logged in")
            return True
        except Exception as e:
            print(f"Login Failed: {e}")
            return False
        
    def get_chat_list(self):
        print("Getting chat list...")
        try:
            chat_list_container = self.wait.until(EC.presence_of_element_located((By.ID, "pane-side")))
            chats = chat_list_container.find_elements(By.CSS_SELECTOR, "[role='listitem']")

            if chats:
                print(f"Total {len(chats)} chats found")
                return chats
        except Exception as e:
            print(f"Error getting Chat List: {e}")

    def _scroll_to_top(self, message_container):
        last_height = self.driver.execute_script("return arguments[0].scrollHeight", message_container)
            
        while True:
            self.driver.execute_script("arguments[0].scrollTop = 0", message_container)
            time.sleep(2)
            new_height = self.driver.execute_script("return arguments[0].scrollHeight", message_container)
            if new_height == last_height:
                break
            last_height = new_height

    def _download_blob(self, blob_url):
        """Download blob URL content using JavaScript"""
        script = """
        async function getBlob(url) {
            const response = await fetch(url);
            const blob = await response.blob();
            return new Promise((resolve) => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(blob);
            });
        }
        const callback = arguments[arguments.length - 1];
        getBlob(arguments[0]).then(callback);
        """
        
        return self.driver.execute_async_script(script, blob_url)
    
    def _save_media(self, data_url, message_id, sender):
        """Save media from data URL to file"""
        try:
            # Remove data URL prefix and decode base64
            header, encoded = data_url.split(",", 1)
            data = base64.b64decode(encoded)
        
            extension = '.jpg'
            filename = f"{sender}_{int(time.time())}{extension}"
            filepath = os.path.join("whatsapp_images", filename)
            with open(filepath, "wb") as f:
                f.write(data)
            self.db.save_image(message_id, filepath)
            
            return filepath
        except Exception as e:
            print(f"Error saving media: {str(e)}")
            return None
        
    def _parse_timestamp(self, time_sender):
        pattern = r'\[(.*?)] (.*?): '
        match = re.match(pattern, time_sender)
        if match:
            time_str, sender = match.groups()
            timestamp = datetime.strptime(time_str.strip(), '%H:%M, %d/%m/%Y')
            return timezone.make_aware(timestamp), sender.strip()
        return None, None

    def extract_chat(self, chat_name):
        print(f"Extracting chat from {chat_name}")
        try:
            message_container = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "x1ewm37j")))

            # scroll to top to get all messages
            self._scroll_to_top(message_container)

            # get all messages
            messages = message_container.find_elements(By.CSS_SELECTOR, "[role='row'] .focusable-list-item")
            print(f"Total {len(messages)} messages")

            for message in messages:
                try:
                    # extract message
                    time_stamp_elem = message.find_element(By.CSS_SELECTOR, ".copyable-text")
                    time_stamp = time_stamp_elem.get_attribute("data-pre-plain-text")
                    if time_stamp:
                        timestamp, sender = self._parse_timestamp(time_stamp)
                        if not time_stamp or not sender:
                            continue

                        # extract text
                        try:
                            text_message = message.find_element(By.CLASS_NAME, "_akbu").text
                            print(text_message)
                        except NoSuchElementException:
                            print("Text not found")
                        
                        message_id = self.db.save_message(chat_name, sender, timestamp, text_message)

                        # extract image
                        try:
                            image_elem = message.find_element(By.CLASS_NAME, "x10e4vud")
                            image_url = image_elem.get_attribute("src")
                            if image_url.startswith("blob:"):
                                img_data = self._download_blob(image_url)
                                media_path = self._save_media(img_data, message_id, chat_name)
                                print(f"Image saved to {media_path}")
                        except NoSuchElementException:
                            print("Image not found")

                except NoSuchElementException:
                    print(f"Deleted message")
        except Exception as e:
            print(f"Error extracting chat: {e}")

    def process_chat_list(self, chat_list):
        for chat in chat_list:
            try:
                chat_name = chat.find_element(By.CSS_SELECTOR, "span[title]").get_attribute("title")
                print(f"Chat Name: {chat_name}")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", chat)
                chat.click()
                self.extract_chat(chat_name)
                time.sleep(2)
                print("Chat clicked")
            except Exception as e:
                print(f"Error processing chat: {e}")
