import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
LED_PINS = [16, 20, 21] # my led pins
for pin in LED_PINS:
    GPIO.setup(pin, GPIO.OUT)
pwms = [GPIO.PWM(pin, 1000) for pin in LED_PINS] # 1kHz frequency
for pwm in pwms:
    pwm.start(0)

html = """
<html><body>
  <h2>Control 3 LEDs Instantly</h2>
  <div style='width: 230px; border: 2px solid #888; padding: 10px;'>
    <label>LED 1</label>
    <input type='range' min='0' max='100' value='0' id='led1'><span id='val1'>0</span><br>
    <label>LED 2</label>
    <input type='range' min='0' max='100' value='0' id='led2'><span id='val2'>0</span><br>
    <label>LED 3</label>
    <input type='range' min='0' max='100' value='0' id='led3'><span id='val3'>0</span><br>
  </div>
  <script>
    function setLED(idx, value){
      fetch('/', {method: 'POST', body: `led=${idx}&brightness=${value}`});
    }
    [1,2,3].forEach(function(i){
      let s = document.getElementById('led'+i);
      let v = document.getElementById('val'+i);
      s.oninput = function(){
        v.textContent = s.value;
        setLED(i, s.value);
      };
    });
  </script>
</body></html>
"""

host = ''
port = 8080
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
        # POST HANDLING: Only update LEDs if POST is received
        if request.startswith('POST'):
            idx = request.find('\r\n\r\n')
            body = request[idx+4:] if idx != -1 else ''   # Body is after headers
            items = body.split('&')                       # Split into form fields
            params = {}                                   # Dictionary for values
            for item in items:
                if '=' in item:
                    k,v = item.split('=')                 # key=value
                    params[k] = v                         # Store in dictionary
            if 'led' in params and 'brightness' in params:
                led_idx = int(params['led']) - 1          # Convert from 1,2,3 to index 0,1,2
                val = int(params['brightness'])           # Convert brightness string to int
                pwms[led_idx].ChangeDutyCycle(val)        # Update specified LED

        #Always respond with the same HTML/JavaScript page
        response = (
            "HTTP/1.1 200 OK\r\n" + "Content-Type: text/html\r\n" + f"Content-Length: {len(html.encode())}\r\n" + "Connection: close\r\n" + "\r\n" + html
        )
        conn.sendall(response.encode()) # Send response
        conn.close() # Close connection
finally:
    for pwm in pwms:
        pwm.stop()
    GPIO.cleanup() 
