# Wayland Platform

Qt reports `wayland` as platform name.

QPA for Wayland is not located in `qtbase//src/gui/platform/` but in the module `qtwayland//src/client/`.

## Qt Wayland Scanner

Tool to generate Qt C++ code for the Wayland XML Protocol `src/3rdparty/protocol`.

Source in `src/qtwaylandscanner/qtwaylandscanner.cpp`

## Wayland Resources

* [Wayland Explorer](https://wayland.app/protocols)
* [The Wayland Protocol](https://wayland-book.com)
* [wayland-scanner](https://wayland-book.com/libwayland/wayland-scanner.html)
* [Seats: Handling input](https://wayland-book.com/seat.html)
* https://gitlab.freedesktop.org/wayland/wayland-protocols
* https://gitlab.freedesktop.org/wayland/wayland/-/blob/main/protocol/wayland.xml

```
#include <wayland-client.h>
```

## Wayland Stack

```
kernel -/-> user space

Kernel
    Video Output Management & Inputs: keyboard, mouse, tablet
  -------------------------------------------------------------
  : KMS (Kernel Mode Setting) -/-> ioctl — video chip manager

  : evdev (event device) — /dev/input/...
  / udev (userspace /dev) — device manager (device discovery)
      -/-> libinput
  ----------------------------
      ---> Single Application
      ---> Wayland Compositor
          ---> libwayland-client
              ---> Application


    GPU OpenGL / Vulkan API
  ---------------------------
  : DRM (Direct Rendering Manager) -/-> libDRM ---> Mesa ---> EGL
  : Nvidia Blob -/-> Nvidia Driver
  ----------------------------
      ---> Single Application
      ---> Compositor (screen) / Application (texture)

  : LinuxFB — software-rendered ---> video chip framebuffer


    Sound & Video Capture
    (kind of OpenGL API for Sound/Video)
  ----------------------------------------
  : Alsa (Advanced Linux Sound Architecture)
  : Video4Linux — device drivers and an API for supporting realtime video capture
  : Bluetooth
  ---------------------------
      -/-> PipeWire
          ---> Application
```

## Debug Wayland

```
WAYLAND_DEBUG=1 program
```

* https://wayland.freedesktop.org/extras.html
* [wayland-debug](https://github.com/wmww/w

ayland-debug) A command line tool to help debug Wayland clients and servers

## Debug libinput

```
> evtest

/dev/input/by-id
/dev/input/by-path
```
