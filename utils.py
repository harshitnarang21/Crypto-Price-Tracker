"""
Utility Functions
Helper functions for formatting and display
"""

from colorama import Fore, Style, init
from typing import Optional

# Initialize colorama for cross-platform colored output
init(autoreset=True)


def format_currency(amount: float, decimals: int = 2) -> str:
    """Format number as currency"""
    if amount is None:
        return "$0.00"
    return f"${amount:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 2) -> str:
    """Format number as percentage"""
    if value is None:
        return "N/A"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.{decimals}f}%"


def format_large_number(num: float) -> str:
    """Format large numbers with K, M, B suffixes"""
    if num is None or num == 0:
        return "$0.00"
    if num >= 1_000_000_000:
        return f"${num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"${num/1_000:.2f}K"
    else:
        return format_currency(num)


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text.center(60)}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


def print_success(message: str):
    """Print success message in green"""
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")


def print_error(message: str):
    """Print error message in red"""
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")


def print_warning(message: str):
    """Print warning message in yellow"""
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")


def print_info(message: str):
    """Print info message in blue"""
    print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")


def get_color_for_change(change: float) -> str:
    """Get color code based on price change"""
    if change is None:
        return Style.RESET_ALL
    if change > 0:
        return Fore.GREEN
    elif change < 0:
        return Fore.RED
    else:
        return Style.RESET_ALL


def print_table_row(items: list, widths: Optional[list] = None):
    """Print a formatted table row"""
    if widths is None:
        widths = [15] * len(items)
    
    row = " | ".join(str(item).ljust(width) for item, width in zip(items, widths))
    print(row)


def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def validate_float_input(prompt: str, min_value: Optional[float] = None, 
                        max_value: Optional[float] = None) -> float:
    """Validate and get float input from user"""
    while True:
        try:
            value = float(input(prompt))
            if min_value is not None and value < min_value:
                print_error(f"Value must be at least {min_value}")
                continue
            if max_value is not None and value > max_value:
                print_error(f"Value must be at most {max_value}")
                continue
            return value
        except ValueError:
            print_error("Please enter a valid number")


def validate_int_input(prompt: str, min_value: Optional[int] = None, 
                      max_value: Optional[int] = None) -> int:
    """Validate and get integer input from user"""
    while True:
        try:
            value = int(input(prompt))
            if min_value is not None and value < min_value:
                print_error(f"Value must be at least {min_value}")
                continue
            if max_value is not None and value > max_value:
                print_error(f"Value must be at most {max_value}")
                continue
            return value
        except ValueError:
            print_error("Please enter a valid integer")

