import streamlit as st
import joblib

from reportlab.pdfgen import canvas
import io

st.set_page_config(
    page_title="Health AI Dashboard",
    page_icon="🏥",
    layout="wide"
)


st.markdown("""
<style>

/* Main App */
.stApp{
    background-color:#121212;
    color:white;
}

/* Sidebar */
[data-testid="stSidebar"]{
    background-color:#1b1b1b;
}

/* Sidebar text */
[data-testid="stSidebar"] *{
    color:white !important;
}

/* Radio buttons */
div[role="radiogroup"] label{
    color:white !important;
    font-size:18px !important;
    font-weight:500 !important;
}

/* Input Labels */
label{
    color:white !important;
    font-size:16px !important;
    font-weight:600 !important;
}

/* Text Input */
.stTextInput input{
    background:#1e1e1e !important;
    color:white !important;
    border:2px solid #4CAF50 !important;
    border-radius:10px !important;
}

/* Number Input */
.stNumberInput input{
    background:#1e1e1e !important;
    color:white !important;
    border:2px solid #4CAF50 !important;
    border-radius:10px !important;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"]{
    background:#1e1e1e !important;
    color:white !important;
}

/* Buttons */
.stButton button{
    background:#4CAF50 !important;
    color:white !important;
    font-weight:bold !important;
    border:none !important;
    border-radius:10px !important;
    height:50px !important;
}

/* Headers */
h1,h2,h3,h4,h5,h6{
    color:white !important;
}

/* Sidebar Radio Text */
[data-baseweb="radio"]{
    color:white !important;
}
/* Radio labels */
[data-testid="stSidebar"] label {
    color: white !important;
}

/* Sidebar markdown text */
[data-testid="stSidebar"] p {
    color: white !important;
}

            /* Download Button */
.stDownloadButton button{
    background-color:#4CAF50 !important;
    color:white !important;
    font-weight:bold !important;
    border:none !important;
    border-radius:10px !important;
    height:50px !important;
    width:250px !important;
}

.stDownloadButton button:hover{
    background-color:#45a049 !important;
    color:white !important;
}


</style>
""", unsafe_allow_html=True)



if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        st.image(
        "https://cdn-icons-png.flaticon.com/512/2966/2966486.png",
        width=120
       )
    
        st.container()
        st.markdown("""
               <h1 style='text-align:center;color:#4CAF50;'>
          🏥 HealthAI
           </h1>

           <h4 style='text-align:center;color:white;'>
             Disease prediction
              </h4>
             """, unsafe_allow_html=True)
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")

        if st.button("Login"):
           if username == "admin" and password == "admin123":
              st.session_state.logged_in = True
              st.rerun()
           else:
              st.error("Invalid Credentials")

    
    st.markdown("""
     <style>
      .login-box{
    background:#1e1e1e;
    padding:30px;
    border-radius:15px;
    box-shadow:0 0 15px rgba(0,255,0,0.2);
         }
            </style>
           """, unsafe_allow_html=True)
    


    st.stop()

st.markdown("""
<style>

.stApp {
    background-color: #121212;
    color: white;
}

.stTextInput input,
.stNumberInput input,
.stSelectbox select {
    color: white !important;
    background-color: #1e1e1e !important;
}

[data-testid="stSidebar"] {
    background-color: #1e1e1e;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}

.metric-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)


st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2966/2966486.png",
    width=80
)
 

st.markdown("""
<h1 style='color:white;font-size:52px;'>
🏥 HealthAI Diagnostic System
</h1>
""", unsafe_allow_html=True)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()


st.sidebar.markdown(
"""
Check disease risk 
"""
)

page = st.sidebar.radio(
    "Select Disease",
    ["🩺 Diabetes", "❤️ Heart Disease", "🎗️ Breast Cancer"]
)



st.markdown(
"""
check disease risk 

---
"""
)
import joblib
@st.cache_resource
def load_models():
    diabetes_model = joblib.load("diabetes_model.pkl")
    diabetes_scaler = joblib.load("diabetes_scaler.pkl")

    heart_model = joblib.load("heart_model.pkl")

    breast_model = joblib.load("breast_cancer_model.pkl")
    breast_scaler = joblib.load("breast_cancer_scaler.pkl")

    return (
        diabetes_model,
        diabetes_scaler,
        heart_model,
        breast_model,
        breast_scaler
    )

(
    diabetes_model,
    diabetes_scaler,
    heart_model,
    breast_model,
    breast_scaler
) = load_models()

def create_pdf(patient_name, patient_id, disease, result, risk):

    buffer = io.BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle("HealthAI Report")

    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(150, 800, "HealthAI Medical Report")

    pdf.line(50, 785, 550, 785)

    pdf.setFont("Helvetica", 14)

    pdf.drawString(70, 740, f"Patient Name: {patient_name}")
    pdf.drawString(70, 710, f"Patient ID: {patient_id}")
    pdf.drawString(70, 680, f"Disease: {disease}")
    pdf.drawString(70, 650, f"Result: {result}")
    pdf.drawString(70, 620, f"Risk Score: {risk}%")

    pdf.drawString(70, 560, "Generated by HealthAI Diagnostic System")

    pdf.save()

    buffer.seek(0)

    return buffer



if page == "🩺 Diabetes":

    st.markdown("""
<div style="
background-color:#1e1e1e;
color:white;
padding:20px;
border-radius:12px;
border:1px solid #4CAF50;
margin-bottom:20px;
">
<h2>🩺 Diabetes</h2>
<p>Enter patient clinical measurements below.</p>
</div>
""", unsafe_allow_html=True)

    st.subheader("Patient Information")

    col1, col2 = st.columns(2)

    with col1:
     patient_name = st.text_input(
        "Patient Name",
        key="diabetes_name"
    )

    with col2:
     patient_id = st.text_input(
        "Patient ID",
        key="diabetes_id"
    )

    col1, col2 = st.columns(2)

    with col1:
     pregnancies = st.number_input("Pregnancies")
     glucose = st.number_input("Glucose Level (mg/dL)")
     bp = st.number_input("Blood Pressure (mmHg)")
     skin = st.number_input("Skin Thickness")

    with col2:
     insulin = st.number_input("Insulin")
     bmi = st.number_input("Body Mass Index (BMI)")
     dpf = st.number_input("Diabetes Pedigree Function")
     age = st.number_input("Age")

    if st.button("Predict Diabetes"):

        data = [[
            pregnancies,
            glucose,
            bp,
            skin,
            insulin,
            bmi,
            dpf,
            age
        ]]
       
        data = diabetes_scaler.transform(data)

        prediction = diabetes_model.predict(data)
        probability = diabetes_model.predict_proba(data)[0]
        risk = round(probability[1] * 100, 2)
        

        st.markdown(f"""
<div style="
background:#1e1e1e;
padding:20px;
border-radius:12px;
margin-top:15px;
border:1px solid #4CAF50;
">
<h4 style="color:white;">Risk Score</h4>
<h1 style="color:#4CAF50;">{risk}%</h1>
</div>
""", unsafe_allow_html=True)
        
        if prediction[0] == 1:

                   st.markdown(f"""
<div style="
padding:20px;
border-radius:10px;
background:#1e1e1e;
color:white;
border-left:8px solid #4CAF50;
">
<h3>🔴 High Risk Detected</h3>
Estimated Risk Score: {risk}%
</div>
 """, unsafe_allow_html=True)  


        else:
          st.markdown(f"""
<div style="
padding:20px;
border-radius:10px;
background:#1e1e1e;
color:white;
border-left:8px solid #4CAF50;
">
<h3>🟢 Low Risk</h3>
Estimated Risk Score: {risk}%
</div>
""", unsafe_allow_html=True)
         
        pdf_file = create_pdf(
           patient_name,
          patient_id,
              "Diabetes",
               "High Risk" if prediction[0] == 1 else "Low Risk",
          risk
      )

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
           st.download_button(
        label="📄 Download Report",
        data=pdf_file,
        file_name="Diabetes_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

elif page ==  "❤️ Heart Disease":
    st.markdown("""
<div style="
background-color:#1e1e1e;
color:white;
padding:20px;
border-radius:12px;
border:1px solid #4CAF50;
margin-bottom:20px;
">
<h2> Heart Disease Prediction</h2>
<p>Enter patient clinical measurements below.</p>
</div>
""", unsafe_allow_html=True)
    
    

   
    col1, col2 = st.columns(2)

    with col1:
     patient_name = st.text_input(
        "Patient Name",
        key="heart_name"

    )

    with col2:
     patient_id = st.text_input(
        "Patient ID",
        key="heart_id"
    )

    col1, col2 = st.columns(2)

    with col1:
      age = st.number_input("Age", 1, 120)
      sex = st.selectbox(
          "Gender",
          [0, 1],
          format_func=lambda x: "Female" if x == 0 else "Male"
              )
      
      cp = st.selectbox(
            "Chest Pain Category",
            [0, 1, 2, 3],
            help="Select the type of chest discomfort experienced"
              )

      trestbps = st.number_input(
                   "Resting Blood Pressure (mmHg)"
                )

      chol = st.number_input(
               "Cholesterol Level (mg/dL)"
           )

      fbs = st.selectbox(
          "High Fasting Blood Sugar?",
          [0, 1],
          format_func=lambda x: "No" if x == 0 else "Yes"
       )

    with col2:
      restecg = st.selectbox("Resting ECG", [0, 1, 2])
      thalach = st.number_input(
        "Maximum Heart Rate Achieved"
         )
      exang = st.selectbox(
               "Chest Pain During Exercise?",
               [0, 1],
               format_func=lambda x: "No" if x == 0 else "Yes"
             )

      oldpeak = st.number_input(
             "Stress Test Score",
             value=0.0,
             help="Heart stress measurement during exercise"
)
      slope = st.selectbox(
             "ECG Slope",
             [0,1,2]
           )

      ca = st.selectbox(
              "Blocked Blood Vessels",
            [0,1,2,3,4]
       )

      thal = st.selectbox(
              "Blood Flow Condition",
          [0,1,2,3]
             )

    # Derived features used during training
    age_group = "Young" if age < 40 else "Middle" if age < 60 else "Senior"
    oldpeak_group = "Low" if oldpeak < 1 else "Medium" if oldpeak < 2 else "High"

    if st.button("Predict Heart Disease"):

        import pandas as pd

        input_df = pd.DataFrame([{
            'age': age,
            'trestbps': trestbps,
            'chol': chol,
            'thalach': thalach,
            'oldpeak': oldpeak,
            'sex': sex,
            'cp': cp,
            'fbs': fbs,
            'restecg': restecg,
            'exang': exang,
            'slope': slope,
            'ca': ca,
            'thal': thal,
            'age_group':age_group,
            'oldpeak_group': oldpeak_group

        }])

        prediction = heart_model.predict(input_df)

        prob = heart_model.predict_proba(input_df)[0]
        risk = round(prob[1] * 100, 2)

        
        st.markdown(f"""
<div style="
background:#1e1e1e;
padding:20px;
border-radius:12px;
margin-top:15px;
border:1px solid #4CAF50;
">
<h4 style="color:white;">Risk Score</h4>
<h1 style="color:#4CAF50;">{risk}%</h1>
</div>
""", unsafe_allow_html=True)
        

        if prediction[0] == 1:
            st.markdown(f"""
               <div style="
                padding:20px;
                border-radius:10px;
                background:#1e1e1e;
                border-left:8px solid #4CAF50;
                ">
                <h3>🔴 High Risk Detected</h3>
                Estimated Risk Score: {risk}%
                </div>
               """, unsafe_allow_html=True)

        else:
           st.markdown(f"""
<div style="
padding:20px;
border-radius:10px;
background:#1e1e1e;
color:white;
border-left:8px solid #4CAF50;
">
<h3>🟢 Low Risk</h3>
Estimated Risk Score: {risk}%
</div>
""", unsafe_allow_html=True)
           
        pdf_file = create_pdf(
               patient_name,
              patient_id,
               "Heart Disease",
               "High Risk" if prediction[0] == 1 else "Low Risk",
                risk
          )

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
          st.download_button(
           label="📄 Download Report",
        data=pdf_file,
        file_name="Heart_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )



elif page ==  "🎗️ Breast Cancer":
    st.markdown("""
<div style="
background-color:#1e1e1e;
color:white;
padding:20px;
border-radius:12px;
border:1px solid #4CAF50;
margin-bottom:20px;
">
<h2> 🎗️ Breast Cancer</h2>
<p>Enter patient clinical measurements below.</p>
</div>
""", unsafe_allow_html=True)
        


    col1, col2 = st.columns(2)

    with col1:
      patient_name = st.text_input(
        "Patient Name",
        key="cancerpatient_name"

     )

    with col2:
      patient_id = st.text_input(
        "Patient ID",
        key="cancerpatient_id"
    )

    col1, col2 = st.columns(2)

    with col1:
        radius_mean = st.number_input(
                 "Tumor Radius"
            )

        texture_mean = st.number_input(
                 "Tumor Texture"
           )

        perimeter_mean = st.number_input(
              "Tumor Perimeter"
         )

        area_mean = st.number_input(
              "Tumor Area"
             )

        smoothness_mean = st.number_input(
              "Tumor Smoothness"
             )

    with col2:
        compactness_mean = st.number_input(
             "Tumor Compactness"
             )

        concavity_mean = st.number_input(
               "Tumor Concavity"
               )

        concave_points_mean = st.number_input(
             "Concave Points"
         )

        symmetry_mean = st.number_input(
             "Tumor Symmetry"
           ) 

        fractal_dimension_mean = st.number_input(
                  "Tumor Fractal Dimension"
            )

    if st.button("Predict Breast Cancer"):

        import numpy as np

        data = np.array([[
            radius_mean,
            texture_mean,
            perimeter_mean,
            area_mean,
            smoothness_mean,
            compactness_mean,
            concavity_mean,
            concave_points_mean,
            symmetry_mean,
            fractal_dimension_mean
        ]])

        data = breast_scaler.transform(data)

        prediction = breast_model.predict(data)

        if prediction[0] == "M":
               st.markdown("""
<div style="
background-color:#1e1e1e;
color:white;
padding:20px;
border-radius:12px;
border:1px solid #4CAF50;
margin-bottom:20px;
">
<h2> 🔴 Malignant Tumor Detected</h2>

</div>
""", unsafe_allow_html=True)
           

        else:

               st.markdown("""
<div style="
background-color:#1e1e1e;
color:white;
padding:20px;
border-radius:12px;
border:1px solid #4CAF50;
margin-bottom:20px;
">
<h2> 🟢 Benign Tumor</h2>

</div>
""", unsafe_allow_html=True)
        result = (
              "Malignant"
             if prediction[0] == "M"
                else "Benign"
          )

        pdf_file = create_pdf(
               patient_name,
                  patient_id,
               "Breast Cancer",
              result,
               0
           )

        col1, col2, col3 = st.columns([1,2,1])

        with col2:
         st.download_button(
        label="📄 Download Report",
        data=pdf_file,
        file_name="Cancer_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )



