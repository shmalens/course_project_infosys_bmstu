SELECT
       *
FROM History
WHERE 1
      AND patient = '$patient'
      AND discharge_date is NULL
      AND receipt_date is not NULL
;