# Clash for Linux

This repository provides a convenient way to install, manage, and uninstall Clash on Linux systems. It includes scripts for easy installation, control, and cleanup, along with pre-configured resources.

## Features

*   **Easy Installation:** Automated setup using `install.sh`.
*   **Service Management:** Control Clash (start, stop, restart, enable, disable) via `clashctl.sh` (for bash/zsh) and `clashctl.fish` (for fish shell).
*   **Configuration:** Includes a `mixin.yaml` for custom Clash configurations and `Country.mmdb` for IP-based country lookups.
*   **Simple Uninstallation:** Clean removal with `uninstall.sh`.

## Installation

To install Clash for Linux, simply run the `install.sh` script:

```bash
./install.sh
```

This script will:
1.  Extract the Clash binary and YACD dashboard.
2.  Place the `clash` binary in `resources/bin/`.
3.  Set up the necessary configuration files.
4.  Create systemd service for Clash.
5.  Install `clashctl.sh` and `clashctl.fish` to `/usr/local/bin` for easy access.

## Usage

After installation, you can manage Clash using the `clashctl.sh` or `clashctl.fish` scripts.

### Common Commands

*   **Start Clash:**
    ```bash
    clashctl start
    ```
*   **Stop Clash:**
    ```bash
    clashctl stop
    ```
*   **Restart Clash:**
    ```bash
    clashctl restart
    ```
*   **Enable Clash to start on boot:**
    ```bash
    clashctl enable
    ```
*   **Disable Clash from starting on boot:**
    ```bash
    clashctl disable
    ```
*   **Check Clash status:**
    ```bash
    clashctl status
    ```
*   **View Clash logs:**
    ```bash
    clashctl log
    ```

## Configuration

*   **`resources/mixin.yaml`**: This file is used to customize your Clash configuration. You can modify it to add your proxy settings, rules, and other Clash-specific options.
*   **`resources/Country.mmdb`**: This is a GeoIP database used by Clash for IP-based country detection. Ensure it's up-to-date for accurate geo-filtering.

## Uninstallation

To uninstall Clash for Linux and remove all associated files, run the `uninstall.sh` script:

```bash
./uninstall.sh
```

This script will:
1.  Stop and disable the Clash systemd service.
2.  Remove the Clash binary and configuration files.
3.  Remove the `clashctl.sh` and `clashctl.fish` scripts from `/usr/local/bin`.

## References

ref https://github.com/nelvko/clash-for-linux-install
