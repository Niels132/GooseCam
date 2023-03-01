<H1> GooseCam (work in progress)</H1>
<p>The GooseCam is a scientific optical device to objectively measure gossebumps in humans (e.g. emotional goosebumps) </p>

<H2>Goosebumps</H2>

<H2>About the GooseCam</H2>
<p>...</p>
<H3>TTP communication with the goosecam</H3>
<p>The GooseCam is controlled via TTP communication. The GooseCam device is used as server that listens to client commands (e.g. the experimental software) In the following an example code of such a communication is shown:</p>
<code class = 'python'> 
import socket
  
def send_command(ip, command):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((ip, 8888))
  s.send(bytes(command, 'UTF-8'))
  s.close()
</code>
