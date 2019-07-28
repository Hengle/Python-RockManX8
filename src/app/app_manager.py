import sentry_sdk
from PyQt5.QtWidgets import QApplication

from gui.windows import EditorWindow
from app import config, mcb_manager, exception_manager


class AppManager:
    def __init__(self):
        self.app = QApplication([])
        sentry_sdk.init(dsn='https://acf5a98fa8964650b635e059bfbf75d4@sentry.io/1515321')

    def __init_config__(self):
        return config.load_config_or_default()

    def __init_editor__(self):
        mcb_manager.extract_collection_arcs()
        self.editor_window = EditorWindow()
        self.editor_window.setWindowTitle(config.window_title)
        self.editor_window.show()

    def log_ui(self, message, *format_args):
        if self.editor_window is None:
            return

        message = message.format(*format_args)
        self.editor_window.ui.statusbar.showMessage(message, 5000)

    def run(self):
        if not self.__init_config__():
            return 0

        self.__init_editor__()

        if config.is_valid_collection:
            self.log_ui('Editing X8 from the X Legacy Collection 2')
        else:
            self.log_ui('Editing X8 from PC version released in 2004')

        exception_manager.in_qt_loop = True
        exception_manager.window = self.editor_window
        exit_code = self.app.exec_()
        return exit_code