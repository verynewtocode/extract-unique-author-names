from __future__ import annotations

import argparse
import csv
import json

import psycopg

DEFAULT_POSTGRES_DSN = "postgresql://postgres:postgres@localhost:5433/ssc_course_project"


def fetch_authors(postgres_dsn: str) -> list[str]:
    query = """
SELECT COALESCE(metadata ->> 'author', metadata -> 'info' ->> 'author') AS author
FROM ssc.dim_package
WHERE (
    metadata ? 'author'
    AND metadata ->> 'author' IS NOT NULL
)
OR (
    metadata ? 'info'
    AND metadata -> 'info' ? 'author'
    AND metadata -> 'info' ->> 'author' IS NOT NULL
)
ORDER BY author
"""
    with psycopg.connect(postgres_dsn) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return [row[0] for row in cursor.fetchall() if row[0] is not None]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract only author values from ssc.dim_package metadata."
    )
    parser.add_argument(
        "--postgres-dsn",
        default=DEFAULT_POSTGRES_DSN,
        help="PostgreSQL DSN for the target database.",
    )
    parser.add_argument(
        "--unique",
        action="store_true",
        help="Print unique author values only.",
    )
    parser.add_argument(
        "--json-lines",
        action="store_true",
        help="Output each author as a JSON object with only the author field.",
    )
    parser.add_argument(
        "--csv-output",
        action="store_true",
        help="Write author values to unique_authors.csv instead of printing them.",
    )
    args = parser.parse_args()

    authors = fetch_authors(args.postgres_dsn)
    if args.unique:
        seen: set[str] = set()
        unique_authors = []
        for author in authors:
            if author not in seen:
                seen.add(author)
                unique_authors.append(author)
        authors = unique_authors

    if args.json_lines:
        for author in authors:
            print(json.dumps({"author": author}, ensure_ascii=False))
    elif args.csv_output:
        with open("unique_authors.csv", "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["author"])
            for author in authors:
                writer.writerow([author])
    else:
        for author in authors:
            print(author)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
