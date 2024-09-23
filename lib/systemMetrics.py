import sys
import os

def get_system_metrics():

    # Screen metrics
    if sys.platform.startswith('win'):
        # Windows
        from win32api import GetSystemMetrics
        return GetSystemMetrics(0), GetSystemMetrics(1)
    elif sys.platform.startswith('darwin'):
        # macOS
        return os.environ.get('NSSCREENWIDTH', 1920), os.environ.get('NSSCREENHEIGHT', 1080)
    else:
        # Linux
        return os.environ.get('DISPLAY_WIDTH', 1920), os.environ.get('DISPLAY_HEIGHT', 1080)
