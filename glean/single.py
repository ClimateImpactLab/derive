"""
Usage: `python single.py OPTIONS FILEPATH

Supported configuration options:
- config (default: none): read the options from a config file
- column (default: `rebased`)
- yearsets (default: `no`)
- year or years (default: `null`)
- region or regions (default: `null`)
"""

if __name__ == "__main__":
    from glean.api import single
    from glean.api.configs import consume_config

    config, argv = consume_config()
    single(argv, config)