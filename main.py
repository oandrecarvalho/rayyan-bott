# main.py
import os
import pandas as pd
from playwright.sync_api import sync_playwright

from config import RAYYAN_URL, CSV_FILENAME
from classifier import ArticleClassifier
from scraper import LiteratureScraper

def load_history() -> tuple[list, list]:
    if os.path.exists(CSV_FILENAME):
        df_history = pd.read_csv(CSV_FILENAME)
        return df_history['Título'].tolist(), df_history.to_dict('records')
    return [], []

def main():
    processed_titles, results = load_history()
    ALVO_TOTAL_REVISAO = 1059 

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, channel="chrome")
        context = browser.new_context()
        page = context.new_page()

        print("Iniciando o navegador e acessando o Rayyan...")
        page.goto(RAYYAN_URL)

        input("\n[AÇÃO] Faça o login no Rayyan, acesse o Screening, clique no PRIMEIRO artigo da lista e pressione ENTER aqui para iniciar o MODO AUTOMÁTICO...")

        scraper = LiteratureScraper(context, page)
        
        print(f"\n[INFO] Progresso atual: {len(processed_titles)}/{ALVO_TOTAL_REVISAO} artigos processados.")
        print("Iniciando triagem 100% automática...\n")

        while len(processed_titles) < ALVO_TOTAL_REVISAO:
            try:
                page.wait_for_selector('[data-testid="result-item-base"]', timeout=30000)
                articles = page.locator('[data-testid="result-item-base"]')
                
                current_article = None
                title = ""
                
                for idx in range(articles.count()):
                    temp_title = articles.nth(idx).locator('[data-testid="result-item-title"]').inner_text().strip()
                    if temp_title not in processed_titles:
                        current_article = articles.nth(idx)
                        title = temp_title
                        break
                
                if not current_article:
                    page.keyboard.press("ArrowDown")
                    page.wait_for_timeout(800)
                    continue

                print(f"\n[Processando {len(processed_titles) + 1}/{ALVO_TOTAL_REVISAO}]: {title[:60]}...")
                current_article.click()
                page.wait_for_timeout(1000) # Tempo para abrir a barra lateral

                # 1. Coleta dados das páginas
                rayyan_text, scopus_url = scraper.extract_rayyan_data()
                scopus_text = ""

                if scopus_url:
                    scopus_text = scraper.extract_scopus_data(scopus_url)

                # 2. Executa a classificação mecânica de palavras-chave
                texto_total = f"{title}\n{rayyan_text}\n{scopus_text}"
                final_decision, motivo, matches = ArticleClassifier.classify(texto_total)

                # 3. Executa o clique automático no Rayyan baseado na decisão do sistema
                print(f"   Decisão do Sistema: {final_decision}")
                if matches:
                    print(f"   Termos: {list(matches.keys())}")

                if final_decision == "INCLUDE":
                    # Localiza o botão 'Include' do Rayyan e clica
                    page.locator('[data-testid="decision-button"][aria-label="Include"]').click()
                else:
                    # Localiza o botão 'Exclude' do Rayyan e clica
                    page.locator('[data-testid="decision-button"][aria-label="Exclude"]').click()

                # 4. Salva o registro no CSV para o seu controle e auditoria posterior
                results.append({
                    "Título": title,
                    "Decisão": final_decision,
                    "Confiança": "100% Automático (Palavras-Chave)",
                    "Motivo": motivo,
                    "URL Scopus": scopus_url
                })
                processed_titles.append(title)

                pd.DataFrame(results).to_csv(CSV_FILENAME, index=False, encoding='utf-8-sig')
                
                # 5. Avança para o próximo artigo na tela
                page.keyboard.press("ArrowDown")
                page.wait_for_timeout(1000) # Pausa amigável para o Rayyan processar o clique antes do próximo

            except Exception as e:
                print(f"[Aviso] Erro no artigo atual: {e}. Pulando...")
                page.keyboard.press("ArrowDown")
                page.wait_for_timeout(1000)
                continue

        print("\nTriagem automática concluída com sucesso!")
        browser.close()

if __name__ == "__main__":
    main()