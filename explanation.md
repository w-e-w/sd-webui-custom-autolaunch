<details>
<summary>

`Custom autolaunch command`: Override the default behavior of autolaunch - click to see explanation
</summary>

Custom command example
```shell
"C:\Program Files\Mozilla Firefox\firefox.exe" -new-window {url}
```

<details><summary>Example command explanation</summary>
<br>
This is a command that consisted of three parts, the function is to launch Web UI in a new Firefox window.

The three part corresponds to `Executable`, `Argument(s)`, `{url}`:
- `Executable` : Path to Firefox executable<br>
Paths that contain spaces needs to be enclosed in quotes.
- `Argument(s)` : A command line argument of Firefox, this maks it launch a new window.<br>
Different programs would have different arguments, please read the documentation of the application of your choice.<br>
You may use multiple arguments.
- `{url}` : placeholder for Web UI's URL, it will automatically be replaced with the actual URL.<br>
When using the placeholder input exactly `{url}` lowercase including the brackets
</details>

<details><summary>Security Warning & Why command is not editable</summary>
<br>
In essence this extension allows any one to run any command when Web UI loads,
this is a huge security risk as it can be exploited to do just about anything,
as such the `command` setting is `Read-only` if Web UI can be accessed remotely.

> Accessible remotely is defined as if any of `--share`, `--listen`, `--ngrok`, `--server-name` Command Line Arguments are in use.

If necessary you can forcibly allow modification by using `--enable-insecure-extension-access`
> Use this only when necessary and immediately disabled afterwards.
</details>
</details>
