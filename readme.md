# Generalized TLDR 

## setup dataproc cluster

```
gcloud dataproc clusters create ${MYCLUSTER} \
    --single-node \
    --image-version=1.5 \
    --region=${REGION} \
    --metadata='PIP_PACKAGES=nltk sklearn networkx' \
    --worker-machine-type=n1-standard-2 \
    --master-machine-type=n1-standard-2 \
    --initialization-actions=gs://goog-dataproc-initialization-actions-${REGION}/python/pip-install.sh,gs://${MYBUCKET}/nltk_download.sh
```

## submit spark job

```
gcloud dataproc jobs submit pyspark --cluster ${MYCLUSTER} summarize.py -- gs://${MYBUCKET}/articles/ english gs://${MYBUCKET}/summaries/
```