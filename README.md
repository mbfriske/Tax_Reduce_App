# tax_reduce_app

# Dallas Strategic Property Tax Advisors 
Appeal with confidence! Harnessing the power of machine learning, we have helped thousands of Dallas property owners to determine their chances of winning an appeal even before they step into the courtroom.

Website: https://taxreduceapp.herokuapp.com/
By: Estuardo, Jill, Matt, Michael, Nick 

## About Tax Appraisal App:  

### DATA : Dallas Central Appraisal District
http://dallascad.org/DataProducts.aspx 
* Our application uses the 2017, 2018, & 2019 appraisal data to determine if you are eligible to appeal your property tax

##  About the process:
* Gathering, exploring and cleaning the data
    * Uploading our data to AWS and connecting to postgres 
    * Using a Jupyter Notebook with pandas, matplotlib, seaborn, and sqlachmey libraries to query to the data, clean the data and visually explore the data 
* SckKit Learn libray was used to run the cleaned data through machine learning models 
    * Using Logistic Regression, KNN, Decision Tree, Random Forest, and Support Vector Machine models we are able to predict the your eligibity to appeal for alower tax rate 
    * Support Vector Machine model is the most accurate for predicting the outcome 
