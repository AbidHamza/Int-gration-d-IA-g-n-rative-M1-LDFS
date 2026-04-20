# Integration des systemes d'IA generative - M1 LDFS

Bienvenue dans ce depot pedagogique concu pour le cours de Master 1 intitule **Integration des systemes d'IA generative**.

Ce cours s'adresse a des etudiants qui savent programmer en Python mais qui n'ont aucune connaissance prealable en intelligence artificielle. Chaque notion est expliquee depuis zero, avec des exemples concrets et des manipulations immediates.

---

## Ce que vous allez apprendre

A la fin de ce cours, vous serez capable de :

- Expliquer simplement ce qu'est un modele de langage et comment il fonctionne
- Construire des prompts efficaces pour obtenir des reponses utiles et fiables
- Comparer et choisir un modele open source adapte a un besoin
- Connecter une API de LLM dans une application Python
- Construire un systeme RAG pour interroger vos propres documents
- Identifier et prevenir les principaux risques lies a l'IA generative
- Concevoir et documenter un projet integrant plusieurs de ces composants

Aucune connaissance en mathematiques, statistiques ou machine learning n'est requise.

---

## Prerequis

- Python 3.10 ou superieur (`python --version`)
- Connaissance des bases de Python (variables, fonctions, boucles, fichiers)
- Environ 3 Go d'espace disque libre (pour les modeles Ollama et Hugging Face)
- Un compte Hugging Face gratuit (Room 03 uniquement) : https://huggingface.co

**Aucune cle API payante n'est requise. Tout le cours fonctionne en local.**

---

## Installation

### 1. Cloner le depot et installer les dependances Python

```bash
git clone https://github.com/AbidHamza/Int-gration-d-IA-g-n-rative-M1-LDFS.git
cd Int-gration-d-IA-g-n-rative-M1-LDFS
pip install -r requirements.txt
```

### 2. Installer Ollama (moteur LLM local, gratuit)

Ollama permet de faire tourner un LLM directement sur votre machine, sans cle ni connexion Internet.

- Telecharger : https://ollama.com
- Verifier l'installation : `ollama --version`
- Lancer le serveur (a laisser ouvert pendant les exercices) : `ollama serve`
- Dans un autre terminal, telecharger le modele par defaut (environ 640 Mo) :

```bash
ollama pull tinyllama
```

Pour Room 05 (RAG), un modele plus performant est recommande (environ 1.3 Go) :

```bash
ollama pull llama3.2:1b
```

### 3. Configurer l'environnement

```bash
cp .env.example .env
```

Sous Windows PowerShell :

```powershell
Copy-Item .env.example .env
```

Le fichier `.env` par defaut fonctionne sans modification pour les Rooms 01, 02, 04, 05, 06, 07, 08. Pour Room 03, ajoutez votre token Hugging Face (gratuit) dans `HF_TOKEN`.

### 4. Verifier que tout fonctionne

```bash
python utils.py
```

Vous devez voir : le fournisseur detecte (Ollama), le modele utilise (tinyllama) et un message **Test de connexion reussi**. Si le test echoue, assurez-vous qu'Ollama est lance (`ollama serve`) et que le modele est telecharge (`ollama list`).

---

## Parcours des 8 Rooms

Le cours est organise en 8 Rooms progressives. Chaque Room produit un resultat visible et exploitable.

| Room | Titre | Ce que vous construisez |
|------|-------|------------------------|
| 01 | Decouvrir l'IA generative | Votre premier dialogue avec un LLM, observation des hallucinations |
| 02 | Construire avec des prompts | Un assistant pedagogique avec des prompts structures |
| 03 | Explorer les modeles open source | Un tableau comparatif de 3 modeles Hugging Face |
| 04 | Connecter une API | Un mini service FastAPI interface avec un LLM |
| 05 | Creer un systeme RAG | Un assistant qui repond en citant vos documents |
| 06 | Comprendre les risques | Une grille d'audit de reponses generees |
| 07 | Projets guides | Trois assistants thematiques complets |
| 08 | Projet final | Un systeme integrant prompts, API, RAG et analyse des risques |

Commencez par la Room 01 et progressez dans l'ordre. Chaque Room suppose que les precedentes ont ete completees.

Note : certaines parties des Rooms 07 et 08 sont volontairement des squelettes a completer (`pass`, `A COMPLETER`). C'est normal pedagogiquement.

---

## Structure de chaque Room

```
README.md          - Objectif, resultat attendu, liste des fichiers
theory.md          - Explications des notions, avec exemples concrets
practice.md        - Exercices guides, etape par etape
challenge.md       - Extension plus avancee pour aller plus loin
rubric.md          - Criteres d'evaluation
code/              - Scripts Python commentes
expected_outputs/  - Exemples de ce que vous devez obtenir
```

---

## Dossiers transverses

```
datasets/    - Fichiers de donnees utilises dans les exercices
templates/   - Modeles de rapport et de livrable
solutions/   - Corriges des exercices (a consulter apres avoir essaye)
evaluation/  - Baremes et grilles d'evaluation du cours
```

---

## Conventions de rendu

- Vos travaux doivent etre remis dans un depot Git personnel, avec un historique de commits lisible.
- Chaque livrable doit inclure un fichier `README.md` decrivant comment l'executer.
- Le code doit s'executer sans erreur avec `pip install -r requirements.txt` et Ollama lance.
- Les reponses aux questions d'analyse doivent etre redigees en francais, en phrases completes.

---

## Obtenir de l'aide

Si un script ne fonctionne pas, verifiez dans l'ordre :

1. Ollama est-il lance ? (`ollama serve` dans un terminal)
2. Le modele est-il telecharge ? (`ollama list` doit contenir `tinyllama`)
3. Le fichier `.env` est-il present ? (copie depuis `.env.example`)
4. Les dependances sont-elles installees ? (`pip install -r requirements.txt`)
5. Python est-il en version 3.10+ ? (`python --version`)
6. Consultez le fichier `expected_outputs/` de la Room pour comparer avec votre resultat.
