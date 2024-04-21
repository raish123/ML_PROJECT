from flask import Flask,render_template,redirect,request,url_for
import numpy as np,pandas as pd
from sklearn.preprocessing import StandardScaler
from src.pipelines.predict_pipeline import  PredictPipeline,CustomData


#creating a flask object
app = Flask('__name__',template_folder='templates')



#now creating route built in method of flask generally we used to map the url with specific function always used with decorator function
@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')


#now creating route for predicting the model 
@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
    results = None  # Initialize results variable
    if request.method=="POST":
        data = CustomData(
                gender=request.form.get('gender'),
                race_ethnicity=request.form.get('ethnicity'),
                parental_level_of_education=request.form.get('parental_level_of_education'),
                lunch=request.form.get('lunch'),
                test_preparation_course=request.form.get('test_preparation_course'),
                reading_score=float(request.form.get('writing_score')),
                writing_score=float(request.form.get('reading_score'))
            )
        pred_df = data.get_data_as_data_frame()
        print(pred_df)

        predict_pipeline = PredictPipeline()
        #now predicting
        results = predict_pipeline.predict(pred_df)


    return render_template('home.html',results = results)














if __name__ == '__main__':
    app.run(debug=True)