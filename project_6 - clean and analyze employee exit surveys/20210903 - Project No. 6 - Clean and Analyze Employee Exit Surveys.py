#!/usr/bin/env python
# coding: utf-8

# # Project 6 - Clean and Analyze Employee Exit Surveys

#  
#  

# ## 1. Introduction:

# This project aims cleaning and analyzing exit surveys to learn how different factors affect employee resignations.
# 
# To reach this goal, we wil try to reply for the following questions:
# * Are employees who only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been there longer?
# * Are the younger employees resigning due to some kind of dissatisfaction? What about older employees?
# 
# 

# 
# We will work with two modified datasets from exit surveys from employees of:
# * the Department of Education, Training and Employment ([DETE](https://data.gov.au/dataset/ds-qld-fe96ff30-d157-4a81-851d-215f2a0fe26d/details?q=exit%20survey))
# * and the Technical and Further Education ([TAFE](https://en.wikipedia.org/wiki/TAFE_Queensland)) institute in Queensland, Australia. 

# ## Initial overviewing of datasets :

# ### 2.1 Importing datasets

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


dete_survey=pd.read_csv("dete_survey.csv")


# In[3]:


tafe_survey=pd.read_csv("tafe_survey.csv")


# ### 2.2 Checking first and last 5 rows of each dataset: 

# #### 2.2.1 dete_survey:

# In[4]:


pd.set_option('display.max_columns', None)


# In[5]:


dete_survey


# In[6]:


dete_survey.info()


# In[7]:


dete_survey.isnull().sum()


# #### 2.2.2 tafe_survey:

# In[8]:


tafe_survey


# In[9]:


tafe_survey.info()


# In[10]:


tafe_survey.isnull().sum().sort_values()


# ### 2.3. First notes about datasets:

# #### Notes of dete_survey: 
#  - dataset dimension: 822 rows × 56 columns
#  - columns with many missing values which we will need mandatory explore and try to understand the reason and if we have any solution:
# 
#         Business Unit                          696
#         Aboriginal                             806
#         Torres Strait                          819
#         South Sea                              815
#         Disability                             799
#         NESB                                   790
# 
# - Then we have following column still with many missing values, although less than above ones:
#         
#         Classification                         367
#       
# - Dates columns `Cease Date` and`DETE Start Date` contains value "Not Stated" -  this kind of information must be replace by NaN in order to be list as null field.
# 

# #### Notes of tafe_survey: 
# - dataset dimension: 702 rows × 72 columns
# - the columns with more missing values are the following:
# 
#         Contributing Factors. Career Move - Public Sector                265
#         Contributing Factors. Maternity/Family                           265
#         Contributing Factors. Ill Health                                 265
#         InductionInfo. Topic:Did you undertake a Corporate Induction?    270
#         Main Factor. Which of these was the main factor for leaving?     589
#         
#         
#     

# #### Note common for both dataset:
# - Columns with date values are not with datetime type - this columns type must be changed, because we will need to use this information to check how many time workers were in their job before their resignation.
# - Columns name must be simplified and the same in both datasets, mainly the ones that we already know that we will use: age, genre, dates, reason for person left from the job, ...
# - Columns about same information must have the same name in both dataset.
# - Attending this project goal we must identify what are the columns which we could identify as reason for the resignation, and disregard the other columns.

# ### 2.4. Datasets dictionary: 
# 

# From the information collected, the dictionary for the main columns should be according to the following:
# * **dete_survey:**
#     - `ID`: An id used to identify the participant of the survey
#     - `SeparationType`: Tason why the person's employment ended
#     - `Cease Date`: The year or month the person's employment ended
#     - `DETE Start Date`: The year the person began employment with the DETE
# 
# 
# * **tafe_survey:**
#     - `Record ID`: An id used to identify the participant of the survey
#     - `Reason for ceasing employment:` The reason why the person's employment ended
#     - `LengthofServiceOverall`. `Overall Length of Service at Institute (in years)`: The length of the person's employment (in years)
# 

# ## 3. Data Cleaning

# ### 3.1 Converting the "Not Stated" value to NaN in dete_survey:

# In[11]:


dete_survey=pd.read_csv("dete_survey.csv", na_values= "Not Stated")


# In[12]:


dete_survey.head(5)


# <img src="replace_by_nan.png">

# ### 3.2 - Dropping columns that we will not use in our analyze:

# Attending our main goal for this project, we can drop some columns which even contains interesting information, that information is not mandatory to answer to the questions of our project's goal.
# 
# Regarding DETE survey we will drop following columns because we consider all of them are referring to dissatisfaction reason. So, we will not see to them now.
# <img src="dete_drop_col.png">

# In[13]:


dete_survey_updated= dete_survey.drop(dete_survey.columns[28:49], axis=1)


# The new columns in our dete dataset are the following

# In[14]:


dete_survey_updated.info()


#   

# Regarding tafe_survey we decided to drop following columns, which we considered that are detailed reason of dissatisfaction:
# <img src="tafe_drop_col.png">

# In[15]:


tafe_survey_updated= tafe_survey.drop(tafe_survey.columns[17:66], axis=1)


# In[16]:


tafe_survey_updated.info()


# <span style="background: yellow">**IMPORTANT:**</span>
# 
# 
# Following dropping above columns we have smaller dataset, with what will be much more easier to check the common columns and to give to those columns the same name.
# New datasets dimension:
# - dete_survey_updated: 822 rows x 35 columns
# - tafe_survey_updated: 702 rows x 23 columns
# 

# ### 3.3 - Renaming columns: 

# Regarding **dete_survey_updated**, we will use the following criteria to update the column names:
# 
# * Make all the capitalization lowercase.
# * Remove any trailing whitespace from the end of the strings.
# * Replace spaces with underscores ('_').
# 

# In[17]:


dete_survey_updated.columns=dete_survey_updated.columns.str.lower().str.strip().str.replace("\s+","_", regex=True)


# In[18]:


dete_survey_updated.columns


# Regarding **tafe_survey_updated**, we will use the same criteria as before to update the column names, and additionally we will check columns one by one and check if we we can immediately to correspond it to the same name that we we have already in dete_survey_updated.
#     
# * Make all the capitalization lowercase.
# * Remove any trailing whitespace from the end of the strings.
# * Replace spaces with underscores ('_').
# 
# 

# In[19]:


tafe_survey_updated.columns


# | tafe_columns | common_column_with_dete | not_common_column |
# | --- | --- | --- |
# |'Record ID', | id||
# |'Institute', |business_unit||
# |'WorkArea', || workarea|
# |'CESSATION YEAR',|cease_date||
# |'Reason for ceasing employment',|separationtype||
# |'Contributing Factors. Career Move - Public Sector ',|career_move_to_public_sector'||
# |'Contributing Factors. Career Move - Private Sector ',|career_move_to_private_sector ||
# |'Contributing Factors. Career Move - Self-employment',|| self_employment|
# |'Contributing Factors. Ill Health',|ill_health||
# |'Contributing Factors. Maternity/Family',|maternity/family||
# |'Contributing Factors. Dissatisfaction',|| dissatisfaction|
# |'Contributing Factors. Job Dissatisfaction',|job_dissatisfaction|
# |'Contributing Factors. Interpersonal Conflict',||interpersonal_conflict|
# |'Contributing Factors. Study', || ~study/travel |
# |'Contributing Factors. Travel',| |~study/travel|
# |'Contributing Factors. Other', | |other|
# |'Contributing Factors. NONE',|none_of_the_above||
# |'Gender. What is your Gender?',| gender||
# |'CurrentAge. Current Age',|age||
# |'Employment Type. Employment Type'| employment_status||
# |'Classification. Classification',| | ~classification & position||
# |'LengthofServiceOverall. Overall Length of Service at Institute (in years)',||institute_service|
# |'LengthofServiceCurrent. Length of Service at current workplace (in years)'|| role_service|

# In[20]:


columns_rename= {'Record ID':"id",
'Institute': "business_unit",
'WorkArea':"workarea",
'CESSATION YEAR':"cease_date",
'Reason for ceasing employment':"separationtype",
'Contributing Factors. Career Move - Public Sector ':"career_move_to_public_sector",
'Contributing Factors. Career Move - Private Sector ':"career_move_to_private_sector",
'Contributing Factors. Career Move - Self-employment':"self_employment",
'Contributing Factors. Ill Health':"ill_health",
'Contributing Factors. Maternity/Family':"maternity/family",
'Contributing Factors. Dissatisfaction':"dissatisfaction",
'Contributing Factors. Job Dissatisfaction':"job_dissatisfaction",
'Contributing Factors. Interpersonal Conflict':"interpersonal_conflict",
'Contributing Factors. Study':"study",
'Contributing Factors. Travel':"travel",
'Contributing Factors. Other':"other",
'Contributing Factors. NONE':"none_of_the_above",
'Gender. What is your Gender?':"gender",
'CurrentAge. Current Age':"age",
'Employment Type. Employment Type':"employment_status",
'Classification. Classification' :"position",
'LengthofServiceOverall. Overall Length of Service at Institute (in years)':"institute_service",
'LengthofServiceCurrent. Length of Service at current workplace (in years)':"role_service"
}


# In[21]:


tafe_survey_updated.rename(columns_rename, axis=1, inplace=True)


# In[22]:


tafe_survey_updated.columns


# ### Dropping rows not regarding resignation

# In `separationtype` we have other kind of reasons to leave from the job that were not by employees resignation.  Attending our project goal, we will drop those reasons:

# In[23]:


# checking the unique values in this column


# In[24]:


dete_survey_updated["separationtype"].value_counts()


# In[26]:


tafe_survey_updated["separationtype"].value_counts()


# In[274]:



plt.figure(figsize=(30,12))
plt.subplot(1,2,1)
dete_survey_updated["separationtype"].value_counts().plot(kind='pie',
                                                         autopct='%1.0f%%',
                                                         startangle=55,
                                                         cmap='tab10',
                                                         explode=(0,0.2,0.2,0.2,0,0,0,0,0),
                                                         textprops={'fontsize': 24,'color':"w", "weight":"bold"},
                                                         shadow=True,
                                                         radius=0.9,
                                                         pctdistance=0.8,
                                                         title="DETE Separation type",
                                                         
                                                         legend=True
                                                     )
plt.title('DETE Separation type', fontsize=40)   
plt.legend(loc="upper left", fontsize= 24,  bbox_to_anchor=(-0.5, 0, 1.5, 0))

plt.subplot(1,2,2)
tafe_survey_updated["separationtype"].value_counts().plot(kind='pie',
                                                         autopct='%1.0f%%',
                                                         startangle=55,
                                                         cmap='tab20b',
                                                         explode=(0.1,0,0,0,0,0),
                                                        
                                                         legend=True,
                                                         shadow=True,
                                                         radius=0.9,
                                                         pctdistance=0.8,
                                                         label=False,
                                                         title="TAFE Separation type",
                                                         textprops={'fontsize': 24, "weight":"bold",'color':"w" },
                                                        
                                                        )
plt.title('TAFE Separation type', fontsize=40)   
plt.legend(loc="upper left", fontsize= 24,  bbox_to_anchor=(0.5, 0, 1.5, 0))
plt.show()


# Based on this results, we can see that the resignation has a big percentage among the reasons for employee exit.
# 
# * In the DETE, most employee exit because of retirement (by age,voluntary early and health)- 50%, followed closely by resignation(other reasons, employer, move overseas/interstate)-38%.
# * In the TAFE, most employee exit because they resigned (49%), followed by contract expiration(18%), retrenchment (15%), and retirement (12%).
# 
# 

# In[27]:


# identifying columns which we want to keep for our analyze


# <font size="5" color="blue"> **DETE dataset**:</font>

# In[28]:


dete_survey_updated["resignation"]=dete_survey_updated["separationtype"].str.contains(r'[Rr]esignation', regex=True)


# In[29]:


dete_survey_updated["resignation"]


# In[30]:


tafe_survey_updated["resignation"]=tafe_survey_updated["separationtype"].str.contains(r'[Rr]esignation', regex=True)


# In[31]:


tafe_survey_updated["resignation"]


# In[32]:


# dropping rows with what we will not work


# In[33]:


dete_resignation=dete_survey_updated.copy().set_index("resignation").drop(False)


# In[34]:


dete_resignation


# <font size="5" color="blue"> **TAFE dataset**:</font>

# In[35]:


tafe_resignation=tafe_survey_updated.copy().set_index("resignation").drop(False)


# In[36]:


tafe_resignation


# <span style="background: yellow">**IMPORTANT:**</span>
# 
# 
# Following dropping above rows we have smaller datasets, with what will be much more easier to work:
# New datasets dimension:
# - dete_survey_updated: 311 rows x 35 columns
# - tafe_survey_updated: 341 rows x 23 columns
# 
# 
# Now we are in conditions to analyze the following 2 information in order we can reply to the two questions in this project objectives:
# 1. Checking the lenght of service in each instition of employees that resigned
# 1. Checking dissatisfaction of employees that resigned
# 

# ## 4 - Institution and Role Service time per institute

# <font size="5" color="blue"> **Tafe dataset**:</font>

# Let's us check the tafe dataset. Our date columns are:
# 
# - `institute_service` - The length of the person's employment in this institute (in years) - split per years ranges
# - `role_service` - The length of the person's employment in the current workplace (in years)
# - `cease_date ` - The year or month the person's employment ended
# 

# In[37]:


tafe_resignation["cease_date"].value_counts()


# In[38]:


tafe_resignation["institute_service"].value_counts()


# In[39]:


tafe_resignation["role_service"].value_counts()


# <font size="5" color="blue"> **DETE dataset**:</font>

# In the dete we have:
# - `cease_date`: The year or month the person's employment ended
# - `dete_start_date`: The year the person began employment with the DETE
# - `role_start_dat`: the year the person began the employment in the current workplace
# 
# First, if we only have the year that person began. We will disregard the month and put both columns at same format. 
# 
# 
# Then, we will create one column with the difference between these values, then present the values between years ranges which will correspond to the `institute_service` and the `role_service` of tafe dataset
# 

# In[40]:


# 1 -  we will extract from the cease_date the year information:


# In[41]:


dete_resignation["cease_date"].value_counts()


# In[42]:


dete_resignation["cease_date"]=dete_resignation["cease_date"].astype(str)


# In[43]:


dete_resignation["cease_date"].dtype


# In[44]:


dete_resignation["cease_date"]=dete_resignation["cease_date"].str.extract(r"([1-2]{1}[0-9]{3})")


# In[45]:


dete_resignation["cease_date"]


# In[46]:


dete_resignation["cease_date"].value_counts()


# In[47]:


dete_resignation["cease_date"]=dete_resignation["cease_date"].astype("float")


# In[48]:


dete_resignation["cease_date"].dtype


#   

# In[49]:


# 2 -  we will check if dete_start_date at same format


# In[50]:


dete_resignation["dete_start_date"].dtype


# In[51]:


dete_resignation["dete_start_date"].value_counts()


# In[52]:


dete_resignation["role_start_date"]


# In[53]:


# 3 - we will calculate the period during what employee work at the institute and at current workplace:


# In[54]:


dete_resignation["institute_service_exact_time"]=dete_resignation["cease_date"]-dete_resignation["dete_start_date"]


# In[55]:


dete_resignation["institute_service_exact_time"].value_counts().sort_index()


# In[56]:


dete_resignation.boxplot("institute_service_exact_time")


# In[57]:


dete_resignation["role_service_exact_time"]=dete_resignation["cease_date"]-dete_resignation["role_start_date"]


# In[58]:


dete_resignation["role_service_exact_time"].value_counts().sort_index()


# In[59]:


dete_resignation.boxplot("role_service_exact_time")


# **CONCLUSION: based ont this data reffering the role service in the dete, we should disregard "-1" and "1813".**

# In[60]:


# 4 - we will present the information in ranges of year


# In[61]:


#if we just want split the data by random bins:
dete_resignation["institute_service_exact_time"].value_counts(bins=7).sort_index()


# In[62]:


#if we just want split the data exactly in a specific bins:
bins=[(-1, 1), (1, 2), (2, 4), (4, 6), (6, 10), (10, 20), (20,49)]

index=pd.IntervalIndex.from_tuples(bins)
intervals=index.values
labels=["Less than 1 year", "1-2", "3-4", "5-6", "7-10", "11-20", "More than 20 years"]
to_name={interval:label for interval, label in zip(intervals,labels)}

dete_resignation["institute_service"]=pd.CategoricalIndex(pd.cut(dete_resignation["institute_service_exact_time"], bins=index)).rename_categories(to_name)


# In[63]:


dete_resignation["institute_service"].value_counts().sort_index()


# In[64]:


bins=[(-1, 1), (1, 2), (2, 4), (4, 6), (6, 10), (10, 20), (20,49)]

index=pd.IntervalIndex.from_tuples(bins)
intervals=index.values
labels=["Less than 1 year", "1-2", "3-4", "5-6", "7-10", "11-20", "More than 20 years"]
to_name={interval:label for interval, label in zip(intervals,labels)}

#dete_resignation["role_service"]=pd.cut(dete_resignation["role_service_exact_time"], bins=bins, labels=labels, ordered=True)
dete_resignation["role_service"]=pd.CategoricalIndex(pd.cut(dete_resignation["role_service_exact_time"], bins=index)).rename_categories(to_name)


# In[65]:


dete_resignation["role_service"].value_counts().sort_index()


# ## 5 - Dissatisfaction of employees per institute

# The following columns are the columns that identified if employees resigned becauase dissatisfaction or not.
# This columns must only contains boolean (True, False, NaN).
# If the employee indicated any of these factors caused them to resign, we'll mark them as dissatisfied in a new column. 
# 
# <img src="dissatisfaction.png">
# 
# 
# **Tafe survey:**
# The columns reffering to dissatisfaction are the following and are not with boolean description, yet:
# * dissatisfaction 
# * job_dissatisfaction
#     
# **Dete survey:**
# The columns reffering to dissatisfaction are the following and are already with boolean description:
# * job_dissatisfaction
# * dissatisfaction_with_the_department
# * physical_work_environment
# * lack_of_recognition
# * lack_of_job_security
# * work_location
# * employment_conditions
# * work_life_balance
# * workload
# 
# 

# ### 5.1 - TAFE: Converting content of dissatisfaction columns to boolean content:

# In[66]:


#rechecking content of each column:


# In[67]:


tafe_resignation["dissatisfaction"].value_counts()


# In[68]:


tafe_resignation["job_dissatisfaction"].value_counts()


# In[69]:


#create a function to change the column content:


# In[70]:


def label(element, x):
    if element == x:
        return True
    elif element== "-":
        return False
    else:
        return None


# In[71]:


# convert the column content in boolean value:


# In[72]:


tafe_resignation["dissatisfaction_bol"]=tafe_resignation["dissatisfaction"].apply(label, x="Contributing Factors. Dissatisfaction ")


# In[73]:


tafe_resignation["dissatisfaction_bol"].value_counts(dropna=False)


# In[74]:


tafe_resignation["job_dissatisfaction_bol"]=tafe_resignation["job_dissatisfaction"].apply(label, x="Job Dissatisfaction")


# In[75]:


tafe_resignation["job_dissatisfaction_bol"].value_counts(dropna=False)


# ### 5.2 - TAFE: Creating dissatisfied column for each dataset -> if true means this was the reason for the resignation

# **tafe survey:**

# In[76]:


# create a new column if with final classification:


# In[77]:


tafe_resignation["dissatisfied"]=tafe_resignation[["dissatisfaction_bol","job_dissatisfaction_bol"]].any(axis=1, skipna=False)


# In[78]:


tafe_resignation["dissatisfied"]. value_counts()


# **dete survey:**

# In[79]:


dete_resignation["dissatisfied"]=dete_resignation[["job_dissatisfaction",
    "dissatisfaction_with_the_department",
    "physical_work_environment",
    "lack_of_recognition",
    "lack_of_job_security",
    "work_location",
    "employment_conditions",
    "work_life_balance",
    "workload"]].any(axis=1, skipna=False)


# In[80]:


dete_resignation["dissatisfied"]. value_counts()


# ## 6 - Combining the datasets

# First, let's add a column to each dataframe that will allow us to easily distinguish between the two.
# 
# * Add a column named institute to dete_resignation. Each row should contain the value DETE.
# * Add a column named institute to tafe_resignation. Each row should contain the value TAFE.
# 

# In[81]:


dete_resignation["institute"]="DETE"


# In[82]:


tafe_resignation["institute"]="TAFE"


# In[83]:


combined=pd.concat([dete_resignation,tafe_resignation])


# In[84]:


combined


# ### 6.1 - Drop columns with many missing values

# In[85]:


combined.notnull().sum().sort_values()


# In[86]:


combined_updated=combined.copy().dropna(axis=1, thresh=500)


# In[87]:


combined_updated


# Since this moment we will work only with columns with at least 500 non null values (after combined both dataset), this means that are the common columns between dataset with less missing values.

# ## Resignation vs Institute Service Time vs Dissatisfaction 

# ###  7.1 - Resignation vs Institute_Service time

# In[88]:


combined_updated["institute_service"].value_counts()


# As we saw before, we have 7 ranges of years for `institute_service` and `role_service`.
# However in order to simplify, we decided to reduce it to the following 4 ranges of years and classification:
# 
#     New: Less than 3 years at a company
#     Experienced: 3-6 years at a company
#     Established: 7-10 years at a company
#     Veteran: 11 or more years at a company
# 

# In[89]:


def label_service_time(element):
    if element == "Less than 1 year" or element == "1-2":
        return "New"
    elif element == "3-4" or element == "5-6":
        return "Experienced"
    elif element == "7-10":
        return "Established"
    elif element == "11-20" or element == "More than 20 years":
        return "Veteran"
    else:
        return None


# In[90]:


combined_updated["service_cat"]=combined_updated["institute_service"].apply(label_service_time)


# In[326]:


service_cat_dist=combined_updated["service_cat"].value_counts()


# In[327]:


service_cat_dist


# In[374]:


service_cat_dist.plot(kind='pie', subplots=True, wedgeprops=dict(width=.5),
                      startangle=45, autopct="%1.1f%%", pctdistance=0.8
                     )
plt.title("Experience level of resigned employee")
plt.show()


# <span style="background: yellow">IMPORTANT</span>
# Based on this results we can conclude that the majority of employers that resigned are the newer employees

# ### 7.2 - Resignation vs Dissatisfaction

# In[276]:


combined_updated["dissatisfied"].value_counts(dropna=False)


# In[292]:


print("IMPORTANT:"
 "\n"   
    "Rechecking the results about the dissatisfaction frequency, we can conclude: \n"
f"* only {240/(403+240+9)*100:,.2f}% of employees confirmed that dissastifaction were the motivation for their resignation.\n"
f"* {403/(403+240+9)*100:,.2f}% of employees are not dissastified\n"
f"* and the remaining {9/(403+240+9)*100:,.2f}% of employees didn't reply to this question\n"
"\n"
"--> As the percentage of NULL values are too small, we will replace this values, for the most common value in this column.\n"
    "So we will replace NaN values by FALSE"     )


# In[298]:


#replacing NaN values by FALSE


# In[295]:


combined_updated["dissatisfied"]=combined_updated["dissatisfied"].fillna(False)


# In[296]:


combined_updated["dissatisfied"].value_counts(dropna=False)


# In[ ]:


#creating pivot table comparing dissastified and service_cat


# In[307]:


dissatisfaction_pvt=combined_updated.pivot_table(values="dissatisfied", index="service_cat")


# In[308]:


dissatisfaction_pvt


# In[309]:


# creating plot of the results


# In[384]:


dissatisfaction_pvt.plot(kind="bar", rot=30, legend =False, colormap='Paired')
plt.title("Dissatisfied percentage distrubution attending institute service time")
plt.ylabel("dissatisfation")
plt.show()


# <span style="background: yellow">IMPORTANT</span>
# Based on this results, the most dissatisfied employees that resigned are the ones that worked for the institutes for a long periods

# ## 8 - Conclusions:

# We checked that there are different kind of exits from their job. We focus our analyze in the resignation type, which represent a big part of employees exits from this institutes: <br> <img src="separationtypes.png">

# After check the information regarding dissatisfaction and institute service times, we are in conditions to reply to our initial questions:
# 
# 1.    **Are employees who only worked for the institutes for a short period of time resigning due to some kind of dissatisfaction? What about employees who have been there longer?**
# 2.   **Are the younger employees resigning due to some kind of dissatisfaction? What about older employees?**
# 
# - Based on data: the majority of employees that resigned worked for the institutes for a short period (less than 6 years)
# 
# 
# - The most dissatisfied employees that resigned are the ones that worked for the institutes for a long periods (more than 7 years)
# 
# So we can conclude that employees with 7 or more years of service in institute are more likely to resign due to some kind of dissatisfaction with the job than employees with less than 7 years of service.
# 
# 

# |Employees_category|TT resigned employees|    % dissatisfied employees|
#      |---|---| ---|  
#     |New: Less than 3 years at a company       |  193|29.53%|
#     |Experienced: 3-6 years at a company  |  172|34.30%|
#     |Established: 7-10 years at a company |   62|51.61%|
#     |    Veteran: 11 or more years at a company    |  136|48.53%|
# 

# <table><tr>
#     <td><img src="institute_service_time.png"></td>
#     <td><img src="dissatisfied.png"></td>
#  </tr></table>

# ## 9 - Bibligraphy:

# * Stack overflow: [How to rename categories after using pandas.cut with IntervalIndex?](https://stackoverflow.com/questions/55204418/how-to-rename-categories-after-using-pandas-cut-with-intervalindex)
# * Stack overflow: [How to change plot colors?](https://stackoverflow.com/questions/43938425/matplotlib-change-colormap-tab20-to-have-three-colors)
# * Matplotlib.org: [Pie plot proprieties](https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_demo2.html?highlight=textprops), [pie plot arguments](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.pie.html#matplotlib.pyplot.pie) and [text proprieties](https://matplotlib.org/stable/tutorials/text/text_props.html)
