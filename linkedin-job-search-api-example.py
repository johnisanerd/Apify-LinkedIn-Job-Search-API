"""
LinkedIn Job Search API: A Quick Start Example
See more at: https://apify.com/johnvc/linkedin-job-search-scraper?fpr=9n7kx3
Input schema: https://apify.com/johnvc/linkedin-job-search-scraper/input-schema?fpr=9n7kx3

This script shows how to call the LinkedIn Job Search API on Apify from Python and
read its structured JSON output. It is a no-login LinkedIn job scraper: it reads
LinkedIn's public guest pages, so no cookie, session, or account is involved.

The default run is a near-zero-cost autocomplete call. The --example recipes mirror
published Store tasks (see the README Recipes section) and keep their cost knobs
clamped so a first run stays inexpensive.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3

Examples:
  uv run python linkedin-job-search-api-example.py
  uv run python linkedin-job-search-api-example.py --example default
  uv run python linkedin-job-search-api-example.py --example search-without-account
  uv run python linkedin-job-search-api-example.py --example company-id-lookup
  uv run python linkedin-job-search-api-example.py --example under-10-applicants
"""

from __future__ import annotations

import argparse
import os
from typing import Any

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

ACTOR_ID = "johnvc/linkedin-job-search-scraper"


def _print_items(items: list[dict[str, Any]]) -> None:
    """Print a short, readable summary of dataset rows.

    Each row carries a ``resultType``: a free ``searchMeta`` count row, a billed
    ``jobListing`` or full ``job`` record, a ``suggestion`` from a typeahead mode,
    or a free ``error`` row. We print a few key fields per type.

    Args:
        items: Rows returned from the Actor's default dataset.
    """
    print(f"Returned {len(items)} row(s).\n")
    for item in items:
        result_type = item.get("resultType")
        if result_type == "searchMeta":
            print(
                "[searchMeta] "
                f"{item.get('resultsCountCaption')} "
                f"(parsed={item.get('resultsCountParsed')}, "
                f"capped={item.get('resultsCountIsCapped')})"
            )
        elif result_type == "jobListing":
            print(
                "[jobListing] "
                f"{item.get('jobTitle')} at {item.get('companyName')} "
                f"({item.get('location')}) posted {item.get('postedDate')} "
                f"-> {item.get('jobUrl')}"
            )
        elif result_type == "job":
            print(
                "[job] "
                f"{item.get('title')} at {item.get('companyName')} "
                f"({item.get('location')}); seniority={item.get('seniorityLevel')}; "
                f"type={item.get('employmentType')}; salary={item.get('salaryText')}; "
                f"applicants={item.get('numApplicantsText')}"
            )
        elif result_type == "suggestion":
            print(
                "[suggestion] "
                f"{item.get('suggestionType')}: {item.get('displayName')} "
                f"(id={item.get('suggestionId')})"
            )
        elif result_type == "error":
            print(
                "[error] "
                f"{item.get('errorCode')}: {item.get('errorMessage')} "
                f"({item.get('sourceUrl')})"
            )
        else:
            print(item)


def _run(client: ApifyClient, run_input: dict[str, Any]) -> None:
    """Call the Actor with an input and print a summary of the rows it returns.

    Args:
        client: An authenticated Apify client.
        run_input: The Actor input for this run.
    """
    run = client.actor(ACTOR_ID).call(run_input=run_input)
    if run is None:
        raise SystemExit("The Actor run did not return a result.")
    items = list(client.dataset(run.default_dataset_id).iterate_items())
    _print_items(items)


def run_default(client: ApifyClient) -> None:
    """Cheap general quick-start: a job-title autocomplete lookup.

    Autocomplete rows are the cheapest thing this Actor returns, so this default
    run costs almost nothing while still exercising a real mode end to end.
    """
    # Inputs are kept tiny (autocomplete, maxItems=5) to keep this first run
    # near free. Raise these once you have your own API key and know your budget.
    run_input: dict[str, Any] = {
        "search_mode": "autocomplete",
        "query": "soft",
        "maxItems": 5,
    }
    _run(client, run_input)


def run_search_without_account(client: ApifyClient) -> None:
    """Mirrors Store task: Search LinkedIn Jobs Without an Account or Login.

    https://apify.com/johnvc/linkedin-job-search-scraper/examples/search-linkedin-jobs-without-an-account?fpr=9n7kx3

    Reads LinkedIn's public guest pages, so no login or cookie is used. Returns a
    free searchMeta count row plus job listings.
    """
    # Same shape as the published task, but maxItems is clamped to 10 to keep the
    # first run cheap. Raise maxItems (up to 1000) once you know your budget.
    run_input: dict[str, Any] = {
        "search_mode": "search",
        "keywords": "software engineer",
        "location": "United States",
        "datePosted": "pastWeek",
        "maxItems": 10,
    }
    _run(client, run_input)


def run_company_id_lookup(client: ApifyClient) -> None:
    """Mirrors Store task: Look Up LinkedIn Company IDs for Job Filters.

    https://apify.com/johnvc/linkedin-job-search-scraper/examples/look-up-linkedin-company-ids-for-job-filters?fpr=9n7kx3

    A LinkedIn company id finder: type a company name and read suggestionId and
    displayName, the numeric ids the companyIds filter needs.
    """
    # Suggestion rows are inexpensive; maxItems stays small.
    run_input: dict[str, Any] = {
        "search_mode": "companySuggestions",
        "query": "applied materials",
        "maxItems": 5,
    }
    _run(client, run_input)


def run_under_10_applicants(client: ApifyClient) -> None:
    """Mirrors Store task: Find LinkedIn Jobs With Under 10 Applicants.

    https://apify.com/johnvc/linkedin-job-search-scraper/examples/find-linkedin-jobs-with-under-10-applicants?fpr=9n7kx3

    Surfaces fresh, low-competition postings by filtering to jobs with fewer than
    10 applicants so far, applied at the source before billing.
    """
    # Same shape as the published task, with maxItems clamped to 10 for a cheap run.
    run_input: dict[str, Any] = {
        "search_mode": "search",
        "keywords": "data engineer",
        "location": "United States",
        "under10Applicants": True,
        "datePosted": "pastWeek",
        "maxItems": 10,
    }
    _run(client, run_input)


def main() -> None:
    """Dispatch a quick-start or task-aligned recipe."""
    parser = argparse.ArgumentParser(description="LinkedIn Job Search API examples")
    parser.add_argument(
        "--example",
        default="default",
        choices=[
            "default",
            "search-without-account",
            "company-id-lookup",
            "under-10-applicants",
        ],
        help="Which recipe to run (see the README Recipes section).",
    )
    args = parser.parse_args()

    token = os.getenv("APIFY_TOKEN")
    if not token:
        raise SystemExit("Set APIFY_TOKEN in .env or the environment.")

    client = ApifyClient(token)
    dispatch = {
        "default": run_default,
        "search-without-account": run_search_without_account,
        "company-id-lookup": run_company_id_lookup,
        "under-10-applicants": run_under_10_applicants,
    }
    dispatch[args.example](client)


if __name__ == "__main__":
    main()
