install:
  cd client && bun install
  cargo update
  echo "Skipping venv creation"

  uv pip install .

  uvx maturin develop
  
build:
  uvx maturin develop


api-key-gen:
  lighthouse-web3 api-key -n