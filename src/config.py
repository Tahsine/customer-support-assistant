from prompts import CONCIERGE_PROMPT, SALE_EXPERT_PROMPT, CLAIMS_MANAGER_PROMPT
from workflow_tools import transfer_to_sales, transfer_to_claims


STEP_CONFIG = {
    "concierge": {
        "prompt": CONCIERGE_PROMPT,
        "tools": [transfer_to_sales, transfer_to_claims],
        "requires": [], # Pas de données préalables requises
    },
    "concierge": {
        "prompt": SALE_EXPERT_PROMPT,
        "tools": [transfer_to_claims], # Peut rediriger vers les sinistres si besoin
        "requires": ["policy_type"], # Nécessite de savoir quel type d'assurance
    },
    "concierge": {
        "prompt": CLAIMS_MANAGER_PROMPT,
        "tools": [transfer_to_sales], # Peut rediriger vers les ventes après un sinistre
        "requires": [],
    },
}

### NOTE
"""
Gestion de la charge cognitive (Context Management) : Si tu donnais tous les outils et toutes les instructions à un seul agent, il pourrait s'embrouiller (halluciner un processus de vente alors qu'on parle d'un accident). Ici, chaque expert a un périmètre étanche.

Le champ requires : C'est ta sécurité. Si le système essaie d'envoyer un utilisateur vers sales_expert mais que la variable policy_type est vide, LangGraph pourra lever une alerte ou forcer le Concierge à poser la question d'abord. C'est ce qui rend ton workflow robuste.

Multimodalité prête pour la V1 : Comme tu utilises google-genai, l'expert claims_manager peut déjà analyser une photo de voiture accidentée envoyée par l'utilisateur. Le prompt lui indique explicitement qu'il peut le faire.

Évolutivité Business : Demain, tu veux ajouter un agent "Juridique" ? Tu crées un LEGAL_PROMPT, tu l'ajoutes dans STEP_CONFIG, et tu donnes l'outil de transfert au Concierge. Ton code backend ne change presque pas, tu ne fais qu'ajouter des briques.
"""