SELECT
       id,
       room,
       patients_amount
FROM disease_history.Room
WHERE 1
   AND patients_amount < '$max_patient_amount'