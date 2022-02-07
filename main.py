#!/usr/bin/env python3
import click
import soco

@click.command()
@click.argument("sonos_ip")
@click.argument("stream_url")
def cli(sonos_ip, stream_url):
    """Plays the given STREAM_URL on the SONOS_IP device"""
    speaker = soco.SoCo(sonos_ip)
    speaker.clear_queue()
    speaker.add_uri_to_queue(stream_url)
    speaker.play_from_queue(0)

def main():
    cli(prog_name="sonos-play")


if __name__ == "__main__":
    main()
