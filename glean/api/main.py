"""
Main API entry points
"""

import sys
import csv
import copy
import numpy as np

from glean.api import bundles, results, weights, weights_vcv, configs


def single(argv, config):
    configs.handle_multiimpact_vcv(config)
    columns, basenames, transforms, vectransforms = configs.interpret_filenames(
        argv, config
    )

    data = {}  # {region => { year => value }}

    for ii in range(len(basenames)):
        for region, years, values in bundles.iterate_regions(
            basenames[ii], columns[ii], config
        ):
            if region not in data:
                data[region] = {}
            for year, value in bundles.iterate_values(years, values, config):
                if region == "all":
                    value = vectransforms[ii](value)
                else:
                    value = transforms[ii](value)

                if year not in data[region]:
                    data[region][year] = value
                else:
                    data[region][year] += value

    writer = csv.writer(sys.stdout)
    writer.writerow(["region", "year", "value"])

    for region in data:
        if region == "all":
            for rr in range(len(config["regionorder"])):
                for year in data[region]:
                    if bundles.deltamethod_vcv is not None:
                        value = bundles.deltamethod_vcv.dot(
                            data[region][year][:, rr]
                        ).dot(data[region][year][:, rr])
                    else:
                        value = data[region][year][rr]
                    writer.writerow([config["regionorder"][rr], year, value])
        else:
            for year in data[region]:
                if bundles.deltamethod_vcv is not None:
                    value = bundles.deltamethod_vcv.dot(data[region][year]).dot(
                        data[region][year]
                    )
                else:
                    value = data[region][year][rr]
                writer.writerow([region, year, value])


def quantiles(argv, config):
    configs.handle_multiimpact_vcv(config)

    do_gcmweights = config.get("do-gcmweights", True)
    evalqvals = config.get("evalqvals", ["mean", 0.17, 0.5, 0.83])
    output_format = config.get("output-format", "edfcsv")

    columns, basenames, transforms, vectransforms = configs.interpret_filenames(
        argv, config
    )

    # Collect all available results
    data, years = results.sum_into_data(
        config["results-root"], basenames, columns, config, transforms, vectransforms
    )
    if configs.is_parallel_deltamethod(config):
        # corresponds to each value in data, if doing parallel deltamethod
        config2 = copy.copy(config)
        config2["deltamethod"] = True
        parallel_deltamethod_data, parallel_deltamethod_years = results.sum_into_data(
            config["deltamethod"],
            basenames,
            columns,
            config2,
            transforms,
            vectransforms,
        )

    for filestuff in data:
        print("Creating file: " + str(filestuff))

        if (
            configs.is_parallel_deltamethod(config)
            and filestuff not in parallel_deltamethod_data
        ):
            print(
                str(filestuff)
                + " is not in delta method output. Skipping model specification..."
            )
            continue

        with open(configs.csv_makepath(filestuff, config), "w") as fp:
            writer = csv.writer(fp, quoting=csv.QUOTE_MINIMAL)
            rownames = configs.csv_rownames(config)

            if output_format == "edfcsv":
                writer.writerow(
                    rownames
                    + [
                        q if isinstance(q, str) else "q" + str(int(q * 100))
                        for q in evalqvals
                    ]
                )
                if configs.is_parallel_deltamethod(config):
                    encoded_evalqvals = weights_vcv.WeightedGMCDF.encode_evalqvals(
                        evalqvals
                    )
                else:
                    encoded_evalqvals = weights.WeightedECDF.encode_evalqvals(evalqvals)
            elif output_format == "valuescsv":
                writer.writerow(rownames + ["batch", "gcm", "iam", "value", "weight"])

            for rowstuff in configs.csv_sorted(list(data[filestuff].keys()), config):
                print("Outputing row: " + str(rowstuff))
                if do_gcmweights:
                    model_weights = weights.get_weights(
                        configs.csv_organized_rcp(filestuff, rowstuff, config)
                    )

                allvalues = []
                allvariances = []  # only used for parallel deltamethod
                allweights = []
                allmontevales = []

                for batch, gcm, iam in data[filestuff][rowstuff]:
                    value = data[filestuff][rowstuff][(batch, gcm, iam)]
                    if config.get("deltamethod", False):
                        value = results.deltamethod_variance(value, config)

                    if do_gcmweights:
                        try:
                            weight = model_weights[gcm.lower()]
                        except Exception as ex:
                            import traceback  # CATBELL

                            print(
                                "".join(
                                    traceback.format_exception(
                                        ex.__class__, ex, ex.__traceback__
                                    )
                                )
                            )  # CATBELL
                            print(
                                "Warning: No weight available for %s, so dropping."
                                % gcm
                            )
                            weight = 0.0
                    else:
                        weight = 1.0

                    allvalues.append(value)
                    allweights.append(weight)
                    allmontevales.append([batch, gcm, iam])

                    if configs.is_parallel_deltamethod(config):
                        allvariances.append(
                            results.deltamethod_variance(
                                parallel_deltamethod_data[filestuff][rowstuff][
                                    (batch, gcm, iam)
                                ],
                                config,
                            )
                        )

                # print filestuff, rowstuff, allvalues
                if len(allvalues) == 0:
                    continue

                if output_format == "edfcsv":
                    if configs.is_allregions(config):
                        assert "all" in rowstuff
                        allvalues = np.array(allvalues)
                        if configs.is_parallel_deltamethod(config):
                            allvariances = np.array(allvariances)
                        for ii in range(allvalues.shape[1]):
                            if configs.is_parallel_deltamethod(config):
                                distribution = weights_vcv.WeightedGMCDF(
                                    allvalues[:, ii], allvariances[:, ii], allweights
                                )
                            else:
                                distribution = weights.WeightedECDF(
                                    allvalues[:, ii],
                                    allweights,
                                    ignore_missing=config.get("ignore-missing", False),
                                )
                            myrowstuff = list(rowstuff)
                            myrowstuff[rownames.index("region")] = config[
                                "regionorder"
                            ][ii]
                            writer.writerow(
                                myrowstuff
                                + list(distribution.inverse(encoded_evalqvals))
                            )
                    else:
                        if configs.is_parallel_deltamethod(config):
                            distribution = weights_vcv.WeightedGMCDF(
                                allvalues, allvariances, allweights
                            )
                        else:
                            distribution = weights.WeightedECDF(
                                allvalues,
                                allweights,
                                ignore_missing=config.get("ignore-missing", False),
                            )

                        writer.writerow(
                            list(rowstuff)
                            + list(distribution.inverse(encoded_evalqvals))
                        )
                elif output_format == "valuescsv":
                    for ii in range(len(allvalues)):
                        if isinstance(allvalues[ii], list) or isinstance(
                            allvalues[ii], np.ndarray
                        ):
                            if "region" in config.get(
                                "file-organize", []
                            ) and "year" not in config.get("file-organize", []):
                                for jj in range(min(len(allvalues[ii]), len(years))):
                                    row = (
                                        list(rowstuff)
                                        + allmontevales[ii]
                                        + [allvalues[ii][jj], allweights[ii]]
                                    )
                                    row[rownames.index("year")] = years[
                                        jj
                                    ]  # still set from before
                                    writer.writerow(row)
                                continue

                            for jj in range(len(allvalues[ii])):
                                myrowstuff = list(rowstuff)
                                myrowstuff[rownames.index("region")] = config[
                                    "regionorder"
                                ][jj]
                                writer.writerow(
                                    myrowstuff
                                    + allmontevales[ii]
                                    + [allvalues[ii][jj], allweights[ii]]
                                )
                        else:
                            writer.writerow(
                                list(rowstuff)
                                + allmontevales[ii]
                                + [allvalues[ii], allweights[ii]]
                            )
