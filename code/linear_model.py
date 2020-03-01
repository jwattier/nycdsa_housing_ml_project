# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.3.4
#   kernelspec:
#     display_name: 'Python 3.7.6 64-bit (''base'': conda)'
#     language: python
#     name: python37664bitbaseconda78814975a87e45dd93a41087a924c115
# ---

import pandas as pd
# %pylab inline

# file_path = r"../pre_processed_data/pre_processed.csv"
file_path = r"C:\Users\jason\OneDrive\Documents\Jason\NYC Data Science Academy\projects\machine_learning\ghub_work_area\pre_processed_data\pre_processed.csv"
# import pre_processed file 
pre_process_df = pd.read_csv(filepath_or_buffer=file_path, index_col=0, header=0)
pre_process_df.sample(5)

# + pycharm={"is_executing": false}
len(pre_process_df.columns)

# +
# remove target variables from data frame
X = pre_process_df.loc[:, pre_process_df.columns.difference(["saleprice", "log_saleprice"])]

y = pre_process_df["saleprice"]
y_log = pre_process_df["log_saleprice"]

print(X.shape)
print(y.shape)
y_log.shape

# +
# train, test split with train set to 80%
# A linear regression model will be evaluated first in the absence of regularization
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state=42)
X_train_log, X_test_log, y_train_log, y_test_log = train_test_split(X, y_log, test_size= 0.2, random_state=42)

# +
from sklearn.linear_model import HuberRegressor, LinearRegression
# Evaluation of Huber regressor against SalePrice w/o log-transform 
# Huber regression is a linear model that is more robust to outliers than the standard model, which penalizes the model
# for higher deviations.

hr = HuberRegressor()
hr.fit(X=X_train, y=y_train)
print(f"Train R2 is {hr.score(X=X_train, y=y_train)}")
print(f"Test R2 is {hr.score(X=X_test, y=y_test)}")
# -

# Standard regression w/o log transform 
lr = LinearRegression()
lr.fit(X=X_train, y=y_train)
print(f"Train R2 is {lr.score(X=X_train, y=y_train)}")
print(f"Test R2 is {lr.score(X=X_test, y=y_test)}")

# +
# Standard regression w/log transform 
lr_log = LinearRegression()
lr_log.fit(X=X_train_log, y=y_train_log)
print(f"Train R2 is {lr_log.score(X=X_train_log, y=y_train_log)}")
print(f"Test R2 is {lr_log.score(X=X_test_log, y=y_test_log)}")

# There is a slight improvement (~2%) in the train R2 and test R2 utilizing log transform 

# + [markdown] pycharm={"name": "#%% md\n"}
# ## Model Evaluation - Linear Regression
# ### The following section evaluates the random error, constant variance and normal distribution with mean 0 assumption of linear model in the context of the four initial models utilizing a residual plot from Yellowbrick.
#
# -

# Residual Plot for Huber LR with no log-transform
from yellowbrick.regressor import ResidualsPlot
rpv_hr = ResidualsPlot(hr)
rpv_hr.fit(X=X_train, y=y_train)
rpv_hr.score(X=X_test, y=y_test)
rpv_hr.poof()

rpv_lr = ResidualsPlot(lr)
rpv_lr.fit(X=X_train, y=y_train)
rpv_lr.score(X=X_test, y=y_test)
rpv_lr.poof()


# Residual Plot for LR with log transform 
rpv_lr_log = ResidualsPlot(lr_log)
rpv_lr_log.fit(X=X_train_log, y=y_train_log)
rpv_lr_log.score(X=X_test_log, y=y_test_log)
rpv_lr_log.poof()

# + [markdown] pycharm={"name": "#%% md\n"}
# ## Model Evaluation of Ordinary Least Squares -Log Transform
# - Evaluation of log-transformed OLS model as the residuals plot appeared to satisfy most of the principal assumptions of linear regression. 
# -

import statsmodels.api as sm
X_add_constant = sm.add_constant(X_train_log)
ols_log = sm.OLS(y_train_log, X_add_constant)
ans_log = ols_log.fit()
print(ans_log.summary())

# + [markdown] pycharm={"name": "#%% md\n"}
# - based on the OLS review, several factors are deemed non-significant by the model (e.g., there is not enough evidience to support that they are important to predicting sales price). These preidctors are bedrooms, lotfrontage, and whether a home is a new home. 
# - There are several coefficients that on the surface do not appear to make sense - namely the negative coefficient associated with two_plus_cr_garabe, this coefficient is negative whereas the domain association with this feature being that a two car or more garage capacity is good for a house. 
# - The model will be recaliberated dropping these three features.
# - homeage is being excluded in favor of remodelage due to its lower significance. 
# - garagecars is being dropped because there is an overalp between that variable and the "two_plus_cr_garg" feature

# +
X_train_log = X_train_log.loc[:, X.columns.difference(["bedroomsabvgr", "lotfrontage", "newHome", "homeage", "garagecars"])]
X_test_log = X_test_log.loc[:, X.columns.difference(["bedroomsabvgr", "lotfrontage", "newHome", "homeage", "garagecars"])]


lr_log.fit(X=X_train_log, y=y_train_log)
lr_log.score(X=X_test_log, y=y_test_log)
print(f"Train R2 is {lr_log.score(X=X_train_log, y=y_train_log)}")
print(f"Test R2 is {lr_log.score(X=X_test_log, y=y_test_log)}")

# + [markdown] pycharm={"name": "#%% md\n"}
# - The train and test R2 are very similar to the model (e.g., 90/89%) prior to dropping the four variables. 
# - The residual plot and stats model output will be evaluated to confirm that the prior assumptions still hold as well as to identify any other items to potentiall exclude before proceeding to cross-validation.
#
# -

rpv_lr_log = ResidualsPlot(lr_log)
rpv_lr_log.fit(X=X_train_log, y=y_train_log)
rpv_lr_log.score(X=X_test_log, y=y_test_log)
rpv_lr_log.poof()

X_add_constant = sm.add_constant(X_train_log)
ols_log = sm.OLS(y_train_log, X_add_constant)
ans_log = ols_log.fit()
print(ans_log.summary())


# - Evaluation of OLS for non-log LR

X_add_constant_non_log = sm.add_constant(X_train)
ols = sm.OLS(y_train, X_add_constant_non_log)
ans = ols.fit()
print(ans.summary())

# + pycharm={"is_executing": false}
# Prediction error plot to further evaluate normality of residual distribution
from yellowbrick.regressor import prediction_error

visualizer = prediction_error(lr_log, X_train_log, y_train_log)

# + [markdown] pycharm={"name": "#%% md\n"}
# - qq plot of prediction error appears to follow in a straight line, which is indicative of a normally distributed error term.
#

# + pycharm={"is_executing": false}
from yellowbrick.regressor import cooks_distance

cd_visualizer = cooks_distance(X=X_train, y=y_train_log)

# + [markdown] pycharm={"name": "#%% md\n"}
# ## Cross Validation through YellowBrick
# ### **Evaluation of R2 over 4-fold Cross-Validation**
# - linear log model is evaluated via 4-k fold

# +
from sklearn.model_selection import KFold

from yellowbrick.model_selection import CVScores

# Instantiate the KFold settings
cv = KFold(n_splits=4, random_state=42)

cv_visualizer = CVScores(model=lr_log, cv=cv, scoring="r2")

cv_visualizer.fit(X=X_train_log, y=y_train_log) # fit data into visualizer 
cv_visualizer.poof()

# + [markdown] pycharm={"name": "#%% md\n"}
# - Median cross-validation R2 score is 89% and fairly consistent. 
# - Evaluating next via sci-kit learn's model selection package
#
# -

# ### **Evaluation of RMSE (Root Mean Square Error)**

# +
from sklearn.model_selection import cross_val_score
lr_r2_scores = cross_val_score(estimator = lr_log, X = X_train_log, y = y_train_log, scoring = 'r2', cv= 4)
lr_rmse = -1 * cross_val_score(estimator= lr_log, X = X_train_log, y = y_train_log, scoring = "neg_root_mean_squared_error", cv=4)
lr_mse = -1 * cross_val_score(estimator= lr_log, X = X_train_log, y = y_train_log, scoring = "neg_mean_squared_error", cv=4)
lr_mae = -1 * cross_val_score(estimator= lr_log, X = X_train_log, y = y_train_log, scoring = "neg_median_absolute_error", cv=4)

def display_cv_scores(scores):
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard Deviation:", scores.std())
 
print("CV scores for R2 are:")   
display_cv_scores(lr_r2_scores)
print("")
print("CV scores for RMSE are:")
display_cv_scores(lr_rmse)
print("")
print("CV scores for MSE are:")
display_cv_scores(lr_mse)
print("")
print("CV scores for MAE are:")
display_cv_scores(lr_mae)

# +
cv_rmse = KFold(n_splits=4, random_state=42)

# note that scikit-learn's implementation of RMSE is negative root mean squared error 
cv_visualizer_rmse = CVScores(model=lr_log, cv=cv, scoring="neg_median_absolute_error")

cv_visualizer_rmse.fit(X=X_train_log, y=y_train_log) # fit data into visualizer 
cv_visualizer_rmse.poof()
# -



# + [markdown] pycharm={"name": "#%% md\n"}
# - Based upon cross-validation and test R2, we appear to have a strong and consistent predictor of housing prices.
# - The mean average is .89, which is also the value of the test R2 on the 20% hold out test-set. The standard deviation is also fairly low (e.g., 1.3%), which indicates that our model is not overly sensitive to the input data set.
#
# -

# ## VIF Evaluation
#
# - VIF (Variance Inflation Factor) is reviewed to determine if there is any multi-collinearity. Generally, any feature with a VIF value of 5 or higher is generally regarded as a feature that is likely to be co-linear with another feature or combination of other features in the model. 

# +
from patsy import dmatrices
from statsmodels.stats.outliers_influence import variance_inflation_factor

features_vif = "+".join(X_train_log.columns)

features_target = pd.concat([X_train_log, y_train_log], axis="columns")

y_VIF, X_VIF = dmatrices('log_saleprice ~' + features_vif, features_target, return_type = "dataframe")

vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(X_VIF.values, i) for i in range(X_VIF.shape[1])]
vif["features"] = X_VIF.columns

vif.round(1)

# -

# - There are no features with a VIF factor greater than 5, the general cutoff for multicollinearity "concern." The highest VIF value are 3.1 and 3.2 for adj_ovr_qual and good_ament_ct, respctively.

# ## Model Output as Picket Object
# - Output of model object to be utilized in prediction

# +
from joblib import dump

#dump(lr_log, '../model_files/lr_log_model.joblib')
dump(lr_log, r"C:\Users\jason\OneDrive\Documents\Jason\NYC Data Science Academy\projects\machine_learning\ghub_work_area\model_files\lr_log_model.joblib")
# -

lr_log.predict(X_test_log)


X_test_log.columns

# + [markdown] pycharm={"name": "#%%\n"}
# # Additonal Model Evaluation 
# ## **Feature Importance**
# ### 1. Lasso Evaluation
# - Relatively and on a holistic level, seeing which feature coefficients are "pushed" to zero via a Lasso Regularization can indicate the relative importance of those features to a model. 
# - To utilize a regularization method - even for evaluation purposes - it is general good practice to standardize the input variables first prior to fitting the model.
# -

from sklearn import preprocessing
std = preprocessing.StandardScaler()
X_train_log_std = std.fit_transform(X_train_log)

# +
from sklearn import linear_model
lasso_model = linear_model.LassoLarsCV(
    cv=4, max_n_alphas=10
).fit(X_train_log_std, y_train_log)
fig, ax = plt.subplots(figsize=(12, 8))
cm = iter(
    plt.get_cmap("tab20")(
        np.linspace(0, 1, X_train_log_std.shape[1])
    )
)
for i in range(X_train_log_std.shape[1]):
    c = next(cm)
    ax.plot(
        lasso_model.alphas_,
        lasso_model.coef_path_.T[:, i],
        c=c,
        alpha=0.8,
        label=X_train_log.columns[i],
    )

ax.axvline(
    lasso_model.alpha_,
    linestyle="-",
    c="k",
    label="alphaCV",
)

plt.ylabel("Regression Coefficients")
ax.legend(X_train_log.columns, bbox_to_anchor=(1,1))
plt.xlabel("alpha")
plt.title(
    "Regression Coefficients Progression for Lasso Paths"
)
fig.savefig(
    "mlpr_lasso_w_bsmt_adj.png",
    dpi=300,
    bbox_inches="tight",
)
# -

# - The visualization of the Lasso regularization with increasing alphas indicates that the most significant factors are building square feet, adjusted overall quality, good amenities count, total baths and bad amenities count.

# ### 2. Mutual Information
# - Scikit learn's mutual information score for regressions helps to quantifies the amount of information gained by including the feature listed. 
# - The value is bounded between 0 and 1. If the value is zero, there is no relationship between the target and the feature.  

# +
from sklearn import feature_selection

mic = feature_selection.mutual_info_regression(
    X_train_log, y_train_log
)

fig, ax = plt.subplots(figsize=(10, 8))
(
    pd.DataFrame(
        {"feature": X_train_log.columns, "vimp": mic}
    )
    .set_index("feature")
    .plot.barh(ax=ax)
)
fig.savefig("mutual_info.png")
# -

# **Conclusions**
# - This visualization largely confirms the same relatively most important features (e.g., square footage, overall quality) that the Lasso visualization conferred. It does appear to note that abnormal sales and single family home are not signficant factors, which a little harder to visually distill in the Lassso chart.

# ### 3. SHAP (SHaply Additive exPlanations)
# - The SHAP library for Python has several nice visualizations that help to inform how predictors influence the output of the model.
# - The below summary chart helps us to see the global effect of features on the target log sales price. For example, high values of building sqft increase the model output and lower values by contrast lower the target variable.

# +
import shap
shap.initjs()

exp = shap.LinearExplainer(model = lr_log, data=X_train_log)
vals = exp.shap_values(X_train_log)
fig, ax = plt.subplots(figsize=(6, 4))
shap.summary_plot(vals, X_train_log)
fig.savefig(
    "shap_summary_plt_reduced.png",
    bbox_inches="tight",
    dpi=300,
)
# -

# - Another method of more narrowly looking at overall feature importance versus inspection of how different value of a feature impact the model, which reflects the mean absoluate SHAP value. 

shap.summary_plot(vals, X_train_log, plot_type="bar")

# ** Conclusion **
# - Similar to the Lasso and mutual information graphs - the SHAP summary plot of feature importance highlights the same top factors in terms of overall impact (sq footage, overall quality, total baths, good amentity count).

# # Example Predictions (For Purposes of Presentation)

# +
y_test_log_predict = lr_log.predict(X_test_log)
y_test_predict_Series = pd.DataFrame(data=y_test_log_predict, index=y_test_log.index, columns=["log_saleprice_predict"])

test_set_w_predict = pd.concat([X_test_log, y_test_log, y_test_predict_Series], axis="columns")
# -

test_set_w_predict.sample(5)

test_set_w_predict["saleprice"] = np.exp(test_set_w_predict["log_saleprice"])
test_set_w_predict["saleprice_predict"] = np.exp(test_set_w_predict["log_saleprice_predict"])
test_set_w_predict["residual"] = test_set_w_predict.saleprice - test_set_w_predict.saleprice_predict


test_set_w_predict.sample(5)

file_path_train = r"C:\Users\jason\OneDrive\Documents\Jason\NYC Data Science Academy\projects\machine_learning\ghub_work_area\data\train.csv"
train_df = pd.read_csv(file_path_train, header=0, index_col=0)
train_df.loc[[1095, 68, 1216, 531, 1290], ["YrSold", "YearRemodAdd", "YearBuilt"]]

test_set_w_predict[["residual"]].aggregate([mean, median, np.std])

test_set_w_predict[["residual"]].hist()
plt.xlabel("$ Dollars")
plt.ylabel("Count")
plt.title("Difference in Sale Price: Actual Less Predicted")
plt.savefig("Histogram_of_Residuals.png")

test_set_w_predict["perc_miss"] = test_set_w_predict["residual"]/test_set_w_predict["saleprice"]

test_set_w_predict["perc_miss"].abs().median()

test_set_w_predict["perc_miss"].abs().mean()


