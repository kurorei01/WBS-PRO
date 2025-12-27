import time
import sys
from colorama import Fore, Style
from threading import Event


def print_banner():
    banner_main = (
        Fore.MAGENTA + Style.BRIGHT + """
 ██████╗  ███████╗███╗   ██╗            ███████╗
 ██╔═══╝  ██╔════╝████╗  ██║                ██╔╝
 ██║  ███╗█████╗  ██╔██╗ ██║               ██╔╝
 ██║   ██║██╔══╝  ██║╚██╗██║              ██╔╝
 ╚██████╔╝███████╗██║ ╚████║             ██╔╝
  ╚═════╝ ╚══════╝╚═╝  ╚═══╝            ███████╗
"""
    )
    banner_mid = (
        Fore.LIGHTMAGENTA_EX + Style.BRIGHT + """
════════════════════════════════════════════════════
      ⚡ G E N  Z  •  B U G  S C A N N E R ⚡
════════════════════════════════════════════════════
"""
    )
    banner_footer = (
        Fore.MAGENTA + Style.BRIGHT
        + "🏃💨 Gen Z power on: Ready to scan the web! ✧˖°.🖥️🔒\n"
        + "       ⚡ DEVELOPED BY SIBER GEN Z ⚡\n" 
        
    )
    print(banner_main + banner_mid)
    print(banner_footer)

def loading_animation(stop_event: Event) -> None:
    """Run a small terminal animation until `stop_event` is set."""
    frames = [
        "   🏃💨💨💨  ",
        "  🏃💨💨   ",
        " 🏃💨   ",
        
    ]
    idx = 1
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.CYAN}{Style.BRIGHT}Scanning in progress... {frames[idx % len(frames)]}")
        sys.stdout.flush()
        idx += 1
        time.sleep(0.15)
    sys.stdout.write("\r" + " " * 50 + "\r")

def print_completion_message(success: bool):
    """Print completion message based on success status."""
    if success:
        print(Fore.MAGENTA + Style.BRIGHT + "\nGEN Z SCAN selesai! Stay safe out there ✧˖°🖥️🔒\n")
    else:
        print(Fore.RED + Style.BRIGHT + "\nScan gagal total, tapi tool tetap aman. Coba URL lain! 💥\n")