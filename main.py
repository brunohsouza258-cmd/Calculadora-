import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QPushButton

from main_window import MainWindow
from display import Display
from info import Info
from variables import WINDOW_ICON_PATH
from Styles import setupTheme
from buttons import Button, ButtonsGrid


if __name__ == '__main__':
    # Cria a aplicação
    app = QApplication(sys.argv)

    # 👉 APLICA O TEMA AQUI
    setupTheme(app)

    window = MainWindow()

    # Ícone
    icon = QIcon(str(WINDOW_ICON_PATH))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    # Info
    info = Info('Sua conta')
    window.addWidgetToVlayout(info)
    
    # Display
    display = Display()
    window.addWidgetToVlayout(display)

    # Grid
    buttonsGrid = ButtonsGrid(display, info)
    window.v_layout.addLayout(buttonsGrid)

    
    # Executa tudo
    window.adjustFixedSize()
    window.show()
    app.exec()
