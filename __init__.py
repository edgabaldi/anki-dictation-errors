import os
import datetime
from aqt import mw, gui_hooks
from aqt.qt import QAction, QUrl, QDesktopServices, QMessageBox

# Path where the error log will be saved
LOG_FILE = os.path.join(os.path.dirname(__file__), "anki_dictation_errors.txt")

def log_typing_error(reviewer, card, ease):
    """
    Agora usamos o hook 'reviewer_did_answer_card' para saber qual nota 
    você deu (ease). 1 = Again (Fail), 2 = Hard, 3 = Good, 4 = Easy.
    """
    # Só prosseguimos se você apertou '1' (Again/Fail)
    if ease != 1:
        return

    try:
        # Pegamos os valores que confirmamos no diagnóstico
        user_typed = getattr(reviewer, "typedAnswer", "").strip()
        correct_ans = getattr(reviewer, "typeCorrect", "").strip()

        # Verifica se houve erro de digitação (segurança extra)
        if user_typed != correct_ans and correct_ans and user_typed:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            
            log_entry = (
                f"--- {timestamp} (FAILED CARD) ---\n"
                f"Typed:   {user_typed}\n"
                f"Correct: {correct_ans}\n"
                f"Note:    {card.note().model()['name']}\n\n"
            )

            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
                
    except Exception as e:
        print(f"Dictation Logger Error: {e}")

# Trocamos o hook para 'did_answer_card' para ter acesso à nota (ease)
gui_hooks.reviewer_did_answer_card.append(log_typing_error)

# Menu UI
def open_error_log():
    if os.path.exists(LOG_FILE):
        QDesktopServices.openUrl(QUrl.fromLocalFile(LOG_FILE))
    else:
        msg = QMessageBox(mw)
        msg.setText("No failed errors recorded yet!")
        msg.exec()

action = QAction("Open Dictation Error Log", mw)
action.triggered.connect(open_error_log)
mw.form.menuTools.addAction(action)