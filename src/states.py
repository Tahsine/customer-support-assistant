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

### NOTE
"""
Pourquoi ces choix ? (Explications)
1. Le choix des InsuranceStep
Nous avons calqué les étapes sur la structure de ton Mock Website :

concierge : C'est le point d'entrée unique. Son rôle est de classifier l'intention. Si l'utilisateur dit "J'ai eu un accident", le concierge ne traite pas le problème, il fait un handoff immédiat vers le claims_manager.

sales_expert : Cet agent aura accès à tes documents (Agentic RAG). Il est séparé des autres car il a besoin d'un ton persuasif et d'outils de comparaison d'offres.

claims_manager : C'est ici que ton Screen Sharing brillera. Cet agent est spécialisé dans le guidage étape par étape.

2. L'utilisation de policy_type
Dans le pattern Handoff, le but est l'efficacité. Si le concierge détecte dès le début que l'utilisateur clique sur "Auto", il remplit policy_type="auto". Quand le sales_expert prend le relais, son prompt système verra cette donnée et pourra dire : "Bonjour ! Je vois que vous vous intéressez à notre assurance Auto, quelle formule vous tente ?" au lieu de "En quoi puis-je vous aider ?".

3. Le champ active_feature
C'est ici que tu connectes ton Backend (LangChain) à ton Frontend (React) via Convex.

Si l'agent claims_manager décide qu'il est temps d'aider l'utilisateur visuellement, il utilise un outil qui met à jour le state : active_feature="screen_sharing".

Convex étant temps réel, ton widget React verra ce changement instantanément et ouvrira la fenêtre de partage d'écran automatiquement pour l'utilisateur.

Pourquoi le pattern Handoff est parfait ici ?
Selon ta documentation, ce pattern permet à l'agent spécialisé d'avoir une interaction directe avec l'utilisateur. C'est crucial pour ta feature Voice : tu ne veux pas d'un agent intermédiaire (orchestrateur) qui rajoute de la latence. L'agent "Sales" doit parler directement au client pour une fluidité maximale.

"""