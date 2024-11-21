from selenium.webdriver.common.by import By

import SpeechToText as sp
import Browser as br
import time
import pyautogui
import grid as grid
import WORDS as w
from threading import Thread

class MouseController:
    """
    Κλάση για να μετακινούμε τον mouse cursor, να κάνουμε click, μέσω φωνής να κάνουμε type π.χ σε κάποιο search bar.
    
    Φωνητικές Εντολές:
        1) πάνω - κάτω - αριστερά - δεξιά αριθμός π.χ (δεξιά 100)
            Ο mouse cursor θα μετακινηθεί 100 pixel δεξιά
        2) νέα αναζήτηση 
            Θα πούμε το καινούργιο search term αφού πρώτα το πρόγραμμα μας πεί "Please say your search term"
        3) click - κλίκ (same thing :D)
            Για το mouse click functionality
        4) Όταν το mouse cursor είναι π.χ πάνω από κάποιο search bar και πούμε click και εφανιστεί το cursor
           που υποδικνύει ότι αναμένετε είσοδος από το keyboard, ο χρήστης μπορεί να πεί type και αφού ακουστεί το "Please say what you want to type"
           ο χρήστης λέει αυτό που θέλει να πληκτρολογήσει και πατιέται αυτόματα ENTER αλλιώς μπορεί να πεί delete ή διαγραφή για να διγραφεί 
           οτιδήποτε υπάρχει στο search bar.
    """
    def __init__(self):
        self.br_obj = br.Browser()
        self.num_of_search = 0
        self.search_bar_text = ""
        self.text_query = ""

        # Αρχικά το mouse cursor ξεκινάει από το κέντρο της οθόνης
        screen_width, screen_height = pyautogui.size()
        pyautogui.moveTo(screen_width // 2, screen_height // 2)

    def type_in_search_bar(self):
        while True:
            # audio_query = sp.obtain_audio_from_mic(None)
            # self.text_query = sp.convert_speech_to_text(audio_query)
            # print(self.text_query)

            if self.text_query.lower() == w.TYPE:
                # Αναμονή για να μιλήσει ο user αφού πεί "type"
                audio_search = sp.obtain_audio_from_mic("Please say what you want to type")
                search_term = sp.convert_speech_to_text(audio_search)
                print(f'search term: {search_term}')

                if search_term != 0:
                    if search_term.lower() in w.DELETE_LS:
                        # Διαγραγή του τυχόν υπάρχοντος κειμένου στο search bar
                        pyautogui.click(clicks=4)
                        pyautogui.press("backspace")
                        self.search_bar_text = ""
                    else:
                        # Πληκτρολόγηση του term που λέει ο χρήστης στο search bar 
                        pyautogui.typewrite(self.search_bar_text + search_term)
                        self.search_bar_text = self.search_bar_text + search_term
                        pyautogui.press("enter")
                        break
            elif self.text_query.lower() in w.DELETE_LS:
                pyautogui.press("backspace", presses=len(self.search_bar_text))
                self.search_bar_text = ""

    def start(self):
        running = True
        while running:
            while True:
                audio_query = sp.obtain_audio_from_mic(w.MESSAGE) # Please say what you want to search
                self.text_query = sp.convert_speech_to_text(audio_query)
                if self.text_query == 0:
                    continue
                else:
                    break

            self.br_obj.perform_google_search(self.text_query)
            if self.num_of_search == 0: # Αν ο χρήστης κάνει αναζήτηση πρώτη φορά accept τα cookies
                self.br_obj.accept_google_cookies()

            while True:
                print('Continued after thread\n')
                audio_query = sp.obtain_audio_from_mic(None)
                time.sleep(2)
                self.text_query = sp.convert_speech_to_text(audio_query)
                print(self.text_query)

                try:
                    query_parts = self.text_query.split()
                except:
                    continue

                if query_parts[0].lower() in w.CLICK_LS:
                    # Ο χρήστης μπορεί να πει CLIK 'το κείμενο από το link που βλέπει,
                    # και με selenium να βρούμε το element που θέλει να κλικάρει και να 
                    # πραγματοποιήσουμε το click functionality
                    if len(query_parts) > 1:
                        elem_text = ' '.join(query_parts[1:]).lower().strip()
                        print(elem_text)
                        try:
                            element = self.br_obj.driver.find_elements(By.XPATH, f"//a[translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZΑΆΒΓΔΕΈΖΗΉΘΙΊΚΛΜΝΞΟΌΠΡΣΤΥΎΦΧΨΩΏö', 'abcdefghijklmnopqrstuvwxyzαβγδεζηθικλμνξοπρστυφχψωo') = '{elem_text}']")[0]
                            element.click()
                        except:
                            print('No such link with text:', elem_text)
                    else:
                        pyautogui.click()  # Εκτέλεσε mouse click
                elif query_parts[0].lower() == w.PRESS and len(query_parts) > 1: # Κουμπιά
                    # Το ίδιο πράγμα με το παραπάνω σχόλιο αλλά με PRESS στην περίπτωση που ο χρήστης
                    # θέλει να πατήσει κάποιο button element
                    elem_text = ' '.join(query_parts[1:]).lower().strip()
                    print(elem_text)
                    found = False
                    try:
                        element = self.br_obj.driver.find_elements(By.XPATH, f"//button[translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZΑΆΒΓΔΕΈΖΗΉΘΙΊΚΛΜΝΞΟΌΠΡΣΤΥΎΦΧΨΩΏö', 'abcdefghijklmnopqrstuvwxyzαβγδεζηθικλμνξοπρστυφχψωö') = '{elem_text}']")[0]
                        element.click()
                        found = True
                    except:
                        print('No such button with text:', elem_text)

                    if not found:
                        try:
                            element = self.br_obj.driver.find_elements(By.XPATH, f"//span[translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZΑΆΒΓΔΕΈΖΗΉΘΙΊΚΛΜΝΞΟΌΠΡΣΤΥΎΦΧΨΩΏö', 'abcdefghijklmnopqrstuvwxyzαβγδεζηθικλμνξοπρστυφχψωö') = '{elem_text}']")[0]
                            element.click()
                            found = True 
                        except:
                            print('No such span with text:', elem_text)

                    if not found:
                        try:
                            element = self.br_obj.driver.find_elements(By.XPATH, f"//div[@role='button' and translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZΑΆΒΓΔΕΈΖΗΉΘΙΊΚΛΜΝΞΟΌΠΡΣΤΥΎΦΧΨΩΏö', 'abcdefghijklmnopqrstuvwxyzαβγδεζηθικλμνξοπρστυφχψωö') = '{elem_text}']")[0]
                            element.click()
                            found = True 
                        except:
                            print('No such button with text:', elem_text)


                elif self.text_query.lower() == w.BACK:
                    self.br_obj.driver.back()  # Πήγαινε πίσω στην προηγούμενη σελίδα
                elif self.text_query.lower() == w.TYPE:
                    self.type_in_search_bar()
                elif self.text_query.lower() in w.GRID_OPEN_LS:
                    thread = Thread(grid.grid()) # Σημείωση: να το κάνω με threads
                    thread.start()
                elif self.text_query.lower() in w.GRID_CLOSE_LS:
                    grid.close()
                elif self.text_query.lower() == w.NEW_SEARCH:
                    self.num_of_search += 1
                    self.search_bar_text = ""
                    break
                elif query_parts[0].lower() in w.DOWN_LS + w.LEFT_LS + w.RIGHT_LS + w.UP_LS: # Εντολή μετακίνησης κέρσορα
                    direction = query_parts[0].lower()
                    num = self.parse_number(query_parts[1].lower())
                    self.move_mouse(direction, num)
                elif query_parts[0].lower() == w.SCROLL and len(query_parts) == 3:
                    direction = query_parts[1].lower()
                    amount = self.parse_number(query_parts[2].lower())
                    if direction in w.DOWN_LS:
                        pyautogui.scroll(-amount)
                    elif direction in w.UP_LS:
                        pyautogui.scroll(amount)
                elif self.text_query.lower() in w.EXIT_LS:
                    running = False
                    break

    def parse_number(self, num_str: str):
        # Σε περίπτωση που πει 1000 και το αναγνωρίσει ως "χείλια":
        if num_str in w.THOUSAND_LS:
            return 1000

        num = 0
        if num_str is not None and len(num_str) > 0:
            if '.' in num_str:
                num_str = num_str.replace('.', '')
            try:
                num = int(num_str)
            except ValueError:
                pass

        return num

    def move_mouse(self, direction, num):
        current_x, current_y = pyautogui.position()

        if direction.strip() in w.DOWN_LS:
            new_x = current_x
            new_y = current_y + num
            if new_y > pyautogui.size().height:
                # Αν το ποντίκι είναι out of sight -> scroll down
                pyautogui.press('down', presses=9)
        elif direction.strip() in w.UP_LS:
            new_x = current_x
            new_y = current_y - num
            if new_y < 0:
                # # Αν το ποντίκι είναι out of sight -> scroll up
                pyautogui.press('up', presses=9)
        elif direction.strip() in w.RIGHT_LS:
            new_x = current_x + num
            new_y = current_y
        elif direction.strip() in w.LEFT_LS:
            new_x = current_x - num
            new_y = current_y
        else:
            return

        pyautogui.moveTo(new_x, new_y, duration=0.5)