"""Pretty printing helpers so you can SEE what the agents are doing."""
from __future__ import annotations

import sys

# Make sure emoji and accents print on Windows terminals.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from rich.console import Console
    from rich.markup import escape
    from rich.panel import Panel

    _console = Console()
except ImportError:  # rich is optional
    _console = None


def title(text: str) -> None:
    if _console:
        _console.rule(f"[bold cyan]{escape(text)}")
    else:
        print(f"\n===== {text} =====")


def panel(text: str, heading: str = "", style: str = "green") -> None:
    if _console:
        _console.print(Panel(escape(text), title=escape(heading), border_style=style))
    else:
        print(f"\n--- {heading} ---\n{text}\n")


def event(who: str, what: str, style: str = "white") -> None:
    if _console:
        _console.print(f"[bold]{escape(who)}[/bold] [{style}]{escape(what)}[/{style}]",
                       highlight=False)
    else:
        print(f"{who} {what}")


def info(text: str) -> None:
    if _console:
        _console.print(f"[dim]{escape(text)}[/dim]")
    else:
        print(text)
