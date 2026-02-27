# Makefile pour Dataiku Workflow Chatbot
# Simplifie les commandes Docker Compose

.PHONY: help build up down restart logs shell clean check-env

# Couleurs pour l'output
GREEN  := \033[0;32m
YELLOW := \033[0;33m
RED    := \033[0;31m
NC     := \033[0m # No Color

# Variables
IMAGE_NAME := dataiku-chatbot
CONTAINER_NAME := dataiku-workflow-chatbot

# Commande par défaut
.DEFAULT_GOAL := help

## help: Affiche cette aide
help:
	@echo "$(GREEN)Dataiku Workflow Chatbot - Commandes disponibles$(NC)"
	@echo ""
	@echo "$(YELLOW)Configuration:$(NC)"
	@echo "  make check-env    - Vérifie que .env existe et contient les variables requises"
	@echo "  make setup        - Setup initial (vérifie .env et build)"
	@echo ""
	@echo "$(YELLOW)Développement:$(NC)"
	@echo "  make build        - Build l'image Docker"
	@echo "  make up           - Démarre le chatbot (build + run)"
	@echo "  make down         - Arrête le chatbot"
	@echo "  make restart      - Redémarre le chatbot"
	@echo "  make logs         - Affiche les logs (Ctrl+C pour quitter)"
	@echo "  make logs-f       - Suit les logs en temps réel"
	@echo ""
	@echo "$(YELLOW)Debug:$(NC)"
	@echo "  make shell        - Ouvre un shell dans le conteneur"
	@echo "  make status       - Affiche le statut du conteneur"
	@echo "  make inspect      - Inspecte le conteneur"
	@echo ""
	@echo "$(YELLOW)Nettoyage:$(NC)"
	@echo "  make clean        - Supprime le conteneur et les volumes"
	@echo "  make clean-all    - Supprime tout (conteneur, volumes, images)"
	@echo ""
	@echo "$(YELLOW)Production:$(NC)"
	@echo "  make prod         - Build et démarre en mode production"
	@echo "  make health       - Vérifie la santé du service"
	@echo ""

## check-env: Vérifie les variables d'environnement
check-env:
	@echo "$(YELLOW)Vérification de la configuration...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(RED)❌ Fichier .env manquant !$(NC)"; \
		echo "$(YELLOW)Créez un fichier .env avec :$(NC)"; \
		echo "  ANTHROPIC_API_KEY=sk-ant-api03-..."; \
		echo "  DSS_URL=https://..."; \
		echo "  DSS_API_KEY=..."; \
		echo "  DSS_PROJECT_KEY=TEST_WORKFLOW"; \
		exit 1; \
	fi
	@echo "$(GREEN)✅ Fichier .env trouvé$(NC)"
	@if ! grep -q "ANTHROPIC_API_KEY=" .env || grep -q "ANTHROPIC_API_KEY=$$" .env; then \
		echo "$(RED)❌ ANTHROPIC_API_KEY manquante dans .env$(NC)"; \
		exit 1; \
	fi
	@echo "$(GREEN)✅ ANTHROPIC_API_KEY configurée$(NC)"
	@echo "$(GREEN)✅ Configuration OK !$(NC)"

## setup: Setup initial
setup: check-env
	@echo "$(GREEN)Setup initial...$(NC)"
	@mkdir -p logs
	@echo "$(GREEN)✅ Setup terminé !$(NC)"

## build: Build l'image Docker
build:
	@echo "$(YELLOW)Build de l'image Docker...$(NC)"
	docker-compose build --no-cache
	@echo "$(GREEN)✅ Image buildée avec succès !$(NC)"

## up: Démarre le chatbot
up: check-env
	@echo "$(YELLOW)Démarrage du chatbot...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Chatbot démarré !$(NC)"
	@echo "$(GREEN)🌐 Accès: http://localhost:8501$(NC)"
	@echo "$(YELLOW)💡 Utilisez 'make logs' pour voir les logs$(NC)"

## down: Arrête le chatbot
down:
	@echo "$(YELLOW)Arrêt du chatbot...$(NC)"
	docker-compose down
	@echo "$(GREEN)✅ Chatbot arrêté$(NC)"

## restart: Redémarre le chatbot
restart:
	@echo "$(YELLOW)Redémarrage du chatbot...$(NC)"
	docker-compose restart
	@echo "$(GREEN)✅ Chatbot redémarré !$(NC)"

## logs: Affiche les logs
logs:
	docker-compose logs

## logs-f: Suit les logs en temps réel
logs-f:
	docker-compose logs -f

## shell: Ouvre un shell dans le conteneur
shell:
	@echo "$(YELLOW)Ouverture d'un shell dans le conteneur...$(NC)"
	docker-compose exec dataiku-chatbot /bin/bash || \
	docker exec -it $(CONTAINER_NAME) /bin/bash

## status: Affiche le statut
status:
	@echo "$(YELLOW)Statut du chatbot:$(NC)"
	@docker-compose ps
	@echo ""
	@echo "$(YELLOW)Utilisation des ressources:$(NC)"
	@docker stats $(CONTAINER_NAME) --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" || true

## inspect: Inspecte le conteneur
inspect:
	docker inspect $(CONTAINER_NAME)

## health: Vérifie la santé du service
health:
	@echo "$(YELLOW)Vérification de la santé du service...$(NC)"
	@curl -f http://localhost:8501/_stcore/health || echo "$(RED)❌ Service non accessible$(NC)"
	@docker ps --filter name=$(CONTAINER_NAME) --format "{{.Status}}"

## clean: Supprime le conteneur et les volumes
clean:
	@echo "$(YELLOW)Nettoyage...$(NC)"
	docker-compose down -v
	@echo "$(GREEN)✅ Nettoyage terminé$(NC)"

## clean-all: Supprime tout (conteneur, volumes, images)
clean-all:
	@echo "$(RED)⚠️  Suppression complète (conteneur + volumes + images)$(NC)"
	docker-compose down -v --rmi all
	@echo "$(GREEN)✅ Suppression complète terminée$(NC)"

## prod: Build et démarre en mode production
prod: check-env build
	@echo "$(GREEN)Démarrage en mode production...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Chatbot en production !$(NC)"
	@echo "$(GREEN)🌐 Accès: http://localhost:8501$(NC)"
	@make health
