# git pull origin feat/addCatalogsAndEmployees

git add .

git commit -m "$(date +%Y-%m-%d_%H:%M:%S) Se refacturizo para que se acepte id_gerenre_regional valla con valor null y ya no sea obligatorio"

git push origin celula_venta --force

docker login -u "intelnexoec" -p "dckr_pat_uSMon0cOOI_TXSP6hqgGh5UryMI"

export SHORT_COMMIT=$(git log -1 --pretty="%H" | cut -b -8)
export DOCKER_IMAGE_VERSION="dev_${SHORT_COMMIT}"

# pip install --upgrade pip setuptools wheel
# pip install -r requirements.txt
# pip freeze > requirements.txt


docker build -t intelnexoec/xtrim-api-edificio:${DOCKER_IMAGE_VERSION} -f Dockerfile .
docker tag intelnexoec/xtrim-api-edificio:${DOCKER_IMAGE_VERSION} intelnexoec/xtrim-api-edificio:latest
docker push intelnexoec/xtrim-api-edificio:${DOCKER_IMAGE_VERSION}
docker push intelnexoec/xtrim-api-edificio:latest
echo "tag: ${DOCKER_IMAGE_VERSION}"
