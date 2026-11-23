# Evaluating a rare-event classifier

The recovered historical fraud notebooks reported accuracy and positive-class recall. In an invented test set of 100 observations with one positive, an always-negative classifier has 99% accuracy but misses the only positive. Accuracy alone does not establish useful detection.

`lamat_quant.classification.binary_metrics` reports confusion counts and accuracy, positive precision, positive recall, and false-positive rate for explicit binary labels (1 is the event), supplied as lists or one-dimensional NumPy arrays. A rate with a zero denominator is `None`: if there are no positive predictions, precision is undefined; if there are no actual positives, recall is undefined; and if there are no actual negatives, the false-positive rate is undefined. Counts and sample composition are needed to interpret every rate. Small samples make estimates unstable.

This is an evaluation exercise, not a fraud detector. Use a separate untouched test set, decide thresholds and model choices on training/validation data, and prevent information from later observations or related accounts from leaking across splits. Class imbalance, sampling and changing populations affect interpretation. Precision on an artificially balanced sample does not directly represent precision at deployment prevalence. The metrics do not establish calibration, fairness, causality or operational suitability. Explanation methods must also state their baseline and output scale, and explanations for held-out observations do not validate a model.

The helper and its examples use invented labels; no historical data, model or saved outputs are used. The original notebooks and their data provenance remain under private review in #54.
