#!/usr/bin/env python3
"""India tech recruiting feed, firmographics on every job. Python, Node.js and cURL clients for the Instahyre Jobs Scraper on Apify, pay per result.

Command-line client for the themineworks/instahyre-jobs-scraper actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/instahyre-jobs-scraper/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/instahyre-jobs-scraper"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--job-function-slugs", help="Comma-separated. Instahyre job-function slugs to filter by, for example 'backend-development'…")
    ap.add_argument("--job-type", help="Filter by employment type")
    ap.add_argument("--company-size", help="Filter by hiring company's size band")
    ap.add_argument("--max-jobs", type=int, help="Maximum jobs to return across all pages/functions")
    ap.add_argument("--monitor-mode", action=argparse.BooleanOptionalAction, help="When enabled, this and every subsequent scheduled run delivers ONLY jobs not seen in a…")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.job_function_slugs: run_input["jobFunctionSlugs"] = [s.strip() for s in a.job_function_slugs.split(",") if s.strip()]
    if a.job_type is not None: run_input["jobType"] = a.job_type
    if a.company_size is not None: run_input["companySize"] = a.company_size
    if a.max_jobs is not None: run_input["maxJobs"] = a.max_jobs
    if a.monitor_mode is not None: run_input["monitorMode"] = a.monitor_mode

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
