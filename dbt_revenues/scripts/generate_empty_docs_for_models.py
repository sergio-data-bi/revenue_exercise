from pathlib import Path

def main():
    dbt_path = Path(__file__).parent.parent
    models_path = dbt_path / "models"
    docs_path = dbt_path / "docs"
    docs_path.mkdir(exist_ok=True)

    for file in models_path.rglob('*.sql'):
        doc_file = docs_path / f"{file.stem}.md"
        if not doc_file.exists():
            doc_file.write_text(f"{{% docs {file.stem} %}}\n\n{{% enddocs %}}")

if __name__ == "__main__":
    main()
