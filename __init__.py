import os
import datetime
import traceback
from anki.utils import strip_html
from aqt import mw, gui_hooks
from aqt.qt import QAction, QUrl, QDesktopServices, QMessageBox

def get_log_path():
    """Generates a log filename based on the current date."""
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    return os.path.join(os.path.dirname(__file__), f"{date_str}.txt")

def write_debug(msg):
    """Writes technical error details to a debug_log.txt file."""
    debug_path = os.path.join(os.path.dirname(__file__), "debug_log.txt")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(debug_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

def get_today_rev_count():
    """
    Queries Anki's database to count how many UNIQUE cards (distinct cid) 
    were reviewed today since midnight.
    """
    try:
        # Get timestamp for today at 00:00:00
        now = datetime.datetime.now()
        start_of_day_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)
        # Anki revlog IDs are timestamps in milliseconds
        start_timestamp_ms = int(start_of_day_dt.timestamp() * 1000)
        
        if mw.col:
            # Using 'distinct cid' ensures we count cards, not button presses (attempts)
            query = f"select count(distinct cid) from revlog where id > {start_timestamp_ms}"
            count = mw.col.db.scalar(query)
            return count if count is not None else 0
        return "N/A (Collection not loaded)"
    except Exception as e:
        write_debug(f"Error in get_today_rev_count: {str(e)}\n{traceback.format_exc()}")
        return "Error"

def log_typing_error(reviewer, card, ease):
    """
    Hooks into the answering process. Logs details if the user 
    presses '1' (Again/Fail) during a typing task.
    """
    # Only proceed if the user failed the card (ease 1)
    if ease != 1:
        return
    try:
        # Extract user input and the correct answer from the reviewer object
        user_typed = getattr(reviewer, "typedAnswer", "").strip()
        raw_correct = getattr(reviewer, "typeCorrect", "").strip()
        correct_ans = strip_html(raw_correct)

        # Log only if there is an actual difference and valid data exists
        if user_typed != correct_ans and correct_ans and user_typed:
            log_file = get_log_path()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            log_entry = (
                f"--- {timestamp} (FAILED CARD) ---\n"
                f"Typed:   {user_typed}\n"
                f"Correct: {correct_ans}\n"
                f"Note:    {card.note().model()['name']}\n\n"
            )
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
    except Exception as e:
        write_debug(f"Error in log_typing_error: {str(e)}")

# Register the hook to trigger when a card is answered
gui_hooks.reviewer_did_answer_card.append(log_typing_error)

def open_error_log():
    """
    Calculates the daily unique review count, updates the file header, 
    and opens the log file for the user.
    """
    try:
        log_file = get_log_path()
        rev_count = get_today_rev_count()
        # This header provides the denominator for the Prompt v4.0 analysis
        header_info = f"=== SESSION SUMMARY: {rev_count} UNIQUE CARDS REVIEWED TODAY ===\n\n"

        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            # Update the first line if it's already a summary, otherwise insert it
            if lines and lines[0].startswith("=== SESSION SUMMARY"):
                lines[0] = header_info
            else:
                lines.insert(0, header_info)

            with open(log_file, "w", encoding="utf-8") as f:
                f.writelines(lines)
            
            # Open the file with the default system text editor
            QDesktopServices.openUrl(QUrl.fromLocalFile(log_file))
        else:
            msg = QMessageBox(mw)
            msg.setText(f"No errors recorded yet.\nUnique Cards Reviewed Today: {rev_count}")
            msg.exec()
    except Exception as e:
        write_debug(f"Error in open_error_log: {str(e)}")

# Add a shortcut to the Tools menu in the Anki main window
action = QAction("Open Dictation Error Log", mw)
action.triggered.connect(open_error_log)
mw.form.menuTools.addAction(action)