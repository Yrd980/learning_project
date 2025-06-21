. script/common.sh >&/dev/null
. script/clashctl.sh >&/dev/null

_valid_env

[ -d "$CLASH_BASE_DIR" ] && _error_quit "please uninstall script,to clean path：$CLASH_BASE_DIR"

_get_kernel



