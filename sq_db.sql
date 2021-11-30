CREATE TABLE  IF NOT EXISTS users(
    id integer  PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL,
    firstname text NOT NULL,
    lastname text NOT NULL,
    dateborn text NOT NULL,
    name_organization text NOT NULL,
    position text NOT NULL,
    email text NOT NULL,
    hpsw text NOT NULL,
    time integer NOT NULL,
    role integer NOT NULL DEFAULT 1
);

CREATE TABLE  IF NOT EXISTS courses(
    themes text NOT NULL,
    edu_materials text NOT NULL,
    edu_other text NOT NULL default 'text',
    edu_additional text NOT NULL default 'text',
    time integer NOT NULL
);

CREATE TABLE  IF NOT EXISTS docs_edu(
    id integer  PRIMARY KEY AUTOINCREMENT,
    themes text NOT NULL,
    protocol blob NOT NULL,
    sertificate blob NOT NULL
);

CREATE TABLE IF NOT EXISTS tests(
    label integer,
    qestion text,
    answer blob,
    a_just text
);

CREATE TABLE IF NOT EXISTS a_just(
	id integer,
	laj	blob,
	llu	blob
);

CREATE TABLE IF NOT EXISTS status_course(
    id            integer PRIMARY KEY AUTOINCREMENT,
    theme         text,
    status_course text NOT NULL DEFAULT 'Экзамен не сдан',
    count_prob    integer DEFAULT 0,
    rez_procent   integer NOT NULL DEFAULT 0,
    protocol      blob,
    sertificat    blob
);

CREATE TABLE IF NOT EXISTS status_finances(
    id integer PRIMARY KEY AUTOINCREMENT,
    dogovor text,
    price text,
    act text,
    final integer DEFAULT 0
);

