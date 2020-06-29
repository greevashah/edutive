# Edutive
The proposed application aids aspiring students by providing a variety of MCQ tests to practice. These tests will be adaptive to the user's performance in previous tests. Users will also be able to see the analysis of their performance in each test. The system will simulate the exact test pattern of the entrance exam the aspirant is opting for, hence taking him a step closer to achieve desired grade.

Hosted on - https://edutive.herokuapp.com/

## Getting Started  
- Clone the Repo `git clone https://github.com/greevashah/edutive.git`
- Move to directory `cd edutive`
- Run the following commands
   ```
   pip install -r requirements.txt
   .\be_env\Scripts\activate
   ```
- Download the [Database](https://github.com/greevashah/edutive/blob/master/Database/edutive.sql) , import it on xampp and replace all database connections. 
- Run `python app.py` for a dev server. Navigate to `http://localhost:5000/`.


## Test Generation
* [Rendering Test](https://github.com/greevashah/edutive/blob/65f988fd5411d68a8d9f8a1cae7ff292fd683cbb/static/js/capture_parameter.js#L68-L111)
* [Storing Answer](https://github.com/greevashah/edutive/blob/65f988fd5411d68a8d9f8a1cae7ff292fd683cbb/static/js/capture_parameter.js#L139-L184)
* [Test Submission](https://github.com/greevashah/edutive/blob/65f988fd5411d68a8d9f8a1cae7ff292fd683cbb/static/js/capture_parameter.js#L219-L269)
## Test Adaptiveness Logic
* Fuzzifier: [Src code](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/pythonBlueprint/thanking.py#L12-L64)
* Machine Learning based Intelligence: [Usage](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/pythonBlueprint/thanking.py#L65-L64) | [Src code](https://github.com/greevashah/edutive/blob/master/linreg.py/) | [Training Dataset](https://github.com/greevashah/edutive/blob/master/train.csv/)
* Inference Enginee & Defuzzifier: [Src code](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/pythonBlueprint/thanking.py#L336-L345)

## User Performance Analysis
*  Test Dashboard
   - [Cards](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/templates/dashboard.html#L100-L163)
   - [Tables](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/templates/dashboard.html#L165-L281)
   - [Bar-Graphs](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/static/js/dashboard.js#L10-L59)
   - [Pie-Charts](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/static/js/dashboard.js#L61-L87)
    
*  Test Profile
   - [Cards](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/templates/profile.html#L102-L180)
   - [Tables](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/templates/profile.html#L195-L235)
   - [Timeline](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/pythonBlueprint/profile.py#L89-L122)
   - [Line Chart](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/static/js/profile.js#L39-L69)
## Gamification

* [Checkpoint Logic](https://github.com/greevashah/edutive/blob/aba25d6b3ef198b846b6dce2aa32e3d53b871f0e/pythonBlueprint/thanking.py#L134-L193)


