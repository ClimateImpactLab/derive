"""
Usage: `python quantiles.py CONFIG <->BASENAME<:column>...

Supported configuration options:
- column (default: `rebased`)
- yearsets (default: `no`)
- years (default: `null`)
- regions (default: `null`)
- results-root
- output-dir
- do-montecarlo
- only-rcp
- only-iam
- only-ssp
- only-models (default: `all`)
- deltamethod (default: `no`) -- otherwise, results root for deltamethod
- file-organize (default: rcp, ssp)
- do-gcmweights (default: true)
- evalqvals (default: ['mean', .17, .5, .83])
- ignore-missing (default: no)
"""

if __name__ == "__main__":
    import warnings
    from glean.api import quantiles
    from glean.api.configs import consume_config

    warnings.warn(
        "quantiles.py is deprecated, please use `glean quantiles`", FutureWarning
    )

    config, argv = consume_config()
    quantiles(argv, config)
