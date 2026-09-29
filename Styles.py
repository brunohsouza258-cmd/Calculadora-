# QSS - Estilos do QT for Python
# https://doc.qt.io/qtforpython/tutorials/basictutorial/widgetstyling.html
# Dark Theme
# https://pyqtdarktheme.readthedocs.io/en/latest/how_to_use.html
import qdarktheme
from variables import (DARKER_PRIMARY_COLOR, DARKEST_PRIMARY_COLOR,
                       PRIMARY_COLOR)

qss = f"""
    PushButton[cssClass="specialButton"] {{
        color: #fff;
        background: {PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:hover {{
        color: #fff;
        background: {DARKER_PRIMARY_COLOR};
    }}
    PushButton[cssClass="specialButton"]:pressed {{
        color: #fff;
        background: {DARKEST_PRIMARY_COLOR};
    }}
"""


def setupTheme(app):
    app.setStyleSheet("""
        QWidget {
            background-color: #121212;
            color: #ffffff;
            font-size: 18px;
        }

        QLineEdit {
            background-color: #1e1e1e;
            border: 2px solid #333;
            border-radius: 10px;
            padding: 10px;
            font-size: 24px;
        }

        QPushButton {
            background-color: #2a2a2a;
            border: none;
            border-radius: 10px;
            padding: 15px;
            font-size: 18px;
        }

        QPushButton:hover {
            background-color: #3a3a3a;
        }

        QPushButton:pressed {
            background-color: #505050;
        }

        QPushButton#equal {
            background-color: #00c853;
            color: black;
        }

        QPushButton#equal:hover {
            background-color: #00e676;
        }

        QPushButton#clear {
            background-color: #d50000;
        }

        QPushButton#clear:hover {
            background-color: #ff1744;
        }
    """)
