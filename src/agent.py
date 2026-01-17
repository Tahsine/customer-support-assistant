from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from states import InsuranceSupportState
from middleware import apply_step_config
from workflow_tools import transfer_to_sales, transfer_to_claims, query_knwoledge_base, escalate_to_human, provide_final_solution

# 1. Model Initialisation
model = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview"
)

# 2. On rassemble TOUS les outils définis.
# Même si le middleware filtre les outils par étape, l'agent doit connaître
# l'existence de la boîte à outils complète au démarrage.
all_tools = [
    transfer_to_claims,
    transfer_to_sales,
    query_knwoledge_base,
    escalate_to_human,
    provide_final_solution
]

# 3. Création de l'agent avec configuration dynamique
agent = create_agent(
    model=model,
    tools=all_tools,
    state_schema=InsuranceSupportState,
    middleware=[apply_step_config],
    checkpointer=InMemorySaver()
)

### NOTE
"""
Le Checkpointer (InMemorySaver) : La Mémoire Vive
C'est ce qui fait que ton widget est une conversation et non une suite de questions isolées.

Sans checkpointer : L'utilisateur dit "Je veux une assurance Auto". Le Concierge fait le handoff vers l'expert Sales. L'utilisateur répond "Ok, quelles sont les options ?". Sans mémoire, l'agent redevient un Concierge et demande "Bonjour, comment puis-je vous aider ?".

Avec checkpointer : L'état current_step: "sales_expert" est sauvegardé. Le deuxième message est traité directement par l'expert.

Note pour ton business : En production avec Convex, tu remplaceras InMemorySaver par une persistance dans ta base de données pour que l'utilisateur retrouve sa conversation même s'il rafraîchit la page.

La liste all_tools
Tu pourrais te demander : "Si le middleware définit les outils, pourquoi les mettre tous ici ?". C'est parce que lors de l'initialisation, LangChain doit préparer les "schémas" (JSON) de chaque outil pour que le modèle Gemini sache comment les appeler techniquement. Le middleware, lui, ne fait que restreindre cette liste au moment T.

Le state_schema
Il garantit que ton agent respecte la structure de données que nous avons définie à l'étape 1. Si l'agent essaie d'écrire dans un champ qui n'existe pas (ex: prix_contrat), le système lèvera une erreur au lieu de polluer la mémoire.
"""