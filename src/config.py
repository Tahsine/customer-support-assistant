from prompts import CONCIERGE_PROMPT, SALE_EXPERT_PROMPT, CLAIMS_MANAGER_PROMPT
from workflow_tools import transfer_to_sales, transfer_to_claims, query_knwoledge_base, provide_final_solution, escalate_to_human


STEP_CONFIG = {
    "concierge": {
        "prompt": CONCIERGE_PROMPT,
        "tools": [query_knwoledge_base, transfer_to_sales, transfer_to_claims],
        "requires": [], # Pas de données préalables requises
    },
    "concierge": {
        "prompt": SALE_EXPERT_PROMPT,
        "tools": [query_knwoledge_base, provide_final_solution, transfer_to_claims], # Peut rediriger vers les sinistres si besoin
        "requires": ["policy_type"], # Nécessite de savoir quel type d'assurance
    },
    "concierge": {
        "prompt": CLAIMS_MANAGER_PROMPT,
        "tools": [query_knwoledge_base, escalate_to_human, transfer_to_sales], # Peut rediriger vers les ventes après un sinistre
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

### UPDATE NOTE
"""
C'est ici que l'on décide quel agent a le droit de faire quoi.

Le Concierge peut répondre aux questions générales (FAQ).

Le Claims Manager peut escalader vers un humain s'il y a un gros litige.

L'Agentic RAG (FAQ) : En mettant query_knowledge_base dans la liste des outils du Concierge, ton agent devient "agentique". S'il reçoit une question comme "Est-ce que vous couvrez les vélos électriques ?", il ne va pas transférer aveuglément. Il va d'abord appeler l'outil RAG, donner la réponse, puis demander : "Voulez-vous que je vous transfère à un expert pour souscrire ?". C'est ça, la valeur ajoutée.

L'Escalade Humaine : C'est ta sécurité business. Une IA qui boucle à l'infini énerve le client. L'outil escalate_to_human permet de déclencher une notification (via Convex ou un Webhook Slack) pour qu'un vrai conseiller reprenne la main sur le widget.

La Clôture (provide_final_solution) : Cela te permet de générer des statistiques : "Combien de conversations ont été résolues par l'IA sans intervention humaine ?". C'est l'argument numéro 1 que tu vendras à tes clients.
"""