from playsound import playsound
from lxml import html
import requests
import time
import argparse
import sys
import re
import sys
import select
import os

DEFAULT_SCRIPT_DURATION = 480 # Default duration for which the script runs (in minutes)
DEFAULT_CHECK_FREQUENCY = 300 # Default mouse click frequency (in seconds)
XPATH_QUERY_FOR_NO_OF_CLASSES = './/div[contains(text(),"Showing")]'
NOTIFICATION_SOUND = "notif.mp3"

class ASUCourseChecker:

    """
    The ASUCourseChecker class
    """

    def __init__(self):
        pass
    
    def get_end_time(self, duration):

        """
        Method to calculate the stop time of the script
        Args:
            duration (int): Duration for which the script should run
        Returns:
            int: The ending time at which the script should stop
        """

        return time.time() + 60*duration

    def check(self, frequency, duration, url, course_count):

        """
            Given a url with correct class search params and course count,
            this method will run periodically and notifies you with a sound
            if a new course available.
            
        """

        end_time = self.get_end_time(duration) # The ending time at which the script should stop
        current_time = time.time() # Get current time

        while end_time > current_time:
            try:
                page = requests.get(url)
                tree = html.fromstring(page.content)
                element = tree.xpath(XPATH_QUERY_FOR_NO_OF_CLASSES)
                classes_str = re.sub(r"[\n\t]*", "", element[0].text)
                total_courses = int(classes_str.split(' ')[-3])
                if total_courses > course_count:
                    self.play_notif()
                    break
                t = time.localtime()
                print("Last checked at " + time.strftime("%H:%M:%S", t))
                time.sleep(frequency)
            except KeyboardInterrupt:
                print('Exiting')
                sys.exit()

    def play_notif(self):
        """
            Method to play the notification on repeat
        """

        print("NEW COURSE FOUND. USE KEYBOARD INTERRUPT TO STOP THE NOTIF LOOP")

        while True:
            try:
                playsound(NOTIFICATION_SOUND)
                time.sleep(2)
            except KeyboardInterrupt:
                print('Exiting')
                sys.exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=int, help="Running duration of the script (in minutes)", default=DEFAULT_SCRIPT_DURATION)
    parser.add_argument('--frequency', type=int, help="Frequency of check (in seconds)", default=DEFAULT_CHECK_FREQUENCY)
    args = parser.parse_args()
    checker = ASUCourseChecker()
    print("Running ASU course checker...")
    url = 'https://webapp4.asu.edu/catalog/myclasslistresults?t=2217&s=CSE&l=grad&hon=F&promod=F&c=TEMPE&e=open&page=1' # Need to remove hardcoding of the params
    course_count = 18 # Need to make this a input param
    checker.check(args.frequency, args.duration, url, course_count) # Start the checker
    sys.exit()
