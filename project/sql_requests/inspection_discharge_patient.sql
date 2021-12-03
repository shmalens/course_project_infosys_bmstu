update disease_history.History
set discharge_date = CURDATE(),
    discharge_diagnose = '$diagnose'
where id = '$history';