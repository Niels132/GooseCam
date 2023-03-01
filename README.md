<H1> GooseCam (work in progress)</H1>
<p>The GooseCam is a scientific optical device to objectively measure gossebumps in humans (e.g. emotional goosebumps) </p>

<H2>Goosebumps</H2>

<H2>About the GooseCam</H2>
<p>The GooseCam is basicaly just a camera that records an specific area of skin. While the camera is recording, LEDs illuminate the area of skin in an angle of 15°. If the Participant now gets goosebumps, they will produce a clear pattern in the video, taht later can be analyzed using fourier analysis.</p>
<H3>TTP communication with the goosecam</H3>


<p>The GooseCam is controlled via TTP communication. The GooseCam device is used as server that listens to client commands (e.g. the experimental software). In the following an example python code of such a communication is shown:</p>

```{r test-python, engine='python'}
import socket
import time 


def send_command(ip, command):
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 8888))
    s.send(bytes(command, 'UTF-8'))
    s.close()
  except:
    print('{}: Error sending "{}"'.format(ip, command))

#example session
ip = '192.168.0.27'
send_command('start_video,test.h264',ip)
time.sleep(10)
send_command('stop_video,',ip)
```
<p> commands that can be used are:
  <ul>
    <li>'light-on'</li>
    <li>'light-off'</li>
    <li>'photo,filename.jpg'</li>
    <li>'start_video,filename.h264'</li>
    <li>'stop_video'</li>
    <li>'annotate,text_to_write_to_log'</li>
  </ul>    
</p>
  
<p>Since many softwares used for designing experimental studies are able to use ttp communication, the field of use for those cameras is quite big. Softwares that have been tested are PsychoPy, E-Prime, Python and Matlab (see code/examples section )</>
  
