
# coding: utf-8

# ## Programming Fundation (Udacity) - Final Project: Exploring Titanic Data.

# ### 1. Description of the dataset:
# The data could be downloaded from the Kaggel	(https://www.kaggle.com/c/titanic), a website for learning data analytics. The raw data consists of 891 observations and 12 variables
# 
# An overview of the variables is as follows:
# 
# Nominal variables (Categorical variables which do not have intrinsic order) -->
# 
# - Sex (as strings):       "Female" or "Male"
# - Embarked (as strings):    Port of Embarkation (C = Cherbourg; Q = Queentown; S = Southampton)
# - Cabin (as strings):      Cabin name 
# - Name (as strings):       Passengers' name in the form of "Last name, Prefix. First name " 
# - Ticket (as strings):      Ticket number 
# - Survived (as integers):   0 = No; 1 = yes.
# 
# Ordinal variables (Categorical variables with intrinsic order) -->
# 
# - PassengerId (as integers): An attribute which allows us to identify each passenger uniquely.
# - Pclass (as integers):     Passenger Class 1 - 1st; 2 - 2nd; 3 - 3rd.
# 
# Continuous variables -->
# 
# - Age (as float variables):   Age in years. if age is less than 1, it is fractional.
# - SibSp (as integers):      Number of Siblings/Spouses
# - Parch (as integers):      Number of Parents/Children
# - Fare (as float variables):  Ticket Price
# 

# ### Questions to be addressed:
# 
# We are interested in what factors impact survival. Having done a preliminary examination of the dataset, I decide to break this question into several parts.
# 
# 1. Did gender influence survival rate?
# 2. Did passenger class influence survival rate?
#       * If so, Why exactly?
# 3. How do survival rates vary for different age groups?
# 4. Do families with larger size survive more often?
#       * Do people who travel together survive more often?

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().magic(u'matplotlib inline')
get_ipython().magic(u'pylab inline')


# In[2]:

# read csv data into a pandas dataframe object.
t_data= pd.read_csv(r'C:\Users\bisheng\Desktop\coursera\1udacity\introtodataanalysis\titanic_data.csv')


# In[3]:

# An overview of the variables in the data.
t_data.info()


# In[4]:

# describe the numerical variables.
t_data.describe(include = ['number'])


# In[5]:

# describe the "object" variables.
t_data.describe(include = ['object'])


# 1. There are small amount of missing values for the variables "Age" and "Embarked", Massive missing values for "cabin".
# 2. The lowest Fare is zero. (Those should be staffs of Titanic.) The distribution of "Fare" is quite wide ranged, which suggests the possibility of outliers.
# 3. People can share the same ticket number, which indicates that they might travel together.

# In[6]:

t_data.head()


# ### 2. Data wrangling

# #### 2.0 Manipulating the variable "Name".
# Name is of format {Last name}, {Prefix.} {First name}. One good reason of breaking Passenger names into their "last name", "prefix" and "first name" is: "Prefix" is closely related to "Age" and "Sex".

# In[7]:

# Import regular expression library.
import re

# I now define a function to extract the title for each name string.

def extract_title(a_string):
   return re.sub('(.*, )|(\\..*)', "", a_string)

t_data["prefix"] = t_data["Name"].apply(extract_title)


# In[8]:

# The following code shows the distinct prefixes, and their corresponding occurances.
t_data["prefix"].value_counts()

# Use t_data["prefix"].value_counts().sum() to confirm that all the passengers have prefix.


# In[9]:

# Now I break the name into Last_name, the prefix, as well as the First_name.

for index, row in t_data.iterrows():
    t_data.loc[index, "Last_Name"] = t_data["Name"].str.split(",").iloc[index][0]    
    if t_data.loc[index, "prefix"] == False:
        t_data.loc[index, "First_Name"] = t_data["Name"].str.split(", ").iloc[index][1]
    else:
        t_data.loc[index, "First_Name"] = row["Name"].split(". ")[1]
        
# Alternatively, we could also use the apply() method to achieve the results.

t_data.head()


# In[10]:

# Drop the name colomn.
t_data = t_data.drop("Name",axis = 1)


# #### 2.1 Investigating Missing values ("Age" and "Embarked").
# 
# The code below displays the percentage (in units of %) of missing data.

# In[11]:

(t_data.isnull().sum()/t_data["PassengerId"].count()) * 100


# There is reasonable amount of missing values for "Age" and "Embarked", so it is possible to find reasonable ways to fill these missing values. 
# 
# With large amount of missing values for "Cabin", I would not try to fill these missing values. I will retain this variable, keeping the possibility of making use of it for side observations open. 

# #### 2.1.0 Age

# In[12]:

# I plot histogram of Age (for non-missing values). There are 10 bins by default: bins = 10. 
ax_age = t_data["Age"].plot.hist()
ax_age.set_title("Histogram for 'Age'")
ax_age.set(xlabel = "Age")


# In[13]:

# The range of "Age" is large, there are potentially outliers.
# I could define a helper function to get the Interquarter range for the purpose of detecting outliers.
def get_IQR(a1_series):
    Q1 = a1_series.quantile(0.25)
    Q3 = a1_series.quantile(0.75)
    IQR = Q3 - Q1
    return Q1 - IQR * 1.5, Q3 + IQR * 1.5 

# The outliers are defined as those points which are situated outside of the IQR.
# The following code returns the outliers. 

t_data[t_data["Age"] > get_IQR(t_data.loc[t_data["Age"].isnull() != True, "Age"])[1]]


# #### Some interesting observations.
# - All the outliers with respect to "Age" are male. Most of them are in the middle-upper class. 
# - Except for the oldest one, none survived.
# - Most of them seem to travel alone: "SibSp" and "Parch" appear to be 0. However, it is possible that they were travelling with servants or other friends.

# ###### 2.1.0.1 Fill the missing values for "Age"

# In[14]:

# The following code helps me identify the prefixes which the missing "Age" values are coming from.

t_data.loc[t_data["Age"].isnull() == True]["prefix"].unique()


# The missing "Age" values are coming from the following prefixes: ['Mr', 'Mrs', 'Miss', 'Master', 'Dr'].
# I suspect that one's "prefix" tells something about one's "Age".
# I thus draw the distribution of (non missing) "Age", given one's prefix. 

# In[15]:

# .subplots() returns an instance of Figure, along with an array of Axes for each subplot.
fig, axes = plt.subplots(nrows=2, ncols=3) 
fig.set_size_inches(w=9,h=5)
t_data.loc[t_data["prefix"] == "Mr", "Age"].plot.hist(ax=axes[0,0]); 
axes[0,0].set_title("Age distribution for 'Mr'")
t_data.loc[t_data["prefix"] == "Mrs", "Age"].plot.hist(ax=axes[0,1]); 
axes[0,1].set_title("Age distribution for 'Mrs'")
t_data.loc[t_data["prefix"] == "Miss", "Age"].plot.hist(ax=axes[0,2]); 
axes[0,2].set_title("Age distribution for 'Miss'")
t_data.loc[t_data["prefix"] == "Master", "Age"].plot.hist(ax=axes[1,0]); 
axes[1,0].set_title("Age distribution for 'Master'")
t_data.loc[t_data["prefix"] == "Dr", "Age"].plot.hist(ax=axes[1,1]); 
axes[1,1].set_title("Age distribution for 'Dr'")
t_data["Age"].plot.hist(ax=axes[1,2]); axes[1,2].set_title('Age distribution for all')
plt.tight_layout()


# ##### Observations.
# Given the prefix (and hence Sex), conditional age distributions have different ranges and shapes. A good example is that the Masters are all of age less than 12. These suggest that we could do better than simply filling the missing values by the median of the unconditional age distribution.
# ##### --------------------
# I decide to fill the missingg values using median, mode or mean of the Age distribution conditional on  their respective prefix: for those with prefix "Mr.", "Mrs", and "Miss", it may be reasonable to fill missing ages with medians since the mode and median are close; It may be more appropriate to assign the mode to the "Master"s, and mean to the "Doctors".

# In[16]:

# I get the respective median age conditional on the prefix Mr, Mrs, Miss

Mr_median_age = t_data.loc[(t_data["prefix"] == "Mr") & (t_data["Age"].isnull() != True), "Age"].median()
# To verify:  t_data.loc[(t_data["prefix"] == "Mr") & (t_data["Age"].isnull() != True), "Age"].describe()

Mrs_median_age = t_data.loc[(t_data["prefix"] == "Mrs") & (t_data["Age"].isnull() != True), "Age"].median()
# To verify:  t_data.loc[(t_data["prefix"] == "Mrs") & (t_data["Age"].isnull() != True), "Age"].describe()

Miss_median_age = t_data.loc[(t_data["prefix"] == "Miss") & (t_data["Age"].isnull() != True), "Age"].median()
# To verify:  t_data.loc[(t_data["prefix"] == "Miss") & (t_data["Age"].isnull() != True), "Age"].describe()


# print Mr_median_age, Mrs_median_age, Miss_median_age


# In[17]:

# I get the respective mode age conditional on the prefix Master, the mean for Dr.

Master_mode_age = t_data.loc[(t_data["prefix"] == "Master") & (t_data["Age"].isnull() != True), "Age"].mode().iloc[0]
# To verify:  t_data.loc[(t_data["prefix"] == "Master") & (t_data["Age"].isnull() != True), "Age"].value_counts()
# Notice that .mode() method can return a series.

Dr_mean_age = t_data.loc[(t_data["prefix"] == "Dr") & (t_data["Age"].isnull() != True), "Age"].mean()
# To verify:  t_data.loc[(t_data["prefix"] == "Dr") & (t_data["Age"].isnull() != True), "Age"].describe()


# In[18]:

# I now create a new column "age_filled", in which the missing values are filled.
# Based on this new column, I create a categorical variables age group. 

t_data["age_filled"] = pd.Series(t_data["Age"], index=t_data.index)
t_data.loc[(t_data["prefix"] == "Mr") & (t_data["age_filled"].isnull()), "age_filled"] = Mr_median_age
t_data.loc[(t_data["prefix"] == "Mrs") & (t_data["age_filled"].isnull()), "age_filled"] = Mrs_median_age
t_data.loc[(t_data["prefix"] == "Miss") & (t_data["age_filled"].isnull()), "age_filled"] = Miss_median_age
t_data.loc[(t_data["prefix"] == "Master") & (t_data["age_filled"].isnull()), "age_filled"] = Master_mode_age
t_data.loc[(t_data["prefix"] == "Dr") & (t_data["age_filled"].isnull()), "age_filled"] = Dr_mean_age
t_data[["age_filled", "Age"]].describe()


# In[ ]:




# ###### 2.1.0.2 Create an ordinal categorical variables Age group.
# 
# When I plotted the histogram, I notice that the there are 10 bins by default, that is to say, the bin size is 8.
# For number of bins less than 10, the shape of the histogram will greatly change at the lower tail.
# For number of bins greater than or equal to 10, the shape of the histogram will be very similar.
# So I will choose to put the ages into 10 categories.

# In[19]:

# To get: [0, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80]
bin_separators = range(0,81,8)

# to get: age_groups = ['age_0_8', 'age_8_16', 'age_16_24', 'age_24_32','age_32_40',
#                       'age_40_48', 'age_48_56', 'age_56_64', 'age_64_72', 'age_72_80']
age_groups = ["age_{}_{}".format(bin_separators[x],bin_separators[x+1]) for x in range(10)]

# The following returns a series with type "Category", not "object"
t_data['Age_groups'] = pd.cut(t_data["age_filled"], bin_separators, labels=age_groups)

pd.value_counts(t_data['Age_groups'])


# Here, I will conduct a goodness-of-fit Chi square test to confirm that the distribution of age conditional on the prefix is indeed siginificantly different from the unconditional age distribution.

# In[20]:

# First step: I will create a helper function for obtaining the array for the observed frequencies.
def relative_freq_series(title):
    absolute_freq_series = t_data.loc[(t_data["Age"].isnull() == False) & (t_data["prefix"] == title), "Age_groups"].value_counts()
    rel_freq_series = absolute_freq_series / t_data[t_data["prefix"] == title].notnull().sum()["Age"]
    return rel_freq_series

# Second step: I get the expected frequencies: (problem, sort)
exp_freq_series = t_data.loc[(t_data["Age"].isnull() == False), "Age_groups"].value_counts()/t_data.notnull().sum()["Age"]

# The two series correspond to each other because they share the same index.


# In[ ]:




# In[21]:

from scipy import stats


# In[22]:

stats.chisquare(relative_freq_series("Mr").sort_index()*100, f_exp = exp_freq_series.sort_index()*100)


# In[23]:

stats.chisquare(relative_freq_series("Mrs").sort_index()*100, f_exp = exp_freq_series.sort_index()*100)


# In[24]:

stats.chisquare(relative_freq_series("Miss").sort_index()*100, f_exp = exp_freq_series.sort_index()*100)


# The above results show that at a 5% critical level,
# 1. For "Mr": the age distribution is not significantly different from the unconditional age distribution.
# 2. For "Mrs": its age distribution is significantly different from the unconditional age distribution.
# 3. For "Miss": the age distribution is significantly different from the unconditional age distribution.
# 
# These suggest that our strategy of filling the missing values is potentially more reasonable.

# In[ ]:




# #### 2.2.0 Embarked - fill Missing values.

# In[25]:

# I create descriptive label for the variable "Embarked".

t_data["Embarked_label"] = t_data.Embarked.map({'C' : 'Cherbourg', 'Q' : 'Queenstown', 'S' : 'Southampton'})

# I create descriptive label for the variable "Pclass".

t_data['Passenger_class_label'] = t_data.Pclass.map({1 : 'First Class', 2 : 'Second Class', 3 : 'Third Class'})


# In[26]:

# I have a look at the observations with missing values on "Embarked".
t_data.loc[t_data["Embarked"].isnull() == True]


# #### It is very likely that these two persons travell together: They share the same ticket number, the same Cabin, and paid the same fare. The Miss. could be the maid of the Mrs. who travelled alone. 
# 
# To fill the missing values reasonably, I would like to have a look at the (absolute) frequency graph of the "Embarked" variable.

# In[27]:

ax = t_data.groupby('Embarked').size().plot(kind='bar')
ax.set_title('Counting the number of passengers from each port')
ax.set(ylabel = 'Number of passengers')
# Alternative command (with order differences): t_data["Embarked"].value_counts().plot(kind = "bar")


# In[28]:

# I draw the histogram of variable "Embarked", conditional on Class, 

plt.figure(1, figsize=(12,3))                # default figure creation
ax1 = plt.subplot(1,3,1)                    # (number_of_rows, num_of_cols_, Plot_num)
ax1.set_title("Pclass1 passengers")
ax1.set(xlabel = "Embarked", ylabel = "Frequency")
t_data.loc[t_data["Pclass"] == 1, "Embarked"].value_counts().plot(kind = 'bar')

ax2 = plt.subplot(1,3,2)                    # the second subplot in the first figure
ax2.set_title("Pclass2 passengers")
ax2.set(xlabel = "Embarked", ylabel = "Frequency")
t_data.loc[t_data["Pclass"] == 2, "Embarked"].value_counts().plot.bar()

ax3 = plt.subplot(1,3,3)                    # the third subplot in the first figure
ax3.set_title("Pclass3 passengers")
ax3.set(xlabel = "Embarked", ylabel = "Frequency")
t_data.loc[t_data["Pclass"] == 3, "Embarked"].value_counts().plot.bar()
plt.tight_layout()


# Most people were embarked at "S". I replace the missing values by the mode "S".

# In[29]:

t_data.loc[t_data["Embarked"].isnull(), "Embarked"] = "S"

# Alternative method:
# t_data["Embarked"] = np.where(t_data["Embarked"].isnull(), # condition check
#                               'S',                          # replaced value if check is true
#                               t_data["Embarked"])     # replaced value if check is false

# To check:  t_data[t_data["Embarked"].isnull()]

# for some reason, the following does not work:
# t_data.loc[t_data["Embarked"].isnull(), "Embarked"].fillna("S", inplace = True)


# In[ ]:




# ##### 2.2 Converting Sex to numeric value; Making children sex-independent.
# 
# It would be more reasonable to isolate kids from the original categories male and female.

# In[30]:

# check whether there are missing values by the unique() method
t_data["Sex"].unique()

# replace "female" with 1 and "male" with 0. 
t_data.loc[t_data["Sex"] == "female", "Sex"] = 1
t_data.loc[t_data["Sex"] == "male", "Sex"] = 0

# assign 2 to kids belonging to the age group age_0_8, regardless of their gender.
t_data.loc[t_data["Age_groups"] == "age_0_8", "Sex"] = 2

# I create descriptive labels for each instance.
t_data["Survived_label"] = t_data.Survived.map({0: "Male", 1: "Female", 2: "Kids"})

# check.
t_data["Sex"].value_counts()
# t_data.sort_values(["Sex"], ascending = False)


# In[ ]:




# ##### 2.3 Family size and potentially related people
# 
# People who travel together can have diverse relationships:
# 1. They could come from the same family
# 2. People can travel together because they are friends or partners
# 3. A child needs to be looked after by someone if the parents are not arround
# 4. Rich people may have servants with them, etc.
# 
# The aim of this sub-section is to detect such relationships.

# #### 2.3.1 Family size
# I will define a quantitative variable "Family_size" which counts the number of members within a family.
# 
# I also define a qualitative variable "Family": 1 stands for having a family, 0 otherwise.

# In[31]:

# I define the family size.
t_data["Family_size"] = t_data["SibSp"] + t_data["Parch"]

# I also define a qualitative variable, which is equal to 1 when this person has a family, and 0 otherwise. 
t_data["Family"] = np.where(t_data["Family_size"] >=1, 1, 0)


# I use the following code to make a summary of percentage of each family size.

# In[32]:

(t_data["Family_size"].value_counts()/t_data["PassengerId"].count()) * 100


# In[34]:

# A plot can be made to visualize the above statistics.
plt.figure(1, figsize=(9,5))
ax=sns.countplot(x="Family_size", data=t_data, palette='RdBu');
ax.set(xlabel='Family_size', title='Counting number of passengers for each Family_size')
plt.show()


# It appears that around 60% of people are of familiy size 0. 
# 
# ##### Is it indeed the case that they were travelling alone? The following subsection will give an answer.

# #### 2.3.2 Ticket number
# 
# I manage to find that that people who share the same "Ticket" number are probably travelling together. I now show how I proceeded.

# At the beginning, I had no exact clue on which direction to proceed. So I tried to first spot those people who are potentially servants. I heard that most servants are females. So I made some hypothesis on the universal characteristics of potential maids.
# 1. Maids must embark at the same port as the persons they look after.
# 2. Maids must be an adult, and not married
# 3. I make the big assumptioin that the ticket fare for the maids is identical with that of the family she travels with. (This is inspired by the study of subsection 2.2.0)

# In[35]:

# Based on my assumption, I group by ["Embarked", "Fare"].
# The person who this maid looks after may have a different prefix from her.

step1_df = t_data.groupby(["Embarked", "Fare"]).filter(lambda x: x[(x["prefix"]=="Miss") & (x["age_filled"]>=19) & (x["Family"]==0)].count()["prefix"]>0)
# Alternative: t_data.groupby(["Embarked", "Fare"]).filter(lambda x: sum(x["prefix"] == "Miss")>0)

# I sort the table by "Fare".
step2_df = step1_df.sort_values(["Embarked", "Fare"])
step2_df.groupby("Fare").filter(lambda x: len(x["PassengerId"])>1)


# #### From the table above, I notice that there are a lot of identical "Ticket" number. And people who have the same fare seem to share the same ticket number quite often, which implies that these people might have bought the ticket together.
# 
# This leads me to think that ticket number may be a better trait for checking whether people are travelling together.
# 
# I now proceed through this direction: using ticket number to spot people who travel together.

# In[36]:

# I run the following code to group data by ticket number.
step_together_df = t_data.groupby(["Ticket"]).filter(lambda x: (x["Fare"].nunique()==1) & (x["Fare"].count()>1)).sort_values(["Ticket"])
# Alternative(not working): t_data.groupby(["Ticket"]).filter(lambda x: x["Fare"].value_counts().iloc[0]>1).sort_values(["Ticket"])
step_together_df


# Let us have a look at several records. The first 3 observations suggest that there are two misses who serve as maids for the Countess.We are in the right direction.
# #### It seems that people who have the same ticket number not only share the same fare, but probably also similar cabins. I now do the following check.

# In[37]:

# I want to have a look when ticket number is the same, whether the fare is different.

t_data.groupby(["Ticket"]).filter(lambda x: (x["Fare"].nunique()>1)).sort_values(["Ticket"])


# There is only 1 (Ticket) instance where the fare is different when the ticket number is identical. This suggests ticket number can be a good indicator. For the exception above, I will still consider them as travelling together.

# In[38]:

# I now use Ticket as an instrument to create another categorical variable travelling_together.
# When a ticket number is shared by more than 1 person, travelling_together will be assigned value 1.
# Otherwise, travelling_together will be assigned value 0.

def check_together(a_string):
    if a_string in step_together_df["Ticket"].unique():
        return 1
    else:
        return 0
t_data["Together"] = t_data["Ticket"].apply(check_together)


# ##### It is important to remark that this variable "Together" is defined independently of the variable "Family". The variable "Family" is defined from the perspective of the variable "Family_size". The variable "Together" is defined from the perspective of the variable "Ticket". 
# 
# My ultimate objective is to have a more comprehensive variable capturing whether people are travelling together. 
# 
# It is natural to check the following two cases which appear to be contradictory to my initiative:
# 1. People who have family but have different ticket: (t_data["Together"] == 0) & (t_data["Family"] == 1)
# 2. People who have no family but have identical ticket: (t_data["Together"] == 1) & (t_data["Family"] == 0)

# In[43]:

# People who have family but have different ticket number:
# The following code shows there are 85 such observations.
len(t_data[(t_data["Together"]==0) & (t_data["Family"]==1)].sort_values(["Ticket"]))

# A brief view: 
t_data[(t_data["Together"]==0) & (t_data["Family"]==1)].sort_values(["Ticket"]).head(6)


# In[45]:

# People who have no family but have identical ticket number:
# The following code shows there are 73 such observations.
len(t_data[(t_data["Together"]==1) & (t_data["Family"]==0)])

# A brief view:
t_data[(t_data["Together"]==1) & (t_data["Family"]==0)].head()


# In[46]:

# I also sort the dataframe by age.
t_data.loc[t_data["Together"]==0].sort_values(["Age"], ascending = True).head(10)


# I notice that some children less than 8 years old have tickets number different from their parents', but they are travelling with their parents. They belong to the first case above.
# 
# So in order to have a comprehensive variable. I simply do the following:

# In[47]:

t_data.loc[(t_data["Together"] == 0) & (t_data["Family"] >=1), "Together"] =1


# ##### Now "Together" serves as the comprehensive variable capturing whether people are travelling together.

# In[ ]:




# #### 2.3.3 "Ticket size"
# 
# Similar to Family size, it would be beneficial to know how many people are sharing the same ticket number.

# In[48]:

for index, row in t_data.iterrows():
    t_data.loc[index,"Ticket_size"] = t_data.groupby(["Ticket"]).size()[row["Ticket"]]


# In[56]:

# Check by the following code:
t_data.sort_values("Ticket_size", ascending = False).head()


# Recall that this is a partial data set. If we had the complete data set, we would be able to verify: given family size, whether the relationship "Family_size" == 1 + "Ticket_size" holds.

# In[ ]:




# #### 2.4 Manipulating "Fare"

# In[51]:

ax_fare = t_data["Fare"].plot.hist()
ax_fare.set_title("Histogram of the variable 'Fare'")
ax_fare.set(xlabel = "Fare")
# The distribution does not give us much insight. 
# Adjusting bins using the following code will result similar graph.
# plt.hist(t_data["Fare"], bins = np.arange(min(t_data["Fare"]), max(t_data["Fare"]) + 2, 2))


# Is there a way of improving our insight on the "Fare" variable? 
# 
# #### Recall that "Fare" is closely related to "Pclass" (passenger class), I now draw the "Fare" distribution conditional on the "Pclass".

# In[53]:

fig, axes = plt.subplots(nrows=2, ncols=2)
fig.set_size_inches(w=10,h=5)
t_data.loc[t_data["Pclass"] == 1, "Fare"].plot.hist(ax=axes[0,0]); 
axes[0,0].set_title('Fare distribution for Class_1'); axes[0,0].set(xlabel = 'Fare')
t_data.loc[t_data["Pclass"] == 2, "Fare"].plot.hist(ax=axes[0,1]); 
axes[0,1].set_title('Fare distribution for Class_2'); axes[0,1].set(xlabel = 'Fare')
t_data.loc[t_data["Pclass"] == 3, "Fare"].plot.hist(ax=axes[1,0]); 
axes[1,0].set_title('Fare distribution for Class_3'); axes[1,0].set(xlabel = 'Fare');
t_data["Fare"].plot.hist(ax=axes[1,1]); 
axes[1,1].set_title('Fare distribution for all classes'); axes[1,1].set(xlabel = 'Fare')
plt.tight_layout()


# We notice a common feature:
# #### The graphs for all the Pclasses are disturbed by outliers. In particular, it is suspicious that the range of Pclass_3 is comparable to that of Pclass_2.
# 
# I use the following code to have a look at the right tail of the Fare distribution conditional on Pclass_3.

# In[57]:

t_data.loc[(t_data["Pclass"] == 3) & (t_data["Fare"]>=30)].sort_values(["Ticket"], ascending = True).head(10)


# Interesting observations:
# 
# 1. Focusing on the first 7 observations. They share the same ticket number and fare. They must have bought the ticke together, because their names told me that they are all asians and potentially coming from the same country.
#    * It is not reasonable that each paid "56.4958" for having a seat.
# 2. Focusing on the family name "Sage". We observe similar things. This is a large family of 11 (8+2+1) people. It is difficult to imagine that each paid "69.5500" for travelling with Titanic.
# 
# ##### I thus argue that a more reasonable explanation is that the "Fare" variable stands for the total price of a given ticket number.

# In[58]:

# As I argued above. The Fare is the fare of the ticket.
# This means that we should divide the fare by the number of the people, who share the same ticket number.
t_data["each_fare"] = t_data["Fare"]/t_data["Ticket_size"]


# Now let us compare the unconditional "Fare" distribution.

# In[59]:

plt.figure(1, figsize=(9,4))
plt.subplot(1,2,1)
ax1 = t_data["each_fare"].plot.hist()
ax1.set_title("Histogram of 'each_fare'")
ax1.set(xlabel = 'each_fare')
plt.subplot(1,2,2)
ax2 = t_data["Fare"].plot.hist()
ax2.set_title("Histogram of 'fare'")
ax2.set(xlabel = 'fare')
plt.tight_layout()


# There are more concentrations on the left tail. Now let us compare the conditional distributions.

# In[60]:

fig, axes = plt.subplots(nrows=2, ncols=3)
fig.set_size_inches(w=12,h=6)
t_data.loc[t_data["Pclass"] == 1, "Fare"].plot.hist(ax=axes[0,0]); 
axes[0,0].set_title('"Fare" distribution for Pclass_1'); axes[0,0].set(xlabel = 'Fare');
t_data.loc[t_data["Pclass"] == 2, "Fare"].plot.hist(ax=axes[0,1]); 
axes[0,1].set_title('"Fare" distribution for Pclass_2'); axes[0,1].set(xlabel = 'Fare');
t_data.loc[t_data["Pclass"] == 3, "Fare"].plot.hist(ax=axes[0,2]); 
axes[0,2].set_title('"Fare" distribution for Pclass_3'); axes[0,2].set(xlabel = 'Fare');
t_data.loc[t_data["Pclass"] == 1, "each_fare"].plot.hist(ax=axes[1,0]); 
axes[1,0].set_title('"each_Fare" distribution for Pclass_1'); axes[1,0].set(xlabel = 'each_Fare');
t_data.loc[t_data["Pclass"] == 2, "each_fare"].plot.hist(ax=axes[1,1]); 
axes[1,1].set_title('"each_Fare" distribution for Pclass_2'); axes[1,1].set(xlabel = 'each_Fare');
t_data.loc[t_data["Pclass"] == 3, "each_fare"].plot.hist(ax=axes[1,2]); 
axes[1,2].set_title('"each_Fare" distribution for Pclass_3'); axes[1,2].set(xlabel = 'each_Fare');
plt.tight_layout()


# As expected, the values in the upper tails for each Pclass now have more regular behaviors.
# 
# Analogously, we could have a look at the boxplot.

# In[96]:

plt.figure(1, figsize=(9,9))
plt.subplot(1,2,1)
ax=sns.boxplot(x="Pclass", y='Fare', data=t_data, palette='RdBu');
ax.set(title='Fare')
ax.set_xticklabels(["1st class", "2nd class", "3rd class"])
plt.subplot(1,2,2)
ax=sns.boxplot(x="Pclass", y='each_fare', data=t_data, palette='RdBu');
ax.set(title='each_fare')
ax.set_xticklabels(["1st class", "2nd class", "3rd class"])
plt.show()
# t_data.boxplot(column=['each_fare'], by='Pclass')


# Till this stage, I have finished most of the data wrangling process.

# In[ ]:




# ### 3. Survival analysis

# #### 3.0 Sex and survival rate.
# 
# - Did gender influence survival rate? If so, Why exactly?
# 
# I will start by drawing the survival rate conditional on Sex.

# In[62]:

plt.figure(1, figsize=(6,4))
ax=sns.barplot(x="Sex", y='Survived', data=t_data, palette='RdBu');
ax.set(xlabel='Sex/Kids', ylabel = "Survival rate", title='Survival_percentage_conditional_on_Sex')
ax.set_xticklabels(["male", "female", "children"])
plt.show()


# In[63]:

survival_rate_males = t_data.loc[(t_data["Sex"]==0) & (t_data["Survived"]==1), "Sex"].value_counts()/t_data.loc[(t_data["Sex"]==0), "Sex"].value_counts()

survival_rate_females = t_data.loc[(t_data["Sex"]==1) & (t_data["Survived"]==1), "Sex"].value_counts()/t_data.loc[(t_data["Sex"]==1), "Sex"].value_counts()

survival_rate_kids = t_data.loc[(t_data["Sex"]==2) & (t_data["Survived"]==1), "Sex"].value_counts()/t_data.loc[(t_data["Sex"]==2), "Sex"].value_counts()

print "The survival rate of males is {}.".format(survival_rate_males.iloc[0]) + "\n" + "The survival rate of females is {}.".format(survival_rate_females.iloc[0]) + "\n" + "The survival rate of kids is {}.".format(survival_rate_kids.iloc[0])


# Since females and children have priority at emergency, this result is expected to some extent. Males have inferior survival rate; later we will see that maybe it is related to the fact that most of them travelled alone.
# 
# However, it is worthwhile noticing that the number of males largely exceeds that of females or children. The following graph illustrates the problem.

# In[64]:

plt.figure(1, figsize=(6,4))
ax=sns.countplot(x="Survived", hue='Sex', data=t_data, palette='RdBu');
ax.set(xlabel='Survival', title='Survival count, decomposed by Sex')
ax.set_xticklabels(["Not_survived", "Survived"])
ax.legend(labels = ["male", "female", "kids"])
plt.show()


# For those survived, the number of males is comparable to the other 2 groups, although the overall survival rate of males is far lower than the other 2 groups, 
# 
# We could also observe this problem from the following cross table. 

# In[65]:

# I make a contingency table between the "Survived" and "Sex" variables.

Survived_Sex_cross_tab = pd.crosstab(index = t_data["Survived"],columns = t_data["Sex"], margins = True)

Survived_Sex_cross_tab.index = ["Not_Survived","Survived","up_down_margin"]
Survived_Sex_cross_tab.columns = ["Male","Female","Kids", "left_right_margin"]
Survived_Sex_cross_tab

# type(Survived_Sex_cross_tab)


# If Sex did not have any influence on the survival rate, we would expect the survival rate to be uniformly distributedd across Sex. 
# 
# To check the above point, I now adjust the survival rate of each Sex group by their respective fraction. I now check whether the adjusted survival rate is uniform. I use a simple chi-square goodness of fit, which suggests that the adjusted survival rate is not uniform.

# In[66]:

weight_of_Sex = (Survived_Sex_cross_tab.loc["up_down_margin"]/len(t_data)).iloc[:-1]

survival_rate_on_Sex = (Survived_Sex_cross_tab.loc["Survived"]/Survived_Sex_cross_tab.loc["up_down_margin"]).iloc[:-1]

(chisq_value, p_value) = stats.chisquare(100* weight_of_Sex * survival_rate_on_Sex)

print "H0: The adjusted survival rate is uniformly distributed across Sex."
print "H1: The adjusted survival rate is not uniformly distributed across Sex."
print "The p value {} suggests that at a 5% critical level, we reject H0.".format(p_value)


# I also ask the question whether age is an important factor which leads to the inferior survival rate among males. The following figures seem to suggest that it be not the case. Indeed, the two distributions look similar.

# In[67]:

plt.figure(1, figsize=(12,6))
plt.subplot(2,1,1)
ax=sns.countplot(x="Age_groups", data=t_data[(t_data["Sex"]==0) & (t_data["Survived"]==1)], palette='RdBu');
ax.set(xlabel='Age_groups', title='Age_groups_Count_Conditional_on_Survived');
ax.set(title='Decomposing survived males by Age_groups')
plt.subplot(2,1,2)
ax=sns.countplot(x="Age_groups", data=t_data[(t_data["Sex"]==0) & (t_data["Survived"]==0)], palette='RdBu');
ax.set(xlabel='Age_groups', title='Age_groups_Count_Conditional_on_unsurvived');
ax.set(title='Decomposing unsurvived males by Age_groups')
plt.tight_layout()


# #### Furthermore, I conduct chi-square independence test to check the relationship between "Sex" and "Survival". 

# In[68]:

# Now I do the chi-square independence test to confirm that the "Sex" variable has influence on the survival.
(test_stat, p_value, degree_of_f, expected_freq)=stats.chi2_contingency(pd.crosstab(t_data.Survived, t_data.Sex), correction = True)

print "H0: Survival is independent of Sex."
print "H1: Survival is not independent of Sex."
print "The p value {} suggests that at a 5% critical level, we reject H0.".format(p_value)


# The result implies that the variable Sex has impact on Survival.
# 
# #### Is there a relationship between the size of each Sex group and its corresonpding survival rate? The following result suggests it be not the case.

# In[69]:

stats.spearmanr((t_data.loc[t_data["Survived"]==1,"Sex"].value_counts()/t_data["Sex"].value_counts()).sort_index(),                 t_data["Sex"].value_counts().sort_index())


# In[ ]:




# #### 3.1 Passenger class and survival rate
# 
# - Did passenger class influence survival rate? If so, Why exactly?

# In[97]:

# Bar plot on survival rate for each passenger class.
plt.figure(1, figsize=(9,5))
ax=sns.barplot(x="Pclass", y='Survived', data=t_data, palette='RdBu');
ax.set(xlabel='Pclass', ylabel = "Survival rate", title='Survival rate across Pclass')
ax.set_xticklabels(["1st class", "2nd class", "3rd class"])
plt.show()


# In[71]:

survival_rate_Pclass1 = t_data.loc[(t_data["Pclass"]==1) & (t_data["Survived"]==1), "Pclass"].value_counts()/t_data.loc[(t_data["Pclass"]==1), "Pclass"].value_counts()

survival_rate_Pclass2 = t_data.loc[(t_data["Pclass"]==2) & (t_data["Survived"]==1), "Pclass"].value_counts()/t_data.loc[(t_data["Pclass"]==2), "Pclass"].value_counts()

survival_rate_Pclass3 = t_data.loc[(t_data["Pclass"]==3) & (t_data["Survived"]==1), "Pclass"].value_counts()/t_data.loc[(t_data["Pclass"]==3), "Pclass"].value_counts()

print "The survival rate of Pclass 1 is {}.".format(survival_rate_Pclass1.iloc[0]) + "\n" + "The survival rate of Pclass 2 is {}.".format(survival_rate_Pclass2.iloc[0]) + "\n" + "The survival rate of Pclass 3 is {}.".format(survival_rate_Pclass3.iloc[0])


# The third class has the lowest survival rate. However, again, we also expect that the number of this third class is the largest, as illustrated by the following graph.

# In[98]:

# count plot
plt.figure(1, figsize=(9,5))
ax=sns.countplot(x="Pclass", hue='Survived', data=t_data, palette='RdBu');
ax.set(xlabel='Pclass', title='Survival_Count_across_Passenger_classes')
ax.legend(labels = ["not survived","survived"])
ax.set_xticklabels(["1st class", "2nd class", "3rd class"])
plt.show()


# The figure above suggests that there seem to be far more passengers in the third class. (passengers may not be uniformly distributed across passenger classes.)
# 
# As in the previous subsection, I take into account of this size effect of the group, and adjust the group survival rate. I proceed as follows.

# In[73]:

# Again I make a contingency table between the "Survived" and "Pclass" variables.

Survived_Pclass_cross_tab = pd.crosstab(index = t_data["Survived"],columns = t_data["Pclass"], margins = True)

Survived_Pclass_cross_tab.index = ["Not_Survived","Survived","up_down_margin"]
Survived_Pclass_cross_tab.columns = ["Pclass_1","Pclass_2","Pclass_3", "left_right_margin"]
Survived_Pclass_cross_tab

# type(Survived_Sex_cross_tab)


# In[74]:

weight_of_Pclass = (Survived_Pclass_cross_tab.loc["up_down_margin"]/len(t_data)).iloc[:-1]

survival_rate_on_Pclass = (Survived_Pclass_cross_tab.loc["Survived"]/Survived_Pclass_cross_tab.loc["up_down_margin"]).iloc[:-1]

(chisq_value, p_value) = stats.chisquare(100* weight_of_Pclass * survival_rate_on_Pclass)

print "H0: The adjusted survival rate is uniformly distributed across Pclass."
print "H1: The adjusted survival rate is not uniformly distributed across Pclass."
print "The p value {} suggests that at a 5% critical level, we do not reject H0.".format(p_value)


# The above shows that, if we take into account of the number of passengers travelling in each class, the survival rate of Pclass 3 is not statistically inferior to the other two classes. 
# 
# Now I do the chi-square independence test to confirm that the "Plcass" variable has influence on the survival.

# In[75]:

(test_stat, p_value, degree_of_f, expected_freq)=stats.chi2_contingency(pd.crosstab(t_data.Survived, t_data.Pclass), correction = True)

print "H0: Survival is independent of Pclass."
print "H1: Survival is not independent of Pclass."
print "The p value {} suggests that at a 5% critical level, we reject H0.".format(p_value)


# Why is this the case? Maybe it has something to do with the Sex.
# 
# In the following two plots, we notice that it may be because there are unproportionately more males at the 3rd class who did not survive compared to the other two passenger classes.

# In[99]:

# Countplot, by Sex
plt.figure(1, figsize=(9,5))
ax=sns.countplot(x="Pclass", hue = "Sex", data=t_data, palette='RdBu');
ax.set(xlabel='Pclass', title='Survival count across Pclass, decomposed by Sex')
ax.legend(labels = ["male","female", "Kids"])
ax.set_xticklabels(["1st class", "2nd class", "3rd class"])
plt.show()

# The above code could be also rewriten as follows. Check the difference.
# plt.figure(1, figsize=(9,5))
# ax=sns.factorplot(x="Pclass", hue = "Sex", data=t_data, palette='RdBu', kind = 'count');
# ax.set(xlabel='Pclass', title='Survival_Count_Based_on_Pclass')
# plt.show()


# In[100]:

# barplot shows the inferior survival rate of males at 3rd class. 
plt.figure(1, figsize=(9,6))
ax=sns.barplot(x="Pclass", y='Survived', hue = "Sex", data=t_data, palette='RdBu');
ax.set(xlabel='Pclass', ylabel = "Survival rate", title='Survival rate across Pclass, decomposed by Sex')
# ax.legend(labels = ["male","female", "Kids"])
ax.set_xticklabels(["1st class", "2nd class", "3rd class"])
plt.show()


# In[ ]:




# #### 3.2 Age groups and survival rate.
# 
# - How do survival rates vary for different age groups?

# I start by plotting the survival rate for each age group.

# In[78]:

plt.figure(1, figsize=(9,5))
ax=sns.barplot(x="Age_groups", y='Survived', data=t_data);
ax.set(xlabel='Age_groups', ylabel = "Survival Rate", title='Survival_Rate_Based_on_Age_groups')
# ax.legend(labels = ["Not_Survived","Survived"])
plt.tight_layout()


# I decompose each age group by Sex, and draw the corresponding survival rate.

# In[79]:

plt.figure(1, figsize=(9,5))
ax=sns.barplot(x="Age_groups", y="Survived", hue='Sex', data=t_data, palette='RdBu');
ax.set(xlabel='Age_groups', ylabel = "Survival Rate", title='Survival_Rate_Based_on_Age_groups, decomposed by Sex')
# ax.legend(labels = ["Not_Survived","Survived"])
plt.tight_layout()


# The following plot shows that the number of males is larger than that of females in each age group. 

# In[80]:

plt.figure(1, figsize=(9,5))
ax=sns.countplot(x="Age_groups", hue='Sex', data=t_data, palette='RdBu');
ax.set(xlabel='Age_groups', title='Survival_Count_Based_on_Age_groups, decomposed by Sex.')
# ax.legend(labels = ["Not_Survived","Survived"])
plt.tight_layout()


# I now do a chi-square independence test to examine the relationship between Age_groups and survival.

# In[81]:

# Now I do the chi-square independence test to confirm that the "Age_groups" variable 
# has influence on the survival.
(test_stat, p_value, degree_of_f, expected_freq)=stats.chi2_contingency(pd.crosstab(t_data.Survived, t_data.Age_groups), correction = True)

print "H0: Survival is independent of Age_groups."
print "H1: Survival is not independent of Age_groups."
print "The p value {} suggests that at a 5% critical level, we reject H0.".format(p_value)


# In[ ]:




# #### 3.3 Family size and survival rate.
# 
# - Do families with larger size survive more often?
# - Do people who travel together survive more often?

# In[82]:

# Countplot
plt.figure(1, figsize=(9,5))
ax=sns.countplot(x="Family_size", hue='Survived', data=t_data, palette='RdBu');
ax.set(xlabel='Family_size', title='Survival_Count_for_each_Family_size')
plt.tight_layout()


# In[83]:

# barplot
plt.figure(1, figsize=(9,5))
ax=sns.barplot(x="Family_size", y="Survived", data=t_data, palette='RdBu');
ax.set(xlabel='Family_size', ylabel="Survival rate", title='Survival_Rate_across_Family_size')
plt.tight_layout()


# We notice that 
# 1. people with family size 0 are less likely to survive. ((survival rate < 50%))
# 2. for family size ranging from 1 to 3, the survival rate is above 50%.
# 3. there is survival penalty (survival rate < 50%) for those families with a size greater than 3. 
# 
# Why are there survival penalties? I now examine the families with size greater than 3. It turns out that most of these families are in the 3rd class.

# In[84]:

# t_data.loc[t_data["Family_size"] >=4].sort_values(["Pclass"], ascending = False)

t_data.loc[t_data["Family_size"]>=4, "Pclass"].value_counts()


# The following graph shows that number of youngsters in these families (size>=4) is unproportionately high.

# In[85]:

plt.figure(1, figsize=(9,4))
ax=sns.countplot(x="Age_groups", hue= 'Survived', data=t_data.loc[t_data["Family_size"]>=4], palette='RdBu');
ax.set(xlabel='Age_groups', ylabel = 'count', title='survival_count_by_age_groups, from families of size >= 4')
plt.tight_layout()

# On average, neither the children nor the adults have higher survival rate.


# I notice that the survival rate of kids ("age_group_0_8") in such families are especially low.

# In[86]:

# # I now show that kids within big family tend not to survive.
plt.figure(1, figsize=(9,5))
ax=sns.countplot(x="Family_size", hue='Survived', data=t_data[(t_data["Age_groups"] == "age_0_8") & (t_data["Family_size"] >= 4)],                  palette='RdBu');
ax.set(xlabel='Family_size', title='Survival count for kids from families with size >=4')
plt.show()


# These kids were all from the third class.

# In[87]:

t_data[(t_data["Age_groups"] == "age_0_8") & (t_data["Family_size"] >= 4)].Pclass.value_counts()


# In[ ]:




# I now ask why do the families of size ranging from 0 to 3 have higher survival rate. 
# 
# Decomposing by Pclass, I find that these families are distributed relatively uniformly across passenger classes.

# In[88]:

t_data.loc[(t_data["Family_size"]>0) & (t_data["Family_size"]<4), "Pclass"].value_counts()


# I then decompose them by Sex, I find that these families have slightly higher proportion of females, who in general survived more often.

# In[89]:

plt.figure(1, figsize=(9,5))
ax=sns.countplot(x="Age_groups", hue='Sex', data=t_data[(t_data["Family_size"]>0) & (t_data["Family_size"]<4)],                  palette='RdBu');
ax.set(xlabel='Age_groups', title='Survival_Count_Based_on_Age_groups, decomposed by Sex.')
# ax.legend(labels = ["Not_Survived","Survived"])
plt.tight_layout()


# In[ ]:




# In[ ]:




# At last, I ask whether people's survival rate is higher, if they travel together with at least one person.

# In[90]:

plt.figure(1, figsize=(6,4))
ax=sns.barplot(x="Together", y='Survived', data=t_data, palette='RdBu');
ax.set(xlabel='Travelling together', ylabel = "Survival Rate", title='Survival percentage, conditional on together or not')
ax.set_xticklabels(["alone", "Together"])
plt.show()


# The survival rate is considerably lower if one travels alone.
# 
# I decompose the people who travel alone by Sex, I find that male is the dominant sex at the alone group, who has the least survival rate among all Sexes.

# In[91]:

plt.figure(1, figsize=(6,4))
ax=sns.countplot(x="Together", hue = "Sex", data=t_data, palette='RdBu');
ax.set(xlabel='Travelling together', title='Survival count, conditional on "together or alone" / "Sex"')
ax.set_xticklabels(["alone", "Together"])
ax.legend(labels = ["male", "female", "Kids"])
plt.show()


# I also decompose the people who travel alone by Pclass, I find that 3rd class is dominant at the alone group, which is the class with the lowest survival rate.

# In[104]:

plt.figure(1, figsize=(6,4))
ax=sns.countplot(x="Together", hue = "Pclass", data=t_data, palette='RdBu');
ax.set(xlabel='Travelling together', title='Survival_count, Together or not / Pclass')
ax.set_xticklabels(["alone", "Together"])
# ax.legend("Pclass", ["1st class", "2nd class", "3rd class"])
ax.legend(["1st class", "2nd class", "3rd class"])
plt.show()


# The following code shows that there seem to be interaction effect from the variables Pclass and Sex:
# 
# Those who travel alone are very likely to be both male and in the 3rd class.

# In[93]:

# t_data.groupby(["Sex", "Pclass"]).\
# filter(lambda x: (x["Fare"].nunique()>1)).sort_values(["Ticket"])
t_data[t_data["Together"]==0].groupby(["Together", "Sex", "Pclass"]).size()


# In[ ]:




# ### 4. Summary

# In this exercise, I have the following key observations in manipulating the data:
# 
# 1. I decompose the "Name" variable and extract "prefix" to help me better fill the missing values in "Age".
# 2. Apart from familiy size, I find that "Ticket" number is a good measure for identifying whether people were travelling together.
# 3. I find that the "Fare" variable actually accounts for the price of one ticket, whereas many people who travel together can share one ticket. I thus divide the Fare by ticket size to find the price each individual paid. 
# 
# I have the following results in investigating which factors may contribute to survival. 
# 
# 1. The survival rate of males is significantly lower than that of females and kids.
#     * Male (16.51%) versus Female(74.31%) and Kids (65.52%)
# 2. Passengers in the 3rd class are less likely to survive. 
#     * Pclass_1 (62.96%), Pclass_2 (47.28%), Pclass_3 (24.24%)
#     * This inferior survival rate is largely contributed by large number of males who travel alone in this class.
# 3. Survival rate is highest for children less than 8 years old. Females have dominant survival rate compared to males in each age group. 
# 4. Family size
#    * Families of size ranging from 1 to 3 have survival rates higher than 50%. These families have a good number of females (compared to that of males), which contribute to higher survial rates.
#    * There is survival penalty for those families of size greater than 3. Most of these families travel in 3rd class.
# 5. People who travel alone survive less often. It is males who travael alone in the third class that contribute most to the inferior survival rate of this group.  

# #### 4.0 Further observations and limitations

# The above data set does not allow us to access some important information for survival. For example, we do not know the time point at which a passenger realizes that he/she should escape; we do not know the exact distribution of cabines, each individual' whereabout and their activities at the time of crash; who were closest to the rescure boat; was evacuation organized efficiently; how many people did not survive because they tried to helped the others etc.
# 
# For future work, it would be also important to use more advanced methods such as random forests, PCA etc. to give more structured explanations based on the existing data.

# ### 5. Selected references

# #### Graphs: 
# 
# http://stackoverflow.com/questions/6541123/improve-subplot-size-spacing-with-many-subplots-in-matplotlib
# 
# http://stackoverflow.com/questions/31029560/plotting-categorical-data-with-pandas-and-matplotlib
# 
# https://scientificallysound.org/2016/06/09/matplotlib-how-to-plot-subplots-of-unequal-sizes/
# 
# http://www.cnblogs.com/wei-li/archive/2012/05/23/2506940.html
# 
# http://stackoverflow.com/questions/25239933/how-to-add-title-to-subplots-in-matplotlib
# 
# http://chrisalbon.com/python/seaborn_color_palettes.html
# 
# 
# #### Tests: 
# 
# https://hflog.wordpress.com/2014/04/01/how-to-perform-a-chi-squared-goodness-of-fit-test-in-python/
# 
# http://hamelg.blogspot.com/2015/11/python-for-data-analysis-part-25-chi.html
# 
# 
# #### Groupby related:
# 
# http://stackoverflow.com/questions/20995196/python-pandas-counting-and-summing-specific-conditions
# 
# http://stackoverflow.com/questions/33823091/python-pandas-counting-the-frequency-of-a-specific-value-in-each-row-of-datafra
