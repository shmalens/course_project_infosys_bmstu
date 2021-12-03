SELECT DISTINCT
                Patient.id,
                first_name,
                second_name,
                surname
FROM disease_history.Patient
         LEFT OUTER JOIN disease_history.History H on Patient.id = H.patient
WHERE 1
  AND H.id is not NULL
  AND H.discharge_diagnose is not NULL
;