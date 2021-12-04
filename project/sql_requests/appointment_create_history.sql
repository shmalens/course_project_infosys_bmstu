insert into disease_history.History (receipt_date,
                                     receipt_diagnose,
                                     patient)
values (CURDATE(),
        '$diagnose',
        '$patient'
       );