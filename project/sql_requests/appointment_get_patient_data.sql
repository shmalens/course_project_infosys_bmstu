SELECT
       id,
       first_name,
       second_name,
       surname,
       birthday,
       address,
       passport,
       diagnose
FROM disease_history.Referral
WHERE 1
  AND id = '$referral_id'
;