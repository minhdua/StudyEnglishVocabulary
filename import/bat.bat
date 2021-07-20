@echo off  
set list=TOIECALUNIT01 TOIECALUNIT02 TOIECALUNIT03 TOIECALUNIT04 TOIECALUNIT05 TOIECALUNIT06 TOIECALUNIT07 TOIECALUNIT08 TOIECALUNIT0910 TOIECALUNIT11 TOIECALUNIT12  
set list2="Toiec A Listening Unit 1" "Toiec A Listening Unit 2" "Toiec A Listening Unit 3" "Toiec A Listening Unit 4" "Toiec A Listening Unit 5" "Toiec A Listening Unit 6" "Toiec A Listening Unit 7" "Toiec A Listening Unit 8" "Toiec A Listening Unit 9-10" "Toiec A Listening Unit 11" "Toiec A Listening Unit 12" 
(for %%a in (%list%) do (     start notepad++ %%a.csv )) 