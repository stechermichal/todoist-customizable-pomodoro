from datetime import timedelta, datetime

from todoist.api import TodoistAPI


class Task:
    """Overall class to manage behavior of pushing generated tasks to Todoist."""

    def __init__(self):
        self.api = TodoistAPI(self.get_api())

        # Get a start time and slice the string into two variables to use work_start.
        self.start_working_time = input("What time will you start studying? Please input as hh:mm\n")
        self.desired_cycles = int(input("How many study cycles would you like to do?\n"))
        hours = self.start_working_time[:2]
        minutes = self.start_working_time[3:5]

        # Get length of each cycle to calculate timedelta from start time.
        month_of_task = int(input("What month? Enter as a number. Leave empty for current\n") or datetime.now().month)
        day_of_task = int(input("On what day? Enter as a number.  Leave empty for current\n") or datetime.now().day)

        # Calc using user values for work/break length.
        self.work_start = datetime(datetime.now().year, month_of_task, day_of_task, int(hours), int(minutes))
        self.work_duration = timedelta(minutes=int(input("How long will you study each cycle?\n")))
        self.break_duration = timedelta(minutes=int(input("How long will your breaks be?\n")))

    @staticmethod
    def get_api():
        """Either uses input api and saves it for next time or reads api used last time from file."""
        user_api = input("Paste api token.\nLeave empty for last used:\n")
        while True:
            if len(user_api) == 0:
                with open('api_token.txt', 'r') as file_object:
                    return file_object.read()
            elif len(user_api) == 40:
                with open('api_token.txt', "w") as file_object:
                    file_object.write(user_api)
                    return user_api
            else:
                print("Please paste the token as raw data with no quotation marks or whitespace.")

    def find_inbox_id(self):
        """Finds the id of the default 'Inbox' project."""
        for project in self.api.state['projects']:
            if project['name'] == 'Inbox':
                return project['id']

    def make_task(self):
        """Run loop that adds a new task into Todoist for as many times as user specified."""
        current_cycles = 0
        while current_cycles < self.desired_cycles:
            work_cycle = self.work_start + (self.work_duration + self.break_duration) * current_cycles
            print(f"{work_cycle} - {work_cycle + self.work_duration} WORK")
            self.api.items.add(f"WORK - {work_cycle:%H:%M} - {work_cycle + self.work_duration:%H:%M}",
                               project_id=self.find_inbox_id(), due={"string": work_cycle})
            break_cycle = self.work_start + self.work_duration + (
                        self.work_duration + self.break_duration) * current_cycles
            print(f"{break_cycle} - {break_cycle + self.break_duration} BREAK")
            self.api.items.add(f"BREAK - {break_cycle:%H:%M} - {break_cycle + self.break_duration:%H:%M}",
                               project_id=self.find_inbox_id(), due={"string": break_cycle})
            current_cycles += 1

        self.api.commit()


if __name__ == '__main__':
    ts = Task()
    ts.make_task()
