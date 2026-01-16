from langchain.agents import AgentState
from typing_extensions import NotRequired
from typing import Literal

# 1. Définition des étapes (Steps) de notre worflow
# Chaque step correspond à une spécialisation métier identifiée sur le site.
# Le site actuelle de demo est sur une entreprise de d'assurance

InsuranceStep = Literal[
    "concierge",        # Acceuil, identification et routage
    "sales_expert",     # Expert "Nos Offres" (RAG sur les contracts)
    "claims_manager",   # Expert "Sinistres" (Processus de déclaration)
    "account_support"   # Support technique "Espace Client"
]

class InsuranceSupportState(AgentState):
    """
    L'objet State est la 'mémoire partagée' entre les agents.
    Il permet de stocker les informations extraites durant la conversation.
    """

    # LE CHAMP CLE: Détermine quel agent (config + outils) prend la main.
    current_step: NotRequired[InsuranceStep]

    # --- DONNEES METIER (Context Engineering) ---
    # Permet à l'Expert Vente de savoir de quel produit on on parle sans reposer la question.
    policy_type: NotRequired[Literal["auto", "habitation", "santé"]]

    # --- GESTION DES KILLER FEATURES ---
    # Pour savoir si on doit activer l'interface Voice ou le Screen Sharing.
    active_feature: NotRequired[Literal["voice", "screen_sharing", "none"]]

    # ID de dossier pour l'agent de sinistre
    claim_id: NotRequired[str]