# tap-playstore

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md) for
[reports from the Google Play Store](https://support.google.com/googleplay/android-developer/answer/6135870).

It's a thin wrapper around [tap-gcs-csv](https://github.com/fixdauto/tap-gcs-csv/) that declares
all the tables for you, and avoids having to sample the data to determine the schema.

## Config

```javascript
{
  "start_date": "2015-01-01T00:00:00Z",
  // A path to a JSON credentials file for a service account. Make sure you give that
  // user permissions by inviting them to your Play Store account and giving them
  // "View app information and download bulk reports (read-only)" and
  // "View financial data, orders, and cancellation survey responses" permissions.
  // These permissions must be granted account-wide, not just for one app.
  // It can take a few hours before the grant takes effect.
  "credentials_path": "./client_secret.json",
  // The path to the bucket Google sends reports to. You can get this from the
  // "Copy Cloud Storage URI" button from the reports page.
  "bucket": "pubsite_prod_rev_01234567890123456789"
}
```
