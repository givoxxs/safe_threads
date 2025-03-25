import psutil
import time
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("system_metrics.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("system_monitor")

# Settings
CHECK_INTERVAL = 60  # seconds
CPU_THRESHOLD = 90  # percentage
MEMORY_THRESHOLD = 80  # percentage
LOG_RETENTION_DAYS = 7

def get_system_metrics():
    """Collect system metrics."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "timestamp": datetime.now().isoformat(),
        "cpu_percent": cpu_percent,
        "memory_percent": memory.percent,
        "memory_available_mb": memory.available / (1024 * 1024),
        "disk_percent": disk.percent,
        "disk_free_gb": disk.free / (1024 * 1024 * 1024)
    }

def log_metrics(metrics):
    """Log the system metrics."""
    logger.info(
        f"CPU: {metrics['cpu_percent']}% | "
        f"Memory: {metrics['memory_percent']}% "
        f"({metrics['memory_available_mb']:.2f} MB available) | "
        f"Disk: {metrics['disk_percent']}% "
        f"({metrics['disk_free_gb']:.2f} GB free)"
    )
    
    # Check for high resource usage
    if metrics['cpu_percent'] > CPU_THRESHOLD:
        logger.warning(f"HIGH CPU USAGE: {metrics['cpu_percent']}%")
    
    if metrics['memory_percent'] > MEMORY_THRESHOLD:
        logger.warning(f"HIGH MEMORY USAGE: {metrics['memory_percent']}%")

def clean_old_logs():
    """Remove log files older than LOG_RETENTION_DAYS."""
    try:
        current_time = time.time()
        log_dir = os.path.dirname(os.path.abspath("system_metrics.log"))
        
        for file in os.listdir(log_dir):
            if file.endswith(".log"):
                file_path = os.path.join(log_dir, file)
                file_age = current_time - os.path.getmtime(file_path)
                
                # If file is older than retention period, delete it
                if file_age > (LOG_RETENTION_DAYS * 86400):
                    os.remove(file_path)
                    logger.info(f"Removed old log file: {file}")
    except Exception as e:
        logger.error(f"Error cleaning logs: {str(e)}")

def main():
    """Main monitoring loop."""
    logger.info("System monitoring started")
    
    try:
        while True:
            metrics = get_system_metrics()
            log_metrics(metrics)
            
            # Clean old logs once a day
            if datetime.now().hour == 0 and datetime.now().minute < CHECK_INTERVAL/60:
                clean_old_logs()
            
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error(f"Monitoring error: {str(e)}")

if __name__ == "__main__":
    main()
