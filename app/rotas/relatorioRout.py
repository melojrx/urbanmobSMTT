from flask import Blueprint

relatorio_bp = Blueprint('relatorio', __name__)

from ..controller.relatorioController import *