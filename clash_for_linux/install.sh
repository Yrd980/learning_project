. script/common.sh >&/dev/null
. script/clashctl.sh >&/dev/null

_valid_env

[ -d "$CLASH_BASE_DIR" ] && _error_quit "please uninstall script,to clean path：$CLASH_BASE_DIR"

_get_kernel

/usr/bin/install -D <(gzip -dc "$ZIP_KERNEL") "${RESOURCES_BIN_DIR}/$BIN_KERNEL_NAME"
tar -xf "$ZIP_SUBCONVERTER" -C "$RESOURCES_BIN_DIR"
tar -xf "$ZIP_YQ" -C "${RESOURCES_BIN_DIR}"

/bin/mv -f ${RESOURCES_BIN_DIR}/yq_* "${RESOURCES_BIN_DIR}/yq"

_set_bin "$RESOURCES_BIN_DIR"
_valid_config "$RESOURCES_CONFIG" || {
  echo -n "$(_okcat '✈️ ' 'input subscribe link：')"
  read -r url
  _okcat '⏳' 'downloading...'
  _download_config "$RESOURCES_CONFIG" "$url" || _error_quit "download error: please write config to $RESOURCES_CONFIG reinstall"
  _valid_config "$RESOURCES_CONFIG" || _error_quit "invalid config, please check config：$RESOURCES_CONFIG，convert log：$BIN_SUBCONVERTER_LOG"
}
_okcat '✅' 'config available'
mkdir "$CLASH_BASE_DIR"
echo "$url" >"$CLASH_CONFIG_URL"

/bin/cp -rf "$SCRIPT_BASE_DIR" "$CLASH_BASE_DIR"
/bin/ls "$RESOURCES_BASE_DIR" | grep -Ev 'zip|png' | xargs -I {} /bin/cp -rf "${RESOURCES_BASE_DIR}/{}" "$CLASH_BASE_DIR"
tar -xf "$ZIP_UI" -C "$CLASH_BASE_DIR"

_set_rc
_set_bin
_merge_config_restart
cat <<EOF >"/etc/systemd/system/${BIN_KERNEL_NAME}.service"
[Unit]
Description=$BIN_KERNEL_NAME Daemon, A[nother] Clash Kernel.

[Service]
Type=simple
Restart=always
ExecStart=${BIN_KERNEL} -d ${CLASH_BASE_DIR} -f ${CLASH_CONFIG_RUNTIME}

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "$BIN_KERNEL_NAME" >&/dev/null || _failcat '💥' "autostart fail" && _okcat '🚀' "set auto start"

clashui
_okcat '🎉' 'enjoy 🎉'
clash
_quit
