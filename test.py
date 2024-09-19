import certstream
import pandas as pd
import time

# Initialize a list to store the JSON messages
data_list = []

# Record the start time
start_time = time.time()

def certstream_callback(message, context):
    # Stop listening after 1 second
    if time.time() - start_time > 1:
        raise KeyboardInterrupt  # This will exit the listener

    # Append the entire JSON message to the data list
    data_list.append(message)

try:
    # Start listening to CertStream events
    certstream.listen_for_events(certstream_callback, url='wss://certstream.calidog.io/')
except KeyboardInterrupt:
    # Gracefully exit the listener after 1 second
    pass

# Normalize the list of JSON messages into a flat table
df = pd.json_normalize(data_list)

# Display the DataFrame
print(df)