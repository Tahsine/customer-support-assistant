from typing import Literal
from langchain.tools import tool, ToolRuntime
from langchain.messages import ToolMessage
from langgraph.types import Command

from states import InsuranceSupportState, InsuranceStep

@tool
def transfer_to_sales(
    interest: Literal["auto", "habitation", "sante"],
    runtime: ToolRuntime[None, InsuranceSupportState]
) -> Command:
    """
    Transfère l'utilisateur vers un expert commercial quand il exprime un intérêt
    pour une de nos polices d'assurance.
    """
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=f"Transfert en cours vers l'expert {interest}...",
                    tool_call_id=runtime.tool_call_id
                )
            ],
            "policy_type": interest,
            "current_step": "sales_expert" # On change l'agent actif ici
        }
    )

@tool
def transfer_to_claims(
    runtime: ToolRuntime[None, InsuranceSupportState],
) -> Command:
    """
    Transfère l'utilisateur vers le service des sinistres pour déclarer un accident
    ou suivre un dossier de remboursement.
    """
    return Command(
        update={
            "messages":[
                ToolMessage(
                    content="Je vous mets en relation avec un gestionnaire de sinistres.",
                    tool_call_id=runtime.tool_call_id
                )
            ],
            "current_step": "claims_manager",
        }
    )

@tool
def toogle_special_feature(
    feature: Literal["voice", "screen_sharing"],
    runtime: ToolRuntime[None, InsuranceSupportState]
) -> Command:
    """
    Active une fonctionnalité avancé (Voix ou Partage d'écran)
    pour aider l'utilisateur.
    """
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=f"Activation de la fonctionnalité : {feature}",
                    tool_call_id=runtime.tool_call_id
                )
            ],
            "active_feature": feature,
        }
    )

### NOTE
"""
Pourquoi cette structure ? (Explications)
L'objet Command est le pivot : Contrairement à un outil classique qui renvoie juste du texte, Command modifie la structure même de la conversation. En changeant current_step, tu indiques au backend que le prochain message de l'utilisateur ne doit plus être traité par le "Concierge", mais par l'expert choisi.

Persistance des données (policy_type) : Dans transfer_to_sales, on enregistre le type d'assurance. Cela évite à l'expert suivant de redemander "Pour quel type d'assurance nous contactez-vous ?". C'est ce qu'on appelle le Context Engineering.

L'outil toggle_special_feature (Ta Killer Feature) : * C'est ici que ton business se différencie.

Imagine l'utilisateur qui galère sur le formulaire de sinistre. L'agent (Claims Manager) peut décider d'appeler toggle_special_feature(feature="screen_sharing").

Côté Frontend (React/Convex), ton application écoute les changements du State. Dès que active_feature passe à "screen_sharing", une popup s'affiche sur le site SafeGuard pour demander l'autorisation de partage d'écran.

Expérience fluide : Comme le précise la doc, ce pattern est le meilleur pour l'interaction utilisateur car il évite les latences d'un superviseur central. L'agent "Expert" parle directement au client.
"""