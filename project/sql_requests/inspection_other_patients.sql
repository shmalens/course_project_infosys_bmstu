SELECT Patient.id, first_name, second_name, surname, birthday, address, passport, doctor FROM Patient
LEFT JOIN History H on Patient.id = H.patient
WHERE 1
    AND not doctor = '$doctor'
    AND H.discharge_date is NULL
    AND H.receipt_date is not NULL
;