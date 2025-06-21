function clashon() {
  _get_proxy_port
  systemctl is-active "$BIN_KERNEL_NAME" >&/dev/null || {
    sudo systemctl start "$BIN_KERNEL_NAME" >/dev/null || {
      _failcat 'fail start: please execute clashstatus check log'
      return 1
    }
  }

  local auth=$(sudo "$BIN_YQ" '.authentication[0] // ""' "$CLASH_CONFIG_RUNTIME")
  [ -n "$auth" ] && auth=$auth@

  local http_proxy_addr="http://${auth}127.0.0.1:${MIXED_PORT}"
  local socks_proxy_addr="socks5h://${auth}127.0.0.1:${MIXED_PORT}"
  local no_proxy_addr="localhost,127.0.0.1,::1"

  export http_proxy=$http_proxy_addr
  export https_proxy=$http_proxy
  export HTTP_PROXY=$http_proxy
  export HTTPS_PROXY=$http_proxy

  export all_proxy=$socks_proxy_addr
  export ALL_PROXY=$all_proxy

  export no_proxy=$no_proxy_addr
  export NO_PROXY=$no_proxy

  _okcat 'start proxy enverionment'
}

watch_proxy() {
  [ -z "$http_proxy" ] && [[ $- == *i* ]] && {
    _is_root || _failcat 'not detect enverionment variable，execute clashon to start proxy enverionment' && clashon
  }
}

function clashoff() {
  sudo systemctl stop "$BIN_KERNEL_NAME" && _okcat 'exit proxy enverionment' ||
    _failcat 'exit error: please execute "clashstatus" to check log' || return 1

  unset http_proxy
  unset https_proxy
  unset HTTP_PROXY
  unset HTTPS_PROXY
  unset all_proxy
  unset ALL_PROXY
  unset no_proxy
  unset NO_PROXY
}

clashrestart() {
  { clashoff && clashon; } >&/dev/null
}

function clashstatus() {
  sudo systemctl status "$BIN_KERNEL_NAME" "$@"
}

function clashui() {
  _get_ui_port
  local query_url='api64.ipify.org'

  local public_ip=$(curl -s --noproxy "*" --connect-timeout 2 $query_url)
  local public_address="http://${public_ip:}:${UI_PORT}/ui"

  local local_ip=$(hostname -I | awk '{print $1}')
  local local_address="http://${local_ip}:${UI_PORT}/ui"

  printf "\n"
  printf "╔═══════════════════════════════════════════════╗\n"
  printf "║                %s                  ║\n" "$(_okcat 'Web console')"
  printf "║═══════════════════════════════════════════════║\n"
  printf "║                                               ║\n"
  printf "║     🔓 please enabel port：%-5s                    ║\n" "$UI_PORT"
  printf "║     🏠 local：%-31s  ║\n" "$local_address"
  printf "║     🌏 public：%-31s  ║\n" "$public_address"
  printf "║     ☁️  share：%-31s  ║\n" "$URL_CLASH_UI"
  printf "║                                               ║\n"
  printf "╚═══════════════════════════════════════════════╝\n"
  printf "\n"
}

_merge_config_restart() {
  local backup="/tmp/rt.backup"
  sudo cat "$CLASH_CONFIG_RUNTIME" 2>/dev/null | sudo tee $backup >&/dev/null
  sudo "$BIN_YQ" eval-all '. as $item ireduce ({}; . *+ $item) | (.. | select(tag == "!!seq")) |= unique' \
      "$CLASH_CONFIG_MIXIN" "$CLASH_CONFIG_RAW" "$CLASH_CONFIG_MIXIN" | sudo tee "$CLASH_CONFIG_RUNTIME" >&/dev/null
  _valid_config "$CLASH_CONFIG_RUNTIME" || {
      sudo cat $backup | sudo tee "$CLASH_CONFIG_RUNTIME" >&/dev/null
      _error_quit "check error：pleaes check Mixin config"
  }
  clashrestart
}

function clashsecret() {
    case "$#" in
    0)
        _okcat "current secret：$(sudo "$BIN_YQ" '.secret // ""' "$CLASH_CONFIG_RUNTIME")"
        ;;
    1)
        sudo "$BIN_YQ" -i ".secret = \"$1\"" "$CLASH_CONFIG_MIXIN" || {
            _failcat "secret update error, please input again"
            return 1
        }
        _merge_config_restart
        _okcat "secret update success"
        ;;
    *)
        _failcat "exclude space and quotation"
        ;;
    esac
}

_tunstatus() {
    local tun_status=$(sudo "$BIN_YQ" '.tun.enable' "${CLASH_CONFIG_RUNTIME}")
    [ "$tun_status" = 'true' ] && _okcat 'Tun status：enable' || _failcat 'Tun status：close'
}

_tunoff() {
    _tunstatus >/dev/null || return 0
    sudo "$BIN_YQ" -i '.tun.enable = false' "$CLASH_CONFIG_MIXIN"
    _merge_config_restart && _okcat "Tun mode closed"
}

_tunon() {
    _tunstatus 2>/dev/null && return 0
    sudo "$BIN_YQ" -i '.tun.enable = true' "$CLASH_CONFIG_MIXIN"
    _merge_config_restart
    sleep 0.5s
    sudo journalctl -u "$BIN_KERNEL_NAME" --since "1 min ago" | grep -E -m1 'unsupported kernel version|Start TUN listening error' && {
        _tunoff >&/dev/null
        _error_quit 'unsupported kernel version'
    }
    _okcat "Tun mode started "
}

function clashtun() {
    case "$1" in
    on)
        _tunon
        ;;
    off)
        _tunoff
        ;;
    *)
        _tunstatus
        ;;
    esac
}

function clashupdate() {
    local url=$(cat "$CLASH_CONFIG_URL")
    local is_auto

    case "$1" in
    auto)
        is_auto=true
        [ -n "$2" ] && url=$2
        ;;
    log)
        sudo tail "${CLASH_UPDATE_LOG}" 2>/dev/null || _failcat "not update log"
        return 0
        ;;
    *)
        [ -n "$1" ] && url=$1
        ;;
    esac

    [ "${url:0:4}" != "http" ] && {
        _failcat "not provide effect subscribe link：use ${CLASH_CONFIG_RAW} updating..."
        url="file://$CLASH_CONFIG_RAW"
    }

    [ "$is_auto" = true ] && {
        sudo grep -qs 'clashupdate' "$CLASH_CRON_TAB" || echo "0 0 */2 * * $_SHELL -i -c 'clashupdate $url'" | sudo tee -a "$CLASH_CRON_TAB" >&/dev/null
        _okcat "set auto update" && return 0
    }

    _okcat '👌' "downloding：old config have backup..."
    sudo cat "$CLASH_CONFIG_RAW" | sudo tee "$CLASH_CONFIG_RAW_BAK" >&/dev/null

    _rollback() {
        _failcat '🍂' "$1"
        sudo cat "$CLASH_CONFIG_RAW_BAK" | sudo tee "$CLASH_CONFIG_RAW" >&/dev/null
        _failcat '❌' "[$(date +"%Y-%m-%d %H:%M:%S")] subscribe updat e fail：$url" 2>&1 | sudo tee -a "${CLASH_UPDATE_LOG}" >&/dev/null
        _error_quit
    }

    _download_config "$CLASH_CONFIG_RAW" "$url" || _rollback "download error：rollup"
    _valid_config "$CLASH_CONFIG_RAW" || _rollback "convert error：rolup，change log：$BIN_SUBCONVERTER_LOG"

    _merge_config_restart && _okcat '🍃' 'subscribe update success'
    echo "$url" | sudo tee "$CLASH_CONFIG_URL" >&/dev/null
    _okcat '✅' "[$(date +"%Y-%m-%d %H:%M:%S")] subscribe update success：$url" | sudo tee -a "${CLASH_UPDATE_LOG}" >&/dev/null
}

function clashmixin() {
    case "$1" in
    -e)
        sudo vim "$CLASH_CONFIG_MIXIN" && {
            _merge_config_restart && _okcat "update config"
        }
        ;;
    -r)
        less -f "$CLASH_CONFIG_RUNTIME"
        ;;
    *)
        less -f "$CLASH_CONFIG_MIXIN"
        ;;
    esac
}

function clashctl() {
    case "$1" in
    on)
        clashon
        ;;
    off)
        clashoff
        ;;
    ui)
        clashui
        ;;
    status)
        shift
        clashstatus "$@"
        ;;

    tun)
        shift
        clashtun "$@"
        ;;
    mixin)
        shift
        clashmixin "$@"
        ;;
    secret)
        shift
        clashsecret "$@"
        ;;
    update)
        shift
        clashupdate "$@"
        ;;
    *)
        cat <<EOF

Usage:
    clash      COMMAND  [OPTION]
    mihomo     COMMAND  [OPTION]
    clashctl   COMMAND  [OPTION]
    mihomoctl  COMMAND  [OPTION】

Commands:
    on                   start proxy
    off                  close proxy
    ui                   board address
    status               kernel status
    tun      [on|off]    Tun mode
    mixin    [-e|-r]     Mixin config
    secret   [SECRET]    Web secret
    update   [auto|log]  update subscribe

EOF
        ;;
    esac
}

function mihomoctl() {
    clashctl "$@"
}

function clash() {
    clashctl "$@"
}

function mihomo() {
    clashctl "$@"
}
