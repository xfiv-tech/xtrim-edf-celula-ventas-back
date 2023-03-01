git add .

git commit -m "$(date +%Y-%m-%d_%H:%M:%S)"

git push
docker login -u "intelnexoec" -p "DiegoySophie2O22" docker.io
export SHORT_COMMIT=$(git log -1 --pretty="%H" | cut -b -8)
export DOCKER_IMAGE_VERSION="dev_${SHORT_COMMIT}"

pip freeze > requirements.txt


docker build -t intelnexoec/xtrim-api-edificio:${DOCKER_IMAGE_VERSION} -f Dockerfile .
docker tag intelnexoec/xtrim-api-edificio:${DOCKER_IMAGE_VERSION} intelnexoec/xtrim-api-edificio:latest
docker push intelnexoec/xtrim-api-edificio:${DOCKER_IMAGE_VERSION}
docker push intelnexoec/xtrim-api-edificio:latest
echo "tag: ${DOCKER_IMAGE_VERSION}"