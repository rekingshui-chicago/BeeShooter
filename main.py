#!/usr/bin/env python3
"""
Retro Bee Shooter Game - Main Entry Point
"""
import sys
import logging
from src.game.game_manager import GameManager
from src.utils.config import parse_args, setup_logging

def main():
    """Main entry point for the game"""
    # Parse command line arguments
    args = parse_args()
    
    # Setup logging
    logger = setup_logging(args)
    
    try:
        # Create and run game
        game = GameManager(args)
        game.run()
    except Exception as e:
        logger.error("Error in game: %s", str(e), exc_info=True)
        print(f"\nERROR: {str(e)}\n")
        import traceback
        traceback.print_exc()
        print("\nThe game encountered an error. Check game_debug.log for details.")
    finally:
        logger.info("Game shutting down")
        sys.exit()

if __name__ == "__main__":
    main()
