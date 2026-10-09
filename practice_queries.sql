-- All students with their courses
SELECT s.name, c.course_name, c.grade
FROM students s
JOIN courses c ON s.id = c.student_id;

-- Count courses per student
SELECT s.name, COUNT(c.id) AS course_count
FROM students s
LEFT JOIN courses c ON s.id = c.student_id
GROUP BY s.id, s.name;

-- Students above average CGPA
SELECT name, cgpa FROM students
WHERE cgpa > (SELECT AVG(cgpa) FROM students);

-- Branch distribution
SELECT branch, COUNT(*) FROM students GROUP BY branch;