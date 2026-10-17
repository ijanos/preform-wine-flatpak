# PreForm Flatpak (unofficial)

Run Formlabs PreForm on x86_64 Linux using Wine bundled in a Flatpak.
Host Wine is not required.

## Disclaimer

**!!! This flatpak is not verified by, affiliated with, sponsored or supported by Formlabs in any way. !!!**

I work for Formlabs, but this is an independent personal project, not an official Formlabs project. 
It was created using only publicly available tools; no internal Formlabs tools or source code were used.

## Build and run

Install `flatpak` and `flatpak-builder` with your distribution's package manager then run: 


```sh
flatpak remote-add --user --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install --user flathub org.winehq.Wine/x86_64/stable-25.08
flatpak-builder --user --install-deps-from=flathub --force-clean --install build-dir com.formlabs.PreForm.yml
flatpak run com.formlabs.PreForm
```

On immutable distributions, you may need to use `flatpak run org.flatpak.Builder` instead
of `flatpak-builder` after installing the Flatpak Builder runtime.

## Limitations

- Automatic printer discovery is disabled by a Wine compatibility workaround.
- Updates require rebuilding the Flatpak; the PreForm updater is bypassed.

## Files and troubleshooting

The app can access Documents and Downloads. To allow another directory use
Flatseal or this commandline:

```sh
flatpak override --user --filesystem=/absolute/path/to/models com.formlabs.PreForm
```

Wine's private prefix is `~/.var/app/com.formlabs.PreForm/data/wine`.
For diagnostic logging or software OpenGL:

```sh
flatpak run --env=WINEDEBUG=+seh,+loaddll com.formlabs.PreForm
flatpak run com.formlabs.PreForm --openglBackend software
```

## License

The Flatpak generation code is licensed under CC0.
PreForm itself remains subject to Formlabs' license.
