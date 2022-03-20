export JUST_PROJECT_ROOT="`pwd`";
export JUST_BACKEND_ROOT="$JUST_PROJECT_ROOT/server";

function just_format {
  autopep8 "$JUST_BACKEND_ROOT" && echo "Projected Linted!" || { echo "Failed to lint project!"; exit 1; }
}

function just_migrate {
  python3 "$JUST_BACKEND_ROOT/manage.py" migrate;
  python3 "$JUST_BACKEND_ROOT/manage.py" migrate remesh;
}

function just_run {
  python3 "$JUST_BACKEND_ROOT/manage.py" runserver;
}

function just_test {
  python3 "$JUST_BACKEND_ROOT/manage.py" test remesh;
}

function just_venv_create {
  python3 -m venv "$JUST_PROJECT_ROOT/.venv";
}

function just_venv_connect {
  . "$JUST_PROJECT_ROOT/.venv/bin/activate";
}

function just_venv_disconnect {
  deactivate;
}

function just_build_backend {
  pip3 install -e "$JUST_BACKEND_ROOT/setup.py";
}

function just_clean {
  rm -rf "$JUST_PROJECT_ROOT/.venv";
}

