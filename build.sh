git pull origin develop
git add .
git commit -m "$(date +%Y-%m-%d_%H:%M:%S)"
git push origin feat/develop
docker login -u "intelnexoec" -p "dckr_pat_EY2hedAJR91hc9Vn9Hx6-qVpgg0"

export SHORT_COMMIT=$(git log -1 --pretty="%H" | cut -b -8)
export DOCKER_IMAGE_VERSION="dev_${SHORT_COMMIT}"

# pip freeze > requirements.txt

docker build -t intelnexoec/xtrim-api-edificio:${DOCKER_IMAGE_VERSION} -f Dockerfile .
docker tag intelnexoec/xtrim-api-edificio:${DOCKER_IMAGE_VERSION} intelnexoec/xtrim-api-edificio:latest
docker push intelnexoec/xtrim-api-edificio:${DOCKER_IMAGE_VERSION}
docker push intelnexoec/xtrim-api-edificio:latest
echo "tag: ${DOCKER_IMAGE_VERSION}"