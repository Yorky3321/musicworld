#!/bin/bash
ln -sf /app/.apt/usr/lib/x86_64-linux-gnu/pulseaudio/libpulsecommon-16.1.so /app/.apt/usr/lib/x86_64-linux-gnu/libpulsecommon-16.1.so
exec gunicorn mysite.wsgi
