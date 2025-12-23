from __future__ import annotations

import argparse
from uniyoklama import create_app


def main() -> None:
    parser = argparse.ArgumentParser(description="UniYoklama backend")
    parser.add_argument("--config", default="config.cfg", help="Path to .cfg file")
    args = parser.parse_args()

    app = create_app(args.config)
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"], use_reloader=False)


if __name__ == "__main__":
    main()
