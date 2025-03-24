from utils.logging import NeuronLogger, log_function_call

# Configuração inicial
logger = NeuronLogger(
    log_level="DEBUG",
    log_file="neuronpy.log",
    json_format=False
).get_logger()

@log_function_call(logger=logger)
def example_function(param1: str, param2: int):
    """Função de exemplo com logging automático"""
    logger.info("Processando dados...")
    # Sua implementação aqui
    return {"result": "success"}

try:
    example_function("test", 42)
except Exception as e:
    logger.error("Ocorreu um erro no processo principal", exc_info=True)