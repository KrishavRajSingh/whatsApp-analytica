from django.core.management.base import BaseCommand
from message.whatsapp_content_extraction.whatsapp_automation import WhatsAppAutomation

class Command(BaseCommand):
    help  = "Reading Whatsapp Chat Messages"
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Whatsapp Automation")
        wa = WhatsAppAutomation()
        try:
            # whatsapp login
            wa.whatsapp_login()

            # get chat list
            chat_list = wa.get_chat_list()
            if chat_list:
                wa.process_chat_list(chat_list)
        except Exception as e:
            self.stdout.write(f"CommandLine Error: {e}")
        finally:
            wa.driver.quit()
            wa.db.close()
            print("Closing Extraction")
               
        