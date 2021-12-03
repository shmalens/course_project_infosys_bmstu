SELECT Note.id, Note.date, Note.note, D.first_name, D.second_name, D.surname, D.id
FROM disease_history.Note
LEFT JOIN disease_history.Doctor D on D.id = Note.doctor
WHERE history = '$history'
ORDER BY Note.id DESC;