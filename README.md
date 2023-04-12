![logo](https://github.com/miguelvalente/imagemangler/blob/master/logo.png?raw=true)


Image Mangler is a command-line tool to deteriorate an image iteratively using lossy algorithms.

# Installation

You can install Image Mangler via pip:

```bash
pip install imagemangler
```

# Usage

You can run Image Mangler by invoking the imagemangler command in the terminal, followed by the path of the image file you want to mangle:

```bash
imagemangler path/to/image.jpg
```

By default, Image Mangler will automatically mangle the image across all quality steps with a base quality of 70 and a quality step of 2. You can specify your own values for these parameters using the optional flags:


```bash
imagemangler path/to/image.jpg --quality 60 --quality-step 5 --no-auto-mangle
```

For a more details you can use `--help`:

```bash
imagemangler --help
```
