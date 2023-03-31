from enum import Enum

class StatusEnum(Enum):
    AGUARDANDO_ATENDIMENTO = 1
    EM_ANDAMENTO = 2
    INDEFERIDO = 3
    FINALIZADO = 4