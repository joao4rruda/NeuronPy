from utils.logging import default_logger, log_function_call

@log_function_call
def main():
    logger = default_logger
    logger.info("Iniciando aplicação principal")

if __name__ == "__main__":
    main()
