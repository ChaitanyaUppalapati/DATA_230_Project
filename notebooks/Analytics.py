# Load necessary datasets for visualization
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

salaries_df = pd.read_csv("/Users/hiruzen/Programming/Language/Python/PrequsitePrep/src/notebooks/data-230/Project/cleaned/cleaned_salaries.csv")
skills_df = pd.read_csv("/Users/hiruzen/Programming/Language/Python/PrequsitePrep/src/notebooks/data-230/Project/cleaned/cleaned_skills.csv")
job_skills_df = pd.read_csv("/Users/hiruzen/Programming/Language/Python/PrequsitePrep/src/notebooks/data-230/Project/cleaned/cleaned_job_skills.csv")
companies_df = pd.read_csv("/Users/hiruzen/Programming/Language/Python/PrequsitePrep/src/notebooks/data-230/Project/cleaned/cleaned_companies.csv")
job_postings_df = pd.read_csv("/Users/hiruzen/Programming/Language/Python/PrequsitePrep/src/notebooks/data-230/Project/cleaned/cleaned_job_postings.csv")
job_industries_df = pd.read_csv("/Users/hiruzen/Programming/Language/Python/PrequsitePrep/src/notebooks/data-230/Project/cleaned/cleaned_job_industries.csv")
industries_df = pd.read_csv("/Users/hiruzen/Programming/Language/Python/PrequsitePrep/src/notebooks/data-230/Project/cleaned/cleaned_industries.csv")
employee_df = pd.read_csv("/Users/hiruzen/Programming/Language/Python/PrequsitePrep/src/notebooks/data-230/Project/cleaned/cleaned_employee_counts.csv")

merged_df = pd.merge(salaries_df, job_skills_df, on="job_id", how="inner")
merged_df = pd.merge(merged_df, skills_df, on="skill_abr", how="left")
merged_df['avg_salary'] = (merged_df['min_salary'] + merged_df['max_salary']) / 2

top_skills_salary = (
    merged_df.groupby('skill_name')['avg_salary']
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=top_skills_salary, x='avg_salary', y='skill_name', palette='magma')
plt.title("Top 15 Highest Paying Skills")
plt.xlabel("Average Salary (Hourly Equivalent)")
plt.ylabel("Skill")
plt.tight_layout()
plt.show()


# Plot most in-demand skills based on frequency (top 15 by count)
top_skill_counts = (
    merged_df['skill_name']
    .value_counts()
    .head(15)
    .reset_index()
)
top_skill_counts.columns = ['skill_name', 'count']

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=top_skill_counts, x='count', y='skill_name', palette='Blues_d')
plt.title("Top 15 Most In-Demand Skills (by Job Count)")
plt.xlabel("Number of Job Postings")
plt.ylabel("Skill")
plt.tight_layout()
plt.show()



# Merge salaries with job postings to get job_id -> company_id
merged = pd.merge(salaries_df, job_postings_df[['job_id']], on='job_id', how='inner')

# Merge with job_industries to map job_id to industry_id
merged = pd.merge(merged, job_industries_df, on='job_id', how='left')

# Merge with industries to get industry names
merged = pd.merge(merged, industries_df, on='industry_id', how='left')

# Calculate average salary per industry
merged['avg_salary'] = (merged['min_salary'] + merged['max_salary']) / 2
industry_salary = (
    merged.groupby('industry_name')['avg_salary']
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)
# print(merged.head())
# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=industry_salary, x='avg_salary', y='industry_name', palette='plasma')
plt.title("Top 15 Highest Paying Industries")
plt.xlabel("Average Salary")
plt.ylabel("Industry")
plt.tight_layout()
plt.show()


# Plot: Count of Job Postings per Industry (Demand View)

# Count job postings per industry
industry_demand = (
    merged['industry_name']
    .value_counts()
    .head(15)
    .reset_index()
)
industry_demand.columns = ['industry_name', 'count']

# Plot
plt.figure(figsize=(10, 6))
sns.barplot(data=industry_demand, x='count', y='industry_name', palette='crest')
plt.title("Top 15 Most In-Demand Industries (by Job Count)")
plt.xlabel("Number of Job Postings")
plt.ylabel("Industry")
plt.tight_layout()
plt.show()

import plotly.express as px

# Top-paying skills
top_skills = (
    merged_df.groupby('skill_name')['avg_salary']
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    top_skills,
    x='avg_salary',
    y='skill_name',
    orientation='h',
    title="Top 15 Highest Paying Skills",
    labels={'avg_salary': 'Average Salary'},
)
fig.update_layout(yaxis={'categoryorder': 'total ascending'})
fig.show()

# Compute demand and average salary per industry
industry_stats = (
    merged.groupby('industry_name')
    .agg(job_count=('job_id', 'count'), avg_salary=('avg_salary', 'mean'))
    .reset_index()
    .sort_values(by='job_count', ascending=False)
    .head(20)
)

fig = px.scatter(
    industry_stats,
    x='job_count',
    y='avg_salary',
    size='job_count',
    color='industry_name',
    hover_name='industry_name',
    title="Industry: Job Count vs Average Salary",
    labels={'job_count': 'Number of Jobs', 'avg_salary': 'Avg Salary'}
)
fig.show()




# Convert numeric fields and handle missing values
employee_df['employee_count'] = pd.to_numeric(employee_df['employee_count'], errors='coerce')
employee_df['follower_count'] = pd.to_numeric(employee_df['follower_count'], errors='coerce')

# Drop rows with missing numeric values
employee_df_clean = employee_df.dropna(subset=['employee_count', 'follower_count'])

# Compute correlation matrix
corr_matrix = employee_df_clean[['employee_count', 'follower_count']].corr()

# Plot heatmap
plt.figure(figsize=(6, 4))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation Heatmap: Employee vs Follower Count")
plt.tight_layout()
plt.show()


# Load cleaned_companies dataset to explore more variables


# Select numeric-like columns and convert where necessary
numeric_cols = ['company_size', 'zip_code']
for col in numeric_cols:
    companies_df[col] = pd.to_numeric(companies_df[col], errors='coerce')

# Merge with employee_df to expand correlation heatmap
merged_companies = pd.merge(companies_df, employee_df, on='company_id', how='inner')

# Select relevant numeric columns
numeric_subset = merged_companies[['employee_count', 'follower_count', 'company_size']].dropna()

# Correlation matrix
corr = numeric_subset.corr()

# Plot heatmap
plt.figure(figsize=(7, 5))
sns.heatmap(corr, annot=True, cmap='YlGnBu', fmt=".2f")
plt.title("Extended Correlation Heatmap: Company Features")
plt.tight_layout()
plt.show()


# Count jobs grouped by experience level and work type
exp_work_counts = (
    job_postings_df.groupby(["formatted_experience_level", "formatted_work_type"])
    .size()
    .reset_index(name="job_count")
)

# Interactive heatmap using Plotly
fig = px.density_heatmap(
    data_frame=exp_work_counts,
    x="formatted_work_type",
    y="formatted_experience_level",
    z="job_count",
    color_continuous_scale="Viridis",
    title="Job Counts by Experience Level and Work Type",
    labels={"job_count": "Number of Jobs"}
)
fig.update_layout(xaxis_title="Work Type", yaxis_title="Experience Level")
fig.show()
merged1 = pd.merge(salaries_df, job_postings_df, on='job_id', how='left')
merged1 = pd.merge(merged1, employee_df, on='company_id', how='left')

# Merge with company metadata
merged1 = pd.merge(merged1, companies_df, on='company_id', how='left')

# Calculate average salary
merged1['avg_salary'] = (merged1['min_salary'] + merged1['max_salary']) / 2

# Filter out rows with missing values
filtered = merged1.dropna(subset=['avg_salary', 'employee_count'])

# Plot: Salary vs Employee Count with company size as hue
plt.figure(figsize=(10, 6))
sns.scatterplot(data=filtered, x='employee_count', y='avg_salary', hue='company_size', alpha=0.7)
plt.title("Average Salary vs. Company Size (Employee Count)")
plt.xlabel("Employee Count")
plt.ylabel("Average Salary")
plt.xscale("log")
plt.tight_layout()
plt.show()


# Re-import interactive plotting library
import plotly.express as px

# Create interactive scatter plot: Avg Salary vs Employee Count with company size color
interactive_fig = px.scatter(
    filtered,
    x='employee_count',
    y='avg_salary',
    color='company_size',
    hover_data=['name', 'company_id'],
    title="Interactive: Average Salary vs. Company Size (Employee Count)",
    labels={
        "employee_count": "Number of Employees",
        "avg_salary": "Average Salary",
        "company_size": "Company Size"
    },
    log_x=True,
    opacity=0.7
)

interactive_fig.update_layout(height=600)
interactive_fig.show()


# Re-import libraries after environment reset
import pandas as pd
import plotly.express as px

# Reload datasets
# salaries_df = pd.read_csv("/mnt/data/cleaned_salaries.csv")
# job_postings_df = pd.read_csv("/mnt/data/cleaned_job_postings.csv", usecols=["job_id", "company_id"])
# employee_counts_df = pd.read_csv("/mnt/data/cleaned_employee_counts.csv")
# companies_df = pd.read_csv("/mnt/data/cleaned_companies.csv", usecols=["company_id", "company_size", "name"])

# Merge datasets
merged1 = pd.merge(salaries_df, job_postings_df, on='job_id', how='left')
merged1 = pd.merge(merged1, employee_df, on='company_id', how='left')
merged1 = pd.merge(merged1, companies_df, on='company_id', how='left')

# Compute average salary
merged1['avg_salary'] = (merged1['min_salary'] + merged1['max_salary']) / 2

# Filter out rows with missing critical fields
filtered = merged1.dropna(subset=['avg_salary', 'employee_count', 'company_size'])

# Interactive scatter plot
interactive_fig = px.scatter(
    filtered,
    x='employee_count',
    y='avg_salary',
    color='company_size',
    hover_data=['name', 'company_id'],
    title="Interactive: Average Salary vs. Company Size (Employee Count)",
    labels={
        "employee_count": "Number of Employees",
        "avg_salary": "Average Salary",
        "company_size": "Company Size"
    },
    log_x=True,
    opacity=0.7
)

interactive_fig.update_layout(height=600)
interactive_fig.show()




# # Reload the most recent version of the filtered data used for plotting
# salaries_df = pd.read_csv("/mnt/data/cleaned_salaries.csv")
# job_postings_df = pd.read_csv("/mnt/data/cleaned_job_postings.csv", usecols=["job_id", "company_id", "listed_time"])
# employee_counts_df = pd.read_csv("/mnt/data/cleaned_employee_counts.csv")
# companies_df = pd.read_csv("/mnt/data/cleaned_companies.csv", usecols=["company_id", "company_size", "name"])


# ---- Chapter 7: KDE Plot ----
fig_kde = px.histogram(
    filtered,
    x='avg_salary',
    nbins=60,
    marginal="rug",
    histnorm='density',
    title="Chapter 7: KDE - Average Salary Distribution",
    labels={"avg_salary": "Average Salary"}
)
fig_kde.update_traces(opacity=0.6)
fig_kde.show()

# ---- Chapter 8: ECDF ----
fig_ecdf = px.ecdf(
    filtered,
    x='avg_salary',
    title="Chapter 8: ECDF of Average Salary",
    labels={"avg_salary": "Average Salary"}
)
fig_ecdf.show()

# ---- Chapter 9: Violin Plot by Company Size ----
fig_violin = px.violin(
    filtered,
    y="avg_salary",
    x="company_size",
    box=True,
    points="all",
    title="Chapter 9: Salary Distribution by Company Size",
    labels={"avg_salary": "Average Salary", "company_size": "Company Size"}
)
fig_violin.show()

# ---- Chapter 11: Treemap of Salary by Company Size and Company Name ----
fig_treemap = px.treemap(
    filtered,
    path=["company_size", "name"],
    values="avg_salary",
    title="Chapter 11: Treemap - Avg Salary by Company Size & Company",
    hover_data=["employee_count"]
)
fig_treemap.show()
