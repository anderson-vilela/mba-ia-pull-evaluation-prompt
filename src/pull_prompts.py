"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub (leonanluppi/bug_to_user_story_v1)
3. Salva localmente em prompts/bug_to_user_story_v1.yml
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith() -> bool:
    """
    Faz pull do prompt do LangSmith Prompt Hub e salva em arquivo YAML local.

    Returns:
        bool: True se sucesso, False caso contrário
    """
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_file = "prompts/bug_to_user_story_v1.yml"

    print(f"Puxando prompt do LangSmith Hub: {prompt_name}...")

    try:
        # Puxa o prompt do Hub
        prompt_template = hub.pull(prompt_name)
        print("   ✓ Prompt carregado com sucesso do Hub")

        system_prompt = ""
        user_prompt = "{bug_report}"

        # Extrair mensagens do ChatPromptTemplate
        if hasattr(prompt_template, "messages"):
            for msg in prompt_template.messages:
                content = getattr(msg, "prompt", msg).template if hasattr(getattr(msg, "prompt", msg), "template") else str(msg)
                msg_class = msg.__class__.__name__.lower()

                if "system" in msg_class:
                    system_prompt = content
                elif "human" in msg_class or "user" in msg_class:
                    user_prompt = content

        # Fallback caso não seja ChatPromptTemplate
        if not system_prompt and hasattr(prompt_template, "template"):
            system_prompt = prompt_template.template

        # Montar a estrutura do YAML
        prompt_data = {
            "bug_to_user_story_v1": {
                "description": "Prompt para converter relatos de bugs em User Stories",
                "system_prompt": system_prompt.strip(),
                "user_prompt": user_prompt.strip(),
                "version": "v1",
                "created_at": "2025-01-15",
                "tags": ["bug-analysis", "user-story", "product-management"]
            }
        }

        # Salvar em arquivo YAML
        success = save_yaml(prompt_data, output_file)
        if success:
            print(f"   ✓ Prompt salvo localmente em: {output_file}")
            return True
        else:
            print(f"   ❌ Erro ao salvar arquivo: {output_file}")
            return False

    except Exception as e:
        print(f"   ❌ Erro ao fazer pull de '{prompt_name}': {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH HUB")

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        return 1

    success = pull_prompts_from_langsmith()

    if success:
        print("\n✅ Processo de pull concluído com sucesso!")
        return 0
    else:
        print("\n❌ Falha no processo de pull.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
