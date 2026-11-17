# Task 16: historical LSTM teaching notebook — review record

**Decision:** Retain the original as a linked historical teaching notebook; defer a runnable rewrite until its training text, Reddit data and pretrained model assets have documented provenance and permission. [Board task #16](https://github.com/gllamat/lamat/issues/16) expressly permits a documented decision to retain the original.

## Source inspected

The public [ITAM Reddit example](https://gist.github.com/gllamat/d87c1ca46a73e17499f0368c5db31101/fffe3eb2176f63a26139970a51bc0f60059cb4cc), revision `fffe3eb2176f63a26139970a51bc0f60059cb4cc`, was inspected on 17 November 2026. GitHub attributes the gist to `gllamat` and reports creation on 16 March 2021. Account ownership does not establish authorship or rights for every dataset or model. The notebook was read, not executed; linked resources were not downloaded or tested for availability, safety, licence or compatibility.

The notebook presents LSTM text generation alongside Reddit/finance material, under a heading referring to both WallStreetBets and Macbeth. Its code refers to Keras sequential models, LSTM layers, JSON model reconstruction and loading weights. It reads external files and CSVs and references resources hosted on Google Drive, GitHub Gist and Amazon S3. These dependencies and the provenance of their contents need independent review. A check of the code found file-opening calls but no explicit `encoding=` argument; a modern text pipeline should specify and validate encoding and normalization. The historical Keras API and external model artifacts have not been tested against current versions.

## Scope and rights

Separate a future character-generation lesson from the Reddit/financial analysis. For the former, establish the exact training corpus, edition, jurisdiction, licence, preprocessing and the provenance and permission for the model architecture and weights; a literary work's age alone does not settle rights for every edition or derived dataset. For the latter, establish the source, collection period, provider terms, consent/privacy treatment, permitted retention and licence for any Reddit material. The notebook’s use of a source or a model file does not itself grant permission to redistribute it.

The legacy notebook should remain clearly dated and linked from the archive. Do not copy its datasets, credentials, output or model files into the new repository. A later example can use an explicitly licensed or owner-created small text corpus, pinned dependencies, UTF-8 handling and seeded experiments; label generated text as an illustrative demonstration rather than a financial predictor. Any financial model would require a separate, point-in-time evaluation and documented limitations.

## Human verification

Inspect the linked revision and this decision. Review the source references, corpus and weights with their owners before changing this decision. The archive link and this review preserve the teaching lineage without claiming that the old notebook runs today. No code, weights or data were executed or incorporated in this review.
