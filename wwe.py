import pandas as pd
import scipy.stats as stats
df = pd.read_csv("WWE.csv")

print(df.iloc[0])
print(df.iloc[0,2])

df = df.drop(columns = ["date", "event", "location", "link", "date_of_birth", "date_of_death"])
print(df)
print(df.mean(numeric_only = True))

print(df.shape)
print(df.info)
df = df.dropna()

#Descriptive statistics
#Measures of Central Tendency
mean_reigns = df["reign"].mean()
print(f"the mean reigns are {mean_reigns}")

mean_days = df["days"].mean()
print(f"the mean days are {mean_days}")

median_reigns = df["reign"].median()
print(f"the median reigns are {median_reigns}")

median_days = df["days"].median()
print(f"the median days are {median_days}")

#measures of variability
std_reigns = df["reign"].std()
print(f"the std reigns are {std_reigns}")

std_days = df["days"].std()
print(f"the std days are {std_days}")

#Quartiles of championship reigns
quartiles_reigns = df["reign"].quantile([0.25, 0.5, 0.75])
print(f"the quartiles are {quartiles_reigns}")

#quartiles of championship days
quartiles_days = df["days"].quantile([0.25, 0.5, 0.75])
print(f"the quartiles are {quartiles_days}")

#Men's title reigns Vs. Female Ttitle Reigns

df["Category"] = df["belt"].str.contains(
    "women", case = False, na = False
).map({
    True: "Women's",
    False: "Men's"
})
print(df["Category"].value_counts())

# Chi Square Test
#H0: The men's and women's title reigns are equally distributed (50-50)
#H1: Men's and Women's title reigns are not  equally distributed

from scipy.stats import chisquare
observed = df["Category"].value_counts()
print(f"the observed total is {observed}")
total = df["Category"].value_counts().sum()
print(total)
expected1 = total/2
expected2 = total/2
expected = [expected1, expected2]

print(f"the expected total for both is {expected}")

result = chisquare(observed, expected)
print(f"the chisquare result is {result.statistic: .8f}")
print(f"P-value is {result.pvalue: .8f}")

# is there a significant difference in days held the title between males and females?
men_days = df[df["Category"]== "Men's"]["days"].dropna()
women_days = df[df["Category"]== "Women's"]["days"].dropna()

from scipy.stats import mannwhitneyu
result = mannwhitneyu(women_days, men_days, alternative = "two-sided")
print(f"the mannwhitneyu result is {result.statistic: .4f}")
print(f"the p-value is {result.pvalue:.4f}")


#Since P value is greater than 0.05, we retain the H0 that there is no significant difference in the days for which the title was held between males and females.

# Does increase in the number of title reigns increase or decrease with the increase in the number of days the title is held?
from scipy.stats import pearsonr
df = df.dropna(subset=["reign", "days"])
Var1 = df["reign"]
Var2 = df["days"]
pearsonr = pearsonr(Var1, Var2)
print(f"the pearsonr result is {pearsonr.statistic}")
print(f"the pvalue for pearsonr is {pearsonr.pvalue}")

#JOHN CENA: GOAT
john = df[df["name"] == "John Cena"]
print(john["days"].mean())

#Randy Orton
randy = df[df["name"] == "Randy Orton"]
print(randy["days"].mean())

john_days_held = john["days"]
randy_days_held = randy["days"]
#Cena vs Orton: Is the diff in days held significant?
from scipy.stats import mannwhitneyu
result = mannwhitneyu(john_days_held, randy_days_held, alternative = "two-sided")
print(f" The mannwhitney value is: {result.statistic:.4f}")
print(f" the pvalue is: {result.pvalue:.4f}")

#Independent samples t test

from scipy.stats import ttest_ind
result = ttest_ind(john_days_held, randy_days_held)
print(f" The ttest_ind value is: {result.statistic:.4f}")
print(f" the pvalue is: {result.pvalue:.4f}")

#damn H0 retained, just by looking at the means, the story looked different, no?" Beauty of numbers
