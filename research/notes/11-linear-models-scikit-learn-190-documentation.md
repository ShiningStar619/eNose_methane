---
title: 1.1. Linear Models — scikit-learn 1.9.0 documentation
id: 11-linear-models-scikit-learn-190-documentation
tags:
- ch5-theory-foundations-05eb4d
created: '2026-08-16T14:03:05.315625Z'
source: https://scikit-learn.org/stable/modules/linear_model.html
source_domain: scikit-learn.org
fetched_at: '2026-08-16T14:03:05.227102Z'
fetch_provider: crawl4ai
status: draft
type: note
tier: unknown
content_type: unknown
deprecated: false
utility_score: 13.0
---

[Skip to main content](https://scikit-learn.org/stable/modules/linear_model.html#main-content)
Back to top
  * System Settings
  * Light




1.9.0 (stable)
[1.10.dev0 (dev)](https://scikit-learn.org/dev/modules/linear_model.html)[1.9.0 (stable)](https://scikit-learn.org/stable/modules/linear_model.html)[1.8.0](https://scikit-learn.org/1.8/modules/linear_model.html)[1.7.2](https://scikit-learn.org/1.7/modules/linear_model.html)[1.6.1](https://scikit-learn.org/1.6/modules/linear_model.html)[1.5.2](https://scikit-learn.org/1.5/modules/linear_model.html)[1.4.2](https://scikit-learn.org/1.4/modules/linear_model.html)
Collapse Sidebar Expand Sidebar
#  1.1. Linear Models[#](https://scikit-learn.org/stable/modules/linear_model.html#linear-models "Link to this heading")
The following are a set of methods intended for regression in which the target value is expected to be a linear combination of the features. In mathematical notation, the predicted value can be written as:
(w,x)=++...+
Across the module, we designate the vector w=(,...,) as `coef_` and as `intercept_`.
To perform classification with generalized linear models, see [Logistic regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression).
##  1.1.1. Ordinary Least Squares[#](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares "Link to this heading")
[`LinearRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression "sklearn.linear_model.LinearRegression") fits a linear model with coefficients w=(,...,) to minimize the residual sum of squares between the observed targets in the dataset, and the targets predicted by the linear approximation. Mathematically it solves a problem of the form:
minXw−y
[`LinearRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression "sklearn.linear_model.LinearRegression") takes in its `fit` method arguments , , `sample_weight` and stores the coefficients of the linear model in its `coef_` and `intercept_` attributes:

```
>>> fromsklearnimport linear_model
>>> reg = linear_model.LinearRegression()
>>> reg.fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
LinearRegression()
>>> reg.coef_
array([0.5, 0.5])
>>> reg.intercept_
0.0

```
Copy to clipboard
The coefficient estimates for Ordinary Least Squares rely on the independence of the features. When features are correlated and some columns of the design matrix have an approximately linear dependence, the design matrix becomes close to singular and as a result, the least-squares estimate becomes highly sensitive to random errors in the observed target, producing a large variance. This situation of _multicollinearity_ can arise, for example, when data are collected without an experimental design.
Examples
  * [Ordinary Least Squares and Ridge Regression](https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols_ridge.html#sphx-glr-auto-examples-linear-model-plot-ols-ridge-py)


###  1.1.1.1. Non-Negative Least Squares[#](https://scikit-learn.org/stable/modules/linear_model.html#non-negative-least-squares "Link to this heading")
It is possible to constrain all the coefficients to be non-negative, which may be useful when they represent some physical or naturally non-negative quantities (e.g., frequency counts or prices of goods). [`LinearRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html#sklearn.linear_model.LinearRegression "sklearn.linear_model.LinearRegression") accepts a boolean `positive` parameter: when set to `True` [Non-Negative Least Squares](https://en.wikipedia.org/wiki/Non-negative_least_squares) are then applied.
Examples
  * [Non-negative least squares](https://scikit-learn.org/stable/auto_examples/linear_model/plot_nnls.html#sphx-glr-auto-examples-linear-model-plot-nnls-py)


###  1.1.1.2. Ordinary Least Squares Complexity[#](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares-complexity "Link to this heading")
The least squares solution is computed using the singular value decomposition of . If is a matrix of shape `(n_samples, n_features)` this method has a cost of O(nsamplesnfeatures2), assuming that nsamples≥nfeatures.
##  1.1.2. Ridge regression and classification[#](https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression-and-classification "Link to this heading")
###  1.1.2.1. Regression[#](https://scikit-learn.org/stable/modules/linear_model.html#regression "Link to this heading")
[`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge") regression addresses some of the problems of [Ordinary Least Squares](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares) by imposing a penalty on the size of the coefficients. The ridge coefficients minimize a penalized residual sum of squares:
minXw−y+αw
The complexity parameter controls the amount of shrinkage: the larger the value of , the greater the amount of shrinkage and thus the coefficients become more robust to collinearity.
As with other linear models, [`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge") will take in its `fit` method arrays , and will store the coefficients of the linear model in its `coef_` member:

```
>>> fromsklearnimport linear_model
>>> reg = linear_model.Ridge(alpha=.5)
>>> reg.fit([[0, 0], [0, 0], [1, 1]], [0, .1, 1])
Ridge(alpha=0.5)
>>> reg.coef_
array([0.34545455, 0.34545455])
>>> reg.intercept_
np.float64(0.13636)

```
Copy to clipboard
Note that the class [`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge") allows for the user to specify that the solver be automatically chosen by setting `solver="auto"`. When this option is specified, [`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge") will choose between the `"lbfgs"`, `"cholesky"`, and `"sparse_cg"` solvers. [`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge") will begin checking the conditions shown in the following table from top to bottom. If the condition is true, the corresponding solver is chosen.  
| **Solver**  | **Condition**  |  
| --- | --- |  
| ‘lbfgs’  | The `positive=True` option is specified.  |  
| ‘cholesky’  | The input array X is not sparse.  |  
| ‘sparse_cg’  | None of the above conditions are fulfilled.  |  
Examples
  * [Ordinary Least Squares and Ridge Regression](https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols_ridge.html#sphx-glr-auto-examples-linear-model-plot-ols-ridge-py)
  * [Plot Ridge coefficients as a function of the regularization](https://scikit-learn.org/stable/auto_examples/linear_model/plot_ridge_path.html#sphx-glr-auto-examples-linear-model-plot-ridge-path-py)
  * [Common pitfalls in the interpretation of coefficients of linear models](https://scikit-learn.org/stable/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html#sphx-glr-auto-examples-inspection-plot-linear-model-coefficient-interpretation-py)
  * [Ridge coefficients as a function of the L2 Regularization](https://scikit-learn.org/stable/auto_examples/linear_model/plot_ridge_coeffs.html#sphx-glr-auto-examples-linear-model-plot-ridge-coeffs-py)


###  1.1.2.2. Classification[#](https://scikit-learn.org/stable/modules/linear_model.html#classification "Link to this heading")
The [`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge") regressor has a classifier variant: [`RidgeClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html#sklearn.linear_model.RidgeClassifier "sklearn.linear_model.RidgeClassifier"). This classifier first converts binary targets to `{-1, 1}` and then treats the problem as a regression task, optimizing the same objective as above. The predicted class corresponds to the sign of the regressor’s prediction. For multiclass classification, the problem is treated as multi-output regression, and the predicted class corresponds to the output with the highest value.
It might seem questionable to use a (penalized) Least Squares loss to fit a classification model instead of the more traditional logistic or hinge losses. However, in practice, all those models can lead to similar cross-validation scores in terms of accuracy or precision/recall, while the penalized least squares loss used by the [`RidgeClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html#sklearn.linear_model.RidgeClassifier "sklearn.linear_model.RidgeClassifier") allows for a very different choice of the numerical solvers with distinct computational performance profiles.
The [`RidgeClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html#sklearn.linear_model.RidgeClassifier "sklearn.linear_model.RidgeClassifier") can be significantly faster than e.g. [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression "sklearn.linear_model.LogisticRegression") with a high number of classes because it can compute the projection matrix (X only once.
This classifier is sometimes referred to as a [Least Squares Support Vector Machine](https://en.wikipedia.org/wiki/Least-squares_support-vector_machine) with a linear kernel.
Examples
  * [Classification of text documents using sparse features](https://scikit-learn.org/stable/auto_examples/text/plot_document_classification_20newsgroups.html#sphx-glr-auto-examples-text-plot-document-classification-20newsgroups-py)


###  1.1.2.3. Ridge Complexity[#](https://scikit-learn.org/stable/modules/linear_model.html#ridge-complexity "Link to this heading")
This method has the same order of complexity as [Ordinary Least Squares](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares).
###  1.1.2.4. Setting the regularization parameter: leave-one-out Cross-Validation[#](https://scikit-learn.org/stable/modules/linear_model.html#setting-the-regularization-parameter-leave-one-out-cross-validation "Link to this heading")
[`RidgeCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html#sklearn.linear_model.RidgeCV "sklearn.linear_model.RidgeCV") and [`RidgeClassifierCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifierCV.html#sklearn.linear_model.RidgeClassifierCV "sklearn.linear_model.RidgeClassifierCV") implement ridge regression/classification with built-in cross-validation of the alpha parameter. They work in the same way as [`GridSearchCV`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html#sklearn.model_selection.GridSearchCV "sklearn.model_selection.GridSearchCV") except that it defaults to efficient Leave-One-Out [cross-validation](https://scikit-learn.org/stable/glossary.html#term-cross-validation). When using the default [cross-validation](https://scikit-learn.org/stable/glossary.html#term-cross-validation), alpha cannot be 0 due to the formulation used to calculate Leave-One-Out error. See [[RL2007]](https://scikit-learn.org/stable/modules/linear_model.html#rl2007) for details.
Usage example:

```
>>> importnumpyasnp
>>> fromsklearnimport linear_model
>>> reg = linear_model.RidgeCV(alphas=np.logspace(-6, 6, 13))
>>> reg.fit([[0, 0], [0, 0.1], [1, 1]], [0, -0.1, 1])
RidgeCV(alphas=array([1.e-06, 1.e-05, 1.e-04, 1.e-03, 1.e-02, 1.e-01, 1.e+00, 1.e+01,
      1.e+02, 1.e+03, 1.e+04, 1.e+05, 1.e+06]))
>>> reg.alpha_
np.float64(0.1)

```
Copy to clipboard
Specifying the value of the attribute will trigger the use of cross-validation with [`GridSearchCV`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html#sklearn.model_selection.GridSearchCV "sklearn.model_selection.GridSearchCV"), for example `cv=10` for 10-fold cross-validation, rather than Leave-One-Out Cross-Validation.
References[#](https://scikit-learn.org/stable/modules/linear_model.html#references "Link to this dropdown")
“Notes on Regularized Least Squares”, Rifkin & Lippert ([technical report](http://cbcl.mit.edu/publications/ps/MIT-CSAIL-TR-2007-025.pdf), [course slides](https://www.mit.edu/~9.520/spring07/Classes/rlsslides.pdf)).
##  1.1.3. Lasso[#](https://scikit-learn.org/stable/modules/linear_model.html#lasso "Link to this heading")
The [`Lasso`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html#sklearn.linear_model.Lasso "sklearn.linear_model.Lasso") is a linear model that estimates sparse coefficients, i.e., it is able to set coefficients exactly to zero. It is useful in some contexts due to its tendency to prefer solutions with fewer non-zero coefficients, effectively reducing the number of features upon which the given solution is dependent. For this reason, Lasso and its variants are fundamental to the field of compressed sensing. Under certain conditions, it can recover the exact set of non-zero coefficients (see [Compressive sensing: tomography reconstruction with L1 prior (Lasso)](https://scikit-learn.org/stable/auto_examples/applications/plot_tomography_l1_reconstruction.html#sphx-glr-auto-examples-applications-plot-tomography-l1-reconstruction-py)).
Mathematically, it consists of a linear model with an added regularization term. The objective function to minimize is:
minP(w)=12nsamplesXw−y+αw
The lasso estimate thus solves the least-squares with added penalty , where is a constant and is the -norm of the coefficient vector.
The implementation in the class [`Lasso`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html#sklearn.linear_model.Lasso "sklearn.linear_model.Lasso") uses coordinate descent as the algorithm to fit the coefficients. See [Least Angle Regression](https://scikit-learn.org/stable/modules/linear_model.html#least-angle-regression) for another implementation:

```
>>> fromsklearnimport linear_model
>>> reg = linear_model.Lasso(alpha=0.1)
>>> reg.fit([[0, 0], [1, 1]], [0, 1])
Lasso(alpha=0.1)
>>> reg.predict([[1, 1]])
array([0.8])

```
Copy to clipboard
The function [`lasso_path`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.lasso_path.html#sklearn.linear_model.lasso_path "sklearn.linear_model.lasso_path") is useful for lower-level tasks, as it computes the coefficients along the full path of possible values.
Examples
  * [L1-based models for Sparse Signals](https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_and_elasticnet.html#sphx-glr-auto-examples-linear-model-plot-lasso-and-elasticnet-py)
  * [Compressive sensing: tomography reconstruction with L1 prior (Lasso)](https://scikit-learn.org/stable/auto_examples/applications/plot_tomography_l1_reconstruction.html#sphx-glr-auto-examples-applications-plot-tomography-l1-reconstruction-py)
  * [Common pitfalls in the interpretation of coefficients of linear models](https://scikit-learn.org/stable/auto_examples/inspection/plot_linear_model_coefficient_interpretation.html#sphx-glr-auto-examples-inspection-plot-linear-model-coefficient-interpretation-py)
  * [Lasso model selection: AIC-BIC / cross-validation](https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_model_selection.html#sphx-glr-auto-examples-linear-model-plot-lasso-model-selection-py)


Note
**Feature selection with Lasso**
As the Lasso regression yields sparse models, it can thus be used to perform feature selection, as detailed in [L1-based feature selection](https://scikit-learn.org/stable/modules/feature_selection.html#l1-feature-selection).
References[#](https://scikit-learn.org/stable/modules/linear_model.html#references-2 "Link to this dropdown")
The following references explain the origin of the Lasso as well as properties of the Lasso problem and the duality gap computation used for convergence control.
  * [Robert Tibshirani. (1996) Regression Shrinkage and Selection Via the Lasso. J. R. Stat. Soc. Ser. B Stat. Methodol., 58(1):267-288](https://doi.org/10.1111/j.2517-6161.1996.tb02080.x)
  * “An Interior-Point Method for Large-Scale L1-Regularized Least Squares,” S. J. Kim, K. Koh, M. Lustig, S. Boyd and D. Gorinevsky, in IEEE Journal of Selected Topics in Signal Processing, 2007 ([Paper](https://web.stanford.edu/~boyd/papers/pdf/l1_ls.pdf))


###  1.1.3.1. Coordinate Descent with Gap Safe Screening Rules[#](https://scikit-learn.org/stable/modules/linear_model.html#coordinate-descent-with-gap-safe-screening-rules "Link to this heading")
Coordinate descent (CD) is a strategy to solve a minimization problem that considers a single feature at a time. This way, the optimization problem is reduced to a 1-dimensional problem which is easier to solve:
min12nsamples+−y+α|
with index meaning all features but . The solution is
=S((y−),α)|
with the soft-thresholding function S(z,α)=sign(z)max(0,z−α). Note that the soft-thresholding function is exactly zero whenever . The CD solver then loops over the features either in a cycle, picking one feature after the other in the order given by (`selection="cyclic"`), or by randomly picking features (`selection="random"`). It stops if the duality gap is smaller than the provided tolerance `tol`.
Mathematical details[#](https://scikit-learn.org/stable/modules/linear_model.html#mathematical-details "Link to this dropdown")
The duality gap is an upper bound of the difference between the current primal objective function of the Lasso, , and its minimum , i.e. G(w,v)≥P(w)−P(). It is given by G(w,v)=P(w)−D(v) with dual objective function
D(v)=12nsamples(v−v)
subject to v∈v≤nsamplesα. At optimum, the duality gap is zero, G(,)=0 (a property called strong duality). With (scaled) dual variable , current residual and dual scaling
c={|r≤nsamplesα,nsamplesα|r,otherwise
the stopping criterion is
tol|ynsamplesG(w,cr).
A clever method to speedup the coordinate descent algorithm is to screen features such that at optimum . Gap safe screening rules are such a tool. Anywhere during the optimization algorithm, they can tell which feature we can safely exclude, i.e., set to zero with certainty.
References[#](https://scikit-learn.org/stable/modules/linear_model.html#references-3 "Link to this dropdown")
The first reference explains the coordinate descent solver used in scikit-learn, the others treat gap safe screening rules.
  * [Friedman, Hastie & Tibshirani. (2010). Regularization Path For Generalized linear Models by Coordinate Descent. J Stat Softw 33(1), 1-22](https://doi.org/10.18637/jss.v033.i01)
  * [O. Fercoq, A. Gramfort, J. Salmon. (2015). Mind the duality gap: safer rules for the Lasso. Proceedings of Machine Learning Research 37:333-342, 2015.](https://arxiv.org/abs/1505.03410)
  * [E. Ndiaye, O. Fercoq, A. Gramfort, J. Salmon. (2017). Gap Safe Screening Rules for Sparsity Enforcing Penalties. Journal of Machine Learning Research 18(128):1-33, 2017.](https://arxiv.org/abs/1611.05780)


###  1.1.3.2. Setting regularization parameter[#](https://scikit-learn.org/stable/modules/linear_model.html#setting-regularization-parameter "Link to this heading")
The `alpha` parameter controls the degree of sparsity of the estimated coefficients.
####  1.1.3.2.1. Using cross-validation[#](https://scikit-learn.org/stable/modules/linear_model.html#using-cross-validation "Link to this heading")
scikit-learn exposes objects that set the Lasso `alpha` parameter by cross-validation: [`LassoCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoCV.html#sklearn.linear_model.LassoCV "sklearn.linear_model.LassoCV") and [`LassoLarsCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLarsCV.html#sklearn.linear_model.LassoLarsCV "sklearn.linear_model.LassoLarsCV"). [`LassoLarsCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLarsCV.html#sklearn.linear_model.LassoLarsCV "sklearn.linear_model.LassoLarsCV") is based on the [Least Angle Regression](https://scikit-learn.org/stable/modules/linear_model.html#least-angle-regression) algorithm explained below.
For high-dimensional datasets with many collinear features, [`LassoCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoCV.html#sklearn.linear_model.LassoCV "sklearn.linear_model.LassoCV") is most often preferable. However, [`LassoLarsCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLarsCV.html#sklearn.linear_model.LassoLarsCV "sklearn.linear_model.LassoLarsCV") has the advantage of exploring more relevant values of `alpha` parameter, and if the number of samples is very small compared to the number of features, it is often faster than [`LassoCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoCV.html#sklearn.linear_model.LassoCV "sklearn.linear_model.LassoCV").
####  1.1.3.2.2. Information-criteria based model selection[#](https://scikit-learn.org/stable/modules/linear_model.html#information-criteria-based-model-selection "Link to this heading")
Alternatively, the estimator [`LassoLarsIC`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLarsIC.html#sklearn.linear_model.LassoLarsIC "sklearn.linear_model.LassoLarsIC") proposes to use the Akaike information criterion (AIC) and the Bayes Information criterion (BIC). It is a computationally cheaper alternative to find the optimal value of alpha as the regularization path is computed only once instead of k+1 times when using k-fold cross-validation.
Indeed, these criteria are computed on the in-sample training set. In short, they penalize the over-optimistic scores of the different Lasso models by their flexibility (cf. to “Mathematical details” section below).
However, such criteria need a proper estimation of the degrees of freedom of the solution, are derived for large samples (asymptotic results) and assume the correct model is candidates under investigation. They also tend to break when the problem is badly conditioned (e.g. more features than samples).
Examples
  * [Lasso model selection: AIC-BIC / cross-validation](https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_model_selection.html#sphx-glr-auto-examples-linear-model-plot-lasso-model-selection-py)
  * [Lasso model selection via information criteria](https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_lars_ic.html#sphx-glr-auto-examples-linear-model-plot-lasso-lars-ic-py)


####  1.1.3.2.3. AIC and BIC criteria[#](https://scikit-learn.org/stable/modules/linear_model.html#aic-and-bic-criteria "Link to this heading")
The definition of AIC (and thus BIC) might differ in the literature. In this section, we give more information regarding the criterion computed in scikit-learn.
Mathematical details[#](https://scikit-learn.org/stable/modules/linear_model.html#mathematical-details-2 "Link to this dropdown")
The AIC criterion is defined as:
AIC=−2log⁡()+2d
where is the maximum likelihood of the model and is the number of parameters (as well referred to as degrees of freedom in the previous section).
The definition of BIC replaces the constant by log⁡(N):
BIC=−2log⁡()+log⁡(N)d
where is the number of samples.
For a linear Gaussian model, the maximum log-likelihood is defined as:
log⁡()=−log⁡(2π)−log⁡()−∑(−
where is an estimate of the noise variance, and are respectively the true and predicted targets, and is the number of samples.
Plugging the maximum log-likelihood in the AIC formula yields:
AIC=nlog⁡(2π)+∑(−+2d
The first term of the above expression is sometimes discarded since it is a constant when is provided. In addition, it is sometimes stated that the AIC is equivalent to the statistic [[12]](https://scikit-learn.org/stable/modules/linear_model.html#id7). In a strict sense, however, it is equivalent only up to some constant and a multiplicative factor.
At last, we mentioned above that is an estimate of the noise variance. In [`LassoLarsIC`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLarsIC.html#sklearn.linear_model.LassoLarsIC "sklearn.linear_model.LassoLarsIC") when the parameter `noise_variance` is not provided (default), the noise variance is estimated via the unbiased estimator [[13]](https://scikit-learn.org/stable/modules/linear_model.html#id8) defined as:
=∑(−
where is the number of features and is the predicted target using an ordinary least squares regression. Note, that this formula is valid only when `n_samples  n_features`.
References
####  1.1.3.2.4. Comparison with the regularization parameter of SVM[#](https://scikit-learn.org/stable/modules/linear_model.html#comparison-with-the-regularization-parameter-of-svm "Link to this heading")
The equivalence between `alpha` and the regularization parameter of SVM, is given by `alpha = 1 / C` or `alpha = 1 / (n_samples * C)`, depending on the estimator and the exact objective function optimized by the model.
##  1.1.4. Multi-task Lasso[#](https://scikit-learn.org/stable/modules/linear_model.html#multi-task-lasso "Link to this heading")
The [`MultiTaskLasso`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.MultiTaskLasso.html#sklearn.linear_model.MultiTaskLasso "sklearn.linear_model.MultiTaskLasso") is a linear model that estimates sparse coefficients for multiple regression problems jointly: is a 2D array, of shape `(n_samples, n_tasks)`. The constraint is that the selected features are the same for all the regression problems, also called tasks.
The following figure compares the location of the non-zero entries in the coefficient matrix W obtained with a simple Lasso or a MultiTaskLasso. The Lasso estimates yield scattered non-zeros while the non-zeros of the MultiTaskLasso are full columns.
**Fitting a time-series model, imposing that any active feature be active at all times.**
Examples
  * [Joint feature selection with multi-task Lasso](https://scikit-learn.org/stable/auto_examples/linear_model/plot_multi_task_lasso_support.html#sphx-glr-auto-examples-linear-model-plot-multi-task-lasso-support-py)

Mathematical details[#](https://scikit-learn.org/stable/modules/linear_model.html#mathematical-details-3 "Link to this dropdown")
Mathematically, it consists of a linear model trained with a mixed -norm for regularization. The objective function to minimize is:
min12nsamplesXW−YFro2+αW
where indicates the Frobenius norm
|AFro=a2
and reads
|A=a2.
The implementation in the class [`MultiTaskLasso`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.MultiTaskLasso.html#sklearn.linear_model.MultiTaskLasso "sklearn.linear_model.MultiTaskLasso") uses coordinate descent as the algorithm to fit the coefficients.
##  1.1.5. Elastic-Net[#](https://scikit-learn.org/stable/modules/linear_model.html#elastic-net "Link to this heading")
[`ElasticNet`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html#sklearn.linear_model.ElasticNet "sklearn.linear_model.ElasticNet") is a linear regression model trained with both and -norm regularization of the coefficients. This combination allows for learning a sparse model where few of the weights are non-zero like [`Lasso`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html#sklearn.linear_model.Lasso "sklearn.linear_model.Lasso"), while still maintaining the regularization properties of [`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge"). We control the convex combination of and using the `l1_ratio` parameter.
Elastic-net is useful when there are multiple features that are correlated with one another. Lasso is likely to pick one of these at random, while elastic-net is likely to pick both.
A practical advantage of trading-off between Lasso and Ridge is that it allows Elastic-Net to inherit some of Ridge’s stability under rotation.
The objective function to minimize is in this case
min12nsamplesXw−y+αρw+α(1−ρ)2w
The class [`ElasticNetCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNetCV.html#sklearn.linear_model.ElasticNetCV "sklearn.linear_model.ElasticNetCV") can be used to set the parameters `alpha` () and `l1_ratio` () by cross-validation.
Examples
  * [L1-based models for Sparse Signals](https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_and_elasticnet.html#sphx-glr-auto-examples-linear-model-plot-lasso-and-elasticnet-py)
  * [Lasso, Lasso-LARS, and Elastic Net paths](https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_lasso_lars_elasticnet_path.html#sphx-glr-auto-examples-linear-model-plot-lasso-lasso-lars-elasticnet-path-py)
  * [Fitting an Elastic Net with a precomputed Gram Matrix and Weighted Samples](https://scikit-learn.org/stable/auto_examples/linear_model/plot_elastic_net_precomputed_gram_matrix_with_weighted_samples.html#sphx-glr-auto-examples-linear-model-plot-elastic-net-precomputed-gram-matrix-with-weighted-samples-py)

References[#](https://scikit-learn.org/stable/modules/linear_model.html#references-4 "Link to this dropdown")
The following two references explain the iterations used in the coordinate descent solver of scikit-learn, as well as the duality gap computation used for convergence control.
  * “Regularization Path For Generalized linear Models by Coordinate Descent”, Friedman, Hastie & Tibshirani, J Stat Softw, 2010 ([Paper](https://www.jstatsoft.org/article/view/v033i01/v33i01.pdf)).
  * “An Interior-Point Method for Large-Scale L1-Regularized Least Squares,” S. J. Kim, K. Koh, M. Lustig, S. Boyd and D. Gorinevsky, in IEEE Journal of Selected Topics in Signal Processing, 2007 ([Paper](https://web.stanford.edu/~boyd/papers/pdf/l1_ls.pdf))


##  1.1.6. Multi-task Elastic-Net[#](https://scikit-learn.org/stable/modules/linear_model.html#multi-task-elastic-net "Link to this heading")
The [`MultiTaskElasticNet`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.MultiTaskElasticNet.html#sklearn.linear_model.MultiTaskElasticNet "sklearn.linear_model.MultiTaskElasticNet") is an elastic-net model that estimates sparse coefficients for multiple regression problems jointly: is a 2D array of shape `(n_samples, n_tasks)`. The constraint is that the selected features are the same for all the regression problems, also called tasks.
Mathematically, it consists of a linear model trained with a mixed -norm and -norm for regularization. The objective function to minimize is:
min12nsamplesXW−YFro2+αρW+α(1−ρ)2W|Fro2
The implementation in the class [`MultiTaskElasticNet`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.MultiTaskElasticNet.html#sklearn.linear_model.MultiTaskElasticNet "sklearn.linear_model.MultiTaskElasticNet") uses coordinate descent as the algorithm to fit the coefficients.
The class [`MultiTaskElasticNetCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.MultiTaskElasticNetCV.html#sklearn.linear_model.MultiTaskElasticNetCV "sklearn.linear_model.MultiTaskElasticNetCV") can be used to set the parameters `alpha` () and `l1_ratio` () by cross-validation.
##  1.1.7. Least Angle Regression[#](https://scikit-learn.org/stable/modules/linear_model.html#least-angle-regression "Link to this heading")
Least-angle regression (LARS) is a regression algorithm for high-dimensional data, developed by Bradley Efron, Trevor Hastie, Iain Johnstone and Robert Tibshirani. LARS is similar to forward stepwise regression. At each step, it finds the feature most correlated with the target. When there are multiple features having equal correlation, instead of continuing along the same feature, it proceeds in a direction equiangular between the features.
The advantages of LARS are:
  * It is numerically efficient in contexts where the number of features is significantly greater than the number of samples.
  * It is computationally just as fast as forward selection and has the same order of complexity as ordinary least squares.
  * It produces a full piecewise linear solution path, which is useful in cross-validation or similar attempts to tune the model.
  * If two features are almost equally correlated with the target, then their coefficients should increase at approximately the same rate. The algorithm thus behaves as intuition would expect, and also is more stable.
  * It is easily modified to produce solutions for other estimators, like the Lasso.


The disadvantages of the LARS method include:
  * Because LARS is based upon an iterative refitting of the residuals, it would appear to be especially sensitive to the effects of noise. This problem is discussed in detail by Weisberg in the discussion section of the Efron et al. (2004) Annals of Statistics article.


The LARS model can be used via the estimator , or its low-level implementation [`lars_path`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.lars_path.html#sklearn.linear_model.lars_path "sklearn.linear_model.lars_path") or [`lars_path_gram`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.lars_path_gram.html#sklearn.linear_model.lars_path_gram "sklearn.linear_model.lars_path_gram").
##  1.1.8. LARS Lasso[#](https://scikit-learn.org/stable/modules/linear_model.html#lars-lasso "Link to this heading")
[`LassoLars`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLars.html#sklearn.linear_model.LassoLars "sklearn.linear_model.LassoLars") is a lasso model implemented using the LARS algorithm, and unlike the implementation based on coordinate descent, this yields the exact solution, which is piecewise linear as a function of the norm of its coefficients.

```
>>> fromsklearnimport linear_model
>>> reg = linear_model.LassoLars(alpha=.1)
>>> reg.fit([[0, 0], [1, 1]], [0, 1])
LassoLars(alpha=0.1)
>>> reg.coef_
array([0.6, 0.        ])

```
Copy to clipboard
Examples
  * [Lasso, Lasso-LARS, and Elastic Net paths](https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_lasso_lars_elasticnet_path.html#sphx-glr-auto-examples-linear-model-plot-lasso-lasso-lars-elasticnet-path-py)


The LARS algorithm provides the full path of the coefficients along the regularization parameter almost for free, thus a common operation is to retrieve the path with one of the functions [`lars_path`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.lars_path.html#sklearn.linear_model.lars_path "sklearn.linear_model.lars_path") or [`lars_path_gram`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.lars_path_gram.html#sklearn.linear_model.lars_path_gram "sklearn.linear_model.lars_path_gram").
Mathematical formulation[#](https://scikit-learn.org/stable/modules/linear_model.html#mathematical-formulation "Link to this dropdown")
The algorithm is similar to forward stepwise regression, but instead of including features at each step, the estimated coefficients are increased in a direction equiangular to each one’s correlations with the residual.
Instead of giving a vector result, the LARS solution consists of a curve denoting the solution for each value of the norm of the parameter vector. The full coefficients path is stored in the array `coef_path_` of shape `(n_features, max_features + 1)`. The first column is always zero.
References
  * Original Algorithm is detailed in the paper [Least Angle Regression](https://hastie.su.domains/Papers/LARS/LeastAngle_2002.pdf) by Hastie et al.


##  1.1.9. Orthogonal Matching Pursuit (OMP)[#](https://scikit-learn.org/stable/modules/linear_model.html#orthogonal-matching-pursuit-omp "Link to this heading")
[`OrthogonalMatchingPursuit`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.OrthogonalMatchingPursuit.html#sklearn.linear_model.OrthogonalMatchingPursuit "sklearn.linear_model.OrthogonalMatchingPursuit") and [`orthogonal_mp`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.orthogonal_mp.html#sklearn.linear_model.orthogonal_mp "sklearn.linear_model.orthogonal_mp") implement the OMP algorithm for approximating the fit of a linear model with constraints imposed on the number of non-zero coefficients (i.e. the pseudo-norm).
Being a forward feature selection method like [Least Angle Regression](https://scikit-learn.org/stable/modules/linear_model.html#least-angle-regression), orthogonal matching pursuit can approximate the optimum solution vector with a fixed number of non-zero elements:
argminwy−Xw subject to w≤nnonzero_coefs
Alternatively, orthogonal matching pursuit can target a specific error instead of a specific number of non-zero coefficients. This can be expressed as:
argminww subject to y−Xw≤tol
OMP is based on a greedy algorithm that includes at each step the atom most highly correlated with the current residual. It is similar to the simpler matching pursuit (MP) method, but better in that at each iteration, the residual is recomputed using an orthogonal projection on the space of the previously chosen dictionary elements.
Examples
  * [Orthogonal Matching Pursuit](https://scikit-learn.org/stable/auto_examples/linear_model/plot_omp.html#sphx-glr-auto-examples-linear-model-plot-omp-py)

References[#](https://scikit-learn.org/stable/modules/linear_model.html#references-5 "Link to this dropdown")
  * <https://www.cs.technion.ac.il/~ronrubin/Publications/KSVD-OMP-v2.pdf>
  * [Matching pursuits with time-frequency dictionaries](https://www.di.ens.fr/~mallat/papiers/MallatPursuit93.pdf), S. G. Mallat, Z. Zhang, 1993.


##  1.1.10. Bayesian Regression[#](https://scikit-learn.org/stable/modules/linear_model.html#bayesian-regression "Link to this heading")
Bayesian regression techniques can be used to include regularization parameters in the estimation procedure: the regularization parameter is not set in a hard sense but tuned to the data at hand.
This can be done by introducing [uninformative priors](https://en.wikipedia.org/wiki/Non-informative_prior#Uninformative_priors) over the hyper parameters of the model. The regularization used in [Ridge regression and classification](https://scikit-learn.org/stable/modules/linear_model.html#ridge-regression) is equivalent to finding a maximum a posteriori estimation under a Gaussian prior over the coefficients with precision . Instead of setting `lambda` manually, it is possible to treat it as a random variable to be estimated from the data.
To obtain a fully probabilistic model, the output is assumed to be Gaussian distributed around :
p(yX,w,α)=(yXw,)
where is again treated as a random variable that is to be estimated from the data.
The advantages of Bayesian Regression are:
  * It adapts to the data at hand.
  * It can be used to include regularization parameters in the estimation procedure.


The disadvantages of Bayesian regression include:
  * Inference of the model can be time consuming.

References[#](https://scikit-learn.org/stable/modules/linear_model.html#references-6 "Link to this dropdown")
  * A good introduction to Bayesian methods is given in [C. Bishop: Pattern Recognition and Machine Learning](https://www.microsoft.com/en-us/research/wp-content/uploads/2006/01/Bishop-Pattern-Recognition-and-Machine-Learning-2006.pdf).
  * Original Algorithm is detailed in the book [Bayesian learning for neural networks](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=db869fa192a3222ae4f2d766674a378e47013b1b) by Radford M. Neal.


###  1.1.10.1. Bayesian Ridge Regression[#](https://scikit-learn.org/stable/modules/linear_model.html#bayesian-ridge-regression "Link to this heading")
[`BayesianRidge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.BayesianRidge.html#sklearn.linear_model.BayesianRidge "sklearn.linear_model.BayesianRidge") estimates a probabilistic model of the regression problem as described above. The prior for the coefficient is given by a spherical Gaussian:
p(wλ)=(w0,)
The priors over and are chosen to be [gamma distributions](https://en.wikipedia.org/wiki/Gamma_distribution), the conjugate prior for the precision of the Gaussian. The resulting model is called _Bayesian Ridge Regression_ , and is similar to the classical [`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge").
The parameters , and are estimated jointly during the fit of the model, the regularization parameters and being estimated by maximizing the _log marginal likelihood_. The scikit-learn implementation is based on the algorithm described in Appendix A of (Tipping, 2001) where the update of the parameters and is done as suggested in (MacKay, 1992). The initial value of the maximization procedure can be set with the hyperparameters `alpha_init` and `lambda_init`.
There are four more hyperparameters, , , and of the gamma prior distributions over and . These are usually chosen to be _non-informative_. By default ====10.
Bayesian Ridge Regression is used for regression:

```
>>> fromsklearnimport linear_model
>>> X = [[0., 0.], [1., 1.], [2., 2.], [3., 3.]]
>>> Y = [0., 1., 2., 3.]
>>> reg = linear_model.BayesianRidge()
>>> reg.fit(X, Y)
BayesianRidge()

```
Copy to clipboard
After being fitted, the model can then be used to predict new values:

```
>>> reg.predict([[1, 0.]])
array([0.50000013])

```
Copy to clipboard
The coefficients of the model can be accessed:

```
>>> reg.coef_
array([0.49999993, 0.49999993])

```
Copy to clipboard
Due to the Bayesian framework, the weights found are slightly different from the ones found by [Ordinary Least Squares](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares). However, Bayesian Ridge Regression is more robust to ill-posed problems.
Examples
  * [Curve Fitting with Bayesian Ridge Regression](https://scikit-learn.org/stable/auto_examples/linear_model/plot_bayesian_ridge_curvefit.html#sphx-glr-auto-examples-linear-model-plot-bayesian-ridge-curvefit-py)

References[#](https://scikit-learn.org/stable/modules/linear_model.html#references-7 "Link to this dropdown")
  * Section 3.3 in Christopher M. Bishop: Pattern Recognition and Machine Learning, 2006
  * David J. C. MacKay, [Bayesian Interpolation](https://citeseerx.ist.psu.edu/doc_view/pid/b14c7cc3686e82ba40653c6dff178356a33e5e2c), 1992.
  * Michael E. Tipping, [Sparse Bayesian Learning and the Relevance Vector Machine](https://www.jmlr.org/papers/volume1/tipping01a/tipping01a.pdf), 2001.


###  1.1.10.2. Automatic Relevance Determination - ARD[#](https://scikit-learn.org/stable/modules/linear_model.html#automatic-relevance-determination-ard "Link to this heading")
The Automatic Relevance Determination (as being implemented in [`ARDRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ARDRegression.html#sklearn.linear_model.ARDRegression "sklearn.linear_model.ARDRegression")) is a kind of linear model which is very similar to the [Bayesian Ridge Regression](https://scikit-learn.org/stable/modules/linear_model.html#id15), but that leads to sparser coefficients .
[`ARDRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ARDRegression.html#sklearn.linear_model.ARDRegression "sklearn.linear_model.ARDRegression") poses a different prior over : it drops the spherical Gaussian distribution for a centered elliptic Gaussian distribution. This means each coefficient can itself be drawn from a Gaussian distribution, centered on zero and with a precision :
p(wλ)=(w0,)
with being a positive definite diagonal matrix and diag(A)=λ={,...,}.
In contrast to the [Bayesian Ridge Regression](https://scikit-learn.org/stable/modules/linear_model.html#id15), each coordinate of has its own standard deviation . The prior over all is chosen to be the same gamma distribution given by the hyperparameters and .
ARD is also known in the literature as _Sparse Bayesian Learning_ and _Relevance Vector Machine_ .
See [Comparing Linear Bayesian Regressors](https://scikit-learn.org/stable/auto_examples/linear_model/plot_ard.html#sphx-glr-auto-examples-linear-model-plot-ard-py) for a worked-out comparison between ARD and [Bayesian Ridge Regression](https://scikit-learn.org/stable/modules/linear_model.html#id15).
See [L1-based models for Sparse Signals](https://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_and_elasticnet.html#sphx-glr-auto-examples-linear-model-plot-lasso-and-elasticnet-py) for a comparison between various methods - Lasso, ARD and ElasticNet - on correlated data.
References
##  1.1.11. Logistic regression[#](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression "Link to this heading")
The logistic regression is implemented in [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression "sklearn.linear_model.LogisticRegression"). Despite its name, it is implemented as a linear model for classification rather than regression in terms of the scikit-learn/ML nomenclature. The logistic regression is also known in the literature as logit regression, maximum-entropy classification (MaxEnt) or the log-linear classifier. In this model, the probabilities describing the possible outcomes of a single trial are modeled using a [logistic function](https://en.wikipedia.org/wiki/Logistic_function).
This implementation can fit binary, One-vs-Rest, or multinomial logistic regression with optional , or Elastic-Net regularization.
Note
**Regularization**
Regularization is applied by default, which is common in machine learning but not in statistics. Another advantage of regularization is that it improves numerical stability. No regularization amounts to setting C to a very high value.
Note
**Logistic Regression as a special case of the Generalized Linear Models (GLM)**
Logistic regression is a special case of [Generalized Linear Models](https://scikit-learn.org/stable/modules/linear_model.html#generalized-linear-models) with a Binomial / Bernoulli conditional distribution and a Logit link. The numerical output of the logistic regression, which is the predicted probability, can be used as a classifier by applying a threshold (by default 0.5) to it. This is how it is implemented in scikit-learn, so it expects a categorical target, making the Logistic Regression a classifier.
Examples
  * [L1 Penalty and Sparsity in Logistic Regression](https://scikit-learn.org/stable/auto_examples/linear_model/plot_logistic_l1_l2_sparsity.html#sphx-glr-auto-examples-linear-model-plot-logistic-l1-l2-sparsity-py)
  * [Regularization path of L1- Logistic Regression](https://scikit-learn.org/stable/auto_examples/linear_model/plot_logistic_path.html#sphx-glr-auto-examples-linear-model-plot-logistic-path-py)
  * [Decision Boundaries of Multinomial and One-vs-Rest Logistic Regression](https://scikit-learn.org/stable/auto_examples/linear_model/plot_logistic_multinomial.html#sphx-glr-auto-examples-linear-model-plot-logistic-multinomial-py)
  * [Multiclass sparse logistic regression on 20newgroups](https://scikit-learn.org/stable/auto_examples/linear_model/plot_sparse_logistic_regression_20newsgroups.html#sphx-glr-auto-examples-linear-model-plot-sparse-logistic-regression-20newsgroups-py)
  * [MNIST classification using multinomial logistic + L1](https://scikit-learn.org/stable/auto_examples/linear_model/plot_sparse_logistic_regression_mnist.html#sphx-glr-auto-examples-linear-model-plot-sparse-logistic-regression-mnist-py)
  * [Plot classification probability](https://scikit-learn.org/stable/auto_examples/classification/plot_classification_probability.html#sphx-glr-auto-examples-classification-plot-classification-probability-py)


###  1.1.11.1. Binary Case[#](https://scikit-learn.org/stable/modules/linear_model.html#binary-case "Link to this heading")
For notational ease, we assume that the target takes values in the set for data point . Once fitted, the [`predict_proba`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression.predict_proba "sklearn.linear_model.LogisticRegression.predict_proba") method of [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression "sklearn.linear_model.LogisticRegression") predicts the probability of the positive class P(=1) as
()=expit(w+)=11+exp⁡(−w−).
As an optimization problem, binary class logistic regression with regularization term minimizes the following cost function:
min∑n(−log⁡(())−(1−)log⁡(1−()))+r(w),
where corresponds to the weights assigned by the user to a specific training sample (the vector is formed by element-wise multiplication of the class weights and sample weights), and the sum S=∑n.
We currently provide four choices for the regularization or penalty term via the arguments and `l1_ratio`:  
| penalty  |  
| --- |  
| none (`C=np.inf`)  |  
|  (`l1_ratio=1`)  |  
|  (`l1_ratio=0`)  | ‖w=w  |  
| ElasticNet (`0<l1_ratio<1`)  | 2w+ρ‖w  |  
For ElasticNet, (which corresponds to the `l1_ratio` parameter) controls the strength of regularization vs. regularization. Elastic-Net is equivalent to when and equivalent to when .
Note that the scale of the class weights and the sample weights will influence the optimization problem. For instance, multiplying the sample weights by a constant is equivalent to multiplying the (inverse) regularization strength by .
###  1.1.11.2. Multinomial Case[#](https://scikit-learn.org/stable/modules/linear_model.html#multinomial-case "Link to this heading")
The binary case can be extended to classes leading to the multinomial logistic regression, see also [log-linear model](https://en.wikipedia.org/wiki/Multinomial_logistic_regression#As_a_log-linear_model).
Note
It is possible to parameterize a -class classification model using only weight vectors, leaving one class probability fully determined by the other class probabilities by leveraging the fact that all class probabilities must sum to one. We deliberately choose to overparameterize the model using weight vectors for ease of implementation and to preserve the symmetrical inductive bias regarding ordering of classes, see [[16]](https://scikit-learn.org/stable/modules/linear_model.html#id38). This effect becomes especially important when using regularization. The choice of overparameterization can be detrimental for unpenalized models since then the solution may not be unique, as shown in [[16]](https://scikit-learn.org/stable/modules/linear_model.html#id38).
Mathematical details[#](https://scikit-learn.org/stable/modules/linear_model.html#mathematical-details-4 "Link to this dropdown")
Let ∈{1,…,K} be the label (ordinal) encoded target variable for observation . Instead of a single coefficient vector, we now have a matrix of coefficients where each row vector corresponds to class . We aim at predicting the class probabilities P(=k) via [`predict_proba`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression.predict_proba "sklearn.linear_model.LogisticRegression.predict_proba") as:
()=exp⁡(+W)∑exp⁡(+W).
The objective for the optimization becomes
minW−∑n∑[=k]log⁡(())+r(W),
where represents the Iverson bracket which evaluates to if is false, otherwise it evaluates to .
Again, are the weights assigned by the user (multiplication of sample weights and class weights) with their sum S=∑n∑.
We currently provide four choices for the regularization or penalty term via the arguments and `l1_ratio`, where is the number of features:  
| penalty  |  
| --- |  
| none (`C=np.inf`)  |  
|  (`l1_ratio=1`)  | ‖W‖=∑m∑W|  |  
|  (`l1_ratio=0`)  | ‖W=∑m∑W2  |  
| ElasticNet (`0<l1_ratio<1`)  | 2‖W+ρ‖W‖  |  
###  1.1.11.3. Solvers[#](https://scikit-learn.org/stable/modules/linear_model.html#solvers "Link to this heading")
The solvers implemented in the class [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression "sklearn.linear_model.LogisticRegression") are “lbfgs”, “liblinear”, “newton-cg”, “newton-cholesky”, “sag” and “saga”:
The following table summarizes the penalties and multinomial multiclass supported by each solver:  
| **Solvers**  |  
| --- |  
| **Penalties**  | **‘lbfgs’**  | **‘liblinear’**  | **‘newton-cg’**  | **‘newton-cholesky’**  | **‘sag’**  | **‘saga’**  |  
| L2 penalty  | yes  | yes  | yes  | yes  | yes  | yes  |  
| L1 penalty  | no  | yes  | no  | no  | no  | yes  |  
| Elastic-Net (L1 + L2)  | no  | no  | no  | no  | no  | yes  |  
| No penalty  | yes  | no  | yes  | yes  | yes  | yes  |  
| **Multiclass support**  |  
| multinomial multiclass  | yes  | no  | yes  | yes  | yes  | yes  |  
| **Behaviors**  |  
| Penalize the intercept (bad)  | no  | yes  | no  | no  | no  | no  |  
| Faster for large datasets  | no  | no  | no  | no  | yes  | yes  |  
| Robust to unscaled datasets  | yes  | yes  | yes  | yes  | no  | no  |  
The “lbfgs” solver is used by default for its robustness. For `n_samples  n_features`, “newton-cholesky” is a good choice and can reach high precision (tiny `tol` values). For large datasets the “saga” solver is usually faster (than “lbfgs”), in particular for low precision (high `tol`). For large dataset, you may also consider using [`SGDClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html#sklearn.linear_model.SGDClassifier "sklearn.linear_model.SGDClassifier") with `loss="log_loss"`, which might be even faster but requires more tuning.
####  1.1.11.3.1. Differences between solvers[#](https://scikit-learn.org/stable/modules/linear_model.html#differences-between-solvers "Link to this heading")
There might be a difference in the scores obtained between [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression "sklearn.linear_model.LogisticRegression") with `solver=liblinear` or [`LinearSVC`](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC "sklearn.svm.LinearSVC") and the external liblinear library directly, when `fit_intercept=False` and the fit `coef_` (or) the data to be predicted are zeroes. This is because for the sample(s) with `decision_function` zero, [`LogisticRegression`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression "sklearn.linear_model.LogisticRegression") and [`LinearSVC`](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html#sklearn.svm.LinearSVC "sklearn.svm.LinearSVC") predict the negative class, while liblinear predicts the positive class. Note that a model with `fit_intercept=False` and having many samples with `decision_function` zero, is likely to be an underfit, bad model and you are advised to set `fit_intercept=True` and increase the `intercept_scaling`.
Solvers’ details[#](https://scikit-learn.org/stable/modules/linear_model.html#solvers%E2%80%99-details "Link to this dropdown")
  * The solver “liblinear” uses a coordinate descent (CD) algorithm, and relies on the excellent C++ [LIBLINEAR library](https://www.csie.ntu.edu.tw/~cjlin/liblinear/), which is shipped with scikit-learn. However, the CD algorithm implemented in liblinear cannot learn a true multinomial (multiclass) model. If you still want to use “liblinear” on multiclass problems, you can use a “one-vs-rest” scheme `OneVsRestClassifier(LogisticRegression(solver="liblinear"))`, see `:class:`~sklearn.multiclass.OneVsRestClassifier`. Note that minimizing the multinomial loss is expected to give better calibrated results as compared to a “one-vs-rest” scheme. For regularization [`sklearn.svm.l1_min_c`](https://scikit-learn.org/stable/modules/generated/sklearn.svm.l1_min_c.html#sklearn.svm.l1_min_c "sklearn.svm.l1_min_c") allows to calculate the lower bound for C in order to get a non “null” (all feature weights to zero) model.
  * The “lbfgs”, “newton-cg”, “newton-cholesky” and “sag” solvers only support regularization or no regularization, and are found to converge faster for some high-dimensional data. These solvers (and “saga”) learn a true multinomial logistic regression model .
  * The “sag” solver uses Stochastic Average Gradient descent . It is faster than other solvers for large datasets, when both the number of samples and the number of features are large.
  * The “saga” solver is a variant of “sag” that also supports the non-smooth penalty (`l1_ratio=1`). This is therefore the solver of choice for sparse multinomial logistic regression. It is also the only solver that supports Elastic-Net (`0  l1_ratio  1`).
  * The “lbfgs” is an optimization algorithm that approximates the Broyden–Fletcher–Goldfarb–Shanno algorithm , which belongs to quasi-Newton methods. As such, it can deal with a wide range of different training data and is therefore the default solver. Its performance, however, suffers on poorly scaled datasets and on datasets with one-hot encoded categorical features with rare categories.
  * The “newton-cholesky” solver is an exact Newton solver that calculates the Hessian matrix and solves the resulting linear system. It is a very good choice for `n_samples` >> `n_features` and can reach high precision (tiny values of `tol`), but has a few shortcomings: Only regularization is supported. Furthermore, because the Hessian matrix is explicitly computed, the memory usage has a quadratic dependency on `n_features` as well as on `n_classes`.


For a comparison of some of these solvers, see .
References
Note
**Feature selection with sparse logistic regression**
A logistic regression with penalty yields sparse models, and can thus be used to perform feature selection, as detailed in [L1-based feature selection](https://scikit-learn.org/stable/modules/feature_selection.html#l1-feature-selection).
Note
**P-value estimation**
It is possible to obtain the p-values and confidence intervals for coefficients in cases of regression without penalization. The [statsmodels package](https://pypi.org/project/statsmodels/) natively supports this. Within sklearn, one could use bootstrapping instead as well.
[`LogisticRegressionCV`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegressionCV.html#sklearn.linear_model.LogisticRegressionCV "sklearn.linear_model.LogisticRegressionCV") implements Logistic Regression with built-in cross-validation support, to find the optimal and `l1_ratio` parameters according to the `scoring` attribute. The “newton-cg”, “sag”, “saga” and “lbfgs” solvers are found to be faster for high-dimensional dense data, due to warm-starting (see [Glossary](https://scikit-learn.org/stable/glossary.html#term-warm_start)).
##  1.1.12. Generalized Linear Models[#](https://scikit-learn.org/stable/modules/linear_model.html#generalized-linear-models "Link to this heading")
Generalized Linear Models (GLM) extend linear models in two ways [[10]](https://scikit-learn.org/stable/modules/linear_model.html#id42). First, the predicted values are linked to a linear combination of the input variables via an inverse link function as
(w,X)=h(Xw).
Secondly, the squared loss function is replaced by the unit deviance of a distribution in the exponential family (or more precisely, a reproductive exponential dispersion model (EDM) [[11]](https://scikit-learn.org/stable/modules/linear_model.html#id43)).
The minimization problem becomes:
min12nsamplesd(,)+w,
where is the L2 regularization penalty. When sample weights are provided, the average becomes a weighted average.
The following table lists some specific EDMs and their unit deviance :  
| Distribution  | Target Domain  | Unit Deviance d(y,)  |  
| --- | --- | --- |  
| Normal  | y∈(−∞,∞)  | (y−  |  
| Bernoulli  | y∈{0,1}  | 2(log⁡+(−)log⁡−)  |  
| Categorical  | y∈{0,1,...,k}  | 2∑i∈{0,1,...,k}I(y=i)log⁡I(y=i)I(y=i)^  |  
| Poisson  | y∈[0,∞)  | 2(ylog⁡−y+)  |  
| Gamma  | y∈(0,∞)  | 2(log⁡+−1)  |  
| Inverse Gaussian  | y∈(0,∞)  | (y−y  |  
The Probability Density Functions (PDF) of these distributions are illustrated in the following figure,
PDF of a random variable Y following Poisson, Tweedie (power=1.5) and Gamma distributions with different mean values (). Observe the point mass at for the Poisson distribution and the Tweedie (power=1.5) distribution, but not for the Gamma distribution which has a strictly positive target domain.[#](https://scikit-learn.org/stable/modules/linear_model.html#id49 "Link to this image")
The Bernoulli distribution is a discrete probability distribution modelling a Bernoulli trial - an event that has only two mutually exclusive outcomes. The Categorical distribution is a generalization of the Bernoulli distribution for a categorical random variable. While a random variable in a Bernoulli distribution has two possible outcomes, a Categorical random variable can take on one of K possible categories, with the probability of each category specified separately.
The choice of the distribution depends on the problem at hand:
  * If the target values are counts (non-negative integer valued) or relative frequencies (non-negative), you might use a Poisson distribution with a log-link.
  * If the target values are positive valued and skewed, you might try a Gamma distribution with a log-link.
  * If the target values seem to be heavier tailed than a Gamma distribution, you might try an Inverse Gaussian distribution (or even higher variance powers of the Tweedie family).
  * If the target values are probabilities, you can use the Bernoulli distribution. The Bernoulli distribution with a logit link can be used for binary classification. The Categorical distribution with a softmax link can be used for multiclass classification.

Examples of use cases[#](https://scikit-learn.org/stable/modules/linear_model.html#examples-of-use-cases "Link to this dropdown")
  * Agriculture / weather modeling: number of rain events per year (Poisson), amount of rainfall per event (Gamma), total rainfall per year (Tweedie / Compound Poisson Gamma).
  * Risk modeling / insurance policy pricing: number of claim events / policyholder per year (Poisson), cost per event (Gamma), total cost per policyholder per year (Tweedie / Compound Poisson Gamma).
  * Credit Default: probability that a loan can’t be paid back (Bernoulli).
  * Fraud Detection: probability that a financial transaction like a cash transfer is a fraudulent transaction (Bernoulli).
  * Predictive maintenance: number of production interruption events per year (Poisson), duration of interruption (Gamma), total interruption time per year (Tweedie / Compound Poisson Gamma).
  * Medical Drug Testing: probability of curing a patient in a set of trials or probability that a patient will experience side effects (Bernoulli).
  * News Classification: classification of news articles into three categories namely Business News, Politics and Entertainment news (Categorical).


References
###  1.1.12.1. Usage[#](https://scikit-learn.org/stable/modules/linear_model.html#usage "Link to this heading")
[`TweedieRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.TweedieRegressor.html#sklearn.linear_model.TweedieRegressor "sklearn.linear_model.TweedieRegressor") implements a generalized linear model for the Tweedie distribution, that allows to model any of the above mentioned distributions using the appropriate `power` parameter. In particular:
  * `power = 0`: Normal distribution. Specific estimators such as [`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge"), [`ElasticNet`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html#sklearn.linear_model.ElasticNet "sklearn.linear_model.ElasticNet") are generally more appropriate in this case.
  * `power = 1`: Poisson distribution. [`PoissonRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PoissonRegressor.html#sklearn.linear_model.PoissonRegressor "sklearn.linear_model.PoissonRegressor") is exposed for convenience. However, it is strictly equivalent to `TweedieRegressor(power=1, link='log')`.
  * `power = 2`: Gamma distribution. [`GammaRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.GammaRegressor.html#sklearn.linear_model.GammaRegressor "sklearn.linear_model.GammaRegressor") is exposed for convenience. However, it is strictly equivalent to `TweedieRegressor(power=2, link='log')`.
  * `power = 3`: Inverse Gaussian distribution.


The link function is determined by the `link` parameter.
Usage example:

```
>>> fromsklearn.linear_modelimport TweedieRegressor
>>> reg = TweedieRegressor(power=1, alpha=0.5, link='log')
>>> reg.fit([[0, 0], [0, 1], [2, 2]], [0, 1, 2])
TweedieRegressor(alpha=0.5, link='log', power=1)
>>> reg.coef_
array([0.2463, 0.4337])
>>> reg.intercept_
np.float64(-0.7638)

```
Copy to clipboard
Examples
  * [Poisson regression and non-normal loss](https://scikit-learn.org/stable/auto_examples/linear_model/plot_poisson_regression_non_normal_loss.html#sphx-glr-auto-examples-linear-model-plot-poisson-regression-non-normal-loss-py)
  * [Tweedie regression on insurance claims](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html#sphx-glr-auto-examples-linear-model-plot-tweedie-regression-insurance-claims-py)

Practical considerations[#](https://scikit-learn.org/stable/modules/linear_model.html#practical-considerations "Link to this dropdown")
The feature matrix should be standardized before fitting. This ensures that the penalty treats features equally.
Since the linear predictor can be negative and Poisson, Gamma and Inverse Gaussian distributions don’t support negative values, it is necessary to apply an inverse link function that guarantees the non-negativeness. For example with `link='log'`, the inverse link function becomes h(Xw)=exp⁡(Xw).
If you want to model a relative frequency, i.e. counts per exposure (time, volume, …) you can do so by using a Poisson distribution and passing y=countsexposure as target values together with exposure as sample weights. For a concrete example see e.g. [Tweedie regression on insurance claims](https://scikit-learn.org/stable/auto_examples/linear_model/plot_tweedie_regression_insurance_claims.html#sphx-glr-auto-examples-linear-model-plot-tweedie-regression-insurance-claims-py).
When performing cross-validation for the `power` parameter of `TweedieRegressor`, it is advisable to specify an explicit `scoring` function, because the default scorer [`TweedieRegressor.score`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.TweedieRegressor.html#sklearn.linear_model.TweedieRegressor.score "sklearn.linear_model.TweedieRegressor.score") is a function of `power` itself.
##  1.1.13. Stochastic Gradient Descent - SGD[#](https://scikit-learn.org/stable/modules/linear_model.html#stochastic-gradient-descent-sgd "Link to this heading")
Stochastic gradient descent is a simple yet very efficient approach to fit linear models. It is particularly useful when the number of samples (and the number of features) is very large. The `partial_fit` method allows online/out-of-core learning.
The classes [`SGDClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html#sklearn.linear_model.SGDClassifier "sklearn.linear_model.SGDClassifier") and [`SGDRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html#sklearn.linear_model.SGDRegressor "sklearn.linear_model.SGDRegressor") provide functionality to fit linear models for classification and regression using different (convex) loss functions and different penalties. E.g., with `loss="log"`, [`SGDClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html#sklearn.linear_model.SGDClassifier "sklearn.linear_model.SGDClassifier") fits a logistic regression model, while with `loss="hinge"` it fits a linear support vector machine (SVM).
You can refer to the dedicated [Stochastic Gradient Descent](https://scikit-learn.org/stable/modules/sgd.html#sgd) documentation section for more details.
###  1.1.13.1. Perceptron[#](https://scikit-learn.org/stable/modules/linear_model.html#perceptron "Link to this heading")
The [`Perceptron`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html#sklearn.linear_model.Perceptron "sklearn.linear_model.Perceptron") is another simple classification algorithm suitable for large scale learning and derives from SGD. By default:
  * It does not require a learning rate.
  * It is not regularized (penalized).
  * It updates its model only on mistakes.


The last characteristic implies that the Perceptron is slightly faster to train than SGD with the hinge loss and that the resulting models are sparser.
In fact, the [`Perceptron`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html#sklearn.linear_model.Perceptron "sklearn.linear_model.Perceptron") is a wrapper around the [`SGDClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html#sklearn.linear_model.SGDClassifier "sklearn.linear_model.SGDClassifier") class using a perceptron loss and a constant learning rate. Refer to [mathematical section](https://scikit-learn.org/stable/modules/sgd.html#sgd-mathematical-formulation) of the SGD procedure for more details.
###  1.1.13.2. Passive Aggressive Algorithms[#](https://scikit-learn.org/stable/modules/linear_model.html#passive-aggressive-algorithms "Link to this heading")
The passive-aggressive (PA) algorithms are another family of 2 algorithms (PA-I and PA-II) for large-scale online learning that derive from SGD. They are similar to the Perceptron in that they do not require a learning rate. However, contrary to the Perceptron, they include a regularization parameter `eta0` ( in the reference paper).
For classification, `SGDClassifier(loss="hinge", penalty=None, learning_rate="pa1", eta0=1.0)` can be used for PA-I or with `learning_rate="pa2"` for PA-II. For regression, `SGDRegressor(loss="epsilon_insensitive", penalty=None, learning_rate="pa1", eta0=1.0)` can be used for PA-I or with `learning_rate="pa2"` for PA-II.
References[#](https://scikit-learn.org/stable/modules/linear_model.html#references-8 "Link to this dropdown")
  * [“Online Passive-Aggressive Algorithms”](https://jmlr.csail.mit.edu/papers/volume7/crammer06a/crammer06a.pdf) K. Crammer, O. Dekel, J. Keshat, S. Shalev-Shwartz, Y. Singer - JMLR 7 (2006)


##  1.1.14. Robustness regression: outliers and modeling errors[#](https://scikit-learn.org/stable/modules/linear_model.html#robustness-regression-outliers-and-modeling-errors "Link to this heading")
Robust regression aims to fit a regression model in the presence of corrupt data: either outliers, or error in the model.
###  1.1.14.1. Different scenario and useful concepts[#](https://scikit-learn.org/stable/modules/linear_model.html#different-scenario-and-useful-concepts "Link to this heading")
There are different things to keep in mind when dealing with data corrupted by outliers:
  * **Outliers in X or in y**?  
| Outliers in the y direction  | Outliers in the X direction  |  
| --- | --- |  
  * **Fraction of outliers versus amplitude of error**
The number of outlying points matters, but also how much they are outliers.  
| Small outliers  | Large outliers  |  
| --- | --- |  


An important notion of robust fitting is that of breakdown point: the fraction of data that can be outlying for the fit to start missing the inlying data.
Note that in general, robust fitting in high-dimensional setting (large `n_features`) is very hard. The robust models here will probably not work in these settings.
###  1.1.14.2. RANSAC: RANdom SAmple Consensus[#](https://scikit-learn.org/stable/modules/linear_model.html#ransac-random-sample-consensus "Link to this heading")
RANSAC (RANdom SAmple Consensus) fits a model from random subsets of inliers from the complete data set.
RANSAC is a non-deterministic algorithm producing only a reasonable result with a certain probability, which is dependent on the number of iterations (see `max_trials` parameter). It is typically used for linear and non-linear regression problems and is especially popular in the field of photogrammetric computer vision.
The algorithm splits the complete input sample data into a set of inliers, which may be subject to noise, and outliers, which are e.g. caused by erroneous measurements or invalid hypotheses about the data. The resulting model is then estimated only from the determined inliers.
Examples
  * [Robust linear model estimation using RANSAC](https://scikit-learn.org/stable/auto_examples/linear_model/plot_ransac.html#sphx-glr-auto-examples-linear-model-plot-ransac-py)
  * [Robust linear estimator fitting](https://scikit-learn.org/stable/auto_examples/linear_model/plot_robust_fit.html#sphx-glr-auto-examples-linear-model-plot-robust-fit-py)

Details of the algorithm[#](https://scikit-learn.org/stable/modules/linear_model.html#details-of-the-algorithm "Link to this dropdown")
Each iteration performs the following steps:
  1. Select `min_samples` random samples from the original data and check whether the set of data is valid (see `is_data_valid`).
  2. Fit a model to the random subset (`estimator.fit`) and check whether the estimated model is valid (see `is_model_valid`).
  3. Classify all data as inliers or outliers by calculating the residuals to the estimated model (`estimator.predict(X) - y`) - all data samples with absolute residuals smaller than or equal to the `residual_threshold` are considered as inliers.
  4. Save fitted model as best model if number of inlier samples is maximal. In case the current estimated model has the same number of inliers, it is only considered as the best model if it has better score.


These steps are performed either a maximum number of times (`max_trials`) or until one of the special stop criteria are met (see `stop_n_inliers` and `stop_score`). The final model is estimated using all inlier samples (consensus set) of the previously determined best model.
The `is_data_valid` and `is_model_valid` functions allow to identify and reject degenerate combinations of random sub-samples. If the estimated model is not needed for identifying degenerate cases, `is_data_valid` should be used as it is called prior to fitting the model and thus leading to better computational performance.
References[#](https://scikit-learn.org/stable/modules/linear_model.html#references-9 "Link to this dropdown")
  * <https://en.wikipedia.org/wiki/RANSAC>
  * [“Random Sample Consensus: A Paradigm for Model Fitting with Applications to Image Analysis and Automated Cartography”](https://www.cs.ait.ac.th/~mdailey/cvreadings/Fischler-RANSAC.pdf) Martin A. Fischler and Robert C. Bolles - SRI International (1981)
  * [“Performance Evaluation of RANSAC Family”](http://www.bmva.org/bmvc/2009/Papers/Paper355/Paper355.pdf) Sunglok Choi, Taemin Kim and Wonpil Yu - BMVC (2009)


###  1.1.14.3. Theil-Sen estimator: generalized-median-based estimator[#](https://scikit-learn.org/stable/modules/linear_model.html#theil-sen-estimator-generalized-median-based-estimator "Link to this heading")
The [`TheilSenRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.TheilSenRegressor.html#sklearn.linear_model.TheilSenRegressor "sklearn.linear_model.TheilSenRegressor") estimator uses a generalization of the median in multiple dimensions. It is thus robust to multivariate outliers. Note however that the robustness of the estimator decreases quickly with the dimensionality of the problem. It loses its robustness properties and becomes no better than an ordinary least squares in high dimension.
Examples
  * [Theil-Sen Regression](https://scikit-learn.org/stable/auto_examples/linear_model/plot_theilsen.html#sphx-glr-auto-examples-linear-model-plot-theilsen-py)
  * [Robust linear estimator fitting](https://scikit-learn.org/stable/auto_examples/linear_model/plot_robust_fit.html#sphx-glr-auto-examples-linear-model-plot-robust-fit-py)

Theoretical considerations[#](https://scikit-learn.org/stable/modules/linear_model.html#theoretical-considerations "Link to this dropdown")
[`TheilSenRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.TheilSenRegressor.html#sklearn.linear_model.TheilSenRegressor "sklearn.linear_model.TheilSenRegressor") is comparable to the [Ordinary Least Squares (OLS)](https://scikit-learn.org/stable/modules/linear_model.html#ordinary-least-squares) in terms of asymptotic efficiency and as an unbiased estimator. In contrast to OLS, Theil-Sen is a non-parametric method which means it makes no assumption about the underlying distribution of the data. Since Theil-Sen is a median-based estimator, it is more robust against corrupted data aka outliers. In univariate setting, Theil-Sen has a breakdown point of about 29.3% in case of a simple linear regression which means that it can tolerate arbitrary corrupted data of up to 29.3%.
The implementation of [`TheilSenRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.TheilSenRegressor.html#sklearn.linear_model.TheilSenRegressor "sklearn.linear_model.TheilSenRegressor") in scikit-learn follows a generalization to a multivariate linear regression model [[14]](https://scikit-learn.org/stable/modules/linear_model.html#f1) using the spatial median which is a generalization of the median to multiple dimensions [[15]](https://scikit-learn.org/stable/modules/linear_model.html#f2).
In terms of time and space complexity, Theil-Sen scales according to
nsamplesnsubsamples
which makes it infeasible to be applied exhaustively to problems with a large number of samples and features. Therefore, the magnitude of a subpopulation can be chosen to limit the time and space complexity by considering only a random subset of all possible combinations.
References
Also see the [Wikipedia page](https://en.wikipedia.org/wiki/Theil%E2%80%93Sen_estimator)
###  1.1.14.4. Huber Regression[#](https://scikit-learn.org/stable/modules/linear_model.html#huber-regression "Link to this heading")
The [`HuberRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html#sklearn.linear_model.HuberRegressor "sklearn.linear_model.HuberRegressor") is different from [`Ridge`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html#sklearn.linear_model.Ridge "sklearn.linear_model.Ridge") because it applies a linear loss to samples that are defined as outliers by the `epsilon` parameter. A sample is classified as an inlier if the absolute error of that sample is less than the threshold `epsilon`. It differs from [`TheilSenRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.TheilSenRegressor.html#sklearn.linear_model.TheilSenRegressor "sklearn.linear_model.TheilSenRegressor") and [`RANSACRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RANSACRegressor.html#sklearn.linear_model.RANSACRegressor "sklearn.linear_model.RANSACRegressor") because it does not ignore the effect of the outliers but gives a lesser weight to them.
Examples
  * [HuberRegressor vs Ridge on dataset with strong outliers](https://scikit-learn.org/stable/auto_examples/linear_model/plot_huber_vs_ridge.html#sphx-glr-auto-examples-linear-model-plot-huber-vs-ridge-py)

Mathematical details[#](https://scikit-learn.org/stable/modules/linear_model.html#mathematical-details-5 "Link to this dropdown")
[`HuberRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html#sklearn.linear_model.HuberRegressor "sklearn.linear_model.HuberRegressor") minimizes
min∑n(σ+(w−σ)σ)+α|w2
where the loss function is given by
(z)={if |zϵ,2ϵz−,otherwise
It is advised to set the parameter `epsilon` to 1.35 to achieve 95% statistical efficiency.
References
  * Peter J. Huber, Elvezio M. Ronchetti: Robust Statistics, Concomitant scale estimates, p. 172.


The [`HuberRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html#sklearn.linear_model.HuberRegressor "sklearn.linear_model.HuberRegressor") differs from using [`SGDRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html#sklearn.linear_model.SGDRegressor "sklearn.linear_model.SGDRegressor") with loss set to `huber` in the following ways.
  * [`HuberRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html#sklearn.linear_model.HuberRegressor "sklearn.linear_model.HuberRegressor") is scaling invariant. Once `epsilon` is set, scaling and down or up by different values would produce the same robustness to outliers as before. as compared to [`SGDRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html#sklearn.linear_model.SGDRegressor "sklearn.linear_model.SGDRegressor") where `epsilon` has to be set again when and are scaled.
  * [`HuberRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html#sklearn.linear_model.HuberRegressor "sklearn.linear_model.HuberRegressor") should be more efficient to use on data with small number of samples while [`SGDRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html#sklearn.linear_model.SGDRegressor "sklearn.linear_model.SGDRegressor") needs a number of passes on the training data to produce the same robustness.


Note that this estimator is different from the [R implementation of Robust Regression](https://stats.oarc.ucla.edu/r/dae/robust-regression/) because the R implementation does a weighted least squares implementation with weights given to each sample on the basis of how much the residual is greater than a certain threshold.
##  1.1.15. Quantile Regression[#](https://scikit-learn.org/stable/modules/linear_model.html#quantile-regression "Link to this heading")
Quantile regression estimates the median or other quantiles of conditional on , while ordinary least squares (OLS) estimates the conditional mean.
Quantile regression may be useful if one is interested in predicting an interval instead of point prediction. Sometimes, prediction intervals are calculated based on the assumption that prediction error is distributed normally with zero mean and constant variance. Quantile regression provides sensible prediction intervals even for errors with non-constant (but predictable) variance or non-normal distribution.
Based on minimizing the pinball loss, conditional quantiles can also be estimated by models other than linear models. For example, [`GradientBoostingRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html#sklearn.ensemble.GradientBoostingRegressor "sklearn.ensemble.GradientBoostingRegressor") can predict conditional quantiles if its parameter `loss` is set to `"quantile"` and parameter `alpha` is set to the quantile that should be predicted. See the example in [Prediction Intervals for Gradient Boosting Regression](https://scikit-learn.org/stable/auto_examples/ensemble/plot_gradient_boosting_quantile.html#sphx-glr-auto-examples-ensemble-plot-gradient-boosting-quantile-py).
Most implementations of quantile regression are based on linear programming problem. The current implementation is based on [`scipy.optimize.linprog`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html#scipy.optimize.linprog "\(in SciPy v1.17.0\)").
Examples
  * [Quantile regression](https://scikit-learn.org/stable/auto_examples/linear_model/plot_quantile_regression.html#sphx-glr-auto-examples-linear-model-plot-quantile-regression-py)

Mathematical details[#](https://scikit-learn.org/stable/modules/linear_model.html#mathematical-details-6 "Link to this dropdown")
As a linear model, the [`QuantileRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.QuantileRegressor.html#sklearn.linear_model.QuantileRegressor "sklearn.linear_model.QuantileRegressor") gives linear predictions (w,X)=Xw for the -th quantile, q∈(0,1). The weights or coefficients are then found by the following minimization problem:
min1nsamplesP(−w)+αw.
This consists of the pinball loss (also known as linear loss), see also [`mean_pinball_loss`](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_pinball_loss.html#sklearn.metrics.mean_pinball_loss "sklearn.metrics.mean_pinball_loss"),
P(t)=qmax(t,0)+(1−q)max(−t,0)={t0,t=0,(q−1)t,
and the L1 penalty controlled by parameter `alpha`, similar to [`Lasso`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html#sklearn.linear_model.Lasso "sklearn.linear_model.Lasso").
As the pinball loss is only linear in the residuals, quantile regression is much more robust to outliers than squared error based estimation of the mean. Somewhat in between is the [`HuberRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html#sklearn.linear_model.HuberRegressor "sklearn.linear_model.HuberRegressor").
References[#](https://scikit-learn.org/stable/modules/linear_model.html#references-10 "Link to this dropdown")
  * Koenker, R., & Bassett Jr, G. (1978). [Regression quantiles.](https://gib.people.uic.edu/RQ.pdf) Econometrica: journal of the Econometric Society, 33-50.
  * Portnoy, S., & Koenker, R. (1997). [The Gaussian hare and the Laplacian tortoise: computability of squared-error versus absolute-error estimators. Statistical Science, 12, 279-300](https://doi.org/10.1214/ss/1030037960).
  * Koenker, R. (2005). [Quantile Regression](https://doi.org/10.1017/CBO9780511754098). Cambridge University Press.


##  1.1.16. Polynomial regression: extending linear models with basis functions[#](https://scikit-learn.org/stable/modules/linear_model.html#polynomial-regression-extending-linear-models-with-basis-functions "Link to this heading")
One common pattern within machine learning is to use linear models trained on nonlinear functions of the data. This approach maintains the generally fast performance of linear methods, while allowing them to fit a much wider range of data.
Mathematical details[#](https://scikit-learn.org/stable/modules/linear_model.html#mathematical-details-7 "Link to this dropdown")
For example, a simple linear regression can be extended by constructing **polynomial features** from the coefficients. In the standard linear regression case, you might have a model that looks like this for two-dimensional data:
(w,x)=++
If we want to fit a paraboloid to the data instead of a plane, we can combine the features in second-order polynomials, so that the model looks like this:
(w,x)=+++++
The (sometimes surprising) observation is that this is _still a linear model_ : to see this, imagine creating a new set of features
z=[,,,,]
With this re-labeling of the data, our problem can be written
(w,z)=+++++
We see that the resulting _polynomial regression_ is in the same class of linear models we considered above (i.e. the model is linear in ) and can be solved by the same techniques. By considering linear fits within a higher-dimensional space built with these basis functions, the model has the flexibility to fit a much broader range of data.
Here is an example of applying this idea to one-dimensional data, using polynomial features of varying degrees:
This figure is created using the [`PolynomialFeatures`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html#sklearn.preprocessing.PolynomialFeatures "sklearn.preprocessing.PolynomialFeatures") transformer, which transforms an input data matrix into a new data matrix of a given degree. It can be used as follows:

```
>>> fromsklearn.preprocessingimport PolynomialFeatures
>>> importnumpyasnp
>>> X = np.arange(6).reshape(3, 2)
>>> X
array([[0, 1],
       [2, 3],
       [4, 5]])
>>> poly = PolynomialFeatures(degree=2)
>>> poly.fit_transform(X)
array([[ 1.,  0.,  1.,  0.,  0.,  1.],
       [ 1.,  2.,  3.,  4.,  6.,  9.],
       [ 1.,  4.,  5., 16., 20., 25.]])

```
Copy to clipboard
The features of have been transformed from [,] to [1,,,,,], and can now be used within any linear model.
This sort of preprocessing can be streamlined with the [Pipeline](https://scikit-learn.org/stable/modules/compose.html#pipeline) tools. A single object representing a simple polynomial regression can be created and used as follows:

```
>>> fromsklearn.preprocessingimport PolynomialFeatures
>>> fromsklearn.linear_modelimport LinearRegression
>>> fromsklearn.pipelineimport Pipeline
>>> importnumpyasnp
>>> model = Pipeline([('poly', PolynomialFeatures(degree=3)),
...                   ('linear', LinearRegression(fit_intercept=False))])
>>> # fit to an order-3 polynomial data
>>> x = np.arange(5)
>>> y = 3 - 2 * x + x ** 2 - x ** 3
>>> model = model.fit(x[:, np.newaxis], y)
>>> model.named_steps['linear'].coef_
array([ 3., -2.,  1., -1.])

```
Copy to clipboard
The linear model trained on polynomial features is able to exactly recover the input polynomial coefficients.
In some cases it’s not necessary to include higher powers of any single feature, but only the so-called _interaction features_ that multiply together at most distinct features. These can be gotten from [`PolynomialFeatures`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.PolynomialFeatures.html#sklearn.preprocessing.PolynomialFeatures "sklearn.preprocessing.PolynomialFeatures") with the setting `interaction_only=True`.
For example, when dealing with boolean features, for all and is therefore useless; but represents the conjunction of two booleans. This way, we can solve the XOR problem with a linear classifier:

```
>>> fromsklearn.linear_modelimport Perceptron
>>> fromsklearn.preprocessingimport PolynomialFeatures
>>> importnumpyasnp
>>> X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
>>> y = X[:, 0] ^ X[:, 1]
>>> y
array([0, 1, 1, 0])
>>> X = PolynomialFeatures(interaction_only=True).fit_transform(X).astype(int)
>>> X
array([[1, 0, 0, 0],
       [1, 0, 1, 0],
       [1, 1, 0, 0],
       [1, 1, 1, 1]])
>>> clf = Perceptron(fit_intercept=False, max_iter=10, tol=None,
...                  shuffle=False).fit(X, y)

```
Copy to clipboard
And the classifier “predictions” are perfect:

```
>>> clf.predict(X)
array([0, 1, 1, 0])
>>> clf.score(X, y)
1.0

```
Copy to clipboard
On this page 
scikit-learn is [financially supported](https://scikit-learn.org/stable/institutional_support.html#funding) by Probabl and other institutions.
[ Enterprise-grade solutions and services ](https://probabl.ai/lp/scikit-learn)
