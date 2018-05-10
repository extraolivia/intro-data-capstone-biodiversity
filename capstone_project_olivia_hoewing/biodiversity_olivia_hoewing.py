
# coding: utf-8

# # Capstone 2: Biodiversity Project

# # Introduction
# You are a biodiversity analyst working for the National Parks Service.  You're going to help them analyze some data about species at various national parks.
# 
# Note: The data that you'll be working with for this project is *inspired* by real data, but is mostly fictional.

# # Step 1
# Import the modules that you'll be using in this assignment:
# - `from matplotlib import pyplot as plt`
# - `import pandas as pd`

# In[84]:


from matplotlib import pyplot as plt
import pandas as pd


# # Step 2
# You have been given two CSV files. `species_info.csv` with data about different species in our National Parks, including:
# - The scientific name of each species
# - The common names of each species
# - The species conservation status
# 
# Load the dataset and inspect it:
# - Load `species_info.csv` into a DataFrame called `species`

# In[85]:


species = pd.read_csv('species_info.csv')


# Inspect each DataFrame using `.head()`.

# In[86]:


species.head()


# # Step 3
# Let's start by learning a bit more about our data.  Answer each of the following questions.

# How many different species are in the `species` DataFrame?

# In[87]:


species_count = species.scientific_name.nunique()
print (species_count)


# What are the different values of `category` in `species`?

# In[88]:


category_names = species.category.unique()
print (category_names)


# What are the different values of `conservation_status`?

# In[89]:


conservation_status_types = species.conservation_status.unique()
conservation_status_types


# ## Step 4
# Let's start doing some analysis!
# 
# The column `conservation_status` has several possible values:
# - `Species of Concern`: declining or appear to be in need of conservation
# - `Threatened`: vulnerable to endangerment in the near future
# - `Endangered`: seriously at risk of extinction
# - `In Recovery`: formerly `Endangered`, but currnetly neither in danger of extinction throughout all or a significant portion of its range
# 
# We'd like to count up how many species meet each of these criteria.  Use `groupby` to count how many `scientific_name` meet each of these criteria.

# In[90]:


# df.groupby('column1').column2.measurement().reset_index()
count_per_coservation_status = species.groupby('conservation_status').scientific_name.nunique().reset_index()
count_per_coservation_status


# As we saw before, there are far more than 200 species in the `species` table.  Clearly, only a small number of them are categorized as needing some sort of protection.  The rest have `conservation_status` equal to `None`.  Because `groupby` does not include `None`, we will need to fill in the null values.  We can do this using `.fillna`.  We pass in however we want to fill in our `None` values as an argument.
# 
# Paste the following code and run it to see replace `None` with `No Intervention`:
# ```python
# species.fillna('No Intervention', inplace=True)
# ```

# In[91]:


species.fillna('No Intervention', inplace=True)


# Great! Now run the same `groupby` as before to see how many species require `No Protection`.

# In[92]:


count_per_coservation_status = species.groupby('conservation_status').scientific_name.nunique().reset_index()
count_per_coservation_status


# This is an overview of the numer of species per category. Vascular Plants take up 76%, followed by birds with 8%.

# Let's use `plt.bar` to create a bar chart.  First, let's sort the columns by how many species are in each categories.  We can do this using `.sort_values`.  We use the the keyword `by` to indicate which column we want to sort by.
# 
# Paste the following code and run it to create a new DataFrame called `protection_counts`, which is sorted by `scientific_name`:
# ```python
# protection_counts = species.groupby('conservation_status')\
#     .scientific_name.count().reset_index()\
#     .sort_values(by='scientific_name')
# ```

# In[93]:


protection_counts = species.groupby('conservation_status')    .scientific_name.nunique().reset_index()    .sort_values(by='scientific_name')


# Now let's create a bar chart!
# 1. Start by creating a wide figure with `figsize=(10, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `scientific_name` column of `protection_counts`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `conservation_status` in `protection_counts`
# 5. Label the y-axis `Number of Species`
# 6. Title the graph `Conservation Status by Species`
# 7. Plot the grap using `plt.show()`

# In[94]:


plt.figure(figsize=(10, 4))
ax = plt.subplot()
plt.bar(range(len(protection_counts.conservation_status)),protection_counts.scientific_name)
ax.set_xticks(range(len(protection_counts.conservation_status)))
ax.set_xticklabels(protection_counts.conservation_status)
plt.ylabel('Number of Species')
plt.title('Conservation Status by Species')
plt.show()


# In[95]:


# going off script, I wanted to look into category data
count_per_category = species.groupby('category').scientific_name.count().reset_index().sort_values(by='scientific_name')

count_per_category['Percentage_Amount'] = count_per_category.scientific_name / float(5824)
count_per_category


# In[96]:


# category data plot
plt.figure(figsize=(10,4))
ax = plt.subplot()
plt.bar(range(len(count_per_category.category)), count_per_category.scientific_name)
ax.set_xticks(range(len(count_per_category.category)))
ax.set_xticklabels(count_per_category.category)
plt.ylabel('Number of species per category')
plt.title('Types of Species')
plt.show()


# # Step 4
# Are certain types of species more likely to be endangered?

# Let's create a new column in `species` called `is_protected`, which is `True` if `conservation_status` is not equal to `No Intervention`, and `False` otherwise.

# In[97]:


species['is_protected'] = species.conservation_status != 'No Intervention'


# Let's group by *both* `category` and `is_protected`.  Save your results to `category_counts`.

# In[98]:


category_counts = species.groupby(['category','is_protected']).scientific_name.nunique().reset_index()


# Examine `category_count` using `head()`.

# In[99]:


category_counts.head()


# It's going to be easier to view this data if we pivot it.  Using `pivot`, rearange `category_counts` so that:
# - `columns` is `conservation_status`
# - `index` is `category`
# - `values` is `scientific_name`
# 
# Save your pivoted data to `category_pivot`. Remember to `reset_index()` at the end.

# In[100]:


category_pivot = category_counts.pivot(columns='is_protected',
                              index='category',
                              values='scientific_name').reset_index()


# Examine `category_pivot`.

# In[101]:


category_pivot


# Use the `.columns` property to  rename the categories `True` and `False` to something more description:
# - Leave `category` as `category`
# - Rename `False` to `not_protected`
# - Rename `True` to `protected`

# In[102]:


category_pivot.columns = ['Category','not_protected', 'protected']

category_pivot


# Let's create a new column of `category_pivot` called `percent_protected`, which is equal to `protected` (the number of species that are protected) divided by `protected` plus `not_protected` (the total number of species).

# In[103]:


category_pivot['percent_protected'] = category_pivot.protected / (category_pivot.protected + category_pivot.not_protected) * 100




# Examine `category_pivot`.

# In[104]:


category_pivot


# In[105]:


category_pivot.sort_values(by=['percent_protected'], inplace=True, ascending = False)
category_pivot


# In[106]:


# visualizing the % of protected species 
plt.pie(category_pivot.percent_protected, labels = category_pivot.Category, autopct = '%d%%')
plt.title('Protected Species by Type')
plt.axis('equal')
plt.show()


# It looks like species in category `Mammal` are more likely to be endangered than species in `Bird`.  We're going to do a significance test to see if this statement is true.  Before you do the significance test, consider the following questions:
# - Is the data numerical or categorical?
# - How many pieces of data are you comparing?

# Based on those answers, you should choose to do a *chi squared test*.  In order to run a chi squared test, we'll need to create a contingency table.  Our contingency table should look like this:
# 
# ||protected|not protected|
# |-|-|-|
# |Mammal|?|?|
# |Bird|?|?|
# 
# Create a table called `contingency` and fill it in with the correct numbers

# In[107]:


contingency = [[30, 146],
              [75, 413]]


# In order to perform our chi square test, we'll need to import the correct function from scipy.  Past the following code and run it:
# ```py
# from scipy.stats import chi2_contingency
# ```

# In[108]:


from scipy.stats import chi2_contingency


# Now run `chi2_contingency` with `contingency`.

# In[109]:


chi2, pval, dof, expected = chi2_contingency(contingency)
print (pval)


# It looks like this difference isn't significant!
# 
# Let's test another.  Is the difference between `Reptile` and `Mammal` significant?

# In[110]:


contingency_2 = [[5, 73],
                [30,146]]

chi2, pval, dof, expected = chi2_contingency(contingency_2)
print (pval)


# Yes! It looks like there is a significant difference between `Reptile` and `Mammal`!

# In[111]:


# contingency tables

contingency_1 = [[7,72],
                [75,413]]
contingency_2 = [[7,72],
                [11,115]]
contingency_3 = [[7,72],
                [30,146]]
# amph - non-vasc
contingency_4 = [[7,72],
                [5,328]]
contingency_5 = [[7,72],
                [5,73]]
# amph - vascular plant
contingency_6 = [[7,72],
                [46,4216]]
contingency_7 = [[75,413],
                [11,115]]
contingency_8 = [[75, 413],
                [30,146]]
# bird - non-vasc
contingency_9 = [[75,413],
                [5,328]]
contingency_10 = [[75,413],
                [5,73]]
# bird - vascular plant
contingency_11 = [[75,413],
                [46,4216]]

contingency_12 = [[11,115],
                [30,146]]
# Fish - non-vasc
contingency_13 = [[11,115],
                [5,328]]
contingency_14 = [[11,115],
                [5,73]]
# Fish - vascular plant 
contingency_15 = [[11,115],
                [46,4216]]
# mammal - non-vasc
contingency_16 = [[30,146],
                [5,328]]
# mammal - reptile
contingency_17 = [[30,146],
                [5,73]]
# mammal - vascular plant
contingency_18 = [[30,146],
                [46,4216]]
# non-vasc - reptile
contingency_19 = [[5, 328],
                [5, 73]]
contingency_20 = [[5, 328],
                [46,4216]]
# reptile - vascular plant 
contingency_21 = [[5, 73],
                [46,4216]]


# In[112]:


# print p values 

chi2, pval, dof, expected = chi2_contingency(contingency_1)
print (1, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_2)
print (2, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_3)
print (3, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_4)
print (4, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_5)
print (5, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_6)
print (6, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_7)
print (7, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_8)
print (8, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_9)
print (9, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_10)
print (10, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_11)
print (11, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_12)
print (12, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_13)
print (13, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_14)
print (14, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_15)
print (15, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_16)
print (16, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_17)
print (17, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_18)
print (18, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_19)
print (19, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_20)
print (20, pval)
chi2, pval, dof, expected = chi2_contingency(contingency_21)
print (21, pval)

Based on the p-values, the following combinations are significant from each other: 

Amphibian - Non-vascular Plant \
Amphibian - Vascular Plant \
Bird - Non-vascular Plant \
Bird - Non-vascular Plant \
Fish - Non-vascular Plant \
Fish - Vascular Plant \
Mammal - Non-vascular Plant \
Mammal - Reptile \
Mammal - Vascular Plant \
non-vasc - Reptile \
Reptile - Non-vascular Plant \
# # Step 5

# Conservationists have been recording sightings of different species at several national parks for the past 7 days.  They've saved sent you their observations in a file called `observations.csv`.  Load `observations.csv` into a variable called `observations`, then use `head` to view the data.

# In[113]:


import pandas as pd
observations = pd.read_csv('observations.csv')
observations.head()


# Some scientists are studying the number of sheep sightings at different national parks.  There are several different scientific names for different types of sheep.  We'd like to know which rows of `species` are referring to sheep.  Notice that the following code will tell us whether or not a word occurs in a string:

# In[114]:


# Does "Sheep" occur in this string?
str1 = 'This string contains Sheep'
'Sheep' in str1


# In[115]:


# Does "Sheep" occur in this string?
str2 = 'This string contains Cows'
'Sheep' in str2


# Use `apply` and a `lambda` function to create a new column in `species` called `is_sheep` which is `True` if the `common_names` contains `'Sheep'`, and `False` otherwise.

# In[116]:


species['is_sheep'] = species.common_names.apply(lambda x: 'Sheep' in x)
species.head()


# Select the rows of `species` where `is_sheep` is `True` and examine the results.

# In[117]:


is_sheep_total = species[(species.is_sheep == True)]
is_sheep_total.head(10)


# Many of the results are actually plants.  Select the rows of `species` where `is_sheep` is `True` and `category` is `Mammal`.  Save the results to the variable `sheep_species`.

# In[118]:


sheep_species = species[(species.is_sheep == True) & (species.category == 'Mammal')]
sheep_species


# Now merge `sheep_species` with `observations` to get a DataFrame with observations of sheep.  Save this DataFrame as `sheep_observations`.

# In[119]:


sheep_observations = sheep_species.merge(observations)
sheep_observations


# How many total sheep observations (across all three species) were made at each national park?  Use `groupby` to get the `sum` of `observations` for each `park_name`.  Save your answer to `obs_by_park`.
# 
# This is the total number of sheep observed in each park over the past 7 days.

# In[120]:


obs_by_park = sheep_observations.groupby('park_name').observations.sum().reset_index()
obs_by_park


# Create a bar chart showing the different number of observations per week at each park.
# 
# 1. Start by creating a wide figure with `figsize=(16, 4)`
# 1. Start by creating an axes object called `ax` using `plt.subplot`.
# 2. Create a bar chart whose heights are equal to `observations` column of `obs_by_park`.
# 3. Create an x-tick for each of the bars.
# 4. Label each x-tick with the label from `park_name` in `obs_by_park`
# 5. Label the y-axis `Number of Observations`
# 6. Title the graph `Observations of Sheep per Week`
# 7. Plot the grap using `plt.show()`

# In[121]:


plt.figure(figsize=(16,4))
ax = plt.subplot()
plt.bar(range(len(obs_by_park.park_name)), obs_by_park.observations)
ax.set_xticks(range(len(obs_by_park.park_name)))
ax.set_xticklabels(obs_by_park.park_name)
plt.ylabel('Number of Pbservations')
plt.title('Observations of Sheep per Week')
plt.show()


# Our scientists know that 15% of sheep at Bryce National Park have foot and mouth disease.  Park rangers at Yellowstone National Park have been running a program to reduce the rate of foot and mouth disease at that park.  The scientists want to test whether or not this program is working.  They want to be able to detect reductions of at least 5 percentage point.  For instance, if 10% of sheep in Yellowstone have foot and mouth disease, they'd like to be able to know this, with confidence.
# 
# Use the sample size calculator at <a href="https://www.optimizely.com/sample-size-calculator/">Optimizely</a> to calculate the number of sheep that they would need to observe from each park.  Use the default level of significance (90%).
# 
# Remember that "Minimum Detectable Effect" is a percent of the baseline.

# In[122]:


baseline = 15
confidence_level = 90
mde  = 5/15 * 100
mde


# In[123]:


# insert values into sample size calculator 
sample_size_per_variation = 510


# How many weeks would you need to observe sheep at Bryce National Park in order to observe enough sheep?  How many weeks would you need to observe at Yellowstone National Park to observe enough sheep?

# In[124]:


# use values from obs_by_park 
weeks_per_variation_bryce = 510 / float(250)
weeks_per_variation_bryce


# In[125]:


# use values from obs_by_park
weeks_per_variation_yellowstone = 510 / float(507)
weeks_per_variation_yellowstone


# In[126]:


# A bit more than 2 weeks at Bryce and about 1 week at Yellowstone. 

