"""Progress indicators and spinners for better UX."""

import time
import sys
import threading
from typing import Optional, Callable


class Spinner:
    """Simple spinner for showing progress."""

    FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

    def __init__(self, message: str = "Loading"):
        self.message = message
        self.running = False
        self.thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the spinner."""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._spin, daemon=True)
        self.thread.start()

    def stop(self, final_message: Optional[str] = None) -> None:
        """Stop the spinner."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        if final_message:
            sys.stdout.write(f"\r{final_message}\n")
        else:
            sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()

    def _spin(self) -> None:
        """Spin animation loop."""
        frame_idx = 0
        while self.running:
            frame = self.FRAMES[frame_idx % len(self.FRAMES)]
            sys.stdout.write(f"\r{frame} {self.message}")
            sys.stdout.flush()
            frame_idx += 1
            time.sleep(0.1)


class ProgressBar:
    """Simple progress bar."""

    def __init__(self, total: int, message: str = "Progress"):
        self.total = total
        self.current = 0
        self.message = message

    def update(self, amount: int = 1) -> None:
        """Update progress."""
        self.current = min(self.current + amount, self.total)
        self._render()

    def set(self, value: int) -> None:
        """Set progress to specific value."""
        self.current = min(value, self.total)
        self._render()

    def _render(self) -> None:
        """Render progress bar."""
        percent = (self.current / self.total) * 100 if self.total > 0 else 0
        filled = int((self.current / self.total) * 20) if self.total > 0 else 0
        bar = "█" * filled + "░" * (20 - filled)

        sys.stdout.write(
            f"\r{self.message} [{bar}] {percent:.0f}% ({self.current}/{self.total})"
        )
        sys.stdout.flush()

        if self.current >= self.total:
            sys.stdout.write("\n")
            sys.stdout.flush()


def with_spinner(message: str) -> Callable:
    """Decorator to run function with spinner."""

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            spinner = Spinner(message)
            spinner.start()
            try:
                result = func(*args, **kwargs)
                spinner.stop(f"✓ {message}")
                return result
            except Exception as e:
                spinner.stop(f"✗ {message}")
                raise e

        return wrapper

    return decorator
