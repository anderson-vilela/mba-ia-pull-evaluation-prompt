"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure


def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


class TestPrompts:
    @pytest.fixture(autouse=True)
    def setup(self):
        """Carrega os dados de prompts/bug_to_user_story_v2.yml para todos os testes."""
        yaml_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
        assert yaml_path.exists(), f"Arquivo não encontrado: {yaml_path}"
        data = load_prompts(str(yaml_path))
        assert "bug_to_user_story_v2" in data, "Chave 'bug_to_user_story_v2' não encontrada no YAML"
        self.prompt_data = data["bug_to_user_story_v2"]

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt_data, "Campo 'system_prompt' ausente"
        system_prompt = self.prompt_data["system_prompt"]
        assert isinstance(system_prompt, str), "system_prompt deve ser uma string"
        assert len(system_prompt.strip()) > 0, "system_prompt não pode estar vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: 'Você é um Product Manager')."""
        system_prompt = self.prompt_data.get("system_prompt", "").lower()
        has_role = any(role in system_prompt for role in [
            "product manager",
            "technical lead",
            "agile",
            "você é um",
            "persona"
        ])
        assert has_role, "O prompt não define uma persona adequada de Product Manager / Tech Lead"

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt_data.get("system_prompt", "").lower()
        has_user_story_template = "como um" in system_prompt and "eu quero" in system_prompt
        has_acceptance_criteria = "critérios de aceitação" in system_prompt or "dado que" in system_prompt
        assert has_user_story_template and has_acceptance_criteria, (
            "O prompt deve especificar o formato 'Como um... Eu quero... Para que...' "
            "e critérios de aceitação estruturados"
        )

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt_data.get("system_prompt", "").lower()
        has_few_shot = (
            "few-shot" in system_prompt
            or ("exemplo" in system_prompt and ("resposta:" in system_prompt or "saída:" in system_prompt))
        )
        assert has_few_shot, "O prompt deve conter exemplos de Few-shot (entrada e saída)"

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        full_text = yaml.dump(self.prompt_data)
        assert "TODO" not in full_text, "Foi encontrada a marcação 'TODO' no prompt"

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt_data.get("techniques_applied", [])
        assert isinstance(techniques, list), "'techniques_applied' deve ser uma lista"
        assert len(techniques) >= 2, (
            f"Devem ser listadas no mínimo 2 técnicas em techniques_applied, encontradas: {len(techniques)}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])