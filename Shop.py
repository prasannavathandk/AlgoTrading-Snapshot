from Organizer import Manager
from PreProcessor import Preprocessor
from Processor import Processor

class Shop:
    def __init__(self):
        self.manager = Manager()
        self.prep = Preprocessor(self.manager)
        self.proc = Processor(self.manager)
        print("Shop is open.")

    def __del__(self):
        print("Shop is closed.")    

    def open(self) -> None:
        self.manager.kickoff()
        self.prep.kickoff()
        self.proc.kickOff()