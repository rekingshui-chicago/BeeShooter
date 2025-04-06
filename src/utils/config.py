"""
Configuration utilities for the game
"""
import os
import argparse
import platform
import logging

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Retro Bee Shooter Game')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--debug-level', type=int, choices=[1, 2, 3], default=1,
                        help='Debug verbosity level (1-3)')
    parser.add_argument('--wsl-mode', action='store_true', help='Run in WSL compatibility mode')
    parser.add_argument('--no-sound', action='store_true', help='Disable sound')
    parser.add_argument('--platform', choices=['windows', 'linux', 'macos', 'wsl'],
                        help='Override platform detection')
    return parser.parse_args()

def detect_platform():
    """Detect the current platform"""
    system = platform.system().lower()

    # Check for WSL (Windows Subsystem for Linux)
    if system == 'linux' and os.path.exists('/proc/version'):
        with open('/proc/version', 'r') as f:
            if 'microsoft' in f.read().lower():
                return 'wsl'

    # Map platform.system() to our platform names
    platform_map = {
        'windows': 'windows',
        'linux': 'linux',
        'darwin': 'macos'
    }

    return platform_map.get(system, 'unknown')

def setup_logging(args):
    """Setup logging based on debug level"""
    log_level = logging.WARNING
    if args.debug:
        if args.debug_level == 1:
            log_level = logging.INFO
        elif args.debug_level == 2:
            log_level = logging.DEBUG
        elif args.debug_level == 3:
            log_level = logging.DEBUG  # Same level but more verbose in code

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("game_debug.log", mode='w'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger('bee_shooter')
    logger.info("Game starting with debug=%s, level=%s", args.debug, args.debug_level)
    
    return logger
