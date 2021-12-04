UPDATE disease_history.Room
SET patients_amount = patients_amount - 1
WHERE 1
  AND id = '$room_id'
;