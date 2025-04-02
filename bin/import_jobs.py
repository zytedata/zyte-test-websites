#!/usr/bin/python3

"""
Imports the CSV data from https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset/data (license: CC0)
into the format suitable for zyte_test_websites/jobs/data.json.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path

from zyte_test_websites.jobs.models import Job, JobCategory


def import_jobs(
    reader: csv.DictReader, count: int | None = None
) -> tuple[list[Job], list[JobCategory]]:
    jobs: list[Job] = []
    categories: dict[str, JobCategory] = {}
    category_id = 1
    job_count = 0
    for row in reader:
        try:
            company_profile = json.loads(row["Company Profile"])
        except json.decoder.JSONDecodeError:
            continue
        category_name = company_profile["Sector"]
        if category_name not in categories:
            categories[category_name] = JobCategory(category_id, category_name, {})
            category_id += 1
        jobs.append(
            Job(
                category=categories[category_name],
                id=int(row["Job Id"]),
                title=row["Job Title"],
                date_published=datetime.fromisoformat(row["Job Posting Date"]),
                description=row["Job Description"],
                salary=row["Salary Range"],
                experience=row["Experience"],
                work_type=row["Work Type"],
                contact_name=row["Contact Person"],
                contact_phone=row["Contact"],
                benefits=row["Benefits"]
                .removeprefix("{'")
                .removesuffix("'}")
                .split(", "),
                responsibilities=row["Responsibilities"],
                company_name=row["Company"],
                location=f"{row['location'].encode('latin1').decode('utf-8')}, {row['Country']}",
            )
        )
        job_count += 1
        if count and job_count >= count:
            break
    return jobs, list(categories.values())


def main() -> None:
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    count = int(sys.argv[3])

    with Path(input_file).open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        jobs, categories = import_jobs(reader, count)

    data = {
        "categories": [category.to_dict() for category in categories],
        "jobs": [job.to_dict() for job in jobs],
    }
    Path(output_file).write_text(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
