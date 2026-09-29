from decimal import Decimal, InvalidOperation
from PySide6.QtWidgets import QPushButton, QGridLayout
from variables import MEDIUM_FONTE_SIZE
from utils import isNumordot, isEmpty
from PySide6.QtCore import Slot
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from display import Display
    from info import Info


class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configStyle()

    def configStyle(self):
        font = self.font()

        self.setStyleSheet(
            f'''
            QPushButton {{
                font-size: {MEDIUM_FONTE_SIZE}px;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }}

            QPushButton:hover {{
                opacity: 0.8;
            }}

            QPushButton:pressed {{
                padding-top: 12px;
            }}
            '''
        )

        self.setFont(font)

        self.setMinimumSize(75, 75)

        self.setCheckable(False)


class ButtonsGrid(QGridLayout):
    def __init__(
        self,
        display: 'Display',
        info: 'Info',
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        self._gridmask = [
            ['C', '◀', '^', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '='],
        ]

        self.display = display
        self.info = info

        self._left = None
        self._right = None
        self._op = None

        self._showMessage('Sua conta')

        self._makeGrid()

    def _makeGrid(self):
        for row_number, row_data in enumerate(self._gridmask):
            for column_number, button_text in enumerate(row_data):

                button = Button(button_text)

                if isEmpty(button_text):
                    button.setEnabled(False)

                elif (
                    isNumordot(button_text)
                    and not isEmpty(button_text)
                ):
                    slot = self._makeSlot(
                        self._insertbuttontexttodisplay,
                        button
                    )

                    self._connectButtonClicked(
                        button,
                        slot
                    )

                else:
                    button.setProperty(
                        'cssClass',
                        'specialButton'
                    )

                    self._configSpecialButton(button)

                self.addWidget(
                    button,
                    row_number,
                    column_number
                )

    def _configSpecialButton(self, button):
        text = button.text()

        if text == 'C':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._clear)
            )

        elif text == '◀':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._backspace)
            )

        elif text == '±':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._invertNumber)
            )

        elif text in '+-/*^':
            self._connectButtonClicked(
                button,
                self._makeSlot(
                    self._operatorClicked,
                    button
                )
            )

        elif text == '=':
            self._connectButtonClicked(
                button,
                self._makeSlot(self._equals)
            )

    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _makeSlot(self, func, *args, **kwargs):
        @Slot(bool)
        def realSlot(_):
            func(*args, **kwargs)

        return realSlot

    def _showMessage(self, message):
        self.info.setText(message)

    def _isValidNumber(self, number):
        try:
            Decimal(number)
            return True

        except InvalidOperation:
            return False

    def _insertbuttontexttodisplay(self, button):
        buttonText = button.text()

        currentText = self.display.text()

        # Limpa após resultado
        if '=' in currentText:
            self.display.clear()

            currentText = ''

            self._left = None
            self._right = None
            self._op = None

        # Evita vários pontos
        if buttonText == '.':
            if self._op:
                parts = currentText.split(self._op)

                if '.' in parts[-1]:
                    return
            else:
                if '.' in currentText:
                    return

        self.display.insert(buttonText)

    def _clear(self):
        self._left = None
        self._right = None
        self._op = None

        self.display.clear()

        self._showMessage('Sua conta')

    def _backspace(self):
        self.display.backspace()

    def _invertNumber(self):
        text = self.display.text()

        if text == '':
            self._showMessage(
                'Digite um número'
            )

            return

        try:
            number = Decimal(text) * -1

            self.display.setText(
                str(number.normalize())
            )

        except Exception:
            self.display.setText('Erro')

            self._showMessage(
                'Erro na conta'
            )

    def _operatorClicked(self, button):
        buttonText = button.text()

        displayText = self.display.text()

        if displayText == '':
            self._showMessage(
                'Digite um número'
            )

            return

        if self._op is not None:
            self._showMessage(
                'Operador já definido'
            )

            return

        try:
            self._left = Decimal(displayText)

            self._op = buttonText

            self.display.insert(buttonText)

        except Exception:
            self.display.setText('Erro')

            self._showMessage(
                'Erro na conta'
            )

            self._resetCalculator()

    def _calculate(self):
        result = Decimal('0')

        if self._op == '+':
            result = self._left + self._right

        elif self._op == '-':
            result = self._left - self._right

        elif self._op == '*':
            result = self._left * self._right

        elif self._op == '/':
            result = self._left / self._right

        elif self._op == '^':
            result = self._left ** self._right

        result = result.normalize()

        self._left = result

        self.display.setText(str(result))

    def _resetCalculator(self):
        self._left = None
        self._right = None
        self._op = None

    def _equals(self):
        displayText = self.display.text()

        if self._op is None:
            self._showMessage(
                'Escolha um operador'
            )

            return

        try:
            parts = displayText.split(self._op)

            if len(parts) != 2:
                self._showMessage(
                    'Conta inválida'
                )

                return

            leftValue = Decimal(parts[0])

            rightValue = Decimal(parts[1])

            self._left = leftValue
            self._right = rightValue

            self._calculate()

            resultText = self.display.text()

            expression = (
                f'{leftValue}'
                f'{self._op}'
                f'{rightValue}'
            )

            self.display.setText(
                f'{expression}={resultText}'
            )

            self._showMessage(
                f'{expression}={resultText}'
            )

            self._op = None
            self._right = None

        except ZeroDivisionError:
            self.display.setText('Erro')

            self._showMessage(
                'Não é possível dividir por zero'
            )

            self._resetCalculator()

        except Exception:
            self.display.setText('Erro')

            self._showMessage(
                'Erro na conta'
            )

            self._resetCalculator()