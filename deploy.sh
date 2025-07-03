#!/bin/bash

# Couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Arrêt en cas d'erreur
set -e

git add .
# Crée un message de commit avec la date et l'heure actuelles
commit_msg="deploy: $(date '+%Y-%m-%d %H:%M:%S')"

# Vérifie s'il y a quelque chose à committer

git commit -m "$commit_msg"
echo -e "${GREEN}✔ Commit effectué : $commit_msg${NC}"


# Push
if git push; then
  echo -e "${GREEN}✔ Push réussi sur la branche courante !${NC}"
else
  echo -e "${RED}❌ Erreur lors du push. Essayez git pull puis relancez le script.${NC}"
  exit 1
fi

# Résumé
branch=$(git rev-parse --abbrev-ref HEAD)
echo -e "\n${GREEN}Déploiement terminé sur la branche ${branch}.${NC}" 