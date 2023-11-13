#!/usr/bin/env python
# coding: utf-8

# # Explanatory Data Analysis Challenge (Olympic Games)

# ## Data Import and Inspection

# Import the Datasets Summer (__summer.csv__), Winter (__winter.csv__) and dictionary (__dictionary.csv__) and Inspect! 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random


# In[2]:


summer=pd.read_csv("summer.csv")
winter =pd.read_csv("winter.csv")
dic=pd.read_csv("dictionary.csv")


# In[3]:


summer.head()


# In[4]:


winter.head()


# In[5]:


dic


# In[6]:


# What GDP means?
# Gross domestic product
# Gross domestic product (GDP) is the standard measure of the value added created through the production of
# goods and services in a country during a certain period. As such, it also measures the income earned from 
# that production, or the total amount spent on final goods and services (less imports)
# أجمالي الناتج المحلي


# In[7]:


# population عدد السكان في الدولة


# In[ ]:





# ## Merging and Concatenating

# 1. __Merge__ Summer and Winter (one row for each Medal awarded in any Olympic Games) and save the merged DataFrame in __olympics__. 
# 2. An __additional column__ (e.g. "Edition") shall indicate the Edition -> __Summer or Winter__.
# 3. Add the __full Country name__ from dictionary to olympics (e.g. France for FRA).

# In[ ]:





# In[8]:


olympic = pd.concat([summer,winter],keys=["summer","winter"],names=["Edition"])


# In[9]:


olympic.reset_index(inplace=True)


# In[10]:


olympic.head()


# In[11]:


# rename the country column to Code 
# drop column level_1 ,this one come from index
olympic.rename(columns={"Country":"Code"},inplace=True)
olympic.drop(columns=["level_1"],inplace=True)


# In[12]:


# meerge the olympic with dic to get the Country name by Code
olympic = olympic.merge(dic.iloc[:,:2],how="left",on="Code")


# In[13]:


olympic


# In[14]:


# handeling Null Value
olympic.isna().sum()


# In[15]:


missing_value= olympic.isna().any(axis=1)
missing_value


# In[16]:


olympic[missing_value].Code.unique()


# In[17]:


olympic[missing_value]


# In[18]:


codes_to_country = {'URS': 'Soviet Union',
 'GDR': 'East Germany',
 'ROU': 'Romania',
 'FRG': 'West Germany',
 'TCH': 'Czechoslovakia',
 'YUG': 'Yugoslavia',
 'EUN': 'Unified Team',
 'EUA': 'Unified Team of Germany',
 'ZZX': 'Mixed teams',
 'SRB': 'Serbia',
 'ANZ': 'Australasia',
 'RU1': 'Russian Empire',
 'MNE': 'Montenegro',
 'TTO': 'Trinidad and Tobago',
 'BOH': 'Bohemia',
 'BWI': 'West Indies Federation',
 'SGP': 'Singapore',
 'IOP': 'Independent Olympic Participants'}


# In[19]:


# Use the map function to replace 'Country' based on 'Code', keeping the same code if not found
olympic["Country"]=olympic["Code"].map(codes_to_country).fillna(olympic["Country"])


# In[20]:


olympic[missing_value]


# In[21]:


missing_value =olympic[olympic.isna().any(axis=1)]


# In[22]:


missing_value


# In[23]:


olympic.info()


# In[24]:


olympic.isna().any(axis=1).sum()


# In[25]:


# we have 4 row there is no code,country vale , we can drop it
# Drop columns with any null values
olympic.dropna(inplace=True)


# In[ ]:





# In[26]:


olympic.sample(20)


# In[27]:


dic["Code"].unique()


# In[28]:


summer["Country"].sort_values().unique()


# In[29]:


dic


# In[30]:


# merge olympic with dic to add population ,and GDP by country Code
olympic = olympic.merge(dic.iloc[:,1:],how="left",on="Code")


# In[31]:


olympic.sample(20)


# In[32]:


# handeling Null Value
missing_Popu = olympic[olympic.isna().any(axis=1)]


# In[33]:


missing_Popu


# In[34]:


# search for the population and GDP for each country in the same year if you can find it
# i search on web by helping from chatGPT and Bard to find some Data for that country in that Year


# In[35]:


missing_Popu[["Year","Country"]].set_index("Country").to_dict()


# In[36]:


dic


# In[37]:


# i get the population and GDP per capita but i have two resoucse for this data set for GDP
# first source for GDP form the World Bank 
# second source for GDP from IMF data 
# the differences are relatively small
# so i will get some data from my dic dataset to compare it with that to sourse to see which one can i use


# In[38]:


# get 5 sample data 
sample_dic=dic[["Country","GDP per Capita"]].sample(n=10,random_state=91).dropna()
sample_dic.set_index("Country",inplace=True)
sample_dic


# In[39]:


# transfer the data for dictionary
sample_dic= sample_dic.to_dict()


# In[40]:


sample_dic


# In[41]:


# remove the null value


# In[42]:


olympic[olympic.Country == "Malaysia"]


# In[43]:


# after we search for the missing data for populatin and GDP by helping from Bard and chatGPT
# we find that data and save it in missing_popu_gdp.csv


# In[44]:


missing_popu_gdp=pd.read_csv("missing_popu_gdp.csv")
missing_popu_gdp


# In[45]:


missing_popu_gdp.drop(columns=["Population (in millions)","GDP per capita (in USD)","Year"],inplace=True)


# In[46]:


missing_popu_gdp


# In[47]:


# missing population
missing_popu= missing_popu_gdp[["Country","World Bank's World Development"]]
missing_popu.set_index("Country",inplace=True)
country_to_popu_dic = missing_popu.to_dict()["World Bank's World Development"]
country_to_popu_dic


# In[48]:


# now we need to map in olympic to fill the null value
# Use the map function to replace 'Population' based on 'Country', keeping the same code if not found
olympic["Population"]=olympic["Country"].map(country_to_popu_dic).fillna(olympic["Population"])
olympic


# In[49]:


olympic[olympic["Population"].isna()]
# we minmuze the null value from 6974 to 692 rows around X10


# In[50]:


# we will do the same for GDP per capita
# missing GDP
missing_gdp= missing_popu_gdp[["Country","IMF's World Economic Outlook"]]
missing_gdp.set_index("Country",inplace=True)
country_to_gdp_dic = missing_gdp.to_dict()["IMF's World Economic Outlook"]
country_to_gdp_dic


# In[51]:


# now we need to map in olympic to fill the null value
# Use the map function to replace 'Population' based on 'Country', keeping the same code if not found
olympic["GDP per Capita"]=olympic["Country"].map(country_to_gdp_dic).fillna(olympic["GDP per Capita"])
olympic


# In[52]:


olympic[olympic["GDP per Capita"].isna()]
# we minmuze the null value from 6974 to 692 rows around X10


# In[53]:


olympic[olympic["GDP per Capita"].isna()]["Country"].unique()


# ##### The ZZX code in Olympic meaning is the Mixed team or Mixed NOC (National Olympic Committee) Team. It is an Olympic code used to represent mixed teams or teams from multiple NOCs that compete together in a single event. Mixed teams are becoming increasingly common in the Olympics, as they promote inclusion and diversity.
# 
# ##### The ZZX code is used in the Olympic results database to identify mixed teams. It is also used in the Olympic opening ceremony, where mixed teams march under the Olympic flag.
# 
# ##### Here are some examples of mixed team events in the Olympics:
# 
# ##### * Mixed team biathlon relay
# ##### * Mixed team curling
# #### * Mixed team cross-country skiing relay
# #### * Mixed team luge doubles
# #### * Mixed team ski jumping
# #### * Mixed team snowboarding team cross
# 
# #### The ZZX code is a symbol of the Olympic spirit of unity and cooperation. It is a reminder that the Olympics are about more than just winning and losing. They are also about bringing people together from all over the world to compete in a spirit of friendship and sportsmanship.

# In[54]:


# رمز ZZX بالمعنى الأولمبي هو الفريق المختلط أو فريق NOC المختلط (اللجنة الأولمبية الوطنية). إنه رمز أولمبي يستخدم لتمثيل فرق مختلطة أو فرق من عدة لجان أولمبية وطنية تتنافس معًا في حدث واحد. أصبحت الفرق المختلطة شائعة بشكل متزايد في الألعاب الأولمبية، لأنها تعزز الاندماج والتنوع.

# يتم استخدام رمز ZZX في قاعدة بيانات النتائج الأولمبية لتحديد الفرق المختلطة. كما أنها تستخدم في حفل الافتتاح الأولمبي، حيث تسير الفرق المختلطة تحت العلم الأولمبي.

# فيما يلي بعض الأمثلة على أحداث الفرق المختلطة في الألعاب الأولمبية:

# * تتابع البياتلون المختلط
# * الكيرلنج الجماعي المختلط
# * فريق مختلط للتزلج الريفي على الثلج
# * الزحافات الكبيرة للفريق المختلط
# * القفز على الجليد لفريق مختلط
# * فريق مختلط للتزلج على الجليد

# رمز ZZX هو رمز للروح الأولمبية للوحدة والتعاون. إنه تذكير بأن الألعاب الأولمبية لا تقتصر على الفوز والخسارة. إنها تهدف أيضًا إلى جمع الناس معًا من جميع أنحاء العالم للتنافس بروح الصداقة والروح الرياضية.


# In[55]:


# our propus in this data analysis to show which country the best and here we have Mixed-team
# se we can drop to have less null rows in pouplation and GDP per capita
mixed_team = olympic[olympic["Country"]== "Mixed teams"].index


# In[56]:


olympic.drop(index=mixed_team,inplace=True)


# In[57]:


olympic[olympic["GDP per Capita"].isna()]


# In[58]:


# Independent Olympic Participants (IOP) is a term used to describe athletes who compete at the Olympic Games
# but are not part of a National Olympic Committee (NOC). This can happen for a variety of reasons.
# we can drop it


# In[ ]:





# In[59]:


Independent_Olympic_Participants = olympic[olympic["Country"]== "Independent Olympic Participants"]
Independent_Olympic_Participants


# In[60]:


olympic.drop(index=Independent_Olympic_Participants.index,inplace=True)


# In[61]:


olympic[olympic["Country"]== "Independent Olympic Participants"]


# In[62]:


olympic[olympic["GDP per Capita"].isna()]


# In[63]:


grouped_data=olympic.groupby(["Edition","Country","Gender"])[["Medal","Population","GDP per Capita"]]
grouped_data= grouped_data.agg({"Medal":"count","Population":"first","GDP per Capita":"first"})
grouped_data=grouped_data.reset_index().sort_values(ascending=False,by=["Edition","Medal","Population"])
grouped_data


# In[64]:


top5_summer_edition = grouped_data[grouped_data["Edition"]== "summer"].sort_values(ascending=False,by="Medal").head(5)
top5_winter_edition = grouped_data[grouped_data["Edition"]== "winter"].sort_values(ascending=False,by="Medal").head(5)


# In[65]:


top5 = pd.concat([top5_summer_edition,top5_winter_edition])
top5


# In[ ]:





# # what are  the most  10 country successful of  all  time ?

# In[66]:


olympic


# In[67]:


top_10_country = olympic.Country.value_counts().head(10)


# In[68]:


top_10_country


# In[69]:


top_10_country.plot(kind="bar",figsize=(16,6),fontsize=15)
plt.title("Top 10 Successful Country of all time",fontsize=15)
plt.ylabel("Medals",fontsize=14)
plt.show()


# In[70]:


top_10_country.index


# In[71]:


olympics_10=olympic[olympic.Country.isin(top_10_country.index)]
olympics_10


# In[72]:


plt.figure(figsize=(16,6))
sns.set(font_scale=1.2,palette="dark")
sns.countplot(data=olympics_10 , x="Country")
plt.title("Top 10 Successful Country")
plt.show()


# In[73]:


# sort the country from high to low 
# order=["a","b", .....] order=['United States', 'Soviet Union', 'United Kingdom', 'Germany', 'France',
#        'Italy', 'Sweden', 'Canada', 'Australia', 'Hungary']
plt.figure(figsize=(16,6))
sns.set(font_scale=1.2,palette="dark")
sns.countplot(data=olympics_10 , x="Country",order=top_10_country.index)
plt.title("Top 10 Successful Country")
plt.savefig("Top_10_country.png")
plt.show()


# In[74]:


# we want to see the country in the two Edition (summer,winter)
#  by hue="Edition" it will show two bar for each country (summer,winter)
plt.figure(figsize=(16,6))
sns.set(font_scale=1.2,palette="dark")
sns.countplot(data=olympics_10 , x="Country",hue="Edition",order=top_10_country.index)
plt.title("Top 10 Successful Country")
plt.show()


# In[75]:


# we can see there are country it better in summer edition for winter edition (United States , Soviet Union m ...)
# some country the same in summere , winter like Canada
# some country there are not succesful in winter like ( Australia , Hungary)


# In[76]:


# we want to switch the Country and Edition
# to see each edition alone x="Edition"  , hue="Country"
# and to keep the country sorted we will use hue_order=top_10_country.index beacuse the country now hue
plt.figure(figsize=(16,6))
sns.set(font_scale=1.2,palette="dark")
sns.countplot(data=olympics_10 , x="Edition",hue="Country",hue_order=top_10_country.index)
plt.title("Top 10 Successful Country")
plt.show()


# In[77]:


# top 10 successful country with Medal
plt.figure(figsize=(16,6))
sns.set(font_scale=1.2 , palette="dark")
sns.countplot(data=olympics_10 , x="Country",hue="Medal",hue_order=["Gold","Silver","Bronze"],
             palette=["gold","silver","brown"],order=top_10_country.index)
plt.title("Top 10 Country",fontsize=15)
plt.savefig("top10_with_medals")
plt.show()


# In[78]:


# switch country and Medal
plt.figure(figsize=(16,6))
sns.set(font_scale=1.2 , palette="dark")
sns.countplot(data=olympics_10 , x="Medal",hue="Country",order=["Gold","Silver","Bronze"],hue_order=top_10_country.index)
plt.title("Top 10 Country",fontsize=15)
plt.savefig("top10_by_medals")
plt.show()


# # Do GDP and  Population are matter ?

# In[79]:


olympic


# In[80]:


medal_per_country = olympic.groupby(["Country","Medal"]).Medal.count().unstack(fill_value=0)
medal_per_country = medal_per_country.sort_values(by=["Gold","Silver","Bronze"],ascending=False)
medal_per_country=medal_per_country[["Gold","Silver","Bronze"]]
medal_per_country["Total"]= medal_per_country.sum(axis=1)
medal_per_country_50=medal_per_country.head(50)
medal_per_country_50


# In[81]:


medal_per_country


# In[82]:


pouplation_GDP = olympic[["Country","Population","GDP per Capita"]].drop_duplicates()


# In[83]:


pouplation_GDP


# In[84]:


medal_per_country_50 = medal_per_country.merge(pouplation_GDP, how ="left",on="Country").set_index("Country")


# In[85]:


medal_per_country_50


# In[86]:


# we need to see how many unique game there is
olympic.nunique()


# In[87]:


# some city host the games more thant one
# so we will make unique game by merge year and city in new column call Games
olympic["Game"]= olympic.apply(lambda x :str(x.Year) +" "+ x.City,axis=1)


# In[88]:


olympic


# In[89]:


olympic["Game"].nunique()


# In[90]:


# we have 49 unique games
# we will count the number of Medal in each game by counting each game we can know how many medal for each
olympic["Game"].value_counts()


# In[91]:


# count each country how many games they play
# by group the country and then see how many unique olympic Game they paly
olympic.groupby("Country").apply(lambda x :x.Game.nunique())


# In[92]:


# add the total of unique olympic gmae to our DataFrame medal_per_country
medal_per_country_50["Total_Games"]=olympic.groupby("Country").apply(lambda x : x.Game.nunique())


# In[93]:


medal_per_country_50


# In[94]:


medal_per_country_50.rank(ascending=False)


# In[95]:


medal_per_country.head(5)


# In[ ]:





# In[ ]:





# # the corrlation between the columns

# In[96]:


# we need to see the corrolation between the column for all the country 
#  drop the column (Gold , Silver, Bronze) just we need the total to compaire it with other
medal_per_country.drop(columns=["Gold","Silver","Bronze"],inplace=True)


# In[97]:


medal_per_country.head(5)


# In[98]:


medal_per_country.info()


# In[99]:


# merge the medal per country with Population and GDP per capita
medal_per_country = medal_per_country.merge(pouplation_GDP, how ="left",on="Country").set_index("Country")


# In[100]:


# add the total of unique olympic gmae to our DataFrame medal_per_country
medal_per_country["Total_Games"]=olympic.groupby("Country").apply(lambda x : x.Game.nunique())


# In[ ]:





# In[101]:


# the (Population , GDP per Capita ) columns they are object
# must be intger or float
medal_per_country.Population.unique()


# In[102]:


medal_per_country[medal_per_country.Population.isna()]


# In[103]:


medal_per_country["Population"] = medal_per_country["Population"].apply(lambda x : x.replace(",","") if isinstance(x,str) else x).astype(float)


# In[104]:


medal_per_country["GDP per Capita"] = medal_per_country["GDP per Capita"].apply(lambda x : x.replace(",","") if isinstance(x,str) else x ).astype(float)


# In[105]:


medal_per_country


# In[106]:


medal_per_country.corr(method="pearson")


# ### In a correlation value between -1 / 1, -1 indicates a negative correlation, 1 indicates a positive correlation, and 0 indicates no correlation.

# In[107]:


# we will use spearman method in correlation beacuse it culculate the rank first then the correlation
medal_per_country.corr(method="spearman")


# In[108]:


# we can do it in deffrent way
medal_per_country.rank(ascending=False).corr(method="pearson")


# In[109]:


# as we see it will be the same correlation


# ## 1.Hypothesis : There is no relationship between Total Medals and Population ?

# In[110]:


import scipy.stats as stats


# In[111]:


stats.spearmanr(medal_per_country.Total,medal_per_country.Population ,
               nan_policy="omit")


# In[112]:


result , p_value=stats.spearmanr(medal_per_country.Total,medal_per_country.Population ,
               nan_policy="omit")


# In[113]:


result , round(p_value)


# In[114]:


# Print the result
print(f"The Spearman correlation between total medals and Population is {result:.2f}")
print(f"The p-value is {p_value:.2f}")

# Determine the significance level
alpha = 0.05

# Check if the correlation is statistically significant
if p_value < alpha:
    print("The correlation is statistically significant.")
else:
    print("The correlation is not statistically significant.")


# ### Reject Hypothesis: There is a significant (positive) relationship between total medals and Population, so the larger the country the more successful in the Olympic games.

# In[ ]:





# ## 2.Hypothesis : There is no relationship between Total Medals and GDP per capita ?

# In[115]:


GDP = medal_per_country["GDP per Capita"]
total = medal_per_country["Total"]


# In[116]:


result , p_value = stats.spearmanr(total,GDP,nan_policy="omit")


# In[117]:


result , round(p_value)


# In[118]:


# Print the result
print(f"The Spearman correlation between total medals and GDP per capita is {result:.2f}")
print(f"The p-value is {p_value:.2f}")

# Determine the significance level
alpha = 0.05

# Check if the correlation is statistically significant
if p_value < alpha:
    print("The correlation is statistically significant.")
else:
    print("The correlation is not statistically significant.")


# ### Reject Hypothesis: There is a significant (positive) relationship between total medals and GDP per capita

# In[ ]:





# ### 3.Hypothesis : There is no relationship between Total Medals and Total games ?

# In[119]:


total_games = medal_per_country["Total_Games"]
total_medals= medal_per_country["Total"]


# In[120]:


relation , p_value = stats.spearmanr(total_medals,total_games , nan_policy="omit")


# In[121]:


relation , p_value


# In[122]:


# Print the result
print(f"The Spearman correlation between total medals and total games is {relation:.2f}")
print(f"The p-value is {p_value:.2f}")

# Determine the significance level
alpha = 0.05

# Check if the correlation is statistically significant
if p_value < alpha:
    print("The correlation is statistically significant.")
else:
    print("The correlation is not statistically significant.")


# ### Reject Hypothesis: There is a significant (positive) relationship between total medals and total games

# In[ ]:





# In[123]:


olympic.head()


# In[124]:


sum_vs_win = pd.crosstab(olympic.Country,olympic.Edition)
sum_vs_win


# In[125]:


men_vs_women = pd.crosstab(olympic.Country,olympic.Gender)
men_vs_women


# In[126]:


medal_by_cat = pd.concat([sum_vs_win,men_vs_women],axis=1)
medal_by_cat


# In[127]:


medal_by_cat["total"]= medal_by_cat.summer + medal_by_cat.winter


# In[128]:


medal_by_cat


# In[129]:


medal_by_cat.sort_values(by=["total"],ascending=False,inplace=True)


# In[130]:


medal_by_cat


# In[131]:


ranks = medal_by_cat.rank(ascending=False)


# In[132]:


ranks


# In[133]:


top_50 =ranks.head(50)


# In[134]:


plt.figure(figsize=(40,10))
sns.heatmap(top_50.T,cmap="RdYlGn_r",annot=True,fmt="2.0f")
plt.show()


# In[135]:


top_50.sort_values("winter")


# In[136]:


# top country in winter 
plt.figure(figsize=(40,10))
sns.heatmap(top_50.sort_values("winter").T,cmap="RdYlGn_r",annot=True,fmt="2.0f")
plt.show()


# In[137]:


# top country in summer 
plt.figure(figsize=(40,10))
sns.heatmap(top_50.sort_values("summer").T,cmap="RdYlGn_r",annot=True,fmt="2.0f")
plt.show()


# In[138]:


# we want to see what the country success in winter and summer
top_50.summer.sub(top_50.winter).sort_values()


# In[139]:


rank_diff =top_50.summer.sub(top_50.winter).sort_values().to_frame()


# In[140]:


rank_diff


# In[141]:


plt.figure(figsize=(35,5))
sns.heatmap(rank_diff.T,cmap="RdBu",annot=True,fmt="2.0f",center=0)
plt.savefig("heatmap_by_edition")
plt.show()


# In[142]:


# top country by women
top_50.sort_values("Women")


# In[143]:


plt.figure(figsize=(50,10))
sns.heatmap(top_50.sort_values(by="Women").T,annot=True,cmap="RdYlGn_r",fmt="2.0f")
plt.show()


# In[144]:


# top country by men
top_50.sort_values(by="Men")


# In[145]:


plt.figure(figsize=(50,10))
sns.heatmap(top_50.sort_values(by="Men").T,annot=True,fmt="2.0f",cmap="RdYlGn_r")
plt.show()


# In[146]:


# Men Vs Women
top_50.Men.sub(top_50.Women).sort_values()


# In[147]:


rank_diff2 =top_50.Men.sub(top_50.Women).sort_values().to_frame()
rank_diff2


# In[148]:


plt.figure(figsize=(35,5))
sns.heatmap(rank_diff2.T,cmap="RdBu",annot=True,fmt="2.0f",center=0)
plt.savefig("heatmap_by_gender")
plt.show()


# In[ ]:





# ##  Do Traditions Matter ?

# In[149]:


olympic.head()


# In[150]:


olympic.Sport.value_counts()


# In[151]:


sports = olympic.Sport.value_counts().index
sports


# In[152]:


# bring the top20 country
top20=olympic.Country.value_counts().head(20).index
top20


# In[153]:


# we will bring the country crosstab with sport
by_sport= pd.crosstab(olympic.Country , olympic.Sport)
by_sport


# In[154]:


# transfare the frame to rank
by_sport = by_sport.rank(ascending=False,method="average")
by_sport


# In[155]:


# now filter the top20 country by spoerts
by_sport = by_sport.loc[top20,sports]
by_sport


# In[ ]:


plt.figure(figsize=(30,10))
sns.heatmap(data=by_sport,cmap="RdYlGn_r",linewidths=1,vmin=1,vmax=10)
plt.savefig("heatmap_by_sport")
plt.show()


# In[ ]:


# we can see here the United States the top country in first 3 sports (Aquatics , Athletics ,Rowing)
# the United Kingdom is the top3 ( Athletics ,Rowing)
# the Soviet Union is the top1( Gymnastics)
# the Italy is the top1( Fencing)
# the Canada is the top1( Ice Hockey)
# so this indicater for the Tradition is matter

