'''
A multithreaded pin guesser. To learn more about this project, head over to https://arjundabir.com.
'''

import threading
import requests
from bs4 import BeautifulSoup

thread_count = 43
url = "https://www.guessthepin.com/prg.php"
random_numbers = list(range(0, 10000))
threads = []
stop_event = threading.Event()


def segmented_array_maker(num_of_threads):
    '''
    Based on the number of threads inputted by the user, this segments the arrays that is copied to the threads 
    so each thread has a different set of values from 0-10000.
    '''
    arrays = []
    partition_size = 10000 // num_of_threads
    for i in range(num_of_threads):
        start = i * partition_size
        end = start + partition_size
        array = list(range(start, end))
        arrays.append(array)
    return arrays


def check_value(arr):
    '''
    The method that is passed in each thread which tests pin values.
    Also, this method saves html file if the pin value is correct.
    '''
    for number in arr:
        formatted_number = str(number).zfill(4)
        response = requests.post(
            url, data={"guess": f"{formatted_number}"}, timeout=10)
        html_page = response.text
        if "is not the PIN" not in html_page:
            soup = BeautifulSoup(html_page, features="html.parser")
            with open("success.html", "w", encoding="utf-8") as file:
                file.write(str(soup))
            print(soup)
            print(formatted_number)
            stop_event.set()
            break


def main(num_of_threads):
    '''
    Main function to create and run all the threads
    '''
    arrs = segmented_array_maker(num_of_threads)
    for arr in arrs:
        thread = threading.Thread(target=check_value, args=(arr, ))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    while ((10_000 % thread_count != 0) and (thread_count < 100)):
        thread_count = int(
            input("How many threads would you like to run? Must be divide 10,000 evenly and be between 1-99.\nEnter amount here:"))
    main(thread_count)
    print("Done!")
