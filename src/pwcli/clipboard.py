import threading
import time

try:
    import pyperclip

    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False


def copy_to_clipboard(text: str, clear_after: int = 30) -> bool:
    """Copy text to the clipboard and clear it after a delay."""
    if not PYPERCLIP_AVAILABLE:
        return False

    try:
        pyperclip.copy(text)

        def clear_clipboard() -> None:
            time.sleep(clear_after)
            pyperclip.copy("")

        threading.Thread(target=clear_clipboard, daemon=True).start()
        return True
    except Exception:
        return False