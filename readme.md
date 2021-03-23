# Generalized TLDR 
This project summarizes texts into its most relevant sentences based on the PageRank algorithm.
## How to Use
- clone this repo
- cd into generalized_TLDR
### To use this locally

```python
from summarize import summarize
print(summarize(article_text, article_language, number_of_sentences))
```

### To distribute this with pyspark and dataproc
- create a gs bucket and upload the text files for all the articles to it
## setup your dataproc cluster

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
gcloud dataproc jobs submit pyspark \
    --cluster ${MYCLUSTER} summarize.py \
    -- gs://${BUCKET}/path/to/articles <language> gs://${BUCKET}/path/to/output/dir
```