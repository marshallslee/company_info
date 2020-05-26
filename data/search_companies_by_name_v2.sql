SELECT cg.id AS company_group_id, lang.code AS language_code, co.name
FROM company AS co
INNER JOIN company_group AS cg
ON co.company_group_id = cg.id
INNER JOIN language AS lang
ON lang.id = co.language_id
INNER JOIN (SELECT DISTINCT company_group_id FROM company WHERE MATCH(name) AGAINST('ant' IN BOOLEAN MODE)) AS cgid
ON cg.id = cgid.company_group_id
ORDER BY company_group_id, co.name ASC;
