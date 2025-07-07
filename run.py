import os
import time
import logging
import shutil
import subprocess
from send_report import send_mail

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_locust(locustfile, host, users, rate, duration, generate_report=False):
    directory = os.getenv('REPORT')
    # timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M_%S.%f")
    report_html = f"{locustfile[:-3]}.html"
    report_csv = f"{locustfile[:-3]}.csv"
    
    if os.path.exists(directory) and os.path.isdir(directory):
        shutil.rmtree(directory)
    
    cmd = [
        "locust", "-f", f"locustfiles/{locustfile}", f"-u={users}",
        f"-r={rate}", f"-t={duration}", f"-H={host}", "--headless"
        ]
    
    if generate_report:
        cmd += [
                f"--csv={directory}/{report_csv}",
                f"--html={directory}/{report_html}"
            ]
        
    result = subprocess.run(cmd, capture_output=True, text=True)
    logger.info(f"stdout result : {result.stdout}")
    logger.info(f"stderr result : {result.stderr}")
    time.sleep(3)
    # locust_stats_history(locustfile[:-3])
    send_mail()
