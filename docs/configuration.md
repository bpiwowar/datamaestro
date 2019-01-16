# Specification

Configuration is provided by sets of `yaml` files organized hierarchically by organization name. For example,
`nist.trec.documents.clueweb09` can be found in the file `nist/trec/documents.yaml`. The path `nist/trec` defines the organization.

## Format

### Example

The following is a complete example that describes the Glove dataset

```yaml
name: GloVe word embeddings
website: http://nlp.stanford.edu/projects/glove/
license: Public Domain Dedication and License
tags:
  - word embeddings
papers:
  technical description: http://nlp.stanford.edu/pubs/glove.pdf
description: |
  GloVe is an unsupervised learning algorithm for obtaining vector representations for words.
  Training is performed on aggregated global word-word co-occurrence statistics from a corpus,
  and the resulting representations showcase interesting linear substructures of the word vector space.
...
---
# A variation of the dataset
id: 6b
description: Trained on Wikipedia 2014 + Gigaword 5
download: 
  handler: /archive:Zip
  url: http://nlp.stanford.edu/data/glove.6B.zip
size: 822M
statistics:
  tokens: 6G
  vocabulary: 400K
  cased: false
  dimension: [50, 100, 200, 300]
files:
  "50": glove.6B.50d.txt
  "100": glove.6B.100d.txt
  "200": glove.6B.200d.txt
  "300": glove.6B.300d.txt
...
---
id: 42b
description: Trained on Common Crawl
download: 
  handler: /single:File
  url: http://nlp.stanford.edu/data/glove.42B.300d.zip
size: 2.03G
statistics:
  cased: true
  tokens: 840G
  vocabulary: 2.2M
  dimension: 300
...
---
id: 840b
description: Trained on Common Crawl
download: 
  handler: /single:File
  url: http://nlp.stanford.edu/data/glove.840B.300d.zip
size: 2.03G
statistics:
  cased: true
  tokens: 840G
  vocabulary: 2.2M
  dimension: 300

```

## Fields

### General information

- `abstract` flag used to mark an abstract dataset (sub-datasets have to be defined)
- `name` gives a short name of the dataset
- `description` gives a longer description of the dataset
- `tags` is a list of tags (free vocabulary)
- `tasks` is a list of tasks (free vocabulary)
- `date` is the dataset release date 
- `version` is the version of the dataset
- [`links`](#links) give links to the main website or other related resources (e.g. paper)


### Links

`links` is a dictionary that associates a name with some fields like

- `url` The URL of the link
- `type` Gives the type of resource: either `website` or `paper`

### Nested datasets

Sub-datasets can be defined by defining several documents within the `yaml` file. The first document
will be the main dataset, and the others will be subdatasets.

### Download and data

The field `download` specifies how data should be downloaded. Generic handlers are defined
in datamaestro ([see documentation](download.html)) or defined in datamaestro extensions.

