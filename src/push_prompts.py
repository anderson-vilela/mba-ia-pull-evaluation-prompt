"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt usando validate_prompt_structure.
    """
    return validate_prompt_structure(prompt_data)


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do repositório no Hub (ex: username/bug_to_user_story_v2)
        prompt_data: Dicionário com os dados do YAML
    """
    print(f"Enviando prompt ao LangSmith Hub: {prompt_name}...")

    try:
        # Construir o ChatPromptTemplate
        system_prompt = prompt_data.get("system_prompt", "")
        user_prompt = prompt_data.get("user_prompt", "{bug_report}")

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", user_prompt)
        ])

        # Metadados
        description = prompt_data.get("description", "Prompt otimizado para User Stories")
        tags = prompt_data.get("tags", ["bug-to-user-story", "v2"])

        # Fazer push público
        hub_url = hub.push(
            prompt_name,
            chat_prompt,
            new_repo_is_public=True,
            new_repo_description=description,
            tags=tags
        )

        print(f"   ✓ Push realizado com sucesso!")
        if hub_url:
            print(f"   ✓ URL no Hub: {hub_url}")
        return True

    except Exception as e:
        if "prompt has not changed" in str(e).lower() or "nothing to commit" in str(e).lower():
            print(f"   ✓ Prompt já está atualizado no Hub (sem alterações necessárias)!")
            return True
        print(f"   ❌ Erro ao fazer push de '{prompt_name}': {e}")
        return False


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS OTIMIZADOS AO LANGSMITH HUB")

    required_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(required_vars):
        return 1

    username = os.getenv("USERNAME_LANGSMITH_HUB", "").strip()
    yaml_path = "prompts/bug_to_user_story_v2.yml"

    data = load_yaml(yaml_path)
    if not data or "bug_to_user_story_v2" not in data:
        print(f"❌ Não foi possível carregar 'bug_to_user_story_v2' de {yaml_path}")
        return 1

    prompt_data = data["bug_to_user_story_v2"]

    # Validação prévia
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Validação falhou com os seguintes erros:")
        for err in errors:
            print(f"   - {err}")
        return 1

    print("✓ Prompt passou na validação de estrutura!")

    repo_full_name = f"{username}/bug_to_user_story_v2"
    success = push_prompt_to_langsmith(repo_full_name, prompt_data)

    if success:
        print("\n" + "=" * 60)
        print("✅ SUCESSO: Prompt publicado publicamente no LangSmith Hub!")
        print(f"Acesse: https://smith.langchain.com/hub/{repo_full_name}")
        print("=" * 60)
        return 0
    else:
        print("\n❌ Falha no envio do prompt.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
