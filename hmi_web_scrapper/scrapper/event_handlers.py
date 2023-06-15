from utils.logger import get_logger
import requests
import os
import pandas as pd
from utils.singleton import Singleton as sg
from io import StringIO

# Get the current working directory
cwd = os.getcwd()

class CsvLogEvent:
    def __init__(self, csv_file_name, csv_file_path):
        self.csv_file_name = csv_file_name
        self.csv_file_path = csv_file_path

class CsvLogEventHandler:
    """
    Interface log event handler that you can override methods from.
    """

    def on_created(self, event):
        """Called when a csv  is created.

        :param event:
            Event representing csv creation.
        :type event:
            :class:`CsvLogEvent`
        """

class RecordLogEventHandler(CsvLogEventHandler):

    def __init__(self) -> None:
        self.logger = get_logger(__name__, self.__class__.__name__)

    def on_created(self, event:CsvLogEvent):
        pass



class EStandardLogEventHandler(CsvLogEventHandler):

    def __init__(self) -> None:
        self.logger = get_logger(__name__, self.__class__.__name__)

    def on_created(self, event:CsvLogEvent):
        try:
            df = pd.read_csv(event.csv_file_path, sep=",", header=None)
            # Combine 'Date' and 'Time' into one column and convert it into datetime
            df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
            # Sort by datetime
            df = df.sort_values('DateTime')
            # Return the value of 'General_Information.ModeloSeleccionado' from the last row
            opt_db_sg.curr_e_standard = df['General_Information.ModeloSeleccionado'].iloc[-1]
            self.logger.info(f"csv contents obtained from {event.href_url}")
        except:
            self.logger.error(f"Failed to get {event.csv_file_name}: status code {response.status_code}")


        

    
        



