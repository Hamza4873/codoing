import certstream
import threading
import time

def certstream_callback(message, _):
    print(f"Received message: {message}")

def stop_stream_after(duration, thread):
    time.sleep(duration)
    print(f"Stopping the stream after {duration} seconds.")
    # Stop the thread gracefully
    if thread.is_alive():
        # Raise a SystemExit in the thread to stop it
        print("Terminating the stream...")
        raise SystemExit

# Start the CertStream listener in a separate thread
certstream_thread = threading.Thread(target=certstream.listen_for_events, args=(certstream_callback, 'wss://certstream.calidog.io/'))
certstream_thread.start()

# Set a timer to stop the stream after 10 seconds
duration = 10  # Stop after 10 seconds
stop_timer = threading.Thread(target=stop_stream_after, args=(duration, certstream_thread))
stop_timer.start()