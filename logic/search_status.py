import threading

stop_search = False

search_lock = threading.Lock()

def start_search_var():
    global stop_search
    with search_lock:
        stop_search = True

def cancel_search_var():
    global stop_search
    with search_lock:
        stop_search = False