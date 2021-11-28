SELECT
       History.id,
       P.surname,
       N.note
FROM History
LEFT OUTER JOIN Patient P on P.id = History.patient
LEFT JOIN Note N on History.id = N.history
WHERE 1
      AND N.doctor = '$doctor'
;