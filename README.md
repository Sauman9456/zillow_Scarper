# zillow_Scarper

Step1:Goto the current working directory from command prompt

Step2:intstall requirements.txt (which contain the required Python libraries) by using the following command:
      >>pip install -r requirements.txt

Step3:Run Ariya.py
      >>python Ariya.py

Step4:Provide the Location names as input, this input will be separated by comma and hit the enter for example
      >san-francisco-ca,gray-la,penn-quarter-washington-dc

Step5:Wait for some time, when the execution is over, "zillowInsight-[location].json" and "zillowInsight-[location].csv"
      files for each location is generated insdie the data folder. Now open the generated files you will see many values 
      are filled with "Nodata" beacuse of data is not given for the respected values on the respected webpage 



Note:1st row of each of the generated files contains the details regarding given location which will followed by its 
"neighborhoods" not the "nearby cities"
