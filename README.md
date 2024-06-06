# Infosystems Display

The backend for the Infosystems VFD display that is 
located in the bar at EMF 2024.

It's from a German tram and made in 2000. 

Hostname: `vfd.display.crablab.uk`

## Demosite

There's a demo available at [vfd.display.crablab.uk/demo](http://vfd.display.crablab.uk/demo). 
This provides a basic interface to interact with the display.

## Controlling the display 

Two endpoints are provided: 

- `/time` - displays an updating clock 
- `/message` - takes POST data to display a message 

The `/message` endpoint takes the following form data: 

- `message` - text to display (up to 48 chars)
- `effect`  - chase or split 
- `wipe`    - True/False

eg. 

```
curl vfd.display.crablab.uk/time
```

```
curl vfd.display.crablab.uk/message -F message=Hello,\ World! -F effect=split
```

If the display returns a 409 then it's busy serving another request. Keep trying? 

## Run locally 

```
pip3 install flask pyfis markdown pygments
flask --app main.py run
```

## Contributions 

Improvements are welcome. I spent about an hour making a very minimal interface.

Huge thanks to [Cato](https://github.com/CatoLynx) who supplied both the IBIS
interface and the library to send Telegrams. 