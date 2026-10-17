#!/usr/bin/env python3
"""Validate public fixtures and export a deterministic, static RELAY dataset."""
import sys
from relay_registry import PUBLIC, load_source, publication, validate_registry, validate_repository_sources, validate_publication_boundary


def main():
    try:
        data = load_source()
        errors = validate_registry(data)
        errors.extend(validate_publication_boundary(data))
        if not errors:
            errors.extend(validate_repository_sources(data))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print("FAIL:", error, file=sys.stderr)
        return 1
    PUBLIC.mkdir(parents=True, exist_ok=True)
    for name, raw in publication(data).items():
        (PUBLIC / name).write_bytes(raw)
    print(f"PASS: exported {len(data['cases'])} real public evidence cases and SHA-256 manifest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
