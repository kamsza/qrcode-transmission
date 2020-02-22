# QR code transmission

The project, created to enable image transfer using animated qr codes.

## Sender

This program allows to change chosen image into set of qr codes and print them on the screen. To select file *fileopenbox* from *easygui* package was used. In *qrGenerator* there is *generate* function that divides image into chunks, generates qr codes from them and save them as .png files in qrcode directory. Function *show* from *qrGUI* package is responsible for displaying codes one after another in an endless loop.

## Receiver

This program allows to receive, decode and save transmitted file. First, we need some camera connected with our computer. We can use webcam or smartphone with android and [DroidCamApp](http://www.dev47apps.com) application (both, on it and computer). 
Using DroidCam you need to change ip and port numbers into those shown on your smartphone: 
```python
cap = cv2.VideoCapture("http://192.168.137.132:4747/video") 
```
Using webcam this version should work: 
```python
cap = cv2.VideoCapture("1") 
```
Receiver prints status in real time, showing information about received, mising and repeated qrcodes, that he read. In the end we got information about transfer time, data sent and transfer speed.

## Cleaner

Deletes all garbage sender created.