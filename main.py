import logging
import os

def main():
    logging.debug(f"Program started! [PID: {os.getpid()}]")
    logging.debug(f"Program ended!")

if __name__ == "__main__":
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="[%Y-%m-%d | %H:%M:%S]",
    )

    # call the main function
    main()