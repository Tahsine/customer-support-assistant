from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

from config import STEP_CONFIG

@wrap_model_call
def apply_step_config(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    """
    Configure dynamiquement le comportement de l'agent (SafeGuard)
    selon l'étape actuelle.
    """

    # 1. Récupérer l'étape actuelle (par défaut: concierge pour le premier message)
    current_step = request.state.get("current_step", "concierge")

    # 2. Récupérer la configuration correspondante dans notre STEP_CONFIG
    stage_config = STEP_CONFIG[current_step]

    # 3. Validation des dépendances (Sécurité métier)
    # On vérifie que les données requises (ex: policy_type) sont bien présentes
    for key in stage_config["requires"]:
        if request.state.get(key) is None:
            raise ValueError(
                f"Erreur critique: la donnée '{key}' est manquante pour l'étape '{current_step}'."
            )
    
    # 4. Formater le prompt système avec les variables du State
    # Cela permet d'injecter {policy_type} directement dans  SALE_EXPERT_PROMPT
    system_prompt = stage_config["prompt"].format(**request.state)

    # 5. APPLICATION DE LA CONFIGURATION (Le coeur du pattern).
    # On utilise request.override() pour changer l'identité de l'agent à la volée
    request = request.override(
        system_message=system_prompt,
        tools=stage_config["tools"]
    )

    # 6 On passe la requête modifiée au gestionnaire suivant
    return handler(request)

### NOTE
"""
L'Isolation par request.override() : C'est la méthode la plus propre. Au lieu de créer 3 agents différents (ce qui coûterait cher et serait dur à maintenir), tu as un seul agent Google GenAI qui change de masque à chaque tour. Si le state dit claims_manager, l'agent reçoit instantanément les instructions d'empathie et les outils de sinistres, sans même savoir qu'il était un vendeur 2 secondes avant.

Validation dynamique (requires) : Imagine que ton code tente d'envoyer l'utilisateur vers l'expert de vente sans savoir s'il veut une assurance Auto ou Santé. La boucle for key in stage_config["requires"] bloque l'exécution avant que le LLM ne fasse une erreur. C'est essentiel pour un business sérieux (Assurance).

Injection de Contexte (format(**request.state)) : C'est ici que tes prompts deviennent intelligents. Quand tu as écrit {policy_type} dans ton prompt, c'est ce middleware qui va le remplacer par "Auto" ou "Habitation" en lisant les données collectées précédemment.

Middleware vs Orchestration manuelle : En utilisant le décorateur @wrap_model_call, tu sépares la logique métier (le workflow) de la logique technique (l'appel API). Ton code principal reste propre et facile à tester.
"""