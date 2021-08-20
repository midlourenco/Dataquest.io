#!/usr/bin/env python
# coding: utf-8

# # <p style="text-align: center;"> Storytelling data visualization of  euro exchange rate</p>

# 
# 
# 

# ## 1. Introduction:

# In this project we will use a dataset regarding **euro currency** and our objective will be to find the best way to represent the data information in order to be easy to understand the evolution of the exchange rate euro/US dolar just checking data visualization. 
# 
# So, before start this project, it is important we clarify some concepts:
# 
# 
# - The euro (symbolized with €) is the official currency in most of the countries of the European Union.
# 
# - As all other currency in the world, euro also has **exchange rate** regarding other currency, i.e., the rate at which one currency will be exchanged for another currency.
# 
# - For example, if the exchange rate of the euro to the US dollar is 1.5, it means that we will get 1.5 US dollars per each 1.0 euro that we pay (one euro has more value than one US dollar at this exchange rate).
# 
# 

# The dataset describes the euro daily exchange rates between 1999 and 2021, and its source is the European Central Bank. The data is frequently updated and we can be download [here](https://www.kaggle.com/lsind18/euro-exchange-daily-rates-19992020). We will use one version download on January 2021.  
# 
# Even we have information about much more exchange rates, our focus in the this project will be on the exchange rate between the euro and the American dollar (US dollar / USD).
# 

# 
# 

# ## 2. First overview of dataset: 

# Let us start to import the dataset and check the first and the last 5 five rows of dataset.

# In[1]:


#First: import the libraries we will need for this project:
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.style as style
# To enable Jupyter to display graphs
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


#Second: import the csv file into a pandas DataFrame:
exchange_rates = pd.read_csv("euro-daily-hist_1999_2020.csv")


# In[3]:


#Third: visualize some rows:
exchange_rates #as alternative we could print rows using df.head() and df.tail()


# In[4]:


#Fourth: check some data details (type, null values, ...):
exchange_rates.info()


# 
# 

# Checking this information we can takes following notes:
# - Dataset has 5699 rows × 41 columns
# 
# 
# - There are some currency with many null values. For example "[Greek drachma  ]", "[Maltese lira  ]", "[Cypriot pound  ]", "[Slovenian tolar  ]" and "[Slovak koruna   ]", which more than half of values are null -> this information should be important if we will work with this exchange rates.
# 
# 
# - Although all columns are regarding numerical values, almost all columns are object type, except 3: "[Iceland krona  ]", "[Romanian leu  ]" and "[Turkish lira  ]". -> this should mean that we will need to convert the reaming data to numerical format too (float64), except the first column "Period\Unit:" which should be convert to datetime type.
# 
# 
# - The columns names are not easy to work because square brackets, capital letters and spaces. -> To be easier we should simplified the column names at the least of the columns with what we will work.
# 

# ## 3. Data Cleaning:

# ### 3.1 Rename columns:

# As mentioned before, we will focus on US dolar, so we will rename only `[US dollar ]` and `Period\Unit:` columns:

# In[5]:


exchange_rates.rename({"[US dollar ]":"US_dollar", r"Period\Unit:":"Time"}, axis=1, inplace=True) 
#In order to avoid `unicode error` in the 2nd column name, we need to use "r" before the string name
#as we have "\U..." it is interpreted as eight-character Unicode escape, if we don't put "r" or use double "\\" 


# In[6]:


exchange_rates.columns # to visualize the changes


# ### 3.2 Convert `Time` column in datetime type:

# In[7]:


#format of information in this column is: 2021-01-08 
exchange_rates["Time"]=pd.to_datetime(exchange_rates["Time"], format="%Y-%m-%d")


# In[8]:


exchange_rates["Time"].dtype #checking the changes


# ### 3.3 Sort values by `Time` in ascending order:

# As our goal is to create plots which show the exchange rate evolution by time, it is important to do this step.

# In[9]:


exchange_rates.sort_values("Time", ascending=True,inplace=True) # sort values by time
exchange_rates.reset_index(drop=True, inplace=True) # reset the index (and drop the initial index)


# In[10]:


exchange_rates # visualize the changes


# ### 3.4 Isolate `Time` and `US_dollar` in new dataframe:

# In[11]:


euro_to_dollar=exchange_rates.copy()[["Time", "US_dollar"]]


# In[12]:


euro_to_dollar # checking the new Dataframe


# In[13]:


euro_to_dollar.info()


# Checking this information we can identify:
# - there is not null values in the US_dollar column
# - US_dollar is still with object type - we will need to convert this to a numerical type
# - Before converting it in numerical type, let us inspect the unique values in the "US_dollar" column in order to check if we detect something strange or if we can proceed

# In[14]:


euro_to_dollar["US_dollar"].value_counts()


# Based on this information we see we have 62 times "-" in this column.
# So, if we don't have information, it is not relevant information, for our project. So, we need to remove this rows.

# ### 3.5 Drop rows without rate value in US_dollar column:

# In[15]:


euro_to_dollar=euro_to_dollar[euro_to_dollar["US_dollar"]!="-"]


# In[16]:


euro_to_dollar #checking our new dataset:


# ### 3.6 Convert the`US_dollar` column to float type:

# In[17]:


euro_to_dollar.loc[:,"US_dollar"]=euro_to_dollar.loc[:,"US_dollar"].astype(float)
euro_to_dollar.info()


# 
# 

# ## 4. Data Visualization:

# We will start to create a line plot to visualize the evolution of the euro-dollar exchage rate:

# In[18]:


plt.plot(euro_to_dollar["Time"],euro_to_dollar["US_dollar"])
plt.show()


# The line's shape is not smooth, because as usually the exchange rates go up and down, down and up again, day to day. 
# In order to make easier our objective to check the evolution between 1999 and 2021, instead to focus on daily variation, we want to focus only on long-term trends. So, using **rolling mean (moving average)**, and taking 30 days (one month) as rolling window, we expect to get smooth new line plot.

# In[19]:


euro_to_dollar['rolling_mean'] = euro_to_dollar['US_dollar'].rolling(30).mean()


# In[20]:


plt.plot(euro_to_dollar['Time'], euro_to_dollar['rolling_mean'])
plt.show()


# ## 5. Historical facts and its impact on exchange rate evolution:

# Based on some literature as [corporate finance institute](https://corporatefinanceinstitute.com/resources/knowledge/trading-investing/euro-to-dollar-exchange-rate/), we can find some factors that have impact on exchange rate, from what we will highlight the following:
# * Countries that are included in the Eurozone (and changes to that list)
# * Employment rates, job creation, etc. such in Eurozone as well as in US side
# * Domestic politics and international policies, including the trade agreements, tariffs, and duties set internationally from US side.
# * Economic growth in Eurozone countries
# 
# 
# Relating this factores with some historical facts found in the [Europe Union website](https://europa.eu/euroat20/journey-of-the-euro/) and in news like [here](https://www.poundsterlinglive.com/eurusd/11303-eurusd-u-s-china-trade-fight-will-hurt-but-buy-the-dip-says-bank-of-america), we will try to check its impact in exchange rate (if any) using information in our dataset
# 
# * 1999: The Euro currency is born
# * 2008: The global financial crisis 
# * 2013-2015, the Euro fell heavily as debt problems emerged with the ‘PIIGS’ (Portugal, Italy, Irland, Greece and Spain).
# * 2018: China–United States trade war  - US began setting tariffs and other trade barriers on China 
# * 2020: COVID-19 pandemic
# * USA President terms

# Bellow we can see one **exploratory graph** highlighting the fluctuations during these periods:

# In[21]:


style.use("fivethirtyeight")


# In[22]:


decrease_period=euro_to_dollar.copy()[(euro_to_dollar['Time'].dt.year >= 2007) & (euro_to_dollar['Time'].dt.year <= 2019)]


# In[23]:


fig, ax = plt.subplots(figsize=(10,3))
ax.plot(decrease_period['Time'], decrease_period['rolling_mean'],
            color='#af0b1e',linewidth=2)
ax.axvspan(xmin=13950, xmax=14140, ymin=0.09,color="grey", alpha=0.3)
ax.axvspan(xmin=15950, xmax=16850, ymin=0.09, color='grey',alpha=0.3)
ax.axvspan(xmin=17550, xmax=18250, ymin=0.09, color='grey',alpha=0.3)
plt.show()


# ### 5.1 The impact of the Global Financial crisis in exchange rate EUR/ US dollar

# Let us focus what happen between 2006-2010.
# In Appendix we left some calculations we made to get some values to create this plot.

# In[24]:


financial_crisis=euro_to_dollar.copy()[(euro_to_dollar['Time'].dt.year >= 2006) & (euro_to_dollar['Time'].dt.year <= 2010)]


# In[25]:



#Create the plot area and structure
fig, (ax1, ax2) = plt.subplots(figsize=(8,3), nrows=2, ncols=1)
axes=[ax1, ax2]


#First version of plots - like a shadow of every elements
for ax in axes:
    ax.plot(financial_crisis['Time'], financial_crisis['rolling_mean'],
            color='#af0b1e', alpha=0.1)
    ax.set_ylim(1.12, 1.6) #use same y axis for both graph
    #ax.set_yticks([1.0, 1.2,1.4, 1.6])
    ax.set_yticklabels([])
    #ax.set_facecolor="#dbd7d7"
    ax.tick_params(colors='#948484', which='both', labelsize=10)
    ax.grid(b=True, color="grey", alpha=0.1,linestyle=":")
    

    
### Highlihting the rate growing before crises
ax1.plot(financial_crisis['Time'][:660], financial_crisis['rolling_mean'][:660], color='green', linewidth=2.55, alpha=0.8)
#ax1.xaxis.tick_top()
ax1.set_xticklabels([])
ax1.text(x=13000,y=1.12,s="r*=1.1826",size=10) #check appendix
ax1.text(x=14000,y=1.6,s="r*=1.599",size=10) #check appendix
ax1.text(x=14250,y=1.65,s="Positive rate evolution",size=11,color="green", weight="bold")
ax1.text(x=14250,y=1.55,s="until middle 2008",size=11, color="green", weight="bold")


### Highlihting the floated rate after crisis
ax2.plot((financial_crisis['Time'][660:1300]), (financial_crisis['rolling_mean'][660:1300]),color='#af0b1e', linewidth=2.5, alpha=0.8)
ax2.text(x=13030,y=1.45,s="The rate drops and",size=11, color="#af0b1e", weight="bold")
ax2.text(x=13030,y=1.35,s="grows after 2008",size=11, color="#af0b1e", weight="bold")

### Highlihting the peak of the crisis
ax1.axvspan(xmin=13950, xmax=14140, ymin=0.09,
           alpha=0.3, color='grey')
ax2.axvspan(xmin=13950, xmax=14140, ymin=0.09,
           alpha=0.3, color='grey')
ax2.text(x=14900,y=1.26,s="r*=1.1.2939",size=10) #check appendix

### Highlihting the moment of the dratic rate drop
#ax1.axvline(x=14090, ymin=-5, ymax=1.3, c="red",linestyle=":", linewidth=2)
#ax2.axvline(x=14090, ymin=-3, ymax=2, c="red", linewidth=2,linestyle=":")


#Title and subtitle:
ax1.text(x=13000,y=2.05,s="EUR/USD rate drastic drop after the financial crisis",size=18, weight="bold")
ax1.text(x=13200,y=1.90,s="The global financial crisis has a big impact on the exchange rate. ",size=13)
ax1.text(x=13000,y=1.80,s="The rate started to float after 2008 and never reach again its highest value 1.599",size=13)

#r description
ax.text(x=13000,y=0.9, s="*r means exchange rate EUR/USD", size=11)

#Foot signature/source of graph:
ax2.text(13000,0.8,'©Mariana Lourenço' +' '*59 +"Source: European Central Bank", color="#f0f0f0",backgroundcolor="#4d4d4d", size=12)


plt.show()


# ### 5.2 The impact of the COVID-19 Pandemic in EUR/USD rate

# In[26]:


#2016-2019:
before_pandemic = euro_to_dollar.copy()[(euro_to_dollar['Time'].dt.year >= 2016) & (euro_to_dollar['Time'].dt.year <= 2019)]

#2020:
after_pandemic =euro_to_dollar.copy()[(euro_to_dollar['Time'].dt.year >= 2020) & (euro_to_dollar['Time'].dt.year <= 2021)]


# In[27]:


#import matplotlib.dates as mdates

fig, ax= plt.subplots(figsize=(9,1.5))

ax.plot(before_pandemic['Time'], before_pandemic['rolling_mean'],color='lightblue')
ax.plot(after_pandemic['Time'], after_pandemic['rolling_mean'],color='green' )
#ax.set_ylim(1.1, 1.3) #use same y axis for both graph
#ax.set_yticks([1.1, 1.2,1.3])
#ax.set_yticklabels([1.1, 1.2,1.3])
ax.tick_params(colors='#948484', which='both', labelsize=12)
ax.yaxis.grid(False)
ax.set_yticklabels([])
ax.axhline(1.22,c="black", linewidth=2.5, alpha=0.8)
ax.text(x=16530,y=1.21, s="r*=1.225", size=11)
ax.annotate('Mar-2020', xy=(18400, 1.08), xytext=(18500, 0.95),
            arrowprops=dict(facecolor='black', shrink=0.05),
            )

#Title
ax.text(x=16600,y=1.45,s="COVID-19 Pandemic rises hopes that the euro will valorize ",size=18, weight="bold")
ax.text(x=16750,y=1.40, s="Checking evolution of EUR/USD rate, since first cases in Europe (Mar/2020)",size=14)
ax.text(x=16800,y=1.35, s=" the rate grew, and in Jan-2021 reached the highest values since 2018",size=14)


#r description
ax.text(x=16530,y=0.92, s="*r means exchange rate EUR/USD", size=11)

#Foot signature/source of graph:
ax.text(16530,0.88,'©Mariana Lourenço' +' '*78 +"Source: European Central Bank", backgroundcolor="#4d4d4d", size=12,color="#f0f0f0")
plt.show()


# ## 6. Conclusion:

# In this project, we explore the dataset with exchange rate EUR/USD information between 1999 and 2021 and we related its evolution with some historical facts.

# After explored and cleaned the data, we selected 2 of those historical facts, and we created one graphic set per event, in order to explain to audience the impact of each event in exchange rate. 

# The first selected event was the global financial crisis in 2008. Based in the graph created, we could easily to understand that until 2008, exchange rate was growing, and drastic drop after started the global financial crisis. After 2008 we see that exchange rate floated and never reach again the highest value 1.599.

# Then, we selected the Covid-19 pandemic event. Based in the graph, we can understand that after the first cases appeared in western world the exchange rate EUR/USD reversed the negative trend and equaled values from two years ago.

# We focus our work in exchange rate EUR/USD. However, as we saw at the beggining, our dataset has much more information and we can do similar work with other currency.

# ## 7. Apendix

# Auxiliary calculations for graph 5.1

# In[ ]:


before=euro_to_dollar.copy()[(euro_to_dollar['Time'].dt.year >= 2006) & (euro_to_dollar['Time'].dt.year <= 2008)]
print(before.shape)


# In[ ]:


before.max()


# In[ ]:


before[before["rolling_mean"]== 1.5743]


# In[ ]:


before.min()


# In[ ]:


before[before["Time"]== "2006-01-02"]


# In[ ]:


euro_to_dollar[euro_to_dollar["Time"]=="2011-12-30"]


# Auxiliary calculations for graph 5.2

# In[ ]:


pandemic=euro_to_dollar.copy()[(euro_to_dollar['Time'].dt.year >= 2020) & (euro_to_dollar['Time'].dt.year <= 2021)]
print(before.shape)


# In[ ]:


pandemic.min()


# In[ ]:


pandemic[pandemic["rolling_mean"]<  1.085]


# In[ ]:


pandemic[pandemic["US_dollar"]==  1.0707]


# In[ ]:


pandemic[pandemic["Time"]==  "2021-01-08"]

