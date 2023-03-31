from fpdf import FPDF
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), '../static/img/pdf/')
class PDF(FPDF):

    # Page header
    def header(self):
        self.image(UPLOADS_PATH + 'republicaFederativaBrasil.jpg', 10, 8, 33)
