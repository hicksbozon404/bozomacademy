import psutil
import time
import logging
import os

# --- Configuration ---
LOG_FILE = "system_performance.log"
MONITOR_INTERVAL_SECONDS = 5  # Log every 5 seconds

# --- Logger Setup ---
# Ensure the log directory exists if you want to put it in a specific folder
# log_dir = "logs"
# os.makedirs(log_dir, exist_ok=True)
# log_path = os.path.join(log_dir, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Get a logger instance
logger = logging.getLogger(__name__)

def get_system_metrics():
    """
    Fetches and returns current CPU and memory usage.
    """
    try:
        # CPU Usage
        cpu_percent = psutil.cpu_percent(interval=1) # interval=1 samples CPU over 1 second

        # Memory Usage
        memory_info = psutil.virtual_memory()
        mem_total_gb = memory_info.total / (1024**3) # Convert bytes to GB
        mem_used_gb = memory_info.used / (1024**3)   # Convert bytes to GB
        mem_percent = memory_info.percent

        return {
            "cpu_percent": cpu_percent,
            "memory_total_gb": f"{mem_total_gb:.2f}",
            "memory_used_gb": f"{mem_used_gb:.2f}",
            "memory_percent": mem_percent
        }
    except Exception as e:
        logger.error(f"Error fetching system metrics: {e}")
        return None

def monitor_system():
    """
    Continuously monitors system performance and logs the data.
    """
    logger.info("Starting system performance monitoring...")
    logger.info(f"Logging data to: {os.path.abspath(LOG_FILE)}")
    logger.info(f"Monitoring interval: {MONITOR_INTERVAL_SECONDS} seconds")

    try:
        while True:
            metrics = get_system_metrics()
            if metrics:
                log_message = (
                    f"CPU Usage: {metrics['cpu_percent']}% | "
                    f"Memory Used: {metrics['memory_used_gb']}GB ({metrics['memory_percent']}%) "
                    f"of Total: {metrics['memory_total_gb']}GB"
                )
                logger.info(log_message)
            time.sleep(MONITOR_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logger.info("System monitoring stopped by user (Ctrl+C).")
    except Exception as e:
        logger.critical(f"An unhandled error occurred during monitoring: {e}")
    finally:
        logger.info("System monitoring gracefully terminated.")

if __name__ == "__main__":
    # Check if psutil is installed
    try:
        import psutil
    except ImportError:
        print("The 'psutil' library is not installed.")
        print("Please install it using: pip install psutil")
        exit(1)

    monitor_system()
