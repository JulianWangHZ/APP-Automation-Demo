import time


def handle_permission_dialogs(driver, platform):
    """handle permission dialogs"""
    try:
        print("check and handle permission dialog...")
        try:
          # use mobile: alert script for iOS permission dialogs
          driver.execute_script('mobile: alert', {'action': 'accept', 'buttonLabel': 'Allow'})
          print("ios permission dialog handled")
          time.sleep(2)
        except:
          print("no ios permission dialog or already handled")                   
    except Exception as e:
        print(f"error handling permission dialog: {e}") 