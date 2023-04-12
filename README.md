 - # De Titel
   
   Een python back-end voor BlueTea's virtual Studio
   
   # Installation
   
   Eerst, clone de github repo:
   
       git clone https://github.com/RoyWendries/DigitalTwin.git
       cd DigitalTwin
   
   Vervolgens, installeer de requirements:
   
       pip install -r requirements.txt
   
   Zorg dat alle JSON data van het gespeelde scenario in de Data folder
   zit, en run vervolgens het python bestand:
   
       python Iteration_3/DataAnalysis.py Andere mogelijkheden zijn::
   Dit kan ook zijn:
   
       py Iteration_3/DataAnalysis.py
       
   of:
   
       python3 Iteration_3/DataAnalysis.py
   
   Deze genereerd vervolgens een Parquet bestand in de map Iteration_3,
   wat gebruikt kan worden in het gemaakte PowerBI dashboard. De
   naamgeving is `YYYYMMDD-hhmmss`.
