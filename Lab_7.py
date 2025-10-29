import RPi.GPIO as GPIO
import socket

# SETUP GPIO
GPIO.setmode(GPIO.BCM)
LED_PINS = [16, 20, 21]  # Example GPIO pins; change for your setup
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
pwms = [GPIO.PWM(pin, 1000) for pin in LED_PINS] # 1kHz frequency
for pwm in pwms:
    pwm.start(0)  # Start at 0% brightness
brightness = [0, 0, 0]  # Store brightness levels for each LED

def parsePOSTdata(data): # Parses URL-encoded POST data into a dictionary
    datadict = {}
    datapairs = data.split('&')
    for pair in datapairs:
        keyval = pair.split('=')
        if len(keyval) == 2:
            datadict[keyval[0]] = keyval[1]
    return datadict

def build_form_page(msg=""): # Builds the HTML form page
    return f"""
    <html><body>
      <h2>Control LED Brightness</h2>
      <form method='POST'>
        <label>Select LED:</label><br>
        <input type='radio' name='led' value='1' checked> LED 1 ({brightness[0]}%)<br>
        <input type='radio' name='led' value='2'> LED 2 ({brightness[1]}%)<br>
        <input type='radio' name='led' value='3'> LED 3 ({brightness[2]}%)<br><br>
        <label for='brightness'>Brightness:</label><br>
        <input type='range' id='brightness' name='brightness' min='0' max='100' value='0'><br>
        <input type='submit' value='Set'>
      </form>
      <p>{msg}</p>
    </body></html>
    """

# Socket Web Server Setup
host = ''  # listen on all interfaces
port = 8080 # port number
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(1)
print(f"Serving HTTP on port {port}...")
try:
    while True:
        conn, addr = server.accept()
        request = conn.recv(2048).decode()
        if not request:
            conn.close()
            continue
        # Parse method (GET or POST)
        first_line = request.split('\n')[0]
        if request.startswith('POST'):
            idx = request.find('\r\n\r\n')
            body = request[idx+4:] if idx != -1 else ''
            postvals = parsePOSTdata(body)
            led_idx = int(postvals.get('led', '1')) - 1
            bval = int(postvals.get('brightness', '0'))
            brightness[led_idx] = bval
            pwms[led_idx].ChangeDutyCycle(bval)
            msg = f"Set LED {led_idx+1} to {bval}% brightness."
        else:
            msg = ""
        html = build_form_page(msg)
        response = (
            "HTTP/1.1 200 OK\r\n" +
            "Content-Type: text/html\r\n" +
            f"Content-Length: {len(html.encode())}\r\n" +
            "Connection: close\r\n" +
            "\r\n" +
            html
        )
        conn.sendall(response.encode())
        conn.close()
finally:
    for pwm in pwms:
        pwm.stop()
    GPIO.cleanup()


