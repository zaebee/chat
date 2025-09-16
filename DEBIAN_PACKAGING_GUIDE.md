# Debian Packaging Guide for a Python Web Application

This guide provides a comprehensive walkthrough of the process we followed to package the Hive Chat application as a Debian (`.deb`) package. This allows for easy installation, uninstallation, and management of the application as a system service.

## 1. Introduction to Debian Packaging

Debian packages are archives that contain all the files needed to install and run a piece of software. They are the standard way to distribute software on Debian-based Linux distributions like Ubuntu.

By packaging our application as a `.deb` file, we can:

*   Easily install and uninstall the application with a single command.
*   Automatically manage dependencies (i.e., other required packages).
*   Run the application as a `systemd` service, so it starts automatically on boot.
*   Manage the application's files in a clean and organized way.

## 2. Prerequisites

Before you can build a Debian package, you need to install the necessary packaging tools. These are the tools we used:

```bash
sudo apt-get install dpkg-dev debhelper dh-python python3-setuptools
```

*   `dpkg-dev`: Contains the tools needed to build Debian packages, including `dpkg-buildpackage`.
*   `debhelper`: A collection of scripts that automate common packaging tasks.
*   `dh-python`: A `debhelper` addon that provides tools for packaging Python applications.
*   `python3-setuptools`: Needed by the build process to create a Python wheel.

## 3. The `debian` Directory

All the files related to the Debian package are stored in a directory named `debian` inside the project's root directory.

Here's the final structure of our `debian` directory:

```
debian/
├── changelog
├── control
├── rules
├── source/
│   └── format
├── chat.service
├── postinst
└── prerm
```

Let's go through each of these files.

### `debian/changelog`

This file tracks the changes to the Debian package. It has a specific format that includes the package name, version, distribution, and a list of changes.

```
chat (0.1.0) unstable; urgency=medium

  * Initial release.

 -- Zaebee <sinezub@yandex.ru>  Tue, 16 Sep 2025 12:00:00 +0000
```

### `debian/control`

This is the most important file. It contains the metadata about the package, including its name, version, dependencies, and a description.

```
Source: chat
Section: python
Priority: optional
Maintainer: Zaebee <sinezub@yandex.ru>
Build-Depends: debhelper-compat (= 13), dh-python, python3-all, pybuild-plugin-pyproject, python3-setuptools
Standards-Version: 4.5.0

Package: chat
Architecture: all
Depends: python3-fastapi, python3-jinja2, python3-multipart, python3-uvicorn, python3-websockets, python3:any
Description: A simple multi-user chat application using FastAPI and WebSockets.
```

*   `Build-Depends`: The packages needed to build the application.
*   `Depends`: The packages needed to run the application.

### `debian/rules`

This is an executable script that defines how the package is built. We used `debhelper` and `dh-python` to automate most of the build process.

```makefile
#!/usr/bin/make -f

%:
	dh $@ --with python3 --buildsystem=pybuild

override_dh_auto_install:
	dh_auto_install
	mkdir -p $(CURDIR)/debian/chat/usr/share/chat
	cp -r chat.py static templates $(CURDIR)/debian/chat/usr/share/chat/

override_dh_installsystemd:
	dh_installsystemd --name=chat
```

*   The `override_dh_auto_install` target tells the build process to install the application files into `/usr/share/chat`.
*   The `override_dh_installsystemd` target tells `debhelper` to install the `systemd` service file.

### `debian/source/format`

This file specifies the source format for the package. We used `3.0 (native)` because we are creating a package for an application that doesn't have a separate upstream source tarball.

```
3.0 (native)
```

### `debian/chat.service`

This is the `systemd` service file that defines how to run the application as a service.

```
[Unit]
Description=Hive Chat
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/usr/share/chat
ExecStart=/usr/bin/python3 -m uvicorn chat:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

*   `User` and `Group`: The service runs as the `www-data` user for security reasons.
*   `WorkingDirectory`: The directory where the application is installed.
*   `ExecStart`: The command to start the application. We used `python3 -m uvicorn` for robustness.

### `debian/postinst` and `debian/prerm`

These are post-installation and pre-removal scripts. They are used to enable/disable and start/stop the `systemd` service.

`postinst`:
```bash
#!/bin/sh
set -e

if [ "$1" = "configure" ] ; then
    systemctl enable chat.service
    systemctl start chat.service
fi
```

`prerm`:
```bash
#!/bin/sh
set -e

if [ "$1" = "remove" ] ; then
    systemctl stop chat.service
    systemctl disable chat.service
fi
```

## 4. The `pyproject.toml` file

We needed to make a small change to the `pyproject.toml` file to help the build process. We explicitly told `setuptools` which Python module to include.

```toml
[tool.setuptools]
py-modules = ["chat"]
```

## 5. Building the Package

With all the files in place, we built the package with a single command:

```bash
dpkg-buildpackage -us -uc
```

*   `-us`: Do not sign the source package.
*   `-uc`: Do not sign the `.changes` file.

This command creates the `.deb` file in the parent directory.

## 6. Installing the Package

We first tried to install the package with `dpkg -i`, but this failed because `dpkg` does not automatically install dependencies.

The correct way to install the package and its dependencies is to use `apt`:

```bash
sudo apt-get install -f ../chat_0.1.0_all.deb
```

The `-f` flag tells `apt` to fix any broken dependencies.

## 7. Troubleshooting

We encountered several errors during the process. Here's a summary of the errors and how we fixed them:

*   **`debhelper compat level specified both in debian/compat and in debian/control`**: We removed the `debian/compat` file and kept the `debhelper-compat` build dependency in `debian/control`.
*   **`Backend 'setuptools.build_meta:__legacy__' is not available`**: We added `python3-setuptools` to the `Build-Depends` in `debian/control`.
*   **`can't build with source format '3.0 (quilt)': no upstream tarball found`**: We changed the source format in `debian/source/format` to `3.0 (native)` and removed the Debian revision from the version number in `debian/changelog`.
*   **`Multiple top-level packages discovered in a flat-layout`**: We explicitly specified the `chat` module in `pyproject.toml` using the `py-modules` option.
*   **`unable to open '/usr/lib/systemd/system/chat.service.dpkg-new'`**: We corrected the path in `debian/chat.install` to `/lib/systemd/system/`. When that didn't work, we removed `debian/chat.install` and used `override_dh_installsystemd` in the `rules` file.
*   **`dependency problems - leaving unconfigured`**: We used `apt-get install -f` to install the package and its dependencies.
*   **`service failed (Result: exit-code) ... status=203/EXEC`**: We changed the `ExecStart` command in the `systemd` service file to use the full path to the Python interpreter and run `uvicorn` as a module (`/usr/bin/python3 -m uvicorn ...`).

I hope this guide is helpful! Let me know if you have any other questions.
