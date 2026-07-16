# Data Dictionary

## clinical_cohort_v1.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| PDTRTMNT | float64 | True | Unknown/Standard feature |
| PDSTATE | str | False | Unknown/Standard feature |
| HRPOSTMED | float64 | True | Unknown/Standard feature |
| HRDBSON | float64 | True | Unknown/Standard feature |
| HRDBSOFF | float64 | True | Unknown/Standard feature |
| PDMEDYN | float64 | True | Unknown/Standard feature |
| DBSYN | float64 | True | Unknown/Standard feature |
| ONOFFORDER | float64 | True | Unknown/Standard feature |
| OFFEXAM | float64 | True | Unknown/Standard feature |
| OFFNORSN | float64 | True | Unknown/Standard feature |
| DBSOFFYN | float64 | True | Unknown/Standard feature |
| DBSOFFTM | float64 | True | Unknown/Standard feature |
| ONEXAM | float64 | True | Unknown/Standard feature |
| ONNORSN | float64 | True | Unknown/Standard feature |
| HIFUYN | float64 | True | Unknown/Standard feature |
| DBSONYN | float64 | True | Unknown/Standard feature |
| DBSONTM | float64 | True | Unknown/Standard feature |
| PDMEDDT | str | False | Unknown/Standard feature |
| PDMEDTM | str | False | Unknown/Standard feature |
| EXAMDT | str | False | Unknown/Standard feature |
| EXAMTM | str | False | Unknown/Standard feature |
| NP3SPCH | float64 | True | Unknown/Standard feature |
| NP3FACXP | float64 | True | Unknown/Standard feature |
| NP3RIGN | float64 | True | Unknown/Standard feature |
| NP3RIGRU | float64 | True | Unknown/Standard feature |
| NP3RIGLU | float64 | True | Unknown/Standard feature |
| NP3RIGRL | float64 | True | Unknown/Standard feature |
| NP3RIGLL | float64 | True | Unknown/Standard feature |
| NP3FTAPR | float64 | True | Unknown/Standard feature |
| NP3FTAPL | float64 | True | Unknown/Standard feature |
| NP3HMOVR | float64 | True | Unknown/Standard feature |
| NP3HMOVL | float64 | True | Unknown/Standard feature |
| NP3PRSPR | float64 | True | Unknown/Standard feature |
| NP3PRSPL | float64 | True | Unknown/Standard feature |
| NP3TTAPR | float64 | True | Unknown/Standard feature |
| NP3TTAPL | float64 | True | Unknown/Standard feature |
| NP3LGAGR | float64 | True | Unknown/Standard feature |
| NP3LGAGL | float64 | True | Unknown/Standard feature |
| NP3RISNG | float64 | True | Unknown/Standard feature |
| NP3GAIT | float64 | True | Unknown/Standard feature |
| NP3FRZGT | float64 | True | Unknown/Standard feature |
| NP3PSTBL | float64 | True | Unknown/Standard feature |
| NP3POSTR | float64 | True | Unknown/Standard feature |
| NP3BRADY | float64 | True | Unknown/Standard feature |
| NP3PTRMR | float64 | True | Unknown/Standard feature |
| NP3PTRML | float64 | True | Unknown/Standard feature |
| NP3KTRMR | float64 | True | Unknown/Standard feature |
| NP3KTRML | float64 | True | Unknown/Standard feature |
| NP3RTARU | float64 | True | Unknown/Standard feature |
| NP3RTALU | float64 | True | Unknown/Standard feature |
| NP3RTARL | float64 | True | Unknown/Standard feature |
| NP3RTALL | float64 | True | Unknown/Standard feature |
| NP3RTALJ | float64 | True | Unknown/Standard feature |
| NP3RTCON | float64 | True | Unknown/Standard feature |
| NP3TOT | float64 | True | Unknown/Standard feature |
| DYSKPRES | float64 | True | Unknown/Standard feature |
| DYSKIRAT | float64 | True | Unknown/Standard feature |
| NHY | float64 | True | Hoehn & Yahr Stage |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |
| priority | float64 | True | Unknown/Standard feature |


## FOUND_Self-Reported_Dx_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| SRDXDATE | str | False | Unknown/Standard feature |
| FOPTRDX | str | False | Unknown/Standard feature |
| FOPTRDXOTHER | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Geriatric_Depression_Scale__Short_Version__14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| GDSSATIS | int64 | True | Unknown/Standard feature |
| GDSDROPD | int64 | True | Unknown/Standard feature |
| GDSEMPTY | int64 | True | Unknown/Standard feature |
| GDSBORED | int64 | True | Unknown/Standard feature |
| GDSGSPIR | int64 | True | Unknown/Standard feature |
| GDSAFRAD | int64 | True | Unknown/Standard feature |
| GDSHAPPY | int64 | True | Unknown/Standard feature |
| GDSHLPLS | int64 | True | Unknown/Standard feature |
| GDSHOME | int64 | True | Unknown/Standard feature |
| GDSMEMRY | int64 | True | Unknown/Standard feature |
| GDSALIVE | int64 | True | Unknown/Standard feature |
| GDSWRTLS | int64 | True | Unknown/Standard feature |
| GDSENRGY | int64 | True | Unknown/Standard feature |
| GDSHOPLS | int64 | True | Unknown/Standard feature |
| GDSBETER | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Neurological_Exam_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| MTRRSP | int64 | True | Unknown/Standard feature |
| CORDRSP | int64 | True | Unknown/Standard feature |
| SENRSP | int64 | True | Unknown/Standard feature |
| RFLXRSP | int64 | True | Unknown/Standard feature |
| PLRRRSP | float64 | True | Unknown/Standard feature |
| PLRLRSP | float64 | True | Unknown/Standard feature |
| GAITRSP | float64 | True | Unknown/Standard feature |
| MNTLRSP | float64 | True | Unknown/Standard feature |
| CNRSP | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Participant_Status_08Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PATNO | int64 | True | Patient Identifier |
| COHORT | int64 | True | Unknown/Standard feature |
| COHORT_DEFINITION | str | False | Unknown/Standard feature |
| ENROLL_DATE | str | False | Unknown/Standard feature |
| ENROLL_STATUS | str | False | Unknown/Standard feature |
| STATUS_DATE | str | False | Unknown/Standard feature |
| SCREENEDAM | float64 | True | Unknown/Standard feature |
| ENROLL_AGE | float64 | True | Age of Participant |
| INEXPAGE | float64 | True | Age of Participant |
| AV133STDY | float64 | True | Unknown/Standard feature |
| TAUSTDY | float64 | True | Unknown/Standard feature |
| GAITSTDY | float64 | True | Unknown/Standard feature |
| PISTDY | float64 | True | Unknown/Standard feature |
| SV2ASTDY | float64 | True | Unknown/Standard feature |
| NXTAUSTDY | float64 | True | Unknown/Standard feature |
| DPPDSTDY | float64 | True | Unknown/Standard feature |
| DPPROSTDY | float64 | True | Unknown/Standard feature |
| FD4STDY | float64 | True | Unknown/Standard feature |
| DPASTDY | float64 | True | Unknown/Standard feature |
| DPDPASTDY | float64 | True | Unknown/Standard feature |
| GAITLEAPSTDY | float64 | True | Unknown/Standard feature |
| MDGSTDY | float64 | True | Unknown/Standard feature |
| MNISTDY | float64 | True | Unknown/Standard feature |
| DATELIG | float64 | True | Unknown/Standard feature |
| PPMI_ONLINE_ENROLL | str | False | Unknown/Standard feature |
| ENRLPINK1 | float64 | True | Unknown/Standard feature |
| ENRLPRKN | float64 | True | Unknown/Standard feature |
| ENRLSRDC | float64 | True | Unknown/Standard feature |
| ENRLNORM | float64 | True | Unknown/Standard feature |
| ENRLOTHGV | float64 | True | Unknown/Standard feature |
| ENRLHPSM | int64 | True | Unknown/Standard feature |
| ENRLRBD | int64 | True | Unknown/Standard feature |
| ENRLLRRK2 | int64 | True | Unknown/Standard feature |
| ENRLSNCA | int64 | True | Unknown/Standard feature |
| ENRLGBA | int64 | True | Unknown/Standard feature |


## SCOPA-AUT_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| PTCGBOTH | int64 | True | Unknown/Standard feature |
| SCAU1 | int64 | True | Unknown/Standard feature |
| SCAU2 | int64 | True | Unknown/Standard feature |
| SCAU3 | int64 | True | Unknown/Standard feature |
| SCAU4 | int64 | True | Unknown/Standard feature |
| SCAU5 | int64 | True | Unknown/Standard feature |
| SCAU6 | int64 | True | Unknown/Standard feature |
| SCAU7 | int64 | True | Unknown/Standard feature |
| SCAU8 | int64 | True | Unknown/Standard feature |
| SCAU9 | int64 | True | Unknown/Standard feature |
| SCAU10 | int64 | True | Unknown/Standard feature |
| SCAU11 | int64 | True | Unknown/Standard feature |
| SCAU12 | int64 | True | Unknown/Standard feature |
| SCAU13 | int64 | True | Unknown/Standard feature |
| SCAU14 | int64 | True | Unknown/Standard feature |
| SCAU15 | int64 | True | Unknown/Standard feature |
| SCAU16 | int64 | True | Unknown/Standard feature |
| SCAU17 | int64 | True | Unknown/Standard feature |
| SCAU18 | int64 | True | Unknown/Standard feature |
| SCAU19 | int64 | True | Unknown/Standard feature |
| SCAU20 | int64 | True | Unknown/Standard feature |
| SCAU21 | int64 | True | Unknown/Standard feature |
| SCAU22 | float64 | True | Unknown/Standard feature |
| SCAU23 | float64 | True | Unknown/Standard feature |
| SCAU23A | float64 | True | Unknown/Standard feature |
| SCAU23AT | str | False | Unknown/Standard feature |
| SCAU24 | float64 | True | Unknown/Standard feature |
| SCAU25 | float64 | True | Unknown/Standard feature |
| SCAU26A | int64 | True | Unknown/Standard feature |
| SCAU26AT | str | False | Unknown/Standard feature |
| SCAU26B | int64 | True | Unknown/Standard feature |
| SCAU26BT | str | False | Unknown/Standard feature |
| SCAU26C | int64 | True | Unknown/Standard feature |
| SCAU26CT | str | False | Unknown/Standard feature |
| SCAU26D | int64 | True | Unknown/Standard feature |
| SCAU26DT | str | False | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## University_of_Pennsylvania_Smell_Identification_Test_UPSIT_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| SCENT_01_CORRECT | int64 | True | Unknown/Standard feature |
| SCENT_01_RESPONSE | int64 | True | Unknown/Standard feature |
| SCENT_02_CORRECT | int64 | True | Unknown/Standard feature |
| SCENT_02_RESPONSE | int64 | True | Unknown/Standard feature |
| SCENT_03_CORRECT | int64 | True | Unknown/Standard feature |
| SCENT_03_RESPONSE | int64 | True | Unknown/Standard feature |
| SCENT_04_CORRECT | int64 | True | Unknown/Standard feature |
| SCENT_04_RESPONSE | int64 | True | Unknown/Standard feature |
| SCENT_05_CORRECT | int64 | True | Unknown/Standard feature |
| SCENT_05_RESPONSE | int64 | True | Unknown/Standard feature |
| SCENT_06_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_06_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_07_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_07_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_08_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_08_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_09_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_09_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_10_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_10_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_11_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_11_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_12_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_12_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_13_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_13_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_14_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_14_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_15_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_15_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_16_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_16_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_17_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_17_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_18_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_18_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_19_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_19_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_20_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_20_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_21_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_21_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_22_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_22_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_23_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_23_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_24_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_24_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_25_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_25_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_26_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_26_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_27_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_27_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_28_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_28_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_29_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_29_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_30_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_30_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_31_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_31_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_32_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_32_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_33_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_33_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_34_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_34_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_35_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_35_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_36_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_36_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_37_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_37_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_38_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_38_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_39_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_39_RESPONSE | float64 | True | Unknown/Standard feature |
| SCENT_40_CORRECT | float64 | True | Unknown/Standard feature |
| SCENT_40_RESPONSE | float64 | True | Unknown/Standard feature |
| TOTAL_CORRECT | float64 | True | Unknown/Standard feature |
| upsitorder | float64 | True | Unknown/Standard feature |
| UPSITFORM | int64 | True | Unknown/Standard feature |
| UPSIT_PRCNTGE | float64 | True | Unknown/Standard feature |
| UPSIT_PRCTVER | str | False | Unknown/Standard feature |
| IMPUTED_DATA | bool | False | Unknown/Standard feature |
| UPSIT_SOURCE | str | False | Unknown/Standard feature |
| UPSITLANGCNTR | str | False | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Current_Biospecimen_Analysis_Results_08Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PATNO | int64 | True | Patient Identifier |
| SEX | str | False | Sex of Participant |
| COHORT | str | False | Unknown/Standard feature |
| CLINICAL_EVENT | str | False | Unknown/Standard feature |
| TYPE | str | False | Unknown/Standard feature |
| TESTNAME | str | False | Unknown/Standard feature |
| TESTVALUE | str | False | Unknown/Standard feature |
| UNITS | float64 | True | Unknown/Standard feature |
| RUNDATE | str | False | Unknown/Standard feature |
| PROJECTID | int64 | True | Unknown/Standard feature |
| PI_NAME | str | False | Unknown/Standard feature |
| PI_INSTITUTION | str | False | Unknown/Standard feature |
| update_stamp | str | False | Unknown/Standard feature |


## Kinetic_data_for_SAA_Results_08Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PATNO | int64 | True | Patient Identifier |
| SEX | str | False | Sex of Participant |
| COHORT | str | False | Unknown/Standard feature |
| CLINICAL_EVENT | str | False | Unknown/Standard feature |
| AMPRION_ID | str | False | Unknown/Standard feature |
| TYPE | str | False | Unknown/Standard feature |
| SAAMethod | str | False | Unknown/Standard feature |
| SAA_Result | str | False | Unknown/Standard feature |
| RUNDATE | str | False | Unknown/Standard feature |
| Plate_ID | str | False | Unknown/Standard feature |
| Wells | str | False | Unknown/Standard feature |
| Fmax | int64 | True | Unknown/Standard feature |
| TTT | float64 | True | Unknown/Standard feature |
| AUC_Fluoro | int64 | True | Unknown/Standard feature |
| Time_To_Max_Slope | float64 | True | Unknown/Standard feature |
| Max_Slope | float64 | True | Unknown/Standard feature |
| PROJECTID | int64 | True | Unknown/Standard feature |
| PI_NAME | str | False | Unknown/Standard feature |
| PI_INSTITUTION | str | False | Unknown/Standard feature |


## SAA_Biospecimen_Analysis_Results_08Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PATNO | int64 | True | Patient Identifier |
| SEX | str | False | Sex of Participant |
| COHORT | str | False | Unknown/Standard feature |
| CLINICAL_EVENT | str | False | Unknown/Standard feature |
| TYPE | str | False | Unknown/Standard feature |
| SAAMethod | str | False | Unknown/Standard feature |
| SAA_Status | str | False | Unknown/Standard feature |
| SAA_Type | str | False | Unknown/Standard feature |
| Fmax_24h_Rep1 | int64 | True | Unknown/Standard feature |
| Fmax_24h_Rep2 | int64 | True | Unknown/Standard feature |
| Fmax_24h_Rep3 | int64 | True | Unknown/Standard feature |
| TTT_24h_Rep1 | float64 | True | Unknown/Standard feature |
| TTT_24h_Rep2 | float64 | True | Unknown/Standard feature |
| TTT_24h_Rep3 | float64 | True | Unknown/Standard feature |
| AUC_24h_Rep1 | float64 | True | Unknown/Standard feature |
| AUC_24h_Rep2 | float64 | True | Unknown/Standard feature |
| AUC_24h_Rep3 | float64 | True | Unknown/Standard feature |
| TSmax_24h_Rep1 | float64 | True | Unknown/Standard feature |
| TSmax_24h_Rep2 | float64 | True | Unknown/Standard feature |
| TSmax_24h_Rep3 | float64 | True | Unknown/Standard feature |
| SLOPEMax_24h_Rep1 | float64 | True | Unknown/Standard feature |
| SLOPEMax_24h_Rep2 | float64 | True | Unknown/Standard feature |
| SLOPEMax_24h_Rep3 | float64 | True | Unknown/Standard feature |
| Fmax_150h_Rep1 | float64 | True | Unknown/Standard feature |
| Fmax_150h_Rep2 | float64 | True | Unknown/Standard feature |
| Fmax_150h_Rep3 | float64 | True | Unknown/Standard feature |
| TTT_150h_Rep1 | float64 | True | Unknown/Standard feature |
| TTT_150h_Rep2 | float64 | True | Unknown/Standard feature |
| TTT_150h_Rep3 | float64 | True | Unknown/Standard feature |
| AUC_150h_Rep1 | float64 | True | Unknown/Standard feature |
| AUC_150h_Rep2 | float64 | True | Unknown/Standard feature |
| AUC_150h_Rep3 | float64 | True | Unknown/Standard feature |
| T50_150h_Rep1 | float64 | True | Unknown/Standard feature |
| T50_150h_Rep2 | float64 | True | Unknown/Standard feature |
| T50_150h_Rep3 | float64 | True | Unknown/Standard feature |
| SLOPE_150h_Rep1 | float64 | True | Unknown/Standard feature |
| SLOPE_150h_Rep2 | float64 | True | Unknown/Standard feature |
| SLOPE_150h_Rep3 | float64 | True | Unknown/Standard feature |
| InstrumentRep1 | int64 | True | Unknown/Standard feature |
| InstrumentRep2 | int64 | True | Unknown/Standard feature |
| InstrumentRep3 | int64 | True | Unknown/Standard feature |
| SampleVolRep1 | float64 | True | Unknown/Standard feature |
| SampleVolRep2 | float64 | True | Unknown/Standard feature |
| SampleVolRep3 | float64 | True | Unknown/Standard feature |
| RUNDATE | str | False | Unknown/Standard feature |
| PROJECTID | int64 | True | Unknown/Standard feature |
| PI_NAME | str | False | Unknown/Standard feature |
| PI_INSTITUTION | str | False | Unknown/Standard feature |


## Dopamine_Imaging_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| SUB_EVENT_ID | float64 | True | Unknown/Standard feature |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| OFF_SCHEDULE | float64 | True | Unknown/Standard feature |
| DATSCAN | int64 | True | Unknown/Standard feature |
| DATSCANTRC | float64 | True | Unknown/Standard feature |
| PREVDATDT | float64 | True | Unknown/Standard feature |
| SCNLOC | float64 | True | Unknown/Standard feature |
| SCNINJCT | float64 | True | Unknown/Standard feature |
| VSINTRPT | float64 | True | Unknown/Standard feature |
| VSRPTELG | float64 | True | Unknown/Standard feature |
| DIFFLOC | float64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Xing_Core_Lab_-_Quant_SBR_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PROTOCOL | int64 | True | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PREVIOUSLY_ACQUIRED | str | False | Unknown/Standard feature |
| DATSCAN_LIGAND | str | False | Unknown/Standard feature |
| DATSCAN_DATE | str | False | Unknown/Standard feature |
| DATSCAN_ANALYZED | str | False | Unknown/Standard feature |
| DATSCAN_NOT_ANALYZED_REASON | float64 | True | Unknown/Standard feature |
| DATSCAN_OTHER_SPECIFY | float64 | True | Unknown/Standard feature |
| STRIATUM_REF_CWM | float64 | True | Unknown/Standard feature |
| CAUDATE_REF_CWM | float64 | True | Unknown/Standard feature |
| PUTAMEN_REF_CWM | float64 | True | Unknown/Standard feature |
| PRECAUDATE_REF_CWM | float64 | True | Unknown/Standard feature |
| POSCAUDATE_REF_CWM | float64 | True | Unknown/Standard feature |
| PRECOMMISSURAL_PUTAMEN_REF_CWM | float64 | True | Unknown/Standard feature |
| POSCOMMISSURAL_PUTAMEN_REF_CWM | float64 | True | Unknown/Standard feature |
| PREDORSALPUTAMEN_REF_CWM | float64 | True | Unknown/Standard feature |
| PREVENTRALPUTAMEN_REF_CWM | float64 | True | Unknown/Standard feature |
| POSDORSALPUTAMEN_REF_CWM | float64 | True | Unknown/Standard feature |
| POSVENTRALPUTAMEN_REF_CWM | float64 | True | Unknown/Standard feature |
| STRIATUM_L_REF_CWM | float64 | True | Unknown/Standard feature |
| CAUDATE_L_REF_CWM | float64 | True | Unknown/Standard feature |
| PUTAMEN_L_REF_CWM | float64 | True | Unknown/Standard feature |
| PRECAUDATE_L_REF_CWM | float64 | True | Unknown/Standard feature |
| POSCAUDATE_L_REF_CWM | float64 | True | Unknown/Standard feature |
| PRECOMMISSURAL_PUTAMEN_L_REF_CWM | float64 | True | Unknown/Standard feature |
| POSCOMMISSURAL_PUTAMEN_L_REF_CWM | float64 | True | Unknown/Standard feature |
| PREDORSALPUTAMEN_L_REF_CWM | float64 | True | Unknown/Standard feature |
| PREVENTRALPUTAMEN_L_REF_CWM | float64 | True | Unknown/Standard feature |
| POSDORSALPUTAMEN_L_REF_CWM | float64 | True | Unknown/Standard feature |
| POSVENTRALPUTAMEN_L_REF_CWM | float64 | True | Unknown/Standard feature |
| STRIATUM_R_REF_CWM | float64 | True | Unknown/Standard feature |
| CAUDATE_R_REF_CWM | float64 | True | Unknown/Standard feature |
| PUTAMEN_R_REF_CWM | float64 | True | Unknown/Standard feature |
| PRECAUDATE_R_REF_CWM | float64 | True | Unknown/Standard feature |
| POSCAUDATE_R_REF_CWM | float64 | True | Unknown/Standard feature |
| PRECOMMISSURAL_PUTAMEN_R_REF_CWM | float64 | True | Unknown/Standard feature |
| POSCOMMISSURAL_PUTAMEN_R_REF_CWM | float64 | True | Unknown/Standard feature |
| PREDORSALPUTAMEN_R_REF_CWM | float64 | True | Unknown/Standard feature |
| PREVENTRALPUTAMEN_R_REF_CWM | float64 | True | Unknown/Standard feature |
| POSDORSALPUTAMEN_R_REF_CWM | float64 | True | Unknown/Standard feature |
| POSVENTRALPUTAMEN_R_REF_CWM | float64 | True | Unknown/Standard feature |


## Xing_Core_Lab_-_Visual_Read_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PROTOCOL | int64 | True | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| DATSCAN_LIGAND | float64 | True | Unknown/Standard feature |
| DATSCAN_VISINTRP | str | False | Unknown/Standard feature |
| DATSCAN_DATE | str | False | Unknown/Standard feature |


## Clinical_Diagnosis_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| NEWDIAG | int64 | True | Unknown/Standard feature |
| NEWDIAGOTHER | float64 | True | Unknown/Standard feature |
| DIAGSINLV | int64 | True | Unknown/Standard feature |
| DIAGDT | float64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Concomitant_Medication_Log_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| CMTRT | str | False | Unknown/Standard feature |
| CMDOSE | float64 | True | Unknown/Standard feature |
| CMDOSU | str | False | Unknown/Standard feature |
| CMDOSFRQ | str | False | Unknown/Standard feature |
| ROUTE | float64 | True | Unknown/Standard feature |
| STARTDT | str | False | Unknown/Standard feature |
| STOPDT | str | False | Unknown/Standard feature |
| ONGOING | float64 | True | Unknown/Standard feature |
| CMINDC | float64 | True | Unknown/Standard feature |
| CMINDC_TEXT | str | False | Unknown/Standard feature |
| TOTDDOSE | float64 | True | Unknown/Standard feature |
| RECNO | float64 | True | Unknown/Standard feature |
| SEQNO1 | float64 | True | Unknown/Standard feature |
| SEQNO2 | float64 | True | Unknown/Standard feature |
| WHODRUG | str | False | Unknown/Standard feature |
| EXCLMED | str | False | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Features_of_Parkinsonism_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| FEATBRADY | int64 | True | Unknown/Standard feature |
| FEATPOSINS | int64 | True | Unknown/Standard feature |
| FEATRIGID | int64 | True | Unknown/Standard feature |
| FEATTREMOR | int64 | True | Unknown/Standard feature |
| PSGLVL | float64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Initiation_of_Dopaminergic_Therapy_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| DOPTHERST | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## LEDD_Concomitant_Medication_Log_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| LEDTRT | str | False | Unknown/Standard feature |
| TOTDDA | float64 | True | Unknown/Standard feature |
| LEDDSTRMG | float64 | True | Unknown/Standard feature |
| LEDDOSSTR | str | False | Unknown/Standard feature |
| LEDDOSE | float64 | True | Unknown/Standard feature |
| LEDDOSFRQ | float64 | True | Unknown/Standard feature |
| STARTDT | str | False | Unknown/Standard feature |
| STOPDT | str | False | Unknown/Standard feature |
| LEDD | str | False | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Medical_Conditions_Log_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| RESYR | float64 | True | Unknown/Standard feature |
| MHDIAGYR | int64 | True | Unknown/Standard feature |
| MHCAT | int64 | True | Unknown/Standard feature |
| MHHX | int64 | True | Unknown/Standard feature |
| MHDIAGDT | str | False | Unknown/Standard feature |
| MHTERM | str | False | Unknown/Standard feature |
| RESOLVD | float64 | True | Unknown/Standard feature |
| RESDT | str | False | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## PD_Diagnosis_History_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | int64 | True | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| SXDT | str | False | Unknown/Standard feature |
| PDDXDT | str | False | Unknown/Standard feature |
| DXTREMOR | float64 | True | Unknown/Standard feature |
| DXRIGID | float64 | True | Unknown/Standard feature |
| DXBRADY | float64 | True | Unknown/Standard feature |
| DXPOSINS | float64 | True | Unknown/Standard feature |
| DXOTHSX | float64 | True | Unknown/Standard feature |
| DOMSIDE | float64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Vital_Signs_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| WGTKG | float64 | True | Unknown/Standard feature |
| HTCM | float64 | True | Unknown/Standard feature |
| TEMPC | float64 | True | Unknown/Standard feature |
| BPARM | int64 | True | Unknown/Standard feature |
| SYSSUP | int64 | True | Unknown/Standard feature |
| DIASUP | int64 | True | Unknown/Standard feature |
| HRSUP | int64 | True | Unknown/Standard feature |
| SYSSTND | int64 | True | Unknown/Standard feature |
| DIASTND | int64 | True | Unknown/Standard feature |
| HRSTND | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Gait_Data___Arm_swing__Axivity__14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PATNO | int64 | True | Patient Identifier |
| VISNO | str | False | Unknown/Standard feature |
| StartTime | str | False | Unknown/Standard feature |
| StopTime | str | False | Unknown/Standard feature |
| NumberofDays | int64 | True | Unknown/Standard feature |
| ValidDays6HR | int64 | True | Unknown/Standard feature |
| ValidDays12HR | int64 | True | Unknown/Standard feature |
| NonWearDetected | int64 | True | Unknown/Standard feature |
| UpSideDownDetected | int64 | True | Unknown/Standard feature |
| PercentNight | float64 | True | Unknown/Standard feature |
| NightTimeHr | float64 | True | Unknown/Standard feature |
| PercentWalking | float64 | True | Unknown/Standard feature |
| WalkingTime | float64 | True | Unknown/Standard feature |
| PercentLying | float64 | True | Unknown/Standard feature |
| LyingTime | float64 | True | Unknown/Standard feature |
| PercentSitting | float64 | True | Unknown/Standard feature |
| SittingTime | float64 | True | Unknown/Standard feature |
| PercentStanding | float64 | True | Unknown/Standard feature |
| StandingTime | float64 | True | Unknown/Standard feature |
| PercentSedentary | float64 | True | Unknown/Standard feature |
| SedentaryTime | float64 | True | Unknown/Standard feature |
| PercentOther | float64 | True | Unknown/Standard feature |
| OtherTime | float64 | True | Unknown/Standard feature |
| MeanSVMDaymg | float64 | True | Unknown/Standard feature |
| MeanSVMNightmg | float64 | True | Unknown/Standard feature |
| SumSVMDaymg | float64 | True | Unknown/Standard feature |
| SumSVMNightmg | float64 | True | Unknown/Standard feature |
| PercentActiveDay | float64 | True | Unknown/Standard feature |
| PercentActiveNight | float64 | True | Unknown/Standard feature |
| x_5_10Sec | float64 | True | Unknown/Standard feature |
| x_10_20Sec | float64 | True | Unknown/Standard feature |
| x_20_30Sec | float64 | True | Unknown/Standard feature |
| x_30_60Sec | float64 | True | Unknown/Standard feature |
| x_60_120Sec | float64 | True | Unknown/Standard feature |
| x__120Sec | float64 | True | Unknown/Standard feature |
| StepCount | float64 | True | Unknown/Standard feature |
| NumberOfNappingBouts | float64 | True | Unknown/Standard feature |
| MeanNapBoutmin | float64 | True | Unknown/Standard feature |
| TotalNapTimemin | float64 | True | Unknown/Standard feature |
| ActualNightTimehr | float64 | True | Unknown/Standard feature |
| WakeTimeNightminutes | float64 | True | Unknown/Standard feature |
| PercentWakeNight | float64 | True | Unknown/Standard feature |
| NumWalkBoutsNight | float64 | True | Unknown/Standard feature |
| WalkTimeNightminutes | float64 | True | Unknown/Standard feature |
| PercentWalkNight | float64 | True | Unknown/Standard feature |
| NumberOfRotations | float64 | True | Unknown/Standard feature |
| TimeOfRotationsec | float64 | True | Unknown/Standard feature |
| DegreesOfRotationdeg | float64 | True | Unknown/Standard feature |
| VelocityOfRotationdegsec | float64 | True | Unknown/Standard feature |
| NumberOfBouts | float64 | True | Unknown/Standard feature |
| ActivityLevel | float64 | True | Unknown/Standard feature |
| CadencetimeDomain | float64 | True | Unknown/Standard feature |
| rmsV | float64 | True | Unknown/Standard feature |
| rmsML | float64 | True | Unknown/Standard feature |
| rmsAP | float64 | True | Unknown/Standard feature |
| ampV | float64 | True | Unknown/Standard feature |
| ampML | float64 | True | Unknown/Standard feature |
| ampAP | float64 | True | Unknown/Standard feature |
| wdV | float64 | True | Unknown/Standard feature |
| wdML | float64 | True | Unknown/Standard feature |
| wdAP | float64 | True | Unknown/Standard feature |
| stpRegV | float64 | True | Unknown/Standard feature |
| strRegV | float64 | True | Unknown/Standard feature |
| stepAsymV | float64 | True | Unknown/Standard feature |
| stpRegML | float64 | True | Unknown/Standard feature |
| strRegML | float64 | True | Unknown/Standard feature |
| stepAsymML | float64 | True | Unknown/Standard feature |
| stpRegAP | float64 | True | Unknown/Standard feature |
| strRegAP | float64 | True | Unknown/Standard feature |
| stepAsymAP | float64 | True | Unknown/Standard feature |
| stepTime | float64 | True | Unknown/Standard feature |
| strideTime | float64 | True | Unknown/Standard feature |
| CVStrideTime | float64 | True | Unknown/Standard feature |
| CVStepTime | float64 | True | Unknown/Standard feature |
| CVSteplength | float64 | True | Unknown/Standard feature |
| StepVelocitycmsec | float64 | True | Unknown/Standard feature |
| SampEntropyV | float64 | True | Unknown/Standard feature |
| SampEntropyML | float64 | True | Unknown/Standard feature |
| SampEntropyAP | float64 | True | Unknown/Standard feature |
| rmsV_STD | float64 | True | Unknown/Standard feature |
| rmsML_STD | float64 | True | Unknown/Standard feature |
| rmsAP_STD | float64 | True | Unknown/Standard feature |
| ampV_STD | float64 | True | Unknown/Standard feature |
| ampML_STD | float64 | True | Unknown/Standard feature |
| ampAP_STD | float64 | True | Unknown/Standard feature |
| wdV_STD | float64 | True | Unknown/Standard feature |
| wdML_STD | float64 | True | Unknown/Standard feature |
| wdAP_STD | float64 | True | Unknown/Standard feature |
| stpRegV_STD | float64 | True | Unknown/Standard feature |
| strRegV_STD | float64 | True | Unknown/Standard feature |
| stepAsymV_STD | float64 | True | Unknown/Standard feature |
| stpRegML_STD | float64 | True | Unknown/Standard feature |
| strRegML_STD | float64 | True | Unknown/Standard feature |
| stepAsymML_STD | float64 | True | Unknown/Standard feature |
| stpRegAP_STD | float64 | True | Unknown/Standard feature |
| strRegAP_STD | float64 | True | Unknown/Standard feature |
| stepAsymAP_STD | float64 | True | Unknown/Standard feature |
| stepTime_STD | float64 | True | Unknown/Standard feature |
| strideTime_STD | float64 | True | Unknown/Standard feature |
| CVStrideTime_STD | float64 | True | Unknown/Standard feature |
| CVStepTime_STD | float64 | True | Unknown/Standard feature |
| CVSteplength_STD | float64 | True | Unknown/Standard feature |
| StepVelocitycmsec_STD | float64 | True | Unknown/Standard feature |
| SampEntropyV_STD | float64 | True | Unknown/Standard feature |
| SampEntropyML_STD | float64 | True | Unknown/Standard feature |
| SampEntropyAP_STD | float64 | True | Unknown/Standard feature |


## Gait_Substudy_Gait_Mobility_Assessment_and_Measurement_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| SUB_EVENT_ID | str | False | Unknown/Standard feature |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| AXIVITYUSED | int64 | True | Unknown/Standard feature |
| AXIVITYDT | str | False | Unknown/Standard feature |
| AXIVITYUP | int64 | True | Unknown/Standard feature |
| AXIVITYUPDT | str | False | Unknown/Standard feature |
| OPALUSED | int64 | True | Unknown/Standard feature |
| RARMLEN | float64 | True | Unknown/Standard feature |
| LARMLEN | float64 | True | Unknown/Standard feature |
| RLEGLEN | float64 | True | Unknown/Standard feature |
| LLEGLEN | float64 | True | Unknown/Standard feature |
| GAITASTCMPLT | int64 | True | Unknown/Standard feature |
| GAITASTTM | str | False | Unknown/Standard feature |
| GAITTUG1 | float64 | True | Unknown/Standard feature |
| GAITTUG2 | float64 | True | Unknown/Standard feature |
| GAITASTUS | float64 | True | Unknown/Standard feature |
| GAITASTDUAL | float64 | True | Unknown/Standard feature |
| GAITASTSUBS | float64 | True | Unknown/Standard feature |
| GAITASTMIS | float64 | True | Unknown/Standard feature |
| GAITASTTRANSDT | str | False | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## MDS-UPDRS_Part_III_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| PDTRTMNT | float64 | True | Unknown/Standard feature |
| PDSTATE | str | False | Unknown/Standard feature |
| HRPOSTMED | float64 | True | Unknown/Standard feature |
| HRDBSON | float64 | True | Unknown/Standard feature |
| HRDBSOFF | float64 | True | Unknown/Standard feature |
| PDMEDYN | float64 | True | Unknown/Standard feature |
| DBSYN | int64 | True | Unknown/Standard feature |
| ONOFFORDER | float64 | True | Unknown/Standard feature |
| OFFEXAM | float64 | True | Unknown/Standard feature |
| OFFNORSN | float64 | True | Unknown/Standard feature |
| DBSOFFYN | float64 | True | Unknown/Standard feature |
| DBSOFFTM | float64 | True | Unknown/Standard feature |
| ONEXAM | float64 | True | Unknown/Standard feature |
| ONNORSN | float64 | True | Unknown/Standard feature |
| HIFUYN | float64 | True | Unknown/Standard feature |
| DBSONYN | float64 | True | Unknown/Standard feature |
| DBSONTM | float64 | True | Unknown/Standard feature |
| PDMEDDT | str | False | Unknown/Standard feature |
| PDMEDTM | str | False | Unknown/Standard feature |
| EXAMDT | str | False | Unknown/Standard feature |
| EXAMTM | str | False | Unknown/Standard feature |
| NP3SPCH | float64 | True | Unknown/Standard feature |
| NP3FACXP | float64 | True | Unknown/Standard feature |
| NP3RIGN | float64 | True | Unknown/Standard feature |
| NP3RIGRU | float64 | True | Unknown/Standard feature |
| NP3RIGLU | float64 | True | Unknown/Standard feature |
| NP3RIGRL | float64 | True | Unknown/Standard feature |
| NP3RIGLL | float64 | True | Unknown/Standard feature |
| NP3FTAPR | float64 | True | Unknown/Standard feature |
| NP3FTAPL | float64 | True | Unknown/Standard feature |
| NP3HMOVR | float64 | True | Unknown/Standard feature |
| NP3HMOVL | float64 | True | Unknown/Standard feature |
| NP3PRSPR | float64 | True | Unknown/Standard feature |
| NP3PRSPL | float64 | True | Unknown/Standard feature |
| NP3TTAPR | float64 | True | Unknown/Standard feature |
| NP3TTAPL | float64 | True | Unknown/Standard feature |
| NP3LGAGR | float64 | True | Unknown/Standard feature |
| NP3LGAGL | float64 | True | Unknown/Standard feature |
| NP3RISNG | float64 | True | Unknown/Standard feature |
| NP3GAIT | float64 | True | Unknown/Standard feature |
| NP3FRZGT | float64 | True | Unknown/Standard feature |
| NP3PSTBL | float64 | True | Unknown/Standard feature |
| NP3POSTR | float64 | True | Unknown/Standard feature |
| NP3BRADY | float64 | True | Unknown/Standard feature |
| NP3PTRMR | float64 | True | Unknown/Standard feature |
| NP3PTRML | float64 | True | Unknown/Standard feature |
| NP3KTRMR | float64 | True | Unknown/Standard feature |
| NP3KTRML | float64 | True | Unknown/Standard feature |
| NP3RTARU | float64 | True | Unknown/Standard feature |
| NP3RTALU | float64 | True | Unknown/Standard feature |
| NP3RTARL | float64 | True | Unknown/Standard feature |
| NP3RTALL | float64 | True | Unknown/Standard feature |
| NP3RTALJ | float64 | True | Unknown/Standard feature |
| NP3RTCON | float64 | True | Unknown/Standard feature |
| NP3TOT | float64 | True | Unknown/Standard feature |
| DYSKPRES | float64 | True | Unknown/Standard feature |
| DYSKIRAT | float64 | True | Unknown/Standard feature |
| NHY | float64 | True | Hoehn & Yahr Stage |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## MDS-UPDRS_Part_IV__Motor_Complications_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| NP4WDYSK | int64 | True | Unknown/Standard feature |
| NP4WDYSKDEN | float64 | True | Unknown/Standard feature |
| NP4WDYSKNUM | float64 | True | Unknown/Standard feature |
| NP4WDYSKPCT | float64 | True | Unknown/Standard feature |
| NP4DYSKI | int64 | True | Unknown/Standard feature |
| NP4OFF | int64 | True | Unknown/Standard feature |
| NP4OFFDEN | float64 | True | Unknown/Standard feature |
| NP4OFFNUM | float64 | True | Unknown/Standard feature |
| NP4OFFPCT | float64 | True | Unknown/Standard feature |
| NP4FLCTI | int64 | True | Unknown/Standard feature |
| NP4FLCTX | int64 | True | Unknown/Standard feature |
| NP4DYSTN | int64 | True | Unknown/Standard feature |
| NP4DYSTNDEN | float64 | True | Unknown/Standard feature |
| NP4DYSTNNUM | float64 | True | Unknown/Standard feature |
| NP4DYSTNPCT | float64 | True | Unknown/Standard feature |
| NP4TOT | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## MDS-UPDRS_Part_I_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| NUPSOURC | int64 | True | Unknown/Standard feature |
| NP1COG | int64 | True | Unknown/Standard feature |
| NP1HALL | int64 | True | Unknown/Standard feature |
| NP1DPRS | int64 | True | Unknown/Standard feature |
| NP1ANXS | int64 | True | Unknown/Standard feature |
| NP1APAT | int64 | True | Unknown/Standard feature |
| NP1DDS | int64 | True | Unknown/Standard feature |
| NP1RTOT | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## MDS-UPDRS_Part_I_Patient_Questionnaire_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| NUPSOURC | int64 | True | Unknown/Standard feature |
| NP1SLPN | int64 | True | Unknown/Standard feature |
| NP1SLPD | int64 | True | Unknown/Standard feature |
| NP1PAIN | int64 | True | Unknown/Standard feature |
| NP1URIN | int64 | True | Unknown/Standard feature |
| NP1CNST | int64 | True | Unknown/Standard feature |
| NP1LTHD | int64 | True | Unknown/Standard feature |
| NP1FATG | int64 | True | Unknown/Standard feature |
| NP1PTOT | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## MDS_UPDRS_Part_II__Patient_Questionnaire_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| NUPSOURC | int64 | True | Unknown/Standard feature |
| NP2SPCH | int64 | True | Unknown/Standard feature |
| NP2SALV | int64 | True | Unknown/Standard feature |
| NP2SWAL | int64 | True | Unknown/Standard feature |
| NP2EAT | int64 | True | Unknown/Standard feature |
| NP2DRES | int64 | True | Unknown/Standard feature |
| NP2HYGN | int64 | True | Unknown/Standard feature |
| NP2HWRT | int64 | True | Unknown/Standard feature |
| NP2HOBB | int64 | True | Unknown/Standard feature |
| NP2TURN | int64 | True | Unknown/Standard feature |
| NP2TRMR | int64 | True | Unknown/Standard feature |
| NP2RISE | int64 | True | Unknown/Standard feature |
| NP2WALK | int64 | True | Unknown/Standard feature |
| NP2FREZ | int64 | True | Unknown/Standard feature |
| NP2PTOT | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Roche_PD_Monitoring_App_v2_data_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| STUDYID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| QRSCATID | str | False | Unknown/Standard feature |
| QRSSCAT | float64 | True | Unknown/Standard feature |
| QRSSTAT | float64 | True | Unknown/Standard feature |
| QRSREAS | float64 | True | Unknown/Standard feature |
| QRSCLMD | str | False | Unknown/Standard feature |
| QRSIVQFL | float64 | True | Unknown/Standard feature |
| QRSIVQRS | float64 | True | Unknown/Standard feature |
| QRSTSTID | str | False | Unknown/Standard feature |
| QRSTEST | str | False | Unknown/Standard feature |
| QRSLAT | float64 | True | Unknown/Standard feature |
| QRSDTM | str | False | Unknown/Standard feature |
| QRSDTM_TIME | str | False | Unknown/Standard feature |
| QRSSTDTC | str | False | Unknown/Standard feature |
| QRSSTDTC_TIME | str | False | Unknown/Standard feature |
| QRSENDTC | str | False | Unknown/Standard feature |
| QRSENDTC_TIME | str | False | Unknown/Standard feature |
| QRSRESN | float64 | True | Unknown/Standard feature |
| QRSRESC | str | False | Unknown/Standard feature |
| QRSORESU | float64 | True | Unknown/Standard feature |
| Age | float64 | True | Age of Participant |


## Epworth_Sleepiness_Scale_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| PTCGBOTH | int64 | True | Unknown/Standard feature |
| ESS1 | int64 | True | Unknown/Standard feature |
| ESS2 | int64 | True | Unknown/Standard feature |
| ESS3 | int64 | True | Unknown/Standard feature |
| ESS4 | int64 | True | Unknown/Standard feature |
| ESS5 | int64 | True | Unknown/Standard feature |
| ESS6 | int64 | True | Unknown/Standard feature |
| ESS7 | int64 | True | Unknown/Standard feature |
| ESS8 | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## REM_Sleep_Behavior_Disorder_Screening_Questionnaire_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| PTCGBOTH | int64 | True | Unknown/Standard feature |
| DRMVIVID | int64 | True | Unknown/Standard feature |
| DRMAGRAC | int64 | True | Unknown/Standard feature |
| DRMNOCTB | int64 | True | Unknown/Standard feature |
| SLPLMBMV | int64 | True | Unknown/Standard feature |
| SLPINJUR | int64 | True | Unknown/Standard feature |
| DRMVERBL | int64 | True | Unknown/Standard feature |
| DRMFIGHT | int64 | True | Unknown/Standard feature |
| DRMUMV | int64 | True | Unknown/Standard feature |
| DRMOBJFL | int64 | True | Unknown/Standard feature |
| MVAWAKEN | int64 | True | Unknown/Standard feature |
| DRMREMEM | int64 | True | Unknown/Standard feature |
| SLPDSTRB | int64 | True | Unknown/Standard feature |
| STROKE | int64 | True | Unknown/Standard feature |
| HETRA | int64 | True | Unknown/Standard feature |
| PARKISM | int64 | True | Unknown/Standard feature |
| RLS | int64 | True | Unknown/Standard feature |
| NARCLPSY | int64 | True | Unknown/Standard feature |
| DEPRS | int64 | True | Unknown/Standard feature |
| EPILEPSY | int64 | True | Unknown/Standard feature |
| BRNINFM | int64 | True | Unknown/Standard feature |
| CNSOTH | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Eligibility_Override_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| SUB_EVENT_ID | str | False | Unknown/Standard feature |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## FOUND_Enrollment_Status_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PATNO | int64 | True | Patient Identifier |
| FOSTATUS | int64 | True | Unknown/Standard feature |
| FOCONSENTDATE | str | False | Unknown/Standard feature |
| FOFOLLOWST | float64 | True | Unknown/Standard feature |
| FOFOLLOWMO | float64 | True | Unknown/Standard feature |
| FOVITAL | int64 | True | Unknown/Standard feature |
| FODOD | float64 | True | Unknown/Standard feature |
| FOVITALUPDATE | str | False | Unknown/Standard feature |
| FOVITALSOURCE | float64 | True | Unknown/Standard feature |
| FODODCERTAINTY | float64 | True | Unknown/Standard feature |
| FODEATHCAUSE | float64 | True | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Inclusion_Exclusion_14Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| EXFAMPD | float64 | True | Unknown/Standard feature |
| EXNEURCURR | float64 | True | Unknown/Standard feature |
| INAGE30 | float64 | True | Age of Participant |
| INLRRK2 | float64 | True | Unknown/Standard feature |
| INLRRK2GBA | float64 | True | Unknown/Standard feature |
| INLRRK2GBACORE | float64 | True | Unknown/Standard feature |
| INHY1OR2 | float64 | True | Hoehn & Yahr Stage |
| EX60DYPDRX | float64 | True | Unknown/Standard feature |
| EX90DYPDRX | float64 | True | Unknown/Standard feature |
| EXABCOND | float64 | True | Unknown/Standard feature |
| EXANTCOAG | float64 | True | Unknown/Standard feature |
| EXATYPPD | float64 | True | Unknown/Standard feature |
| EXCURPDRX | float64 | True | Unknown/Standard feature |
| EXDARX6MO | float64 | True | Unknown/Standard feature |
| EXMEDDBS | float64 | True | Unknown/Standard feature |
| EXDEMNTDX | float64 | True | Unknown/Standard feature |
| EXNEURMRI | float64 | True | Unknown/Standard feature |
| EXUNSAFLP | float64 | True | Unknown/Standard feature |
| EXOTHRSN | float64 | True | Unknown/Standard feature |
| IN2CARDPD | float64 | True | Unknown/Standard feature |
| IN2YRPD | float64 | True | Unknown/Standard feature |
| IN7YRPD | float64 | True | Unknown/Standard feature |
| INCNST | float64 | True | Unknown/Standard feature |
| INHOLDRX | float64 | True | Unknown/Standard feature |
| INNOMED6MO | float64 | True | Unknown/Standard feature |
| INPREGNT | float64 | True | Unknown/Standard feature |
| EXPDDEMDX | float64 | True | Unknown/Standard feature |
| INAGE4030 | float64 | True | Age of Participant |
| INAGE6030 | float64 | True | Age of Participant |
| INDATSCN | float64 | True | Unknown/Standard feature |
| INPRESCRN | float64 | True | Unknown/Standard feature |
| INSAA | float64 | True | Unknown/Standard feature |
| INHY1TO3 | float64 | True | Hoehn & Yahr Stage |
| INPDSC | float64 | True | Unknown/Standard feature |
| INPDDXSC | float64 | True | Unknown/Standard feature |
| INSNCAPARK | float64 | True | Unknown/Standard feature |
| INSNCAPARKCORE | float64 | True | Unknown/Standard feature |
| INUPSIT | float64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Age_at_visit_08Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| AGE_AT_VISIT | float64 | True | Age of Participant |


## Demographics_08Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| REC_ID | str | False | Unknown/Standard feature |
| PATNO | int64 | True | Patient Identifier |
| EVENT_ID | str | False | Visit Identifier |
| PAG_NAME | str | False | Unknown/Standard feature |
| INFODT | str | False | Information Date |
| AFICBERB | float64 | True | Unknown/Standard feature |
| ASHKJEW | float64 | True | Unknown/Standard feature |
| BASQUE | float64 | True | Unknown/Standard feature |
| BIRTHDT | str | False | Unknown/Standard feature |
| SEX | int64 | True | Sex of Participant |
| CHLDBEAR | float64 | True | Unknown/Standard feature |
| HOWLIVE | float64 | True | Unknown/Standard feature |
| GAYLES | float64 | True | Unknown/Standard feature |
| HETERO | float64 | True | Unknown/Standard feature |
| BISEXUAL | float64 | True | Unknown/Standard feature |
| PANSEXUAL | float64 | True | Unknown/Standard feature |
| ASEXUAL | float64 | True | Unknown/Standard feature |
| OTHSEXUALITY | float64 | True | Unknown/Standard feature |
| HANDED | float64 | True | Unknown/Standard feature |
| HISPLAT | int64 | True | Unknown/Standard feature |
| RAASIAN | int64 | True | Unknown/Standard feature |
| RABLACK | int64 | True | Unknown/Standard feature |
| RAHAWOPI | int64 | True | Unknown/Standard feature |
| RAINDALS | int64 | True | Unknown/Standard feature |
| RANOS | int64 | True | Unknown/Standard feature |
| RAWHITE | int64 | True | Unknown/Standard feature |
| RAUNKNOWN | int64 | True | Unknown/Standard feature |
| ORIG_ENTRY | str | False | Unknown/Standard feature |
| LAST_UPDATE | str | False | Unknown/Standard feature |


## Subject_Cohort_History_08Jul2026.csv

| Column | Type | Numeric | Description |
|---|---|---|---|
| PATNO | int64 | True | Patient Identifier |
| APPRDX | int64 | True | Unknown/Standard feature |
| COHORT | int64 | True | Unknown/Standard feature |

