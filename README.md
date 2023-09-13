# Stable Diffusion Web UI Custom AutoLaunch command
### Allows you to customize the autolaunch behavior of Web UI

The default `autolaunch` can only launch Web UI in the default browser with no customization available.

However, there are scenarios where users desire to launch the Web UI in a browser of their choice.

In such cases, one would need to manual open the Web UI in their preferred browser or create a custom script that does it for them.

With this extension you will be able to override the default `autolaunch` and set `custom autolaunch command` in settings. 

## Usage
After installation of this extension, you will several new options at the bottom of the `Setting` > `Systems` tab

1. `Enable custom AutoLaunch`<br>
Enable / Disable `Custom AutoLaunch command`

2. `Custom AutoLaunch command`<br>
A custom command to be executed when Web UI you are loads

---
### Custom command example
```shell
"C:\Program Files\Mozilla Firefox\firefox.exe" -new-window {url}
```

This is a command that consisted of three parts, the function is to launch Web UI in a new Firefox window.

The three part corresponds to `Executable`, `Argument(s)`, `{url}`:
- `Executable` : Path to Firefox executable<br>
Paths that contain spaces needs to be enclosed in quotes.
- `Argument(s)` : A command line argument of Firefox, this maks it launch a new window.<br>
Different programs would have different arguments, please read the documentation of the application of your choice.<br>
You may use multiple arguments.
- `{url}` : placeholder for Web UI's URL, it will automatically be replaced with the actual URL.<br>
When using the placeholder input exactly `{url}` lowercase including the brackets

---
### Notes
1. When `Custom AutoLaunch` is enabled the `default autolaunch` will be disabled
2. `Custom AutoLaunch` is triggered under the same conditions governed by<br>
`Automatically open Web UI in browser on startup` and `--autolaunch`<br>
In other words if `open Web UI in browser` is disabled `Custom AutoLaunch` will not trigger

---
## Security Warning & Why command is not editable

In essence this extension allows any one to run any command when Web UI loads<br>
this is a huge security risk as it can be exploited to do just about anything<br>
as such the `command` setting is `Read-only` if Web UI can be accessed remotely.

> Accessible remotely is defined as if any of `--share`, `--listen`, `--ngrok`, `--server-name` Command Line Arguments are in use.

If necessary you can forcibly allow modification by using `--enable-insecure-extension-access`
> Use this only when necessary and immediately disabled afterwards.
