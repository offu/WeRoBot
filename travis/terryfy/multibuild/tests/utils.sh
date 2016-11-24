# Test utilities
RET=${RET:-0}

function ingest {
    local msg="${1:-"no message"}"
    echo "Test failed: $msg"
    RET=1
}

function barf {
    [ "$RET" == 0 ] || exit 1
}
