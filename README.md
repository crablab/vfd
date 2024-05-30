# Infosystems Display

The backend for the Infosystems VFD display that is 
located somewhere at EMF 2024.

Hostname: `vfd.crablab.uk`

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
curl vfd.crablab.uk/time
```

```
curl vfd.crablab.uk/message -F message=Hello,\ World! -F effect=split
```

## Run locally 

```
pip3 install flask pyfis markdown pygments
flask --app main.py run
```

## Contributions 

Improvements are welcome. I spent about an hour making a very minimal interface.

Huge thanks to [Cato](https://github.com/CatoLynx) who supplied both the IBIS
interface and the library to send Telegrams. 