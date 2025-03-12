#!/usr/bin/env python3
"""
ASCII art logo for Telegram Bot Framework.
This module provides functions to display the ASCII logo in the terminal.
"""

def get_logo(color=True):
    """
    Returns the ASCII art logo for Telegram Bot Framework.
    
    Args:
        color (bool): Whether to include ANSI color codes.
        
    Returns:
        str: The ASCII art logo as a string.
    """
    logo = r"""
 ████████╗███████╗██╗     ███████╗ ██████╗ ██████╗  █████╗ ███╗   ███╗
 ╚══██╔══╝██╔════╝██║     ██╔════╝██╔════╝ ██╔══██╗██╔══██╗████╗ ████║
    ██║   █████╗  ██║     █████╗  ██║  ███╗██████╔╝███████║██╔████╔██║
    ██║   ██╔══╝  ██║     ██╔══╝  ██║   ██║██╔══██╗██╔══██║██║╚██╔╝██║
    ██║   ███████╗███████╗███████╗╚██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║
    ╚═╝   ╚══════╝╚══════╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝
                                                                     
                      Bot Framework for Python Developers
"""

    if color:
        # ANSI color codes
        BLUE = "\033[34m"
        CYAN = "\033[36m"
        GREEN = "\033[32m"
        RESET = "\033[0m"
        
        # Add colors to different parts of the logo
        colored_logo = f"{BLUE}{logo.split('Bot Framework')[0]}{CYAN}Bot Framework for Python Developers{RESET}"
        return colored_logo
    else:
        return logo


def print_logo():
    """
    Prints the ASCII art logo to the terminal with colors.
    """
    print(get_logo())


def print_welcome_message():
    """
    Prints the ASCII art logo along with a welcome message.
    """
    print(get_logo())
    print("\n" + "=" * 80)
    print("Welcome to Telegram Bot Framework - Build powerful Telegram bots with ease")
    print("Version: 1.0.0")
    print("=" * 80 + "\n")
    print("Type 'help' for a list of commands or 'start' to run your bot.\n")


if __name__ == "__main__":
    # Test the logo
    print_welcome_message() 