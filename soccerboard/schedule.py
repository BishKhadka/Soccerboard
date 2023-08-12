from pathlib import Path
import os
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import logging

BASE_DIR = Path(__file__).resolve().parent.parent

def run_custom_command():
    '''
    Run custom management command automatically
    '''
    logger = logging.getLogger("Started Scheduled Task To Run Custom Command")
    os.chdir(BASE_DIR)
    subprocess.call(["python3", "manage.py", "replace"])
    logger.info("Model Instances Were Successfully Updated on Schedule")

log_file = os.path.join(BASE_DIR, 'soccerboard/log/schedule.log')
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", filename=log_file)

scheduler = BackgroundScheduler()

#run the custom command every hour
scheduler.add_job(run_custom_command, 'interval', hours=1)
scheduler.start()


