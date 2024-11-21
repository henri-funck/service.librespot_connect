#!/bin/sh

# This script is a proof of concept of the addon

FILE="rtp://127.0.0.1:1234"

case "${1}" in
  "device")
    ffmpeg                                                 \
      -hide_banner -nostats                                \
      -avioflags direct                                    \
      -fflags nobuffer                                     \
      -re                                                  \
      -f s16le -ac 2 -ar 44100 -channel_layout stereo -i - \
      -acodec pcm_s16be                                    \
      -f rtp "${FILE}"                                     \
      -sdp_file /dev/null
    ;;
  "onevent")
    echo "${PLAYER_EVENT}" >&2
    case "${PLAYER_EVENT}" in
      "paused")
        kodi-send --action="PlayerControl(Pause)" >&2
        ;;
      "playing")
        kodi-send --action="PlayMedia(${FILE})" >&2
        ;;
      "sink")
        echo "${SINK_STATUS}" >&2
        ;;
      "stopped")
        kodi-send --action="PlayerControl(Stop)" >&2
        ;;
    esac
    ;;
  *)
    librespot                    \
      --backend pipe             \
      --disable-audio-cache      \
      --disable-credential-cache \
      --name  PoC                \
      --onevent "${0} onevent"   \
      --quiet                    \
      | ${0} device
    ;;
esac
