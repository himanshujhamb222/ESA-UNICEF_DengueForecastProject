import logging

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    # Format of log messages
    handlers=[
        logging.StreamHandler(),  # Output logs to console
    ],
)
# Set logging levels for specific Matplotlib loggers
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("matplotlib.font_manager").setLevel(logging.WARNING)
logging.getLogger("httpcore.http11").setLevel(logging.WARNING)

# Create a logger
logger = logging.getLogger(__name__)
