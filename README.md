# sonos-live-stream

A small tutorial on how to live-stream audio from your computer
to your Sonos sound-system.

## Requirements

- Linux
- Pulseaudio
- ffmpeg
- Docker
- Pipenv and Python 3.9+

## Architecture

Most Sonos speakers (if not all) support streaming radio mp3s by specifying an URL and by adding to the queue
something like:
```
x-rincon-mp3radio://example.com/audio/stream.m3u8
```

By using this feature, one can stream audio from a computer and thus provide an AirPlay-like experience
from your GNU/Linux OS to a Sonos speaker.

To achieve this, we will do the following:

```
┌─────────────┐           ┌────────────────┐
│             │           │                │
│   Firefox   ├───────────►  Virtual Sink  │
│             │           │                │
└─────────────┘           └────────┬───────┘
                                   │ -f pulse -i "VSink"
                          ┌────────▼───────┐       ┌───────────────┐
                          │                │ :8554 │               │
                          │     ffmpeg     ├───────►  rtsp-server  │
                          │                │       │               │
                          └────────────────┘       └───────▲───────┘
                                                           │ :8888
                                                           │
                                                           │
                                                           │
     ┌───────────┐                                         │
     │           │       x-rincon-mp3radio://              │
     │   Sonos   ├─────────────────────────────────────────┘
     │           │
     └───────────┘
```

## Procedure

### Setup

1. Clone this repository
1. `docker-compose up -d`

### Creating a Virtual Sink

```
pactl load-module module-null-sink \
        sink_name=vsink \
        sink_properties=device.description=VSink
```

### Streaming audio to rtsp-server

With this command we'll begin streaming the audio from our Virtual Sink
to the rtsp-server.

```
P=vsink.monitor
ffmpeg -f pulse -i "$P" -f rtsp rtsp://127.0.0.1:8554/audio
```

### Redirecting the stream from Firefox to the virtual-sink

This can be done easily via `pavucontrol`. Go to the playbak tab while reproducing
something on Firefox, then select "vsink" as the output.

### Asking Sonos to play the stream

Assuming:
- `192.168.5.88` is your Sonos IP address
- `192.168.5.38` is your computer IP address

1. `pipenv shell`
1. `python main.py 192.168.5.88 x-rincon-mp3radio://192.168.5.38:8888/audio/stream.m3u8`

