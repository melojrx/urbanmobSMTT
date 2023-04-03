from enum import Enum

class StatusEnum(Enum):
    AGUARDANDO_ATENDIMENTO = 1
    EM_ANDAMENTO = 2
    DEFERIDO = 3
    INDEFERIDO = 4
    FINALIZADO = 5
    REENVIADO= 6