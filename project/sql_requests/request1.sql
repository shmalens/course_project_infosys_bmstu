SELECT Patient.surname,
       H.receipt_diagnose,
       H.discharge_diagnose,
       TO_DAYS(H.discharge_date) - TO_DAYS(H.receipt_date) FROM Patient
LEFT JOIN Doctor D on D.id = Patient.doctor
LEFT JOIN History H on Patient.id = H.patient
WHERE 1
      AND D.id = '$doctor'
;