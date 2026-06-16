# scraper.py
from playwright.sync_api import Page, BrowserContext

class LiteratureScraper:
    def __init__(self, context: BrowserContext, page: Page):
        self.context = context
        self.page = page
        self.scopus_logged_in = False

    def extract_rayyan_data(self) -> tuple[str, str]:
        """Extrai o texto visível no painel do Rayyan e tenta capturar a URL do Scopus."""
        sections = self.page.locator('[data-testid="abstract-body-section"]')
        rayyan_text = ""
        scopus_url = ""

        for j in range(sections.count()):
            rayyan_text += sections.nth(j).inner_text() + "\n"
            
            # Busca links do Scopus na seção
            links = sections.nth(j).locator('a')
            for k in range(links.count()):
                href = links.nth(k).get_attribute('href')
                if href and "scopus.com" in href:
                    scopus_url = href
                    break
        
        return rayyan_text, scopus_url

    def extract_scopus_data(self, scopus_url: str) -> str:
        """Abre uma nova aba, lida com o login se necessário e puxa o texto do Scopus."""
        print(f"-> Abrindo Scopus para extração: {scopus_url}")
        scopus_page = self.context.new_page()
        scopus_text = ""
        
        try:
            # Carrega a estrutura inicial da página
            scopus_page.goto(scopus_url, timeout=20000, wait_until="domcontentloaded")
            
            if not self.scopus_logged_in:
                print("\n" + "="*70)
                print("[AÇÃO OBRIGATÓRIA - PRIMEIRA VEZ]")
                print("Por favor, faça o login institucional no Scopus para liberar os resumos.")
                print("="*70)
                input("Após logar e a página carregar o artigo completamente, aperte ENTER aqui: ")
                self.scopus_logged_in = True

            # Pequeno delay estratégico para o JavaScript injetar os dados dinâmicos na tela
            scopus_page.wait_for_timeout(3000)
            scopus_text = scopus_page.locator("body").inner_text()
            print("   [Sucesso] Texto completo do Scopus integrado!")
            
        except Exception:
            print("   [Aviso] Scopus demorou para responder. Usando dados do Rayyan para este artigo.")
        finally:
            scopus_page.close()

        return scopus_text