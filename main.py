from playwright.sync_api import sync_playwright
from classifier import classify
import csv
import time

MAX_ARTICLES = 10


def save_result(rows):
    with open(
        "resultados.csv",
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "title",
                "decision",
                "score",
                "findings"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context()

    page = context.new_page()

    page.goto("https://rayyan.ai")

    input(
        "Faça login no Rayyan e abra a tela Screening. Pressione ENTER."
    )

    page.wait_for_selector(
        '[data-testid="result-item-base"]'
    )

    articles = page.locator(
        '[data-testid="result-item-base"]'
    )

    print(
        "Quantidade:",
        articles.count()
    )

    total = min(
        MAX_ARTICLES,
        articles.count()
    )

    rows = []

    for index in range(total):

        article = articles.nth(index)

        title = article.locator(
            '[data-testid="result-item-title"]'
        ).inner_text()

        scopus_url = article.get_attribute("url")

        print("\n" + "=" * 80)
        print(f"ARTIGO {index + 1}")
        print(title)

        text_to_analyze = title

        if scopus_url:

            scopus = context.new_page()

            try:

                scopus.goto(
                    scopus_url,
                    wait_until="domcontentloaded",
                    timeout=30000
                )

                time.sleep(3)

                body_text = scopus.locator("body").inner_text()

                text_to_analyze += "\n\n" + body_text

            except Exception as e:
                print(f"Erro Scopus: {e}")

            finally:
                scopus.close()

        result = classify(text_to_analyze)

        print(f"\nSugestão: {result['decision']}")
        print(f"Score: {result['score']}")
        print("Critérios encontrados:")

        for item in result["findings"]:
            print(f"  - {item}")

        decision = input(
            "\n[I]nclude | [E]xclude | [S]kip : "
        ).strip().upper()

        rows.append({
            "title": title,
            "decision": decision,
            "score": result["score"],
            "findings": "; ".join(result["findings"])
        })

    save_result(rows)

    print("\nResultados salvos em resultados.csv")

    browser.close()