from flask import Blueprint

solicitacao_bp = Blueprint('solicitacao', __name__)

from ..controller.solicitacaoController import *