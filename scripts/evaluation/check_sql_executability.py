"""
Check executability of SQL statements from a .jsonl file.
Each line in the input file should be a JSON object with at least:
- instance_id: unique identifier for the SQL case
- selected_database: database name to run against
- sol_sql: the SQL statement to test.
The output is a .jsonl file with execution results for each case.

Command to run:
uv run python evaluation/check_sql_executability.py --input "data/labelled_sets/labelled_set_processed.jsonl" --output "data/evaluation_dumps/labelled_set_executability.jsonl" --workers 6 --timeout 2
"""

import sys
import json
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from conversational_txt2sql.database_utils import execute_sql_query

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def test_row(row, timeout_seconds=None):
    """
    Execute sol_sql using execute_sql_query and return a result dict.
    timeout_seconds is handled by the caller (future.timeout) — this function shouldn't block forever.
    """
    instance_id = row.get("instance_id")
    db = row.get("selected_database")
    sql = row.get("sol_sql")
    out = {
        "instance_id": instance_id,
        "selected_database": db,
        "user_query": row.get("user_query"),
        "executable": False,
        "rows_returned": None,
        "first_row_preview": None,
        "error": None,
    }

    try:
        res = execute_sql_query(sql, db)
        # execute_sql_query returns list-of-records (or []), or a pandas DataFrame converted to records.
        if isinstance(res, list):
            out["rows_returned"] = res
            if res:
                # safe preview: include first row but ensure JSON-serializable
                out["first_row_preview"] = res[0]
            out["executable"] = True
        else:
            # handle unexpected return types
            try:
                # try to infer length for other iterables
                out["rows_returned"] = res  # may raise
                out["executable"] = True
            except Exception:
                out["rows_returned"] = None
                out["first_row_preview"] = str(type(res))
                out["executable"] = True
    except Exception as e:
        out["error"] = f"{type(e).__name__}: {e}"
        logger.exception("Execution failed for %s", instance_id)

    return out


def main(
    input_jsonl: str | Path = None,
    output_jsonl: str | Path = None,
    max_workers: int = 8,
    per_query_timeout: int = 30,
):
    input_path = Path(input_jsonl or ("data" / "labelled_sets" / "labelled_set_generated.jsonl"))
    output_path = Path(output_jsonl or ("data" / "labelled_sets" / "labelled_set_executability.jsonl"))

    logger.info("Reading SQL cases from %s", input_path)
    rows = list(load_jsonl(input_path))
    logger.info("Loaded %d SQL cases", len(rows))

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        futures = {exe.submit(test_row, r): r.get("instance_id") for r in rows}

        for fut in as_completed(futures):
            iid = futures[fut]
            try:
                # apply per-query timeout when retrieving result
                res = fut.result(timeout=per_query_timeout)
            except TimeoutError:
                logger.warning("Timeout executing %s", iid)
                res = {
                    "instance_id": iid,
                    "selected_database": None,
                    "user_query": None,
                    "executable": False,
                    "rows_returned": None,
                    "first_row_preview": None,
                    "error": f"Timeout after {per_query_timeout}s",
                }
            except Exception as e:
                logger.exception("Unhandled exception for %s", iid)
                res = {
                    "instance_id": iid,
                    "selected_database": None,
                    "user_query": None,
                    "executable": False,
                    "rows_returned": None,
                    "first_row_preview": None,
                    "error": f"{type(e).__name__}: {e}",
                }
            results.append(res)

    # write results as jsonl
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as fh:
        for r in results:
            fh.write(json.dumps(r, default=str) + "\n")

    logger.info("Wrote executability results to %s", output_path)
    return output_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Check executability of SQL statements from a .jsonl file.")
    parser.add_argument("--input", "-i", help="Path to input .jsonl (default: data/labelled_sets/labelled_set_generated.jsonl)")
    parser.add_argument("--output", "-o", help="Path to output .jsonl (default: data/labelled_sets/labelled_set_executability.jsonl)")
    parser.add_argument("--workers", "-w", type=int, default=8, help="Max parallel workers")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="Per-query timeout in seconds")

    args = parser.parse_args()
    main(input_jsonl=args.input, output_jsonl=args.output, max_workers=args.workers, per_query_timeout=args.timeout)