CREATE VIEW logdapp_student_1_view AS SELECT Course_ID_id,Student_ID_id, Prof_ID_id , Grade FROM logdapp_enrollment WHERE Student_ID_id=1;

CREATE VIEW logdapp_student_2_view AS SELECT Course_ID_id,Student_ID_id, Prof_ID_id , Grade FROM logdapp_enrollment WHERE Student_ID_id=2;

CREATE VIEW logdapp_student_3_view AS SELECT Course_ID_id,Student_ID_id, Prof_ID_id , Grade FROM logdapp_enrollment WHERE Student_ID_id=3;

CREATE VIEW logdapp_student_4_view AS SELECT Course_ID_id,Student_ID_id, Prof_ID_id , Grade FROM logdapp_enrollment WHERE Student_ID_id=4;

CREATE VIEW logdapp_prof_1_view AS SELECT Course_ID_id,Student_ID_id, Prof_ID_id , Grade FROM logdapp_enrollment WHERE Prof_ID_id=1;

CREATE VIEW logdapp_prof_2_view AS SELECT Course_ID_id,Student_ID_id, Prof_ID_id , Grade FROM logdapp_enrollment WHERE Prof_ID_id=2;

-- CREATE TABLE logdapp_courses (ID varchar(10) NOT NULL PRIMARY KEY, Name varchar(20) NOT NULL);

-- CREATE TABLE logdapp_students (Name varchar(200) NOT NULL, Roll_Number integer AUTO_INCREMENT NOT NULL PRIMARY KEY, Semester integer NOT NULL, Degree varchar(20) NOT NULL, Department varchar(25) NOT NULL, Email varchar(254) NOT NULL);

-- CREATE TABLE logdapp_prof (profid integer AUTO_INCREMENT NOT NULL PRIMARY KEY, name varchar(200) NOT NULL, department varchar(200) NOT NULL, office varchar(200) NOT NULL, email varchar(254) NOT NULL, course varchar(200) NOT NULL);

-- CREATE TABLE logdapp_enrollment (id integer AUTO_INCREMENT NOT NULL PRIMARY KEY, Grade varchar(2) NOT NULL, Course_ID_id varchar(10) NOT NULL, Prof_ID_id integer NOT NULL, Student_ID_id integer NOT NULL);
-- ALTER TABLE logdapp_enrollment ADD CONSTRAINT logdapp_enrollment_Course_ID_id_c79eb17c_fk_logdapp_courses_ID FOREIGN KEY (Course_ID_id) REFERENCES logdapp_courses (ID);
-- ALTER TABLE logdapp_enrollment ADD CONSTRAINT logdapp_enrollment_Prof_ID_id_02f8c550_fk_logdapp_prof_profid FOREIGN KEY (Prof_ID_id) REFERENCES logdapp_prof (profid);
-- ALTER TABLE logdapp_enrollment ADD CONSTRAINT logdapp_enrollment_Student_ID_id_611e3c98_fk_logdapp_s FOREIGN KEY (Student_ID_id) REFERENCES logdapp_students (Roll_Number);
-- COMMIT;

-- CREATE TABLE logdapp_user (profid integer NOT NULL PRIMARY KEY ,USER varchar(10) NOT NULL, PASSWORD varchar(20) NOT NULL,FOREIGN KEY(profid) REFERENCES logdapp_prof (profid));

create user 'student_1'@'%' identified by 'shubham';
create user 'student_2'@'%' identified by 'shubham';
create user 'student_3'@'%' identified by 'shubham';
create user 'student_4'@'%' identified by 'shubham';
create user 'prof_1'@'%' identified by 'shubham';
create user 'prof_2'@'%' identified by 'shubham';

GRANT SELECT ON `loggingdapp`.`logdapp_student_1_view` TO 'student_1'@'%';
GRANT SELECT, INSERT, CREATE ON `loggingdapp`.`django_migrations` TO 'student_1'@'%';
GRANT SELECT ON `loggingdapp`.`logdapp_user_publickey` TO 'student_1'@'%';
GRANT SELECT ON `loggingdapp`.`logdapp_student_2_view` TO 'student_2'@'%';
GRANT SELECT, INSERT, CREATE ON `loggingdapp`.`django_migrations` TO 'student_2'@'%';
GRANT SELECT ON `loggingdapp`.`logdapp_user_publickey` TO 'student_2'@'%';
GRANT SELECT ON `loggingdapp`.`logdapp_student_3_view` TO 'student_3'@'%';
GRANT SELECT, INSERT, CREATE ON `loggingdapp`.`django_migrations` TO 'student_3'@'%';
GRANT SELECT ON `loggingdapp`.`logdapp_user_publickey` TO 'student_3'@'%';
GRANT SELECT ON `loggingdapp`.`logdapp_student_4_view` TO 'student_4'@'%';
GRANT SELECT, INSERT, CREATE ON `loggingdapp`.`django_migrations` TO 'student_4'@'%';
GRANT SELECT ON `loggingdapp`.`logdapp_user_publickey` TO 'student_4'@'%';
GRANT SELECT ON `loggingdapp`.`logdapp_user_publickey` TO 'prof_1'@'%';
GRANT SELECT, UPDATE ON `loggingdapp`.`logdapp_prof_1_view` TO 'prof_1'@'%';
GRANT SELECT, INSERT, CREATE ON `loggingdapp`.`django_migrations` TO 'prof_1'@'%';
GRANT SELECT, INSERT, CREATE ON `loggingdapp`.`django_migrations` TO 'prof_2'@'%';
GRANT SELECT, INSERT, UPDATE ON `loggingdapp`.`logdapp_prof_2_view` TO 'prof_2'@'%';
GRANT SELECT ON `loggingdapp`.`logdapp_user_publickey` TO 'prof_2'@'%';