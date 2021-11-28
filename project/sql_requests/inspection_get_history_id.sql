SELECT
       id
FROM disease_history.History
WHERE 1
      AND patient = '$patient'
      AND discharge_date is NULL
;