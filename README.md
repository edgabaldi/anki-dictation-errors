# Anki Dictation Error Logger

A lightweight Anki add-on designed to track and log typing discrepancies in "Type Answer" cards. It allows users to maintain a persistent record of their mistakes for later review and analysis.

## 🚀 Features

- **Selective Logging**: The plugin only records data when you rate a card as **"Again" (Ease 1)**. Correct answers or "Hard/Good" ratings are ignored to keep the log focused on actual failures.
- **Accurate Comparison**: Records both the `Typed` input and the `Correct` answer side-by-side.
- **Timestamped Entries**: Every entry includes the date and time of the mistake, as well as the Note Type used.
- **Quick Access**: Adds a shortcut under **Tools > Open Dictation Error Log** to open the log file instantly in your default text editor.

## 🛠 Installation

1. Open Anki and navigate to **Tools** -> **Add-ons**.
2. Click **View Files** to open the local add-ons folder.
3. Create a new folder named `register_mistakes_anki`.
4. Save the Python script as `__init__.py` inside that folder.
5. **Restart Anki** to activate the plugin.

## 📖 Usage

1. Start your review session with cards that use the `{{type:Field}}` syntax.
2. When you misspell a word or miss a structure, press **1** (Again).
3. Access your accumulated mistakes anytime via **Tools -> Open Dictation Error Log**.

## 📂 Data Storage

- **File Name**: `anki_dictation_errors.txt`
- **Location**: The file is stored directly within the add-on folder for easy management and portability.

---
**Technical Note**: Developed for Anki 25.09+ (Qt6) environments.