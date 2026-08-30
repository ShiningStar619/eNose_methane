---
title: GroupKFold — scikit-learn 1.9.0 documentation
id: groupkfold-scikit-learn-190-documentation
tags:
- ch5-theory-foundations-05eb4d
created: '2026-08-16T14:01:48.068708Z'
source: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html
source_domain: scikit-learn.org
fetched_at: '2026-08-16T14:01:47.971629Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
utility_score: 14.0
---

[Skip to main content](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html#main-content)
Back to top
  * System Settings
  * Light




1.9.0 (stable)
[1.10.dev0 (dev)](https://scikit-learn.org/dev/modules/generated/sklearn.model_selection.GroupKFold.html)[1.9.0 (stable)](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html)[1.8.0](https://scikit-learn.org/1.8/modules/generated/sklearn.model_selection.GroupKFold.html)[1.7.2](https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.GroupKFold.html)[1.6.1](https://scikit-learn.org/1.6/modules/generated/sklearn.model_selection.GroupKFold.html)[1.5.2](https://scikit-learn.org/1.5/modules/generated/sklearn.model_selection.GroupKFold.html)[1.4.2](https://scikit-learn.org/1.4/modules/generated/sklearn.model_selection.GroupKFold.html)
Collapse Sidebar Expand Sidebar
# GroupKFold[#](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html#groupkfold "Link to this heading") 

sklearn.model_selection.GroupKFold(_n_splits_ , , _shuffle False_, _random_state_)[[source]](https://github.com/scikit-learn/scikit-learn/blob/cc50648cc/sklearn/model_selection/_split.py#L533)[#](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html#sklearn.model_selection.GroupKFold "Link to this definition") 
    
K-fold iterator variant with non-overlapping groups.
Each group will appear exactly once in the test set across all folds (the number of distinct groups has to be at least equal to the number of folds).
The folds are approximately balanced in the sense that the number of samples is approximately the same in each test fold when `shuffle` is True.
Read more in the [User Guide](https://scikit-learn.org/stable/modules/cross_validation.html#group-k-fold).
For visualisation of cross-validation behaviour and comparison between common scikit-learn split methods refer to [Visualizing cross-validation behavior in scikit-learn](https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_indices.html#sphx-glr-auto-examples-model-selection-plot-cv-indices-py) 

Parameters: 
     

**n_splits** int, default=5 
    
Number of folds. Must be at least 2.
Changed in version 0.22: `n_splits` default value changed from 3 to 5. 

**shuffle** bool, default=False 
    
Whether to shuffle the groups before splitting into batches. Note that the samples within each split will not be shuffled.
Added in version 1.6. 

**random_state** int, RandomState instance or None, default=None 
    
When `shuffle` is True, `random_state` affects the ordering of the indices, which controls the randomness of each fold. Otherwise, this parameter has no effect. Pass an int for reproducible output across multiple function calls. See [Glossary](https://scikit-learn.org/stable/glossary.html#term-random_state).
Added in version 1.6.
See also     
For splitting the data according to explicit, domain-specific grouping of the dataset.     
Takes class information into account to avoid building folds with imbalanced class proportions (for binary or multiclass classification tasks).
Notes
Groups appear in an arbitrary order throughout the folds.
Examples

```
>>> importnumpyasnp
>>> fromsklearn.model_selectionimport GroupKFold
>>> X = np.array([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10], [11, 12]])
>>> y = np.array([1, 2, 3, 4, 5, 6])
>>> groups = np.array([0, 0, 2, 2, 3, 3])
>>> group_kfold = GroupKFold(n_splits=2)
>>> group_kfold.get_n_splits()
2
>>> print(group_kfold)
GroupKFold(n_splits=2, random_state=None, shuffle=False)
>>> for i, (train_index, test_index) in enumerate(group_kfold.split(X, y, groups)):
...     print(f"Fold {i}:")
...     print(f"  Train: index={train_index}, group={groups[train_index]}")
...     print(f"  Test:  index={test_index}, group={groups[test_index]}")
Fold 0:
  Train: index=[2 3], group=[2 2]
  Test:  index=[0 1 4 5], group=[0 0 3 3]
Fold 1:
  Train: index=[0 1 4 5], group=[0 0 3 3]
  Test:  index=[2 3], group=[2 2]

```
Copy to clipboard 

get_metadata_routing()[[source]](https://github.com/scikit-learn/scikit-learn/blob/cc50648cc/sklearn/utils/_metadata_requests.py#L1737)[#](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html#sklearn.model_selection.GroupKFold.get_metadata_routing "Link to this definition") 
    
Get metadata routing of this object.
Please check [User Guide](https://scikit-learn.org/stable/metadata_routing.html#metadata-routing) on how the routing mechanism works. 

Returns: 
     

**routing** MetadataRequest 
    
A [`MetadataRequest`](https://scikit-learn.org/stable/modules/generated/sklearn.utils.metadata_routing.MetadataRequest.html#sklearn.utils.metadata_routing.MetadataRequest "sklearn.utils.metadata_routing.MetadataRequest") encapsulating routing information. 

get_n_splits(__,__,_groups_)[[source]](https://github.com/scikit-learn/scikit-learn/blob/cc50648cc/sklearn/model_selection/_split.py#L414)[#](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html#sklearn.model_selection.GroupKFold.get_n_splits "Link to this definition") 
    
Returns the number of splitting iterations as set with the `n_splits` param when instantiating the cross-validator. 

Parameters: 
     

**X** array-like of shape (n_samples, n_features), default=None 
    
Always ignored, exists for API compatibility. 

**y** array-like of shape (n_samples,), default=None 
    
Always ignored, exists for API compatibility. 

**groups** array-like of shape (n_samples,), default=None 
    
Always ignored, exists for API compatibility. 

Returns: 
     

**n_splits** int 
    
Returns the number of splitting iterations in the cross-validator. 

set_split_request(, _groups '$UNCHANGED$'_) → [[source]](https://github.com/scikit-learn/scikit-learn/blob/cc50648cc/sklearn/utils/_metadata_requests.py#L1434)[#](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html#sklearn.model_selection.GroupKFold.set_split_request "Link to this definition") 
    
Configure whether metadata should be requested to be passed to the `split` method.
Note that this method is only relevant when this estimator is used as a sub-estimator within a [meta-estimator](https://scikit-learn.org/stable/glossary.html#term-meta-estimator) and metadata routing is enabled with `enable_metadata_routing=True` (see [`sklearn.set_config`](https://scikit-learn.org/stable/modules/generated/sklearn.set_config.html#sklearn.set_config "sklearn.set_config")). Please check the [User Guide](https://scikit-learn.org/stable/metadata_routing.html#metadata-routing) on how the routing mechanism works.
The options for each parameter are:
  * `True`: metadata is requested, and passed to `split` if provided. The request is ignored if metadata is not provided.
  * `False`: metadata is not requested and the meta-estimator will not pass it to `split`.
  * `None`: metadata is not requested, and the meta-estimator will raise an error if the user provides it.
  * `str`: metadata should be passed to the meta-estimator with this given alias instead of the original name.


The default (`sklearn.utils.metadata_routing.UNCHANGED`) retains the existing request. This allows you to change the request for some parameters and not others.
Added in version 1.3. 

Parameters: 
     

**groups** str, True, False, or None, default=sklearn.utils.metadata_routing.UNCHANGED 
    
Metadata routing for `groups` parameter in `split`. 

Returns: 
     

**self** object 
    
The updated object. 

split(, __,_groups_)[[source]](https://github.com/scikit-learn/scikit-learn/blob/cc50648cc/sklearn/model_selection/_split.py#L660)[#](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html#sklearn.model_selection.GroupKFold.split "Link to this definition") 
    
Generate indices to split data into training and test set. 

Parameters: 
     

**X** array-like of shape (n_samples, n_features) 
    
Training data, where `n_samples` is the number of samples and `n_features` is the number of features. 

**y** array-like of shape (n_samples,), default=None 
    
The target variable for supervised learning problems. 

**groups** array-like of shape (n_samples,) 
    
Group labels for the samples used while splitting the dataset into train/test set. 

Yields: 
     

**train** ndarray 
    
The training set indices for that split. 

**test** ndarray 
    
The testing set indices for that split.
## Gallery examples[#](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html#gallery-examples "Link to this heading")
[Visualizing cross-validation behavior in scikit-learn](https://scikit-learn.org/stable/auto_examples/model_selection/plot_cv_indices.html)
Visualizing cross-validation behavior in scikit-learn
[Release Highlights for scikit-learn 1.4](https://scikit-learn.org/stable/auto_examples/release_highlights/plot_release_highlights_1_4_0.html)
Release Highlights for scikit-learn 1.4
On this page 
scikit-learn is [financially supported](https://scikit-learn.org/stable/institutional_support.html#funding) by Probabl and other institutions.
[ Enterprise-grade solutions and services ](https://probabl.ai/lp/scikit-learn)
  *[*]: Keyword-only parameters separator (PEP 3102)
