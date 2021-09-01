#!/usr/bin/env python3
import os
import json
import singer
from singer.catalog import Catalog
import tap_gcs_csv

REQUIRED_CONFIG_KEYS = ["start_date", "credentials_path", "bucket"]
LOGGER = singer.get_logger()

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

STREAMS = {
    "reviews": {
      "pattern": "reviews/reviews_.*_([0-9]+)\\.csv",
      "search_prefix": "reviews",
      "format": "csv",
      "encoding": "utf-16", # Google seems to arbitrarily switch between utf-8 and utf-16
    },
    "subscription_financial_stats_by_country": {
      "pattern": "financial-stats/subscriptions/subscriptions_.*_country\\.csv",
      "search_prefix": "financial-stats/subscriptions",
      "format": "csv",
      "encoding": "utf-16",
    },
    "subscription_cancellations": {
      "pattern": "subscriptions/cancellations/freeform.*\\.csv",
      "search_prefix": "subscriptions/cancellations",
      "format": "csv",
      "encoding": "utf-8",
      "compression": "zip" # This is actually a zip file, even though the filename is .csv
   },
   "sales": {
      "pattern": "sales/salesreport_([0-9]+)\\.zip",
      "search_prefix": "sales",
      "format": "csv",
      "encoding": "utf-8",
      "compression": "zip",
      "schema_overrides": {
        # these number fields have commas in them, and float("1,000.00") does not work.
        "item_price": {
            "type": ["null", "string"],
            "_conversion_type": "string"
         },
        "taxes_collected": {
            "type": ["null", "string"],
            "_conversion_type": "string"
         },
        "charged_amount": {
            "type": ["null", "string"],
            "_conversion_type": "string"
         }
      }
   },
   "earnings": {
      "pattern": "earnings/earnings_.*\\.zip",
      "search_prefix": "earnings",
      "format": "csv",
      "encoding": "utf-8",
      "compression": "zip",
      "schema_overrides": {
        # force post code to be treated as a string instead of an integer
        "buyer_postal_code": {
            "type": ["null", "string"],
            "_conversion_type": "string"
         }
      }
   }
}
DIMENSION_FIELDS = {
    "acquisition": {
        "buyers_7d": ["channel", "country", "play_country"],
        "subscribers": ["channel", "country", "play_country"],
        "retained_installers": ["channel", "country", "play_country"],
    },
    "stats": {
        "crashes": ["app_version", "device", "os_version", "overview"],
        "gcm": ["app_version", "carrier", "country", "device", "language", "message_status", "os_version", "overview", "response_code"],
        "installs": ["app_version", "carrier", "country", "device", "language", "os_version", "overview"],
        "ratings": ["app_version", "carrier", "country", "device", "language", "os_version", "overview"],
        "store_performance": ["country", "traffic_source"],
    }
}
for category, streams in DIMENSION_FIELDS.items():
    for stream, dimensions in streams.items():
        for dimension in dimensions:
            STREAMS["{}_{}_by_{}".format(stream, category, dimension)] = {
                "pattern": "{}/{}/{}_.*_{}\\.csv".format(
                    category, stream, stream, dimension
                ),
              "search_prefix": "{}/{}/{}_".format(category, stream, stream),
              "format": "csv",
              "encoding": "utf-16"
            }

def discover(cached=True):
    # return the cached catalog
    if cached:
        return Catalog.load(get_abs_path('cached_catalog.json'))
    # This generates the catalog using tap-gcs-csv sampling
    # and caches it to the tap.
    config = args.config
    config['tables'] = []
    for stream_id, table_spec in STREAMS.items():
        table_spec["name"] = stream_id
        table_spec["key_properties"] = [
            '_gcs_source_bucket',
            '_gcs_source_file',
            '_gcs_source_lineno',
        ]
        config['tables'].append(table_spec)
    config['sample_rate'] = 1
    config['max_files'] = 50
    return tap_gcs_csv.discover(config)


def main():
    # Parse command line arguments
    args = singer.utils.parse_args(REQUIRED_CONFIG_KEYS)

    cached_catalog = args.config.get('cached_catalog', True)
    if args.discover:
        catalog = discover(cached_catalog)
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover(cached_catalog)

        tap_gcs_csv.do_sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
