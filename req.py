import http.client

def fetch(url='http://192.168.2.189:8000', method='GET'):
    # Define the URL and headers
    headers = {}

    # Create an HTTP connection
    conn = http.client.HTTPConnection(url.split("/")[2])

    # Send a GET request
    conn.request("GET", "/", headers=headers)

    # Get the response
    response = conn.getresponse()

    # Print the response status and data
    print("Status:", response.status, response.reason)
    data = response.read()
    print("Data:", data.decode())

    # Close the connection
    conn.close()

print(fetch())